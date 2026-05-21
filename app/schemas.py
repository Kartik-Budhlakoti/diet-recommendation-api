from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    age:int
    weight_kg:float
    height_cm:float
    gender:str
    activity_level:str
    health_goal: str

class UserResponse(BaseModel):
    id:int
    name:str
    age:int
    weight_kg:float
    height_cm:float
    gender: str
    activity_level: str
    health_goal: str
    created_at: datetime

    class Config:
        from_attributes = True

class FoodLogCreate(BaseModel):
    user_id:int
    food_item:str
    calories:float
    protein_g: Optional[float] =None
    carbs_g:Optional[float] =None
    fat_g:Optional[float] =None

class FoodLogResponse(BaseModel):
    id:int
    user_id:int
    food_item:str
    calories:float
    protein_g: Optional[float]
    carbs_g:Optional[float]
    fat_g:Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True