from pydantic import BaseModel
from enum import Enum


class Role(str, Enum):
    admin: str = 'admin'
    user: str = 'user'


class User(BaseModel):
    """
    This class implements the user object, where all the objects is going to have a login, password
    and a user id that will be assigned after validation.
    """
    first_name: str
    last_name: str
    email: str
    password: str
    account_role: Role


class Course(BaseModel):
    """
    This class implements the user objet, where all the objects is going to have a name, workload and two lists, one
    that contains who create the course and other the related topics.
    """
    name: str
    workload: float
    created_by: list
    related_topics: list
