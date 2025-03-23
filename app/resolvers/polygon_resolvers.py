from app.database.connection import get_db
from app.schemas.polygon import (PolygonType, PolygonInput, Coordinate, KeyValuePair)
from bson import ObjectId
from typing import Dict, List
import strawberry
from app.utils.utils import convert_mongo_to_polygon_type

db = get_db()

@strawberry.type
class PolygonMutation:
    @strawberry.mutation
    async def create_polygon(self, polygon: PolygonInput) -> PolygonType:
        """
        Creates a new polygon in the database.
        """
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

    @strawberry.mutation
    async def update_polygon(self, id: str, polygon: PolygonInput) -> PolygonType:
        """
        Updates an existing polygon in the database.
        """
        object_id = ObjectId(id)
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

        await db.polygons.update_one({"_id": object_id}, {"$set": polygon_data})
        updated_polygon = await db.polygons.find_one({"_id": object_id})

        if not updated_polygon:
            raise ValueError(f"Polygon with id {id} not found.")

        return convert_mongo_to_polygon_type(updated_polygon)


@strawberry.type
class PolygonQuery:
    @strawberry.field
    async def get_polygon(self, id: str) -> PolygonType:
        """
        Retrieves a polygon by its ID.
        """
        object_id = ObjectId(id)
        polygon = await db.polygons.find_one({"_id": object_id})

        if not polygon:
            raise ValueError(f"Polygon with id {id} not found.")

        return convert_mongo_to_polygon_type(polygon)

    @strawberry.field
    async def get_attributes_by_location(
        self,
        latitude: float,
        longitude: float,
        keys: List[str]  # List of attribute keys to retrieve
    ) -> List[KeyValuePair]:
        """
        Retrieves multiple attributes for a county/state based on its latitude and longitude.
        """
        # Find the polygon that contains the specified latitude and longitude
        polygon = await db.polygons.find_one({
            "area.coordinates": {
                "$elemMatch": {
                    "$elemMatch": {
                        "$and": [
                            {"1": latitude},  # Latitude is at index 1
                            {"0": longitude}  # Longitude is at index 0
                        ]
                    }
                }
            }
        })

        if not polygon:
            raise ValueError(f"No polygon found for the specified location: {latitude}, {longitude}")

        # Retrieve the specified attributes
        attributes = []
        for key in keys:
            found = False
            for attr in polygon["attributes"]:
                if attr["key"] == key:
                    attributes.append(KeyValuePair(key=key, value=attr["value"]))
                    found = True
                    break
            if not found:
                # If the attribute is not found, skip it or provide a default value
                attributes.append(KeyValuePair(key=key, value=""))  # Default value for missing attributes

        return attributes