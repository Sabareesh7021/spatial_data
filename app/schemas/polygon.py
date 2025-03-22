import strawberry

@strawberry.type
class PolygonType:
    id:str
    name: str
    description: str
    area: str

@strawberry.input
class PolygonInput:
    name: str
    description: str
    area: str