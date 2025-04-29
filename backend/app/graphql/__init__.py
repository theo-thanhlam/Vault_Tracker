from .mutation import Mutation
from .resolver import Query
import strawberry
from strawberry.fastapi import GraphQLRouter

schema = strawberry.Schema(query = Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
