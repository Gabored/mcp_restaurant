import os
import uuid
from datetime import datetime
from typing import Dict
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
DEV_BEARER = os.getenv("DEV_BEARER", "DEV_TOKEN")

app = FastAPI(title="booking-api")

# in-memory "DB" for demo
BOOKINGS = {}

class BookInput(BaseModel):
    restaurant_id: str
    arrival_time: str  # ISO 8601
    people: int

@app.post("/book")
def book(payload: BookInput, authorization: str | None = Header(default=None)) -> Dict:
    print(f"[booking-api] /book called with: {payload.dict()}")
    # --- Auth check (dev placeholder) ---
    if not authorization or not authorization.startswith("Bearer "):
        print("[booking-api] missing/invalid Authorization header")
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    if token != DEV_BEARER:
        print("[booking-api] invalid bearer token")
        raise HTTPException(status_code=403, detail="Invalid token")

    # --- Basic input validation / mock availability ---
    try:
        when = datetime.fromisoformat(payload.arrival_time)
    except Exception:
        raise HTTPException(status_code=422, detail="arrival_time must be ISO 8601")

    if payload.people <= 0:
        raise HTTPException(status_code=422, detail="people must be > 0")

    # NOTE: in a real system we'd look up the restaurant and check capacity/availability.
    # For demo we accept all, but log clearly:
    print(f"[booking-api] Auth OK. Attempting to book {payload.people} seats at {payload.arrival_time} for restaurant_id={payload.restaurant_id}")

    booking_id = "bk_" + uuid.uuid4().hex[:10]
    # mock "restaurant lookup" (you could also POST back to similarity-service)
    result = {
        "booking_id": booking_id,
        "restaurant_id": payload.restaurant_id,
        "restaurant_name": "TBD (lookup in directory or pass-through)",  # placeholder
        "people": payload.people,
        "arrival_time": payload.arrival_time,
        "location": "Guadalajara"  # placeholder
    }
    BOOKINGS[booking_id] = result
    print(f"[booking-api] Booking created: {booking_id}")
    return result

@app.get("/health")
def health():
    return {"ok": True}
