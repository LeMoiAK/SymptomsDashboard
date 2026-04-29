from fastapi import FastAPI
from .dbconn import BaseDeclarativeClass, engine
from .routes import logs, analytics, patients, doctors

app = FastAPI(title="Daily Logs API")

# Create tables (dev only; use migrations later)
BaseDeclarativeClass.metadata.create_all(bind=engine)

# Add the sub-URLs routers
app.include_router(logs.router)
app.include_router(analytics.router)
app.include_router(patients.router)
app.include_router(doctors.router)

@app.get("/")
def root():
    return {"status": "ok"}