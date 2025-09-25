import httpx
import os

SIM_BASE = os.getenv("SIMILARITY_API_BASE", "http://localhost:9002")
BOOK_BASE = os.getenv("BOOKING_API_BASE", "http://localhost:9001")

def similarity_search(query: str, when: str, people: int, location: str):
    # POST to similarity service; returns list of Restaurant-like dicts
    payload = {"query": query, "when": when, "people": people, "location": location}
    with httpx.Client(timeout=10.0) as http:
        r = http.post(f"{SIM_BASE}/search", json=payload)
        r.raise_for_status()
        return r.json()

def book_with_token(access_token: str, restaurant_id: str, arrival_time: str, people: int):
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"restaurant_id": restaurant_id, "arrival_time": arrival_time, "people": people}
    with httpx.Client(timeout=10.0) as http:
        r = http.post(f"{BOOK_BASE}/book", json=payload, headers=headers)
        r.raise_for_status()
        return r.json()
