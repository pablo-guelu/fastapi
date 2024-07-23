from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from .database import Base

team_membership = Table(
    "teams_memberships",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.user_id")),
    Column("team_id", Integer, ForeignKey("teams.team_id")),
)

class team_memebership(Base):
    __tablename__ = "teams_memberships"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.team_id"), primary_key=True)
    membership_id = Column(Integer, primary_key=True)

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


