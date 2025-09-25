import json, os, time
from typing import Optional
from authlib.integrations.httpx_client import OAuth2Client

TOKEN_PATH = os.path.join(os.path.dirname(__file__), "token_store.json")

AUTH_URL = os.getenv("OAUTH_AUTH_URL")
TOKEN_URL = os.getenv("OAUTH_TOKEN_URL")
CLIENT_ID = os.getenv("OAUTH_CLIENT_ID")
CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET", None)
SCOPES = os.getenv("OAUTH_SCOPES", "openid").split()

def _load_tokens() -> Optional[dict]:
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def _save_tokens(tok: dict):
    with open(TOKEN_PATH, "w", encoding="utf-8") as f:
        json.dump(tok, f)

def _client(tokens: Optional[dict] = None) -> OAuth2Client:
    return OAuth2Client(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope=" ".join(SCOPES),
        token=tokens,
    )


def get_access_token() -> str:
    # TEMPORARY: bypass OAuth for local demo
    print("[oauth] Using DEV_TOKEN (OAuth bypass for local tests)")
    return "DEV_TOKEN"



""" def get_access_token() -> str:
    tokens = _load_tokens()
    c = _client(tokens)

    # refresh if near expiry
    if tokens and tokens.get("expires_at", 0) - time.time() < 60:
        if "refresh_token" in tokens:
            new = c.refresh_token(TOKEN_URL, refresh_token=tokens["refresh_token"])
            new["expires_at"] = time.time() + new.get("expires_in", 3600)
            _save_tokens(new)
            return new["access_token"]

    if tokens:
        return tokens["access_token"]

    # DEVICE CODE (if the provider supports). Keycloak needs device endpoint;
    # if not available, swap to standard PKCE flow later.
    # For now we prompt the dev with a clear message:
    raise RuntimeError(
        "No OAuth tokens yet. Complete OAuth once before booking.\n"
        "Either implement Device Code here or run a PKCE helper.\n"
        "For now, set BOOKING_API to accept a fixed DEV_BEARER token for local tests."
    )
 """