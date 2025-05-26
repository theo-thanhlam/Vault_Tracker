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
    """
    Input type for filtering or aggregating categories by their `type`.

    Inherits:
        BaseInput

    Fields:
        type (str): A string representing the category type (e.g., 'INCOME', 'EXPENSE').
    """
    type:str
    

@strawberry.type(description="Handles category-related queries")
class CategoryQuery:
    """
    Root-level GraphQL query class for interacting with category data.

    Fields:
        getAllCategories: Fetches all categories belonging to the authenticated user.
        getSumByCategoryType: Returns the total sum grouped by category type.
    """
    @strawberry.field
    def getAllCategories(self, info: Info) -> GetCategorySuccess:
        """
        Fetches all categories associated with the authenticated user.

        Args:
            info (Info): GraphQL context, expected to contain the `user` object.

        Returns:
            GetCategorySuccess: Success object with HTTP 200 code and a list of categories.

        Raises:
            None explicitly, but make sure user is authenticated at the middleware level.
        
        Example response: 
        {
        "data": {
            "getAllCategories": {
            "code": 200,
            "message": "Get Category successfully",
            "values": [
                {
                "id": "...",
                "name": "Salary",
                "type": "INCOME",
                "description": "Monthly salary",
                "user_id": "...",
                "parent_id": null
                }
            ]
            }
        }
        }

        """
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
        """
        Returns the total amounts grouped by category type (e.g., total income or expense).

        Args:
            info (Info): GraphQL context containing user.
            input (TypeInput): Input object specifying the category `type`.

        Returns:
            getSumByCategoryTypeSuccess: Success object with a dict showing total sums.

        Raises:
            CategoryError: If any unexpected error occurs during the DB operation.
        Example response:
        ```
        {
            "data": {
                "getSumByCategoryType": {
                    "code": 200,
                    "message": "Here is sum by category's type",
                    "values": {
                        "INCOME": 3000.0,
                        "EXPENSE": 1500.0
                    }
                }
            }
        }

        ```
        """
        session = db.get_session()
        user = info.context.get("user")
        
        try:
            type_sum = DatabaseHandler.get_total_by_category_type(session=session, user_id=user.id)
            type_sum_dict = {k:v for k,v in type_sum}
        except :
            raise CategoryError(message="Something wrong", code=400)
        
        return getSumByCategoryTypeSuccess(values=type_sum_dict, message="Here is sum by category's type", code=200)
        

    
    