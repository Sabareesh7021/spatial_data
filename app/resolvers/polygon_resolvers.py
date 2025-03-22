from app.database.connection import get_db
from app.schemas.polygon import PolygonType, PolygonInput
from bson import ObjectId
import strawberry

db = get_db()

@strawberry.type
class PolygonMutation:
    @strawberry.mutation
    async def create_polygon(self, polygon: PolygonInput) -> PolygonType:
        polygon_data = {
        "name": polygon.name,
        "description": polygon.description,
        "area": polygon.area,
        }
        result = await db.polygons.insert_one(polygon_data)
        inserted_polygon = await db.polygons.find_one({"_id": result.inserted_id})
       
        return PolygonType(
            id=str(inserted_polygon["_id"]),
            name=inserted_polygon["name"],
            description=inserted_polygon["description"],
            area=inserted_polygon["area"],
        )

    @strawberry.mutation
    async def update_polygon(self, id: str, polygon: PolygonInput) -> PolygonType:
        object_id = ObjectId(id)
        result    = await db.polygons.update_one(
            {"_id": object_id},
            {"$set": {
                "name": polygon.name,
                "description": polygon.description,
                "area": polygon.area
            }}
        )

        if result.matched_count == 0:
            raise ValueError("Polygon not found")

        updated_polygon = await db.polygons.find_one({"_id": object_id})
        return PolygonType(
            id=str(updated_polygon["_id"]),
            name=updated_polygon["name"],
            description=updated_polygon["description"],
            area=updated_polygon["area"]
        )

@strawberry.type
class PolygonQuery:
    @strawberry.field
    async def get_polygon(self, id: str) -> PolygonType:
        polygon = await db.polygons.find_one({"_id": ObjectId(id)})
        return PolygonType(id=id,
            name=polygon["name"],
            description=polygon["description"],
            area=polygon["area"],
        )