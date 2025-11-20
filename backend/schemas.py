# backend/schemas.py
from pydantic import BaseModel, Field

class LoginIn(BaseModel):
    """Schema for the login request body."""
    username: str = Field(..., examples=["johndoe"], description="The user's unique identifier or username.")

    password: str = Field(..., examples=["my_secret_password"],description="The user's password.")

class LoginOut(BaseModel):
    """Schema for the successful login response."""
    access_token: str = Field(...,examples=["eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGl0eSI6IjMiLCJpYXQiOjE3MD..."],description="The JWT access token.")