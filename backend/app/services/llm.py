"""
The llm modules contains the functions to interact with the LLM.
"""

# Get env vars using pydantic
from pydantic import Field
from pydantic_settings import BaseSettings

class DbConfig(BaseSettings):
    LLM_PROVIDER: str = Field(min_length=1)
    OPENAI_MODEL: str = Field(min_length=1)
    OPENAI_API_KEY: str = Field(min_length=1)
    OPENAI_BASE_URL: str = Field(min_length=1)

config = DbConfig()

# Get the Chat to the LLM
from langchain_openai import ChatOpenAI
from .prompts import summary_prompt, verification_prompt, refinement_prompt

def get_llm():
    provider = config.LLM_PROVIDER

    common_kwargs = dict(
        model=config.OPENAI_MODEL,
        temperature=0.2
    )

    if provider == "openai":
        chat = ChatOpenAI(
            api_key=config.OPENAI_API_KEY,
            **common_kwargs
        )
    else:
        # local llama.cpp (OpenAI-compatible)
        chat = ChatOpenAI(
            base_url=config.OPENAI_BASE_URL,
            api_key="not-needed",
            **common_kwargs
        )

    return chat

# LLM helper functions
def join_logs(daily_logs):
    return "\n\n".join(daily_logs)

def run_prompt(LLM, prompt, **kwargs):
    messages = prompt.format_messages(**kwargs)
    response = LLM.invoke(messages)
    return response.content.strip()

# Pipeline to interrogate the LLM
def chunk_logs(daily_logs, batch_size=8):
    for i in range(0, len(daily_logs), batch_size):
        yield daily_logs[i:i + batch_size]


def summarise_batches(LLM, daily_logs, batch_size=8):
    """
    We summarise the logs by batches. If the LLM doesn't have enough context to contain all logs
    we summarise it in batches. Then summarise the summaries of the batches.
    """
    outputs = []

    for batch in list(chunk_logs(daily_logs, batch_size)):
        outputs.append(
            run_prompt(LLM,
                summary_prompt,
                daily_logs=join_logs(batch)
            )
        )

    return outputs


def merge_summaries(LLM, summaries):
    """
    Merge the summaries of the batches together into a single summary
    """
    return run_prompt(LLM,
        summary_prompt,
        daily_logs=join_logs(summaries)
    )


def verify_summary(LLM, daily_logs, summary):
    """Verify the summary is correct"""
    return run_prompt(LLM,
        verification_prompt,
        daily_logs=join_logs(daily_logs),
        summary=summary
    )


def summarise_logs_pipeline(daily_logs, batch_size=8, max_retries=2):
    # Get the LLM
    LLM = get_llm()

    # Summarise the notes, by batch if necessary
    batch_summaries = summarise_batches(LLM, daily_logs, batch_size)
    final_summary = merge_summaries(LLM, batch_summaries)

    for attempt in range(max_retries):
        verification = verify_summary(LLM, daily_logs, final_summary)

        if verification.strip() == "OK":
            return final_summary

        print(f"[Retry {attempt+1}] Issues found:\n{verification}\n")

        # refinement step
        final_summary = run_prompt(LLM,
            refinement_prompt,
            issues=verification,
            summary=final_summary
        )

    return final_summary