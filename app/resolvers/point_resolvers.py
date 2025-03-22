from app.database.connection import get_db
from app.schemas.point import PointType, PointInput, LocationType
from bson import ObjectId
import strawberry

db = get_db()

@strawberry.type
class PointMutation:
    @strawberry.mutation
    async def create_point(self, point: PointInput) -> PointType:
        point_data = {
            "name": point.name,
            "description": point.description,
            "location": {
            "latitude": point.location.latitude,
            "longitude": point.location.longitude
        }
        }
        result = await db.points.insert_one(point_data)
        if not result.inserted_id:  
            raise ValueError("Point not Added")
        
        return PointType(
            id=str(result.inserted_id),
            name=point.name,
            description=point.description,
            location=LocationType(
            latitude=point.location.latitude,
            longitude=point.location.longitude
        )
        )

    @strawberry.mutation
    async def update_point(self, id: str, point: PointInput) -> PointType:
        object_id = ObjectId(id)
        result    = await db.points.update_one(
            {"_id": object_id},
            {"$set": {
                "name": point.name,
                "description": point.description,
                "location": {
                    "latitude": point.location.latitude,
                    "longitude": point.location.longitude
                }
            }}
        )

        if not result.inserted_id:  
            raise ValueError("Point not found")
        
        return PointType(
            id=id,
            name=point.name,
            description=point.description,
            location=LocationType(
            latitude=point.location.latitude,
            longitude=point.location.longitude
        )
        )
    
@strawberry.type
class PointQuery:
    @strawberry.field
    async def get_point(self, id: str) -> PointType:
        point = await db.points.find_one({"_id": ObjectId(id)})
        return PointType(
            id=id,
            name=point["name"],
            description=point["description"],
            location=LocationType(
            latitude=point["location"]["latitude"],
            longitude=point["location"]["longitude"],
        )
        )