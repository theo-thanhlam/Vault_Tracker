
import strawberry
from ..base.types import BaseInput
from ...models import *
from uuid import UUID
from typing import Optional
from strawberry import Info
from .types import *
from ...utils import db
from sqlalchemy import sql
from ..base.mutations import BaseMutation
from ...utils.handler import *
from fastapi import status
from uuid import UUID


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

def update_existing_category(existing_category:CategoryModel,input:UpdateCategoryInput)->CategoryModel:
    parsed_input = input.to_dict()
    
    for k,v in parsed_input.items():
        if v is not None:
            setattr(existing_category, k, v)
    existing_category.updated_at = sql.func.now()
    return existing_category

@strawberry.type(description="Handles category-related mutations")
class CategoryMutation:
    
    @strawberry.mutation
    def create(self, input:CreateCategoryInput,info:Info) -> CategorySuccess:
        session =db.get_session()
        parsed_input = input.to_dict()
        user = info.context.get("user")
        new_category = CategoryModel(user_id = user.id, **parsed_input)
        DatabaseHandler.create_category(session=session, category_doc=new_category)
        success_data = {
            "code":status.HTTP_201_CREATED,
            "message":"Created new category successfully",
            "category":CategoryType(**new_category.to_dict())
        }
        return CategorySuccess(**success_data)
    
    @strawberry.mutation
    def update(self, input:UpdateCategoryInput, info:Info) -> CategorySuccess:
        session =db.get_session()
        parsed_input = input.to_dict()
        user = info.context.get("user")
        existing_category = session.get(CategoryModel, input.id)
        
        if user.id != existing_category.user_id:
            raise CategoryError(message="Unauthorized", code=status.HTTP_401_UNAUTHORIZED, detail="You are not the person who creates this category")
        if not existing_category or existing_category.deleted_at:
            raise CategoryError(message="Not Found", code=status.HTTP_404_NOT_FOUND)
        
        existing_category =update_existing_category(input=input, existing_category=existing_category)
        session.commit()
        
        success_data = {
            "code":status.HTTP_200_OK,
            "message":"Updated category successfully",
            "category":CategoryType(**existing_category.to_dict())
        }
        
        return CategorySuccess(**success_data)
    
    @strawberry.mutation
    def delete(self,input:DeleteCategoryInput, info:Info)->CategorySuccess:
        session = db.get_session()
        user:UserModel = info.context.get("user")
        existing_category = session.get(CategoryModel, input.id)
        
        if user.id != existing_category.user_id:
            raise CategoryError(message="Unauthorized", code=status.HTTP_401_UNAUTHORIZED, detail="You are not the person who creates this category")
        if not existing_category or existing_category.deleted_at:
            raise CategoryError(message="Not Found", code=status.HTTP_404_NOT_FOUND)
        
        existing_category.deleted_at = sql.func.now()
        session.commit()
        return CategorySuccess(message="Deleted transaction successfully", code=status.HTTP_204_NO_CONTENT)



    