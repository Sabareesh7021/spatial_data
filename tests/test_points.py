from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_point():
    response = client.post(
        "/graphql",
        json={
            "query": """
            mutation {
                createPoint(point: {name: "Test Point", description: "Test Description", location: "0,0"}) {
                    name
                    description
                    location
                }
            }
            """
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "createPoint": {
                "name": "Test Point",
                "description": "Test Description",
                "location": "0,0"
            }
        }
    }