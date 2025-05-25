import strawberry
from uuid import UUID
import strawberry.resolvers
from strawberry.types import Info
from .types import *
from ...utils import db
from ...utils.handler import DatabaseHandler
from ..base.types import BaseInput


@strawberry.input
class TypeInput(BaseInput):
    type:str
    

@strawberry.type(description="Handles category-related queries")
class CategoryQuery:
    @strawberry.field
    def getAllCategories(self, info: Info) -> GetCategorySuccess:
        session = db.get_session()
        user = info.context.get("user")
        categories = DatabaseHandler.get_all_categories_by_user_id(session, user.id)
        
        return GetCategorySuccess(
            code=200, 
            message="Get Category successfully", 
            values=categories
        )    
        
    @strawberry.field
    def getSumByCategoryType(self, info:Info, input:TypeInput) -> getSumByCategoryTypeSuccess:
        session = db.get_session()
        user = info.context.get("user")
        
        try:
            type_sum = DatabaseHandler.get_total_by_category_type(session=session, user_id=user.id)
            type_sum_dict = {k:v for k,v in type_sum}
        except :
            raise CategoryError(message="Something wrong", code=400)
        
        return getSumByCategoryTypeSuccess(values=type_sum_dict, message="Here is sum by category's type", code=200)
        

    
    