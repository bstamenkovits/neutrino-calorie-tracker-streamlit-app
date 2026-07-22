import uuid
import datetime
from typing import Optional
from pydantic import BaseModel, Field


class FoodLog(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: Optional[uuid.UUID] = None
    meal_id: uuid.UUID
    ingredient_id: uuid.UUID
    serving_id: uuid.UUID
    quantity: float
    consumed_on: datetime.date = Field(default_factory=datetime.date.today)
    date_created: datetime.datetime = Field(default_factory=datetime.datetime.now)
    date_modified: datetime.datetime = Field(default_factory=datetime.datetime.now)