from fastapi import FastAPI
from app.schemas import schema
from strawberry.asgi import GraphQL

app = FastAPI()
app.add_route("/graphql", GraphQL(schema))

@app.get('/')
@app.post('/')
def root():
    return {"message": "Connected to spatial data", "status":True}