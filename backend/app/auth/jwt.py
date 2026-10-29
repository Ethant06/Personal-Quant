"""
Turn a Bearer access_token into a trusted AuthUser.

We ask Supabase Auth "is this token valid?" instead of decoding with a local
JWT secret. That works with Supabase's newer publishable keys (sb_publishable_...).
"""
from dataclasses import dataclass

import requests
from fastapi import HTTPException, status

from app.core.config import (
    SUPABASE_PUBLISHABLE_KEY,
    SUPABASE_URL,
    auth_env_ready,
)


@dataclass(frozen=True)
class AuthUser:
    """Subset of Supabase Auth user fields we care about in the API."""

    id: str
    email: str | None
    role: str | None


def decode_access_token(token: str) -> AuthUser:
    if not auth_env_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Auth is not configured. Set SUPABASE_URL and "
                "SUPABASE_PUBLISHABLE_KEY in backend/.env (see docs/AUTH_SETUP.md)."
            ),
        )

    try:
        # Official check: GET /auth/v1/user with user JWT + project publishable key
        response = requests.get(
            f"{SUPABASE_URL}/auth/v1/user",
            headers={
                "apikey": SUPABASE_PUBLISHABLE_KEY,
                "Authorization": f"Bearer {token}",
            },
            timeout=10,
        )
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not reach Supabase Auth to verify token",
        ) from exc

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = response.json()
    user_id = data.get("id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return AuthUser(
        id=user_id,
        email=data.get("email"),
        role=data.get("role"),
    )
