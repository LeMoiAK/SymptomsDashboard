from fastapi import FastAPI
from .dbconn import BaseModel, engine
from .routes import logs, analytics

app = FastAPI(title="Daily Logs API")

# Create tables (dev only; use migrations later)
BaseModel.metadata.create_all(bind=engine)

app.include_router(logs.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"status": "ok"}