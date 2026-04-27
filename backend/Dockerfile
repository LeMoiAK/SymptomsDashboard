FROM python:3.14-slim

# Install uv
RUN pip install uv

WORKDIR /app

# Copy dependency files first (cache-friendly)
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --system

# Copy app code
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]