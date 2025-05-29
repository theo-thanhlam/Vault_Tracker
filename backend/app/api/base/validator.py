from ..base.types import BaseInput
from ...models.core.user import UserModel
from typing import List
from uuid import UUID
from ...models.core.category import CategoryModel

class Validator:
    def __init__(self, session, input:BaseInput, user:UserModel):
        self.session = session
        self.input = input
        self.user = user
        
    def _get_categories(self, category_ids:List[UUID]) -> List[CategoryModel]:
        query = self.session.query(CategoryModel.id, CategoryModel.name, CategoryModel.created_at, CategoryModel.updated_at, CategoryModel.deleted_at)\
        .filter(CategoryModel.user_id == self.user.id)\
        .filter(CategoryModel.id.in_(category_ids))\
        .filter(CategoryModel.deleted_at == None)
        results = query.all()
        return results