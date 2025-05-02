from .mutations import Mutation
from .resolvers import Query
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.extensions import DisableValidation

schema = strawberry.Schema(query = Query, mutation=Mutation, 
                        #    extensions=[DisableValidation()]
                           )
graphql_router = GraphQLRouter(schema)