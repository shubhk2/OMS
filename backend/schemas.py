# backend/schemas.py
from pydantic import BaseModel, Field
from apiflask import Schema
from apiflask.fields import Integer, String, Date

class LoginIn(BaseModel):
    """Schema for the login request body."""
    username: str = Field(..., examples=["johndoe"], description="The user's unique identifier or username.")

    password: str = Field(..., examples=["my_secret_password"],description="The user's password.")

class LoginOut(BaseModel):
    """Schema for the successful login response."""
    access_token: str = Field(...,examples=["eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGl0eSI6IjMiLCJpYXQiOjE3MD..."],description="The JWT access token.")

class LeaveRequestIn(Schema):
    leave_type_id = Integer(required=True)
    from_date = Date(required=True)
    to_date = Date(required=True)
    reason = String(required=True)

class LeaveRequestOut(Schema):
    id = Integer()
    leave_type_id = Integer()
    leave_type_name = String()
    from_date = Date()
    to_date = Date()
    reason = String()
    status = Integer()

class OTRequestIn(Schema):
    for_date = Date(required=True)
    extra_task_description = String(required=True)
    requested_minutes = Integer(required=True)

class OTRequestOut(Schema):
    id = Integer()
    for_date = Date()
    requested_minutes = Integer()
    status = Integer()

class WFHRequestIn(Schema):
    from_date = Date(required=True)
    to_date = Date(required=True)
    reason = String(required=True)

class WFHRequestOut(Schema):
    id = Integer()
    from_date = Date()
    to_date = Date()
    status = Integer()

class MonthlyStatusQuery(Schema):
    month = Integer(required=True)
    year = Integer(required=True)

