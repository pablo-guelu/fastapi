from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, Mapped
from .database import Base

team_membership = Table(
    "team_membership",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.user_id")),
    Column("team_id", Integer, ForeignKey("teams.team_id")),
    Column("memebership_id", Integer, primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    status = Column(String)

    teams = relationship("Team", secondary=team_membership, back_populates="users")

class Team(Base):
    __tablename__ = "teams"
    team_id = Column(Integer, primary_key=True)
    name = Column(String, index=True)

    users = relationship("User", secondary=team_membership, back_populates="teams")


class Integration(Base): 
    __tablename__ = "integrations"
    integration_id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    token = Column(String)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    status = Column(String)

    users = relationship("User")
    