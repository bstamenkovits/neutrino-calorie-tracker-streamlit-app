import uuid
import datetime
from typing import Optional
from pydantic import BaseModel, Field


class FoodSummary(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    meal_id: uuid.UUID
    ingredient_id: uuid.UUID
    serving_id: uuid.UUID
    date: datetime.date
    meal_name: str
    name: str
    quantity: float
    serving_name: str
    total_weight_g: float
    total_calories_kcal: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
