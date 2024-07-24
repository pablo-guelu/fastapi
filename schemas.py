from pydantic import BaseModel

class User(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    status: str

class Team(BaseModel):
    team_id: int
    name: str

class Integration(BaseModel):
    integration_id: int
    name: str
    token: str
    user_id: int
    status: str
