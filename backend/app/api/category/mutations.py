
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
    name:str
    type:CategoryTypeEnum
    description:str
    parent_id:Optional[UUID] = None


@strawberry.input
class UpdateCategoryInput(BaseInput):
    id:UUID
    name:Optional[str] = None
    type:Optional[CategoryTypeEnum]= None
    description:Optional[str] = None
    parent_id:Optional[UUID] = None
    
@strawberry.input
class DeleteCategoryInput(BaseInput):
    id:UUID


@strawberry.type
class CategoryMutation(BaseAuthenticatedMutation[CategoryModel, CreateCategoryInput, UpdateCategoryInput, DeleteCategoryInput, CategorySuccess, CategoryType]):
    model = CategoryModel
    success_type = CategorySuccess
    type = CategoryType
    
    
    @strawberry.mutation
    def create(self, input:CreateCategoryInput, info:strawberry.Info) -> CategorySuccess:
        return super().create(input, info)
    
    @strawberry.mutation
    def update(self, input:UpdateCategoryInput, info:strawberry.Info) -> CategorySuccess:
        return super().update(input, info)
    
    @strawberry.mutation
    def delete(self, input:DeleteCategoryInput, info:strawberry.Info) -> CategorySuccess:
        
        return super().delete(input, info)



    