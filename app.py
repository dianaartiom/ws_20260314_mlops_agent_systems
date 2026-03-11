from fastmcp import FastMCP
import requests
import os

mcp = FastMCP("Workshop Registration MCP")

GOOGLE_SCRIPT_URL = os.getenv("GOOGLE_SCRIPT_URL")

EVENT_ID = "mlops-agents-2026-03-14"
EVENT_TITLE = "MLOps for AI Agents Workshop"

@mcp.tool
def register_user(
    full_name: str,
    email: str,
    phone: str,
    ticket_type: str,
    consent: bool,
    notes: str = ""
) -> str:
    """Register a participant for the workshop."""

    payload = {
        "event_id": EVENT_ID,
        "event_title": EVENT_TITLE,
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "ticket_type": ticket_type,
        "consent": consent,
        "notes": notes
    }

    response = requests.post(
        GOOGLE_SCRIPT_URL,
        json=payload,
        timeout=20
    )

    response.raise_for_status()

    return response.text


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))

    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port
    )
