from .mutations import Mutation
from .resolvers import Query
import strawberry
from strawberry.fastapi import GraphQLRouter

schema = strawberry.Schema(query = Query, mutation=Mutation)
graphql_router = GraphQLRouter(schema)