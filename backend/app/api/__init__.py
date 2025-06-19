from .mutation import Mutation
from .query import Query
import strawberry
from strawberry.fastapi import GraphQLRouter
from ..utils import session
from fastapi import Request, Response
from jwt import PyJWTError
from dotenv import load_dotenv
from ..utils.environment import get_environment

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

env = get_environment()
ide = "graphiql" if env == "development" else None

schema = strawberry.Schema(query = Query, mutation=Mutation )
graphql_router = GraphQLRouter(schema, context_getter=get_context,graphql_ide=ide)