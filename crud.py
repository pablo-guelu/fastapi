from sqlalchemy.orm import Session
from . import models, schemas
from typing import List

# USERS

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.User):
    db_user = models.User()
    db_user.email = user.email
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.status = user.status
    db_user.integration_id = user.integration_id
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.User):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    db_user.email = user.email
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.status = user.status
    db_user.integration_id = user.integration_id
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user

# TEAMS

def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.team_id == team_id).first()

def get_team_by_name(db: Session, name: str):
    return db.query(models.Team).filter(models.Team.name == name).first()

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()

def create_team(db: Session, team: schemas.Team):
    db_team = models.Team(**team.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def update_team(db: Session, team_id: int, team: schemas.Team):
    db_team = db.query(models.Team).filter(models.Team.team_id == team_id).first()
    db_team.name = team.name
    db.commit()
    db.refresh(db_team)
    return db_team

def delete_team(db: Session, team_id: int):
    db_team = db.query(models.Team).filter(models.Team.team_id == team_id).first()
    db.delete(db_team)
    db.commit()
    return db_team

# INTEGRATIONS

def get_integrations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Integration).offset(skip).limit(limit).all()

def get_integrations_by_name(db: Session, name: str):
    return db.query(models.Integration).filter(models.Integration.name == name).first()

def get_integration(db: Session, integration_id: int):
    return db.query(models.Integration).filter(models.Integration.integration_id == integration_id).first()

def create_integration(db: Session, integration: schemas.Integration):
    db_integration = models.Integration(**integration.model_dump())
    db_integration.name = integration.name
    db_integration.token = integration.token
    db_integration.status = integration.status
    db.add(db_integration)
    db.commit()
    db.refresh(db_integration)
    return db_integration

def update_integration(db: Session, integration: schemas.Integration):
    db_integration = db.query(models.Integration).filter(models.Integration.integration_id == integration.id).first()
    db_integration.name = integration.name
    db_integration.token = integration.token
    db_integration.status = integration.status
    db.commit()
    db.refresh(db_integration)
    return db_integration

def delete_integration(db: Session, integration_id: int):
    db_integration = db.query(models.Integration).filter(models.Integration.integration_id == integration_id).first()
    db.delete(db_integration)
    db.commit()
    return db_integration

def create_memberships(db: Session, user_ids: List[int], team_id: int):
    for user_id in user_ids:
        user_team = models.team_membership(user_id=user_id, team_id=team_id)
        db.add(user_team)
    db.commit()