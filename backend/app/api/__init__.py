from .mutation import Mutation
from .resolver import Query
from .authentication.mutations import AuthMutation
from .authentication.resolvers import AuthQuery
import strawberry
from strawberry.fastapi import GraphQLRouter
from ..utils import session
from fastapi import Request, Response
from jwt import PyJWTError


def get_context(req:Request, res:Response) ->dict:
   token = req.cookies.get("auth_token")
  
   
   try:
      user = session.get_current_user(token=token)
   except PyJWTError:
      user = None
      
   return {
      "request":req,
      "response":res,
      "user":user
   }


# auth_schema = strawberry.Schema(query = AuthQuery, mutation=AuthMutation )
# auth_graphql_router = GraphQLRouter(auth_schema, context_getter=get_context)


# protected_schema = strawberry.Schema(query = ProtectedQuery, mutation=ProtectedMutation)
                     
# protected_graphql_router = GraphQLRouter(protected_schema, context_getter=get_context)


schema = strawberry.Schema(query = Query, mutation=Mutation )
graphql_router = GraphQLRouter(schema, context_getter=get_context)