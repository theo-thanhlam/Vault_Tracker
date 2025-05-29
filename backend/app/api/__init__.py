from .mutation import Mutation
from .query import Query
from .authentication.mutations import AuthMutation
from .authentication.queries import AuthQuery
import strawberry
from strawberry.fastapi import GraphQLRouter
from ..utils import session
from fastapi import Request, Response
from jwt import PyJWTError
from fastapi import HTTPException

def get_context(req:Request, res:Response) ->dict:
   token = req.cookies.get("auth_token")

   
   user = session.get_current_user(token=token)
   
      
   
      
   return {
      "request":req,
      "response":res,
      "user":user
   }

schema = strawberry.Schema(query = Query, mutation=Mutation )
graphql_router = GraphQLRouter(schema, context_getter=get_context)