from pydantic import BaseModel
from typing import List

class Polygon(BaseModel):
    type: str = "Polygon"
    coordinates: List[List[List[float]]]

class PolygonDetails(BaseModel):
    name: str
    description: str
    area: Polygon