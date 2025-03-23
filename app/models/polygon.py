from pydantic import BaseModel
from typing import List, Dict

class Coordinate(BaseModel):
    latitude: float
    longitude: float
    altitude: float 

class Polygon(BaseModel):
    type: str = "Polygon"
    coordinates: List[List[Coordinate]]  # Nested arrays of Coordinate objects

class PolygonDetails(BaseModel):
    name: str
    description: str
    area: Polygon  # Polygon geometry
    attributes: Dict[str, str]  # Flexible attributes