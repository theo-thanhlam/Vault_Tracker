
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
        return super().update(input, info)

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




    