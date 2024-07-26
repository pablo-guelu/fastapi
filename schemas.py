from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    user_id: Optional[int] = None
    first_name: str
    last_name: str
    email: str
    status: str
    integration_id: Optional[int] = None

class Team(BaseModel):
    team_id: Optional[int] = None
    name: str

class Integration(BaseModel):
    integration_id: Optional[int] = None
    name: str
    token: str
    status: str
    users: Optional[List[User]] = [] 

class TeamMembership(BaseModel):
    user_id: int
    team_id: int
    membership_id: Optional[int] = None