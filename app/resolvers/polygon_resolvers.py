import strawberry
from typing import List
from bson import ObjectId
from app.database.connection import get_db
from app.utils.utils import convert_mongo_to_polygon_type
from app.schemas.polygon import PolygonType, PolygonInput

db = get_db()

@strawberry.type
class PolygonMutation:
    @strawberry.mutation
    async def create_polygon(self, polygon: PolygonInput) -> PolygonType:
        polygon_data = {
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[coord.longitude, coord.latitude] for coord in ring] for ring in polygon.coordinates]
            },
            "fillColor": polygon.fillColor,
            "strokeColor": polygon.strokeColor,
            "strokeWidth": polygon.strokeWidth,
            "tappable": polygon.tappable,
            "zIndex": polygon.zIndex,
            "category": polygon.category
        }
        print(polygon_data)
        result = await db.polygons.insert_one(polygon_data)
        inserted_polygon = await db.polygons.find_one({"_id": result.inserted_id})

        return convert_mongo_to_polygon_type(inserted_polygon)
    
    @strawberry.mutation
    async def update_polygon(self, id: str, polygon: PolygonInput) -> PolygonType:
        polygon_id   = ObjectId(id)
        polygon_data = {
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[coord.longitude, coord.latitude] for coord in ring] for ring in polygon.coordinates]
            },
            "fillColor": polygon.fillColor,
            "strokeColor": polygon.strokeColor,
            "strokeWidth": polygon.strokeWidth,
            "tappable": polygon.tappable,
            "zIndex": polygon.zIndex,
            "category": polygon.category
        }
        await db.polygons.update_one({"_id": polygon_id}, {"$set": polygon_data})
        updated_polygon = await db.polygons.find_one({"_id": polygon_id})

        if not updated_polygon:
            raise Exception("Polygon not found or update failed.")

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

    @strawberry.field
    async def get_polygons_in_region(self, min_lat: float, min_lon: float, max_lat: float, max_lon: float) -> List[PolygonType]:
        query = {
            "geometry": {
                "$geoWithin": {
                    "$geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [min_lon, min_lat], [max_lon, min_lat],
                            [max_lon, max_lat], [min_lon, max_lat], [min_lon, min_lat]
                        ]]
                    }
                }
            }
        }

        polygons = await db.polygons.find(query).to_list(length=100)
        return [convert_mongo_to_polygon_type(polygon) for polygon in polygons]
