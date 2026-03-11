from fastmcp import FastMCP
import requests
import os

mcp = FastMCP("Sheets MCP")

GOOGLE_SCRIPT_URL = os.getenv("GOOGLE_SCRIPT_URL")

@mcp.tool
def register_user(name: str, email: str) -> str:
    """Register a user into the Google Sheet."""
    response = requests.post(
        GOOGLE_SCRIPT_URL,
        json={"name": name, "email": email},
        timeout=20,
    )
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    mcp.run()
