from app.schemas.polygon import PolygonType, Coordinate, KeyValuePair
from typing import Dict

def convert_mongo_to_polygon_type(polygon_data: Dict) -> PolygonType:
    """
    Converts a MongoDB document to a PolygonType object.
    """
    try:
        return PolygonType(
            id=str(polygon_data["_id"]),
            name=polygon_data["name"],
            description=polygon_data["description"],
            area=[
                [
                    Coordinate(
                        latitude=coord[1],
                        longitude=coord[0],
                        altitude=coord[2] if len(coord) > 2 else None
                    )
                    for coord in ring
                ]
                for ring in polygon_data["area"]["coordinates"]
            ],
            attributes=[
                KeyValuePair(key=attr["key"], value=attr["value"])
                for attr in polygon_data["attributes"]
            ],
        )
    except KeyError as e:
        raise ValueError(f"Invalid polygon data: {e}")