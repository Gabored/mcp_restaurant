# mcp_server/models.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class Restaurant:
    id: str
    restaurant_name: str
    location: str
    style: List[str] = field(default_factory=list)
    match_score: float = 0.0

@dataclass
class BookingRequest:
    restaurant_id: str
    arrival_time: str  # ISO 8601
    people: int

@dataclass
class BookingResult:
    booking_id: str
    restaurant_id: str
    restaurant_name: str
    people: int
    arrival_time: str
    location: str
