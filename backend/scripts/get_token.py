"""
Get a Supabase access token for testing GET /auth/me.

Usage (from backend/):
  .\\.venv\\Scripts\\Activate.ps1
  $env:PYTHONPATH = (Get-Location).Path
  python scripts\\get_token.py

It reads SUPABASE_URL + SUPABASE_PUBLISHABLE_KEY from .env,
then asks for email/password of a user you already created in Supabase Auth.
"""
from getpass import getpass

import requests

from app.core.config import SUPABASE_PUBLISHABLE_KEY, SUPABASE_URL, auth_env_ready


def main() -> None:
    if not auth_env_ready():
        raise SystemExit(
            "Missing SUPABASE_URL or SUPABASE_PUBLISHABLE_KEY in backend/.env"
        )

    email = input("Email: ").strip()
    password = getpass("Password: ")

    response = requests.post(
        f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
        headers={"apikey": SUPABASE_PUBLISHABLE_KEY},
        json={"email": email, "password": password},
        timeout=15,
    )

    if response.status_code != 200:
        raise SystemExit(f"Login failed ({response.status_code}): {response.text}")

    token = response.json().get("access_token")
    if not token:
        raise SystemExit(f"No access_token in response: {response.text}")

    print("\n--- paste this into Swagger Authorize (Bearer) ---\n")
    print(token)
    print("\n--- then GET /auth/me ---\n")


if __name__ == "__main__":
    main()
