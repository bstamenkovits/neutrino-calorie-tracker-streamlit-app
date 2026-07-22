import uuid

from pydantic import BaseModel

class Combination(BaseModel):
    ingredient_id: uuid.UUID
    serving_id: uuid.UUID
    ingredient_name: str
    serving_name: str
