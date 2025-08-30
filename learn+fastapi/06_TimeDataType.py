from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime, time, timedelta


# ---------------------------------------------------------
# 1. Event Model with Time Data Types
# ---------------------------------------------------------
class Event(BaseModel):
    event_id: UUID
    start_date: date
    start_time: time
    end_time: time
    repeat_time: time
    execute_after: timedelta

app = FastAPI()

@app.post("/add_event")
def add_event(event: Event):
    return {"message": "Event created successfully", "event": event}    

