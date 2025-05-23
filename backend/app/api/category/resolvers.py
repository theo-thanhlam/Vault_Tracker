import strawberry
from uuid import UUID
import strawberry.resolvers
from strawberry.types import Info
from .types import *
from ...utils import db
from ...utils.handler import DatabaseHandler


@strawberry.type(description="Handles category-related queries")
class CategoryQuery:
    @strawberry.field
    def getCategory(self, info: Info) -> GetCategorySuccess:
        session = db.get_session()
        user = info.context.get("user")
        categories = DatabaseHandler.get_all_categories_by_user_id(session, user.id)
        
        return GetCategorySuccess(
            code=200, 
            message="Get Category successfully", 
            values=categories
        )    

    
    