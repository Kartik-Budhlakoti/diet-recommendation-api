from sqlalchemy import Column , Integer , String, Float , DateTime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age= Column(Integer, nullable=False)
    weight_kg= Column(Float, nullable=False)
    height_cm= Column(Float, nullable=False)
    gender= Column(String, nullable=False)
    activity_level = Column(String, nullable=False)
    health_goal = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class FoodLog(Base):
    __tablename__="food_logs"
    id = Column(Integer , primary_key=True, index=True)
    user_id = Column(Integer , nullable=False)
    food_item= Column(String, nullable=False)
    calories= Column(Float, nullable=False)
    protein_g= Column(Float, nullable=True)
    carbs_g= Column(Float, nullable=True)
    fat_g= Column(Float, nullable=True)
    logged_at=Column(DateTime(timezone=True), server_default=func.now())