from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base
from typing import Optional, List

team_membership = Table(
    "team_membership",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.user_id")),
    Column("team_id", Integer, ForeignKey("teams.team_id")),
    Column("memebership_id", Integer, primary_key=True, autoincrement=True),
)

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), index=True)
    last_name = Column(String(50), index=True)
    email = Column(String(50), unique=True, index=True)
    status = Column(String(50))

    integration_id = Column(Integer, ForeignKey("integrations.integration_id"), nullable=True)
    integration = relationship("Integration", back_populates="users")

    teams = relationship("Team", secondary=team_membership, back_populates="users")

class Team(Base):
    __tablename__ = "teams"
    team_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), index=True)

    users = relationship("User", secondary=team_membership, back_populates="teams")
class Integration(Base): 
    __tablename__ = "integrations"
    integration_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), index=True)
    token = Column(String(80))
    status = Column(String(50))
    users = relationship("User", back_populates="integration")
    