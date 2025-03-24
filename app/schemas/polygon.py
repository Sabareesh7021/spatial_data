import strawberry
from typing import List, Optional

@strawberry.type
class KeyValuePair:
    key: str
    value: str

@strawberry.type
class Coordinate:
    latitude: float
    longitude: float
    altitude: Optional[float] = None

@strawberry.type
class PolygonType:
    id: str
    name: str
    description: str
    area: List[List[Coordinate]]
    attributes: List[KeyValuePair]

@strawberry.input
class KeyValuePairInput:
    key: str
    value: str

@strawberry.input
class CoordinateInput:
    latitude: float
    longitude: float
    altitude: Optional[float] = None

@strawberry.input
class PolygonInput:
    name: str
    description: str
    area: List[List[CoordinateInput]]
    attributes: List[KeyValuePairInput]
