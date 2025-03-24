from pydantic import BaseModel

class Location(BaseModel):
    latitude: float
    longitude: float
    latitudeDelta: float
    longitudeDelta: float

class PointDetails(BaseModel):
    name: str
    description: str
    location: Location