from __future__ import annotations 

import strawberry
from ..base.types import BaseSuccess,BaseType, BaseError, BaseResponse
from ...models.core import CategoryTypeEnum
from uuid import UUID
from typing import List, Optional, Dict
from strawberry.scalars import JSON

@strawberry.type
class CategoryType(BaseType):
    """
    GraphQL output type representing a single category.

    Inherits:
        BaseType: Includes standard fields (id, created_at, updated_at, deleted_at).

    Fields:
        name (str): Name of the category.
        type (CategoryTypeEnum): Enum indicating the type of category (e.g., income, expense).
        description (str): A detailed description of the category.
        user_id (UUID): ID of the user who owns the category.
        children (List): sub category 
    """
    name: str
    type: CategoryTypeEnum
    description: str
    user_id: UUID
    parent_id:Optional[UUID] = None
    children: Optional[List["CategoryType"]] = None

    
    
@strawberry.type
class CategorySuccess(BaseSuccess[CategoryType]):
    """
    Success response for single-category mutations (create, update, delete).

    Inherits:
        BaseSuccess[CategoryType]: Standardized success format for a single CategoryType object.
    """
    pass

    
@strawberry.type
class GetCategorySuccess(BaseSuccess[CategoryType]):
    """
    Success response for fetching multiple categories.

    Inherits:
        BaseSuccess[CategoryType]: Uses CategoryType as the generic.

    Fields:
        values (List[CategoryType]): A list of categories.
    """
    values: List[CategoryType]

    
    
    
class CategoryError(BaseError):
    """
    Error response specifically related to category operations.

    Inherits:
        BaseError: Standard error format with message, code, and optional detail.
    """
    pass


@strawberry.type
class CategoryTypeSum:
    """
    Type representing an aggregated sum grouped by category type.

    Fields:
        type (str): Category type as a string.
        total (float): Total value (e.g., total expenses or income) for this type.
    """
    type: str
    total: float



    