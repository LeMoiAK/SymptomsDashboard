FROM python:3.12-slim

# Install uv
RUN pip install uv

WORKDIR /app

# Copy dependency files first (cache-friendly)
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync

# Copy app code
COPY app ./app
COPY scripts ./scripts
COPY dev_data ./dev_data
COPY alembic ./alembic
COPY alembic.ini ./

EXPOSE 8000

CMD ["uv", "run", "sh", "-c", "alembic upgrade head && uv run -m scripts.dev_seed_data && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
# CMD ["uv", "run", "sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]