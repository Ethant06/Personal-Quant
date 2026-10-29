"""
FastAPI dependencies for protected routes.

Pattern: route declares Depends(get_current_profile) → FastAPI extracts the
Bearer token, we verify it, then load (or create) investory.users.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import text

from app.auth.jwt import AuthUser, decode_access_token
from app.database import engine

# Tells OpenAPI/Swagger to show the Authorize lock (HTTP Bearer scheme)
_bearer = HTTPBearer(auto_error=True)


def get_current_auth_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> AuthUser:
    # credentials.credentials = raw token string (without the word "Bearer")
    return decode_access_token(credentials.credentials)


def get_current_profile(
    auth_user: AuthUser = Depends(get_current_auth_user),
) -> dict:
    """
    Return the investory.users row for this Auth id.

    Fallback INSERT: if the DB trigger missed creating a profile (edge case),
    create one here so /auth/me still works.
    """
    with engine.begin() as conn:
        row = conn.execute(
            text(
                """
                SELECT id, email, display_name, created_at, updated_at
                FROM investory.users
                WHERE id = :id
                """
            ),
            {"id": auth_user.id},
        ).mappings().first()

        if row is None:
            conn.execute(
                text(
                    """
                    INSERT INTO investory.users (id, email, display_name)
                    VALUES (:id, :email, :display_name)
                    ON CONFLICT (id) DO NOTHING
                    """
                ),
                {
                    "id": auth_user.id,
                    "email": auth_user.email,
                    "display_name": (
                        (auth_user.email or "user").split("@", 1)[0]
                    ),
                },
            )
            row = conn.execute(
                text(
                    """
                    SELECT id, email, display_name, created_at, updated_at
                    FROM investory.users
                    WHERE id = :id
                    """
                ),
                {"id": auth_user.id},
            ).mappings().first()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not load or create app user profile",
        )

    return {
        "id": str(row["id"]),
        "email": row["email"],
        "display_name": row["display_name"],
        "created_at": row["created_at"].isoformat() if row["created_at"] else None,
        "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None,
        "auth": {
            "email": auth_user.email,
            "role": auth_user.role,
        },
    }
