"""
Script to experiment with connecting to the PostgreSQL database and run requests.
"""

from app.dbconn import SessionLocal, BaseDeclarativeClass, engine
import app.crud as crud
from sqlalchemy.orm import Session
from datetime import date, timedelta

# Get env vars using pydantic
from pydantic import HttpUrl, Field
from pydantic_settings import BaseSettings

class DbConfig(BaseSettings):
    APP_DB_USER: str = Field(min_length=1)
    APP_DB_PASSWORD: str = Field(min_length=1)
    DATABASE_URL: str = Field(min_length=1)
    LLM_PROVIDER: str = Field(min_length=1)
    OPENAI_MODEL: str = Field(min_length=1)
    OPENAI_API_KEY: str = Field(min_length=1)
    OPENAI_BASE_URL: str = Field(min_length=1)

config = DbConfig()

# Then connect to DB
print(f"URL: {config.DATABASE_URL}")

# LLM call
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

def get_llm():
    provider = config.LLM_PROVIDER

    common_kwargs = dict(
        model=config.OPENAI_MODEL,
        temperature=0.2
    )

    if provider == "openai":
        return ChatOpenAI(
            api_key=config.OPENAI_API_KEY,
            **common_kwargs
        )

    # local llama.cpp (OpenAI-compatible)
    return ChatOpenAI(
        base_url=config.OPENAI_BASE_URL,
        api_key="not-needed",
        **common_kwargs
    )

LLM = get_llm()

# The LLM works in two steps:
# 1. Summarise the logs into a a paragraph
# 2. Verify that the summary is correct and contains only info from the notes
# --- Prompts for Summary in step 1
summary_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        """You are a precise and conservative medical summarization assistant.
Your goal is to summarize daily logs from patients about their symptoms during a treatment into an overview for the doctor.
"""
    ),
    HumanMessagePromptTemplate.from_template(
        """
Summarise the following patient daily logs into ONE concise paragraph.

STRICT RULES:
- Do NOT add new information
- Do NOT infer diagnoses
- Preserve uncertainty (e.g. "possible", "suspected")
- Use original terminology
- Merge repeated observations
- Keep all clinically relevant details
- Find trends between days in a cycle and symptoms

LOGS:
{daily_logs}
"""
    ),
])
# --- Prompts for Verification in step 2
verification_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are a strict medical fact-checker. You check that a summary contains only information supported by the given logs."
    ),
    HumanMessagePromptTemplate.from_template(
        """
Check whether the summary contains claims NOT directly supported by the logs.

Return:
- OK
- or list unsupported statements concisely

LOGS:
{daily_logs}

SUMMARY:
{summary}
"""
    ),
])
# Prompts for correction in step 2 if needed
refinement_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "You are a precise medical summarization assistant."
            ),
            HumanMessagePromptTemplate.from_template(
                """
Revise the summary to remove unsupported claims.

ISSUES:
{issues}

SUMMARY:
{summary}

Return ONE corrected paragraph.
"""
            ),
        ])

# LLM helper functions
def join_logs(daily_logs):
    return "\n\n".join(daily_logs)

def run_prompt(prompt, **kwargs):
    messages = prompt.format_messages(**kwargs)
    response = LLM.invoke(messages)
    return response.content.strip()

# Pipeline to interrogate the LLM
def chunk_logs(daily_logs, batch_size=8):
    for i in range(0, len(daily_logs), batch_size):
        yield daily_logs[i:i + batch_size]


def summarise_batches(daily_logs, batch_size=8):
    """
    We summarise the logs by batches. If the LLM doesn't have enough context to contain all logs
    we summarise it in batches. Then summarise the summaries of the batches.
    """
    outputs = []

    for batch in list(chunk_logs(daily_logs, batch_size)):
        outputs.append(
            run_prompt(
                summary_prompt,
                daily_logs=join_logs(batch)
            )
        )

    return outputs


def merge_summaries(summaries):
    """
    Merge the summaries of the batches together into a single summary
    """
    return run_prompt(
        summary_prompt,
        daily_logs=join_logs(summaries)
    )


def verify_summary(daily_logs, summary):
    """Verify the summary is correct"""
    return run_prompt(
        verification_prompt,
        daily_logs=join_logs(daily_logs),
        summary=summary
    )


def summarise_logs_pipeline(daily_logs, batch_size=8, max_retries=2):
    batch_summaries = summarise_batches(daily_logs, batch_size)
    final_summary = merge_summaries(batch_summaries)

    for attempt in range(max_retries):
        verification = verify_summary(daily_logs, final_summary)

        if verification.strip() == "OK":
            return final_summary

        print(f"[Retry {attempt+1}] Issues found:\n{verification}\n")

        # refinement step
        final_summary = run_prompt(
            refinement_prompt,
            issues=verification,
            summary=final_summary
        )

    return final_summary

# ------------ Main function
if __name__ == "__main__":
    db: Session = SessionLocal()

    # Get the logs
    patient_id = 1
    start_date=date(2026, 4, 15)
    end_date=date(2026, 5, 4)
    logs = crud.get_logs_between_dates_for_patient(db, patient_id=patient_id, start_date=start_date, end_date=end_date)
    print(logs)

    # Get the treatments, assume the earlist treatment to be 2 months before the start_date
    # treatments normally last up to 1 month cycle
    treatment_start_date = start_date - timedelta(days=62)
    treatments = crud.get_treatments_between_dates_for_patient(db, patient_id, treatment_start_date, end_date)
    print(treatments)


    # For each log, we find if in a treatment period
    for log in logs:
        log_date = log.log_date

        # Find the treatment with the closest date before that log
        potential_days_in_cycle = [(log_date - t.treatment_date).days for t in treatments]
        valid_indices = [i for i, v in enumerate(potential_days_in_cycle) if v >= 0]
        min_index = (
            min(valid_indices, key=potential_days_in_cycle.__getitem__)
            if valid_indices else None
        )
        # Generate the text for that treatment time
        treatment_str = ""
        if min_index:
            last_treatment = treatments[min_index]
            # Verify if in a cycle or not
            days_since_last_treatment = (log_date - last_treatment.treatment_date).days
            if (days_since_last_treatment + last_treatment.day_in_cycle) > last_treatment.cycle_duration:
                # Not a treatment - gives days since last treatment
                treatment_str = f"{days_since_last_treatment} Days since last treatment"
            else:
                treatment_str = f"treatment Cycle {last_treatment.cycle_number} Day {days_since_last_treatment + last_treatment.day_in_cycle}"
        else:
            # No treatment found, could be logs before starting any cycle
            treatment_str = "No treatment yet"

        # Complete the log text with date, cycle and treatments
        log_date_str = log_date.strftime("%Y-%m-%d")
        final_log_text = f"{log_date_str} - {treatment_str} - {log.log_text}"
        # Then add symptoms level
        final_log_text += f"\nSymptom levels: Pain={log.symptom_Pain}/4 | Fatigue={log.symptom_Fatigue}/4 | Diarrhea={log.symptom_Diarrhea}/4 | Nausea={log.symptom_Nausea}/4"
        # Then replace it
        log.log_text = final_log_text

    # Then generate the prompt and the call to the LLM
    summary = summarise_logs_pipeline([log.log_text for log in logs], batch_size=14)
    
    print(logs)
    print(logs[0])