import strawberry

@strawberry.type
class LocationType:
    latitude: float
    longitude: float


@strawberry.type
class PointType:
    id: str
    name: str
    description: str
    location: LocationType 


@strawberry.input
class LocationInput:
    latitude: float
    longitude: float


@strawberry.input
class PointInput:
    name: str
    description: str
    location: LocationInput
