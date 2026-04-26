class SummaryService:
    def summarize(self, logs: list[str]) -> str:
        # Replace with real LLM call later
        joined = "\n".join(logs)

        return f"Summary of the week:\n\n{joined[:300]}..."