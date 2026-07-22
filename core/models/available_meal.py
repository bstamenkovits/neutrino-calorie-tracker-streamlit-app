from pydantic import BaseModel, Field
import uuid


class AvailableMeal(BaseModel):
    id: uuid.UUID
    name: str
