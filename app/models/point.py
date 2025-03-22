from pydantic import BaseModel
from typing import Dict

class Location(BaseModel):
    latitude: float
    longitude: float

class PointDetails(BaseModel):
    name: str
    description: str
    location: Location