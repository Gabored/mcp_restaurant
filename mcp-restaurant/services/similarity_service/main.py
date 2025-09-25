from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import re
import uuid

# --- Data seed (hard-coded demo) ---
RESTAURANTS = [
    {
        "id": "r_" + uuid.uuid4().hex[:8],
        "restaurant_name": "Kumo Sushi",
        "location": "Guadalajara",
        "style": ["Asian", "Japanese", "Sushi", "Michelin Star", "Expensive"],
    },
    {
        "id": "r_" + uuid.uuid4().hex[:8],
        "restaurant_name": "Ramen Dojo",
        "location": "Guadalajara",
        "style": ["Asian", "Japanese", "Ramen", "Casual"],
    },
    {
        "id": "r_" + uuid.uuid4().hex[:8],
        "restaurant_name": "El Patio",
        "location": "Guadalajara",
        "style": ["Mexican", "Traditional", "Family"],
    },
    {
        "id": "r_" + uuid.uuid4().hex[:8],
        "restaurant_name": "Sushi Bar CDMX",
        "location": "Ciudad de México",
        "style": ["Asian", "Japanese", "Sushi", "Trendy"],
    },
]

# --- FastAPI app ---
app = FastAPI(title="similarity-service")

class SearchInput(BaseModel):
    query: str
    when: str
    people: int
    location: str

def normalize(text: str) -> List[str]:
    tokens = re.findall(r"[A-Za-zñáéíóúüÁÉÍÓÚÜ]+", text.lower())
    return tokens

def style_match_score(query: str, styles: List[str]) -> float:
    q = set(normalize(query))
    tags = set([s.lower() for s in styles])
    overlap = q.intersection(tags)
    if not tags:
        return 0.0
    return round(len(overlap) / len(tags), 3)

def name_boost(query: str, name: str) -> float:
    q = " ".join(normalize(query))
    n = " ".join(normalize(name))
    return 0.1 if all(word in n for word in q.split()) and q else 0.0

@app.post("/search")
def search(payload: SearchInput) -> List[Dict]:
    print(f"[similarity-service] /search called with: {payload.dict()}")
    out = []
    for r in RESTAURANTS:
        # simple location gate: prefer same-city, otherwise downweight
        loc_factor = 1.0 if r["location"].lower() == payload.location.lower() else 0.7
        score = style_match_score(payload.query, r["style"]) + name_boost(payload.query, r["restaurant_name"])
        score = max(0.0, min(1.0, round(score * loc_factor, 3)))
        out.append({
            "id": r["id"],
            "restaurant_name": r["restaurant_name"],
            "location": r["location"],
            "style": r["style"],
            "match_score": score
        })
    # sort high→low; keep top 5
    out.sort(key=lambda x: x["match_score"], reverse=True)
    print(f"[similarity-service] returning {len(out)} candidates (top score={out[0]['match_score'] if out else 'NA'})")
    return out[:5]
