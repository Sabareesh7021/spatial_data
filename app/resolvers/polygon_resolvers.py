import strawberry
from typing import List
from bson import ObjectId
from pymongo.errors import PyMongoError
from app.database.connection import get_db
from app.utils.utils import convert_mongo_to_polygon_type
from app.schemas.polygon import PolygonType, PolygonInput, KeyValuePair

db = get_db()

@strawberry.type
class PolygonMutation:
    @strawberry.mutation
    async def create_polygon(self, polygon: PolygonInput) -> PolygonType:
        try:
            polygon_data = {
                "name": polygon.name,
                "description": polygon.description,
                "area": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [coord.longitude, coord.latitude, coord.altitude or None]
                            for coord in ring
                        ]
                        for ring in polygon.area
                    ],
                },
                "attributes": [{"key": attr.key, "value": attr.value} for attr in polygon.attributes],
            }

            result = await db.polygons.insert_one(polygon_data)
            inserted_polygon = await db.polygons.find_one({"_id": result.inserted_id})

            if not inserted_polygon:
                raise ValueError("Failed to create polygon: Document not found.")

            return convert_mongo_to_polygon_type(inserted_polygon)

        except PyMongoError as e:
            raise ValueError(f"MongoDB Error: {str(e)}")

    @strawberry.mutation
    async def update_polygon(self, id: str, polygon: PolygonInput) -> PolygonType:
        try:
            object_id = ObjectId(id)
        except Exception:
            raise ValueError("Invalid ObjectId format.")

        polygon_data = {
            "name": polygon.name,
            "description": polygon.description,
            "area": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [coord.longitude, coord.latitude, coord.altitude or None]
                        for coord in ring
                    ]
                    for ring in polygon.area
                ],
            },
            "attributes": [{"key": attr.key, "value": attr.value} for attr in polygon.attributes],
        }

        update_result = await db.polygons.update_one({"_id": object_id}, {"$set": polygon_data})

        if update_result.matched_count == 0:
            raise ValueError(f"Polygon with id {id} not found.")

        updated_polygon = await db.polygons.find_one({"_id": object_id})
        return convert_mongo_to_polygon_type(updated_polygon)


@strawberry.type
class PolygonQuery:
    @strawberry.field
    async def get_polygon(self, id: str) -> PolygonType:
        try:
            object_id = ObjectId(id)
        except Exception:
            raise ValueError("Invalid ObjectId format.")

        polygon = await db.polygons.find_one({"_id": object_id})

        if not polygon:
            raise ValueError(f"Polygon with id {id} not found.")

        return convert_mongo_to_polygon_type(polygon)

    