from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas , models
from app.database import get_db

router = APIRouter()

@router.post("/register" , response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db : Session= Depends(get_db)):
    db_user = models.User(
        name=user.name,
        age=user.age,
        weight_kg= user.weight_kg,
        height_cm=user.height_cm,
        gender= user.gender,
        activity_level=user.activity_level,
        health_goal=user.health_goal
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user