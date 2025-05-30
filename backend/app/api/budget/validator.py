from ..base.validator import Validator
from ..budget.types import BudgetError
from fastapi import status
from ...models.core.category import CategoryModel
from ...models.core.budget import BudgetModel
from typing import List
from uuid import UUID
from ...models.associative import CategoryBudgetModel

class BudgetMutationValidator(Validator):
    
    # def __get_categories(self, category_ids:List[UUID]) -> List[CategoryModel]:
    #     query = self.session.query(CategoryModel.id, CategoryModel.name, CategoryModel.created_at, CategoryModel.updated_at, CategoryModel.deleted_at)\
    #     .filter(CategoryModel.user_id == self.user.id)\
    #     .filter(CategoryModel.id.in_(category_ids))\
    #     .filter(CategoryModel.deleted_at == None)
    #     results = query.all()
    #     return results
    
    def validate_create_input(self):
        category_ids = self.input.categories
        if not category_ids:
            raise BudgetError(message="At least one category is required", code=status.HTTP_400_BAD_REQUEST)
        categories = self._get_categories(category_ids)
        if len(categories) != len(category_ids):
            raise BudgetError(message="Some categories are not found", code=status.HTTP_404_NOT_FOUND)
        return categories
        
    def validate_update_input(self):
        budget_id = self.input.id
        if not budget_id:
            raise BudgetError(message="Budget ID is required", code=status.HTTP_400_BAD_REQUEST)

        # Get the budget
        budget = self.session.query(BudgetModel).filter(
            BudgetModel.id == budget_id,
            BudgetModel.user_id == self.user.id,
            BudgetModel.deleted_at == None
        ).first()

        if not budget:
            raise BudgetError(message="Budget not found", code=status.HTTP_404_NOT_FOUND)
        
        exisiting_budget_categories = self.session.query(CategoryBudgetModel).filter(
            CategoryBudgetModel.budget_id == budget_id
        ).all()
        if not exisiting_budget_categories:
            raise BudgetError(message="Budget categories not found", code=status.HTTP_404_NOT_FOUND)
        category_ids = self.input.categories if self.input.categories else [category.category_id for category in exisiting_budget_categories]
        categories = self._get_categories(category_ids)
        if len(categories) != len(category_ids):
            raise BudgetError(message="Some categories are not found", code=status.HTTP_404_NOT_FOUND)

        return budget, categories
    
    def validate_delete_input(self):
        budget_id = self.input.id
        if not budget_id:
            raise BudgetError(message="Budget ID is required", code=status.HTTP_400_BAD_REQUEST)
        budget = self.session.query(BudgetModel).filter(
            BudgetModel.id == budget_id,
            BudgetModel.user_id == self.user.id,
            BudgetModel.deleted_at == None
        ).first()
        if not budget:
            raise BudgetError(message="Budget not found", code=status.HTTP_404_NOT_FOUND)
        return budget
        