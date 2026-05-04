"""
The prompts module contains the prompts to define our agent.
The agent can:
1. Summarise daily logs
2. Verify these summaries are supported by the logs
3. Correct the summary if not.

The agent works by creating a summary of the logs.
This summary is then verified by a second call to the LLM.
If issues are detected, the LLM tries to correct it.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

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