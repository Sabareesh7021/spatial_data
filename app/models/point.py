from pydantic import BaseModel

class LatLngModel(BaseModel):
    latitude: float
    longitude: float
    latitudeDelta: float
    longitudeDelta: float

class PointDetails(BaseModel):
    name: str
    description: str
    location: LatLngModel
