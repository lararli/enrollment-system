"""
This module implements the creation of
new users and the validation of existent users.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class User(BaseModel):
    """
    This class implements the user object, where all the objects will have a login, password
    and a user id that will be assigned after validation.
    """
    first_name: str
    last_name: str
    email: str
    password: str
    account_role: list


class Course(BaseModel):
    name: str
    workload: float
    created_by: list
    related_topics: list


class Session(BaseModel):
    """
    This class implements a session, where all the objects will have as
    attributes the path containing both information about courses and users.
    """
    # session_id: Optional[UUID] = uuid4()
    user: User
    start_date: datetime
    end_date: datetime
