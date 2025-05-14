
import strawberry
from ..baseType import BaseInput
from ...models.category import CategoryTypeEnum,CategoryModel
from uuid import UUID
from typing import Optional
from strawberry import Info
from .types import CategoryType
from ...utils import db

@strawberry.input
class CreateCategoryInput(BaseInput):
    name:str
    type:CategoryTypeEnum
    parent_id:Optional[UUID] = None


@strawberry.type(description="Handles category-related mutations")
class CategoryMutation:
    @strawberry.mutation
    def createCategory(self, input:CreateCategoryInput,info:Info) -> CategoryType:
        session =db.get_session()
        parsed_input = input.to_dict()
        user = info.context.get("user")
        new_category = CategoryModel(user_id = user.id, **parsed_input)
        try:
            session.add(new_category)
            session.commit()
            session.refresh(new_category)
        except Exception as e:
            raise e
        return CategoryType(**new_category.to_dict())
        
    