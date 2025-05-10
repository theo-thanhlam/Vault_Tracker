from .mutation import ProtectedMutation
from .resolver import ProtectedQuery
from .authentication.mutations import AuthMutation
from .authentication.resolvers import AuthQuery
import strawberry
from strawberry.fastapi import GraphQLRouter
from ..utils import session
from fastapi import Request, Response
from ..utils.handler import JWTHandler
from jwt import PyJWTError
from fastapi import Depends

def get_context(req:Request, res:Response) ->dict:
   token = req.cookies.get("access_token")
   
   try:
      user = session.get_current_user(token=token)
   except PyJWTError:
      user = None
      
   return {
      "request":req,
      "response":res,
      "user":user
   }


auth_schema = strawberry.Schema(query = AuthQuery, mutation=AuthMutation)
auth_graphql_router = GraphQLRouter(auth_schema)


protected_schema = strawberry.Schema(query = ProtectedQuery, mutation=ProtectedMutation
                        #    extensions=[DisableValidation()]
                           )

protected_graphql_router = GraphQLRouter(protected_schema, context_getter=get_context)