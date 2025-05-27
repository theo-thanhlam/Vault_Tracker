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
        ```
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
                "children": [] | None # Recursive
                }
            ]
            }
        }
        }
        ```

        """
        session = db.get_session()
        user = info.context.get("user")
        categories = DatabaseHandler.get_all_categories_by_user_id(session, user.id)
        categories_tree = build_tree(categories)
        
        
        
        return GetCategorySuccess(
            code=200, 
            message="Get Category successfully", 
            values=categories,
            
        )    
        
def build_tree(categories:List[CategoryType]) -> List[CategoryType]:
    item_dict = {
        category.id: CategoryType(
            id=category.id,
            name=category.name,
            created_at=category.created_at,
            deleted_at=category.deleted_at,
            updated_at=category.updated_at,
            type=category.type,
            description=category.description,
            user_id=category.user_id,
            children=[]
        )
        for category in categories
    }
    root_items = []

    for category in categories:
        node = item_dict[category.id]
        if category.parent_id:
            parent_node = item_dict.get(category.parent_id)
            if parent_node:
                parent_node.children.append(node)
        else:
            root_items.append(node)
    
    
    def clean_children(node: CategoryType):
        if not node.children:
            node.children = None
        else:
            for child in node.children:
                clean_children(child)

    for root in root_items:
        clean_children(root)
        
    return root_items
  

    
    