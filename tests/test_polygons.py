from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_polygon():
    response = client.post(
        "/graphql",
        json={
            "query": """
            mutation {
                createPolygon(polygon: {name: "Test Polygon", description: "Test Description", area: "0,0 0,1 1,1 1,0 0,0"}) {
                    name
                    description
                    area
                }
            }
            """
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "createPolygon": {
                "name": "Test Polygon",
                "description": "Test Description",
                "area": "0,0 0,1 1,1 1,0 0,0"
            }
        }
    }