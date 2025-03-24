from typing import Dict
from app.schemas.polygon import PolygonType, LatLng

def convert_mongo_to_polygon_type(polygon_data: Dict) -> PolygonType:
    try:
        return PolygonType(
            id=str(polygon_data["_id"]),
            coordinates=[
                [
                    LatLng(
                        latitude=coord[1],
                        longitude=coord[0]
                    )
                    for coord in ring
                ]
                for ring in polygon_data["geometry"]["coordinates"]
            ],
            fillColor=polygon_data.get("fillColor", "#000"),
            strokeColor=polygon_data.get("strokeColor", "#000"),
            strokeWidth=polygon_data.get("strokeWidth", 1),
            tappable=polygon_data.get("tappable", False),
            zIndex=polygon_data.get("zIndex", 0),
            category=polygon_data.get("category")
        )
    except KeyError as e:
        raise ValueError(f"Invalid polygon data: {e}")
