import strawberry
from ..base.types import BaseInput
from ...models import *
from uuid import UUID
from typing import Optional
from strawberry import Info
from .types import *
from ...utils import db
from sqlalchemy import sql
from ..base.mutations import BaseAuthenticatedMutation
from ...utils.handler import *
from fastapi import status
from uuid import UUID
from ...utils.handler import login_required


@strawberry.input
class CreateCategoryInput(BaseInput):
    """
    Input type for creating a new category.

    Inherits:
        BaseInput: Adds helper method `to_dict()` for parsing.

    Fields:
        name (str): Name of the category.
        type (CategoryTypeEnum): Enum representing the category type.
        description (str): Description of the category.
        parent_id (Optional[UUID]): Optional UUID of a parent category for nested structure.
    """
    name: str
    type: CategoryTypeEnum
    description: str
    parent_id: Optional[UUID] = None



@strawberry.input
class UpdateCategoryInput(BaseInput):
    """
    Input type for updating an existing category.

    Inherits:
        BaseInput: Adds helper method `to_dict()` for parsing.

    Fields:
        id (UUID): Unique identifier of the category to update.
        name (Optional[str]): New name of the category.
        type (Optional[CategoryTypeEnum]): Updated category type.
        description (Optional[str]): Updated description.
        parent_id (Optional[UUID]): Updated parent category ID.
    """
    id: UUID
    name: Optional[str] = None
    type: Optional[CategoryTypeEnum] = None
    description: Optional[str] = None
    parent_id: Optional[UUID] = None

    
@strawberry.input
class DeleteCategoryInput(BaseInput):
    """
    Input type for deleting a category.

    Inherits:
        BaseInput: Adds helper method `to_dict()` for parsing.

    Fields:
        id (UUID): Unique identifier of the category to delete.
    """
    id: UUID



@strawberry.type
class CategoryMutation(
    BaseAuthenticatedMutation[
        CategoryModel,
        CreateCategoryInput,
        UpdateCategoryInput,
        DeleteCategoryInput,
        CategorySuccess,
        CategoryType
    ]
):
    """
    GraphQL mutation type for managing categories.

    Inherits:
        BaseAuthenticatedMutation: Generic mutation base class that handles create, update, and delete operations with authentication.

    Attributes:
        model: SQLAlchemy model for Category.
        success_type: Response type returned after mutation operations.
        type: GraphQL output type used in the success response.
    """

    model = CategoryModel
    success_type = CategorySuccess
    type = CategoryType

    @strawberry.mutation
    def create(self, input: CreateCategoryInput, info: strawberry.Info) -> CategorySuccess:
        """
        Create a new category.

        Args:
            input (CreateCategoryInput): Input data for the new category.
            info (strawberry.Info): GraphQL context containing user/session.

        Returns:
            CategorySuccess: Success response with the created category.
        """
        return super().create(input, info)

    @strawberry.mutation
    def update(self, input: UpdateCategoryInput, info: strawberry.Info) -> CategorySuccess:
        """
        Update an existing category.

        Args:
            input (UpdateCategoryInput): Updated fields and category ID.
            info (strawberry.Info): GraphQL context containing user/session.

        Returns:
            CategorySuccess: Success response with the updated category.
        """
        session = db.get_session()
        user = info.context.get("user")
        existing_category = session.get(self.model, input.id)
        if not existing_category or existing_category.deleted_at:
            raise CategoryError(message="Not Found", code=status.HTTP_404_NOT_FOUND)
        if user.id != existing_category.user_id:
            raise CategoryError(message = "Unauthorized", code=status.HTTP_401_UNAUTHORIZED)

        # Check for circular reference if parent_id is being updated
        if input.parent_id is not None:
            if self.check_circular_reference(session, input.id, input.parent_id):
                raise CategoryError(
                    message="Circular reference detected in category hierarchy",
                    code=status.HTTP_400_BAD_REQUEST
                )

        parsed_input = input.to_dict()
        for k,v in parsed_input.items():
            if v is not None:
                setattr(existing_category, k, v)
        existing_category.parent_id = input.parent_id
        existing_category.updated_at = sql.func.now()
        session.commit()
        return self.success_type(
            code=status.HTTP_200_OK,
            message='Updated successfully',
            values= self.type(**existing_category.to_dict())
        )
        

    @strawberry.mutation
    def delete(self, input: DeleteCategoryInput, info: strawberry.Info) -> CategorySuccess:
        """
        Soft-delete a category by setting `deleted_at`.

        Args:
            input (DeleteCategoryInput): ID of the category to delete.
            info (strawberry.Info): GraphQL context containing user/session.

        Returns:
            CategorySuccess: Response indicating successful deletion.
        """
        return super().delete(input, info)

    def check_circular_reference(self, session, category_id: UUID, parent_id: UUID) -> bool:
        """
        Check if setting parent_id would create a circular reference in the category tree.
        
        Args:
            session: Database session
            category_id (UUID): ID of the category being updated
            parent_id (UUID): Proposed parent category ID
            
        Returns:
            bool: True if circular reference would be created, False otherwise
        """
        if not parent_id:
            return False
        
        # Start with the proposed parent
        current_id = parent_id
        
        # Traverse up the tree until we either:
        # 1. Find the category we're updating (circular reference)
        # 2. Reach a category with no parent (valid)
        while current_id:
            if current_id == category_id:
                return True
            
            parent = session.get(self.model, current_id)
            if not parent or not parent.parent_id:
                break
            
            current_id = parent.parent_id
        
        return False




    