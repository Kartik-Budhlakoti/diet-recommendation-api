from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ActivityLevel(str, Enum):
    sedentary = "sedentary"
    light = "light"
    moderate = "moderate"
    active = "active"
    very_active = "very_active"

class HealthGoal(str , Enum):
    weight_loss = "weight_loss"
    weight_gain = "weight_gain"
    muscle_building = "muscle_building"
    balanced = "balanced"
    diabetes = "diabetes"

class UserCreate(BaseModel):
    name: str
    age:int
    weight_kg:float
    height_cm:float
    gender:str
    activity_level:ActivityLevel
    health_goal: HealthGoal

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
    logged_at: datetime

    class Config:
        from_attributes = True

class DietRecommendation(BaseModel):
    user_id: int
    bmi: float
    bmi_category:str
    daily_calorie: float
    diet_category:str
    breakfast: str
    lunch:str
    dinner:str
    snacks:str
    protein_g:float
    carbs_g:float
    fat_g:float
