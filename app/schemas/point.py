import strawberry

@strawberry.type
class LocationType:
    latitude: float
    longitude: float
    latitudeDelta: float
    longitudeDelta: float


@strawberry.input
class LocationInput:
    latitude: float
    longitude: float
    latitudeDelta: float
    longitudeDelta: float


@strawberry.type
class PointType:
    id: str
    name: str
    description: str
    location: LocationType
    categories: list[str] 

@strawberry.input
class PointInput:
    name: str
    description: str
    location: LocationInput
    categories: list[str] 
