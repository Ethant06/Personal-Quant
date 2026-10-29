"""
Auth-related HTTP routes.

Feature routers live under app/api/ and are mounted from main.py.
Login/signup UI will live in Next.js + Supabase client; this API only
answers "who is the current user?" after a valid Bearer token.
"""
from fastapi import APIRouter, Depends

from app.auth.deps import get_current_profile

# prefix=/auth → paths become /auth/me, /auth/...
# tags=["auth"] → groups these endpoints in Swagger
router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
def read_me(profile: dict = Depends(get_current_profile)):
    """Requires Authorization: Bearer <access_token>."""
    return profile
