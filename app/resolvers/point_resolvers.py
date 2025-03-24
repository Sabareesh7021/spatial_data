import strawberry
from bson import ObjectId
from app.database.connection import get_db
from app.schemas.point import PointType, PointInput, LatLng

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
                "longitude": point.location.longitude,
                "latitudeDelta": point.location.latitudeDelta,
                "longitudeDelta": point.location.longitudeDelta,
            },
            "categories": point.categories
        }
        result = await db.points.insert_one(point_data)
        if not result.inserted_id:  
            raise ValueError("Point not Added")
        
        return PointType(
            id=str(result.inserted_id),
            name=point.name,
            description=point.description,
            location=LatLng(
                latitude=point.location.latitude,
                longitude=point.location.longitude,
                latitudeDelta=point.location.latitudeDelta,
                longitudeDelta=point.location.longitudeDelta,
            ),
            categories=point.categories
        )

    @strawberry.mutation
    async def update_point(self, id: str, point: PointInput) -> PointType:
        object_id = ObjectId(id)
        result = await db.points.update_one(
            {"_id": object_id},
            {"$set": {
                "name": point.name,
                "description": point.description,
                "location": {
                    "latitude": point.location.latitude,
                    "longitude": point.location.longitude,
                    "latitudeDelta": point.location.latitudeDelta,
                    "longitudeDelta": point.location.longitudeDelta,
                },
                "categories": point.categories
            }}
        )

        if result.matched_count == 0:  
            raise ValueError("Point not found")
        
        return PointType(
            id=id,
            name=point.name,
            description=point.description,
            location=LatLng(
                latitude=point.location.latitude,
                longitude=point.location.longitude,
                latitudeDelta=point.location.latitudeDelta,
                longitudeDelta=point.location.longitudeDelta,
            ),
            categories=point.categories
        )
    
@strawberry.type
class PointQuery:
    @strawberry.field
    async def get_point(self, id: str) -> PointType:
        point = await db.points.find_one({"_id": ObjectId(id)})
        if not point:
            raise ValueError("Point not found")

        return PointType(
            id=id,
            name=point["name"],
            description=point["description"],
            location=LatLng(
                latitude=point["location"]["latitude"],
                longitude=point["location"]["longitude"],
                latitudeDelta=point["location"]["latitudeDelta"],
                longitudeDelta=point["location"]["longitudeDelta"],
            ),
            categories=point["categories"]
        )
    
    @strawberry.field
    async def get_points_in_region(self, latitude: float, longitude: float, latitudeDelta: float, longitudeDelta: float, categories: list[str] = None) -> list[PointType]:
        min_lat, max_lat = latitude - latitudeDelta / 2, latitude + latitudeDelta / 2
        min_lon, max_lon = longitude - longitudeDelta / 2, longitude + longitudeDelta / 2

        query = {
            "location.latitude": {"$gte": min_lat, "$lte": max_lat},
            "location.longitude": {"$gte": min_lon, "$lte": max_lon}
        }

        if categories:
            query["categories"] = {"$in": categories} 

        points = await db.points.find(query).to_list(length=None)

        return [
            PointType(
                id=str(point["_id"]),
                name=point["name"],
                description=point["description"],
                location=LatLng(
                    latitude=point["location"]["latitude"],
                    longitude=point["location"]["longitude"],
                    latitudeDelta=point["location"]["latitudeDelta"],
                    longitudeDelta=point["location"]["longitudeDelta"],
                ),
                categories=point["categories"]
            ) for point in points
        ]