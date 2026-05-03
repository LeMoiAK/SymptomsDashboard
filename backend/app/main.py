from fastapi import FastAPI
from .dbconn import BaseDeclarativeClass, engine
from .routes import logs, analytics, patients, doctors, treatments, appointments

app = FastAPI(title="Daily Logs API")

# Add the sub-URLs routers
app.include_router(logs.router)
app.include_router(analytics.router)
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(treatments.router)
app.include_router(appointments.router)

@app.get("/")
def root():
    return {"status": "ok"}