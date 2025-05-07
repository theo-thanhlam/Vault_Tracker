from .mutations import Mutation
from .resolvers import Query
import strawberry
from strawberry.fastapi import GraphQLRouter
from ..utils import session
from fastapi import Request, Response
from ..utils.auth import JWTHandler
from jwt import PyJWTError

def get_context(req:Request, res:Response) ->dict:
   token = req.cookies.get("access_token")
   user = None
   try:
      user = session.get_current_user(token=token)
   except PyJWTError:
      user = None
      
   return {
      "request":req,
      "response":res,
      "user":user
   }

schema = strawberry.Schema(query = Query, mutation=Mutation
                        #    extensions=[DisableValidation()]
                           )
graphql_router = GraphQLRouter(schema, context_getter=get_context)