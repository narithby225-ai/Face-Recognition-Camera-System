"""
Token Schemas
JWT token request/response models
"""

from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data"""
    user_id: Optional[int] = None
    username: Optional[str] = None


class TokenRefresh(BaseModel):
    """Refresh token request"""
    refresh_token: str
