import strawberry
from app.resolvers.point_resolvers import PointQuery, PointMutation
from app.resolvers.polygon_resolvers import PolygonQuery, PolygonMutation

@strawberry.type
class Query(PointQuery, PolygonQuery):
    pass

@strawberry.type
class Mutation(PointMutation, PolygonMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
