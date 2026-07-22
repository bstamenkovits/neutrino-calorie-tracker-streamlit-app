from pydantic import BaseModel, Field
import uuid


class AvailableIngredient(BaseModel):
    id: uuid.UUID
    name: str
    calories_kcal: float
