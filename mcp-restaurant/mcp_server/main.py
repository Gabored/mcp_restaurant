# mcp_server/main.py
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from typing import List, Dict
from dataclasses import asdict

from .models import Restaurant, BookingResult
from .client import similarity_search, book_with_token
from .oauth import get_access_token

load_dotenv()
mcp = FastMCP("restaurant-booker")

@mcp.tool()
def search_candidates(
    query: str,
    when: str,
    people: int,
    location: str
) -> List[Dict]:
    """
    Find candidate restaurants that match the user's intent.
    Returns list of dicts with match_score in [0,1].
    """
    results = similarity_search(query=query, when=when, people=people, location=location)
    # Validate shape by constructing dataclasses, then return as dicts:
    items = [Restaurant(**r) for r in results]
    return [asdict(x) for x in items]

@mcp.tool()
def book_reservation(
    restaurant_id: str,
    arrival_time: str,
    people: int
) -> Dict:
    """
    Book a reservation by restaurant_id.
    Requires OAuth; will use Bearer token to call booking-api.
    """
    token = get_access_token()  # may refresh; raises if not set up yet
    data = book_with_token(token, restaurant_id=restaurant_id, arrival_time=arrival_time, people=people)
    result = BookingResult(**data)
    return asdict(result)

if __name__ == "__main__":
    mcp.run()
