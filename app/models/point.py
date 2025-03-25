from pydantic import BaseModel
from typing import List

class LatLngModel(BaseModel):
    latitude: float
    longitude: float
    latitudeDelta: float
    longitudeDelta: float

class PointDetails(BaseModel):
    name: str
    description: str
    location: LatLngModel
    categories: List[str]
