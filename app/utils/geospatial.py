from geojson import Point, Polygon

def create_geojson_point(coordinates):
    return Point(coordinates)

def create_geojson_polygon(coordinates):
    return Polygon(coordinates)