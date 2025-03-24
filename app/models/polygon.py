from typing import List
from pydantic import BaseModel

from app.models.point import LatLngModel  

class PolygonGeometry(BaseModel):
    type: str = "Polygon"
    coordinates: List[List[LatLngModel]]
    
class PolygonDetails(BaseModel):
    name: str
    description: str
    geometry: PolygonGeometry
    fillColor: str = "#000"
    strokeColor: str = "#000"
    strokeWidth: int = 1
    tappable: bool = False
    zIndex: int = 0
    category: str
