from fastmcp import FastMCP
import requests
import os

mcp = FastMCP("Workshop Registration MCP")

GOOGLE_SCRIPT_URL = os.getenv("GOOGLE_SCRIPT_URL")

def call_apps_script(payload: dict) -> dict:
    if not GOOGLE_SCRIPT_URL:
        raise ValueError("GOOGLE_SCRIPT_URL is not set")

    response = requests.post(
        GOOGLE_SCRIPT_URL,
        json=payload,
        timeout=20,
    )
    response.raise_for_status()

    data = response.json()
    if not data.get("success"):
        raise ValueError(data.get("message", "Unknown Apps Script error"))

    return data

@mcp.tool
def find_events(query: str) -> dict:
    """Find open events matching a user's query."""
    return call_apps_script({
        "action": "find_events",
        "query": query
    })

@mcp.tool
def register_user(
    event_id: str,
    full_name: str,
    email: str,
    phone: str = "",
    ticket_type: str = "",
    consent: bool = True,
    notes: str = "",
) -> dict:
    """Register a participant for a selected event."""
    return call_apps_script({
        "action": "register_user",
        "event_id": event_id,
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "ticket_type": ticket_type,
        "consent": consent,
        "notes": notes
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port,
    )
