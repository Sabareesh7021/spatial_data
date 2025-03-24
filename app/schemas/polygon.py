import strawberry
from typing import List, Optional
from app.schemas.common import LatLng, LatLngInput

@strawberry.type
class PolygonType:
    id: str
    coordinates: List[List[LatLng]]
    fillColor: str
    strokeColor: str
    strokeWidth: Optional[int] = 1
    tappable: Optional[bool] = False
    zIndex: Optional[int] = 0
    category: str

@strawberry.input
class PolygonInput:
    coordinates: List[List[LatLngInput]]
    fillColor: str
    strokeColor: str
    strokeWidth: Optional[int] = 1
    tappable: Optional[bool] = False
    zIndex: Optional[int] = 0
    category: str
