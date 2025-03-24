import strawberry
from typing import List
from app.schemas.common import LatLng, LatLngInput

@strawberry.type
class PointType:
    id: str
    name: str
    description: str
    location: LatLng
    categories: List[str]

@strawberry.input
class PointInput:
    name: str
    description: str
    location: LatLngInput
    categories: List[str]
