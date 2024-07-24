from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
import uvicorn

from . import models, schemas, crud
from .database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

######### Users #########

@app.get("/users/", response_model=list[schemas.User] | schemas.User)
async def read_users(skip: int = 0, limit: int = 100, user_id: int = None, email: str = None, db: Session = Depends(get_db)):
    if user_id is not None:
        db_user = crud.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    if email is not None:
        db_user = crud.get_user_by_email(db, email=email)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    else:
        users = crud.get_users(db, skip=skip, limit=limit)
        return users

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.put("/users/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, user_id=user_id, user=user)

@app.delete("/users/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db=db, user_id=user_id)

######### Teams #########

@app.get("/teams/", response_model=list[schemas.Team] | schemas.Team)
async def read_teams(skip: int = 0, limit: int = 100, team_id: int = None, name: str = None, db: Session = Depends(get_db)):
    if team_id is not None:
        db_team = crud.get_team(db, team_id=team_id)
        if db_team is None:
            raise HTTPException(status_code=404, detail="Team not found")
        return db_team
    if name is not None:
        db_team = crud.get_team_by_name(db, name=name)
        if db_team is None:
            raise HTTPException(status_code=404, detail="Team not found")
        return db_team
    else:
        teams = crud.get_teams(db, skip=skip, limit=limit)
        return teams
    
@app.post("/teams/", status_code=status.HTTP_201_CREATED)
async def create_team(team: schemas.Team, db: Session = Depends(get_db)):
    db_team = crud.get_team_by_name(db, name=team.name)
    if db_team:
        raise HTTPException(status_code=400, detail="Team already exists")
    return crud.create_team(db=db, team=team)

@app.put("/teams/{team_id}", response_model=schemas.Team)
async def update_team(team_id: int, team: schemas.Team, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return crud.update_team(db=db, team_id=team_id, team=team)

@app.delete("/teams/{team_id}", response_model=schemas.Team)
async def delete_team(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return crud.delete_team(db=db, team_id=team_id)


######### Integrations #########

@app.get("/integrations/", response_model=list[schemas.Integration] | schemas.Integration)
async def read_integrations(skip: int = 0, limit: int = 100, name: str = None, db: Session = Depends(get_db)):
    if name is not None:
        db_integration = crud.get_integrations_by_name(db, name=name)
        if db_integration is None:
            raise HTTPException(status_code=404, detail="Integration not found")
        return db_integration
    else:
        integrations = crud.get_integrations(db, skip=skip, limit=limit)
        return integrations
    
@app.post("/integrations/", status_code=status.HTTP_201_CREATED)
async def create_integration(integration: schemas.Integration, db: Session = Depends(get_db)):
    db_integration = crud.get_integrations_by_name(db, name=integration.name)
    if db_integration:
        raise HTTPException(status_code=400, detail="Integration already exists")
    return crud.create_integration(db=db, integration=integration)

@app.put("/integrations/{integration_id}", response_model=schemas.Integration)
async def update_integration(integration_id: int, integration: schemas.Integration, db: Session = Depends(get_db)):
    db_integration = crud.get_integration(db, integration_id=integration_id)
    if db_integration is None:
        raise HTTPException(status_code=404, detail="Integration not found")
    return crud.update_integration(db=db, integration=integration)

@app.delete("/integrations/{integration_id}", response_model=schemas.Integration)
async def delete_integration(integration_id: int, db: Session = Depends(get_db)):
    db_integration = crud.get_integration(db, integration_id=integration_id)
    if db_integration is None:
        raise HTTPException(status_code=404, detail="Integration not found")
    return crud.delete_integration(db=db, integration_id=integration_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)