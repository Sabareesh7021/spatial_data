import strawberry
from typing import Optional

@strawberry.type
class LatLng:
    latitude: float
    longitude: float
    latitudeDelta: Optional[float] = None
    longitudeDelta: Optional[float] = None

@strawberry.input
class LatLngInput:
    latitude: float
    longitude: float
    latitudeDelta: Optional[float]=None
    longitudeDelta: Optional[float]=None
