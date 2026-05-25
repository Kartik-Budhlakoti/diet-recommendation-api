from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas , models
from typing import List
router = APIRouter()

@router.post("/", response_model=schemas.FoodLogResponse)
def log_food(log: schemas.FoodLogCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == log.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_log = models.FoodLog(
        user_id=log.user_id,
        food_item=log.food_item,
        calories=log.calories,
        protein_g= log.protein_g,
        carbs_g = log.carbs_g,
        fat_g = log.fat_g
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/{user_id}", response_model=List[schemas.FoodLogResponse])
def get_logs(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    logs = db.query(models.FoodLog).filter(models.FoodLog.user_id == user_id).all()
    return logs 