from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    status: str
    integration_id: int | None

class Team(BaseModel):
    team_id: int
    name: str

class Integration(BaseModel):
    integration_id: int
    name: str
    token: str
    user: Optional[List[int]] = None
    status: str
