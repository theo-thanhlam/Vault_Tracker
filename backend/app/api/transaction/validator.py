from ..base.types import BaseInput
from ...models.core import UserModel, CategoryModel, GoalModel, BudgetModel
from fastapi import status
from ..transaction.types import TransactionError, CategoryType, GoalType, BudgetType
from typing import List, Optional, Tuple
from ..base.validator import Validator


class TransactionMutationValidator(Validator):
    
    sum_of_allocations = 0
    
    def _validate_category_allocations(self) -> Optional[List[CategoryType]]:
        if not self.input.category_allocations or len(self.input.category_allocations) == 0:
           return None
        category_allocations = []
        for category_allocation in self.input.category_allocations:
            existing_category = self.session.query(CategoryModel).filter_by(id=category_allocation.category_id, user_id=self.user.id).first()
            if not existing_category:
                raise TransactionError(message="Category not found", code=status.HTTP_404_NOT_FOUND)
            category_allocations.append(CategoryType(**existing_category.to_dict()))
            self.sum_of_allocations += category_allocation.amount
        return category_allocations
        
        
   
    def _validate_goal_allocations(self) -> Optional[List[GoalType]]:
      
        if not self.input.goal_allocations or len(self.input.goal_allocations) == 0:
            return None
        
        goal_allocations = []
        for goal_allocation in self.input.goal_allocations:
            existing_goal = self.session.query(GoalModel).filter_by(id=goal_allocation.goal_id, user_id=self.user.id).first()
            if not existing_goal:
                raise TransactionError(message="Goal not found", code=status.HTTP_404_NOT_FOUND)
            goal_allocations.append(GoalType(**existing_goal.to_dict()))
            self.sum_of_allocations += goal_allocation.amount
        return goal_allocations


    def _validate_budget_allocations(self) -> Optional[List[BudgetType]]:
      
        if not self.input.budget_allocations or len(self.input.budget_allocations) == 0:
            return None
        
        budget_allocations = []
        for budget_allocation in self.input.budget_allocations:
            existing_budget = self.session.query(BudgetModel).filter_by(id=budget_allocation.budget_id, user_id=self.user.id).first()
            if not existing_budget:
                raise TransactionError(message="Budget not found", code=status.HTTP_404_NOT_FOUND)
            budget_allocations.append(BudgetType(**existing_budget.to_dict()))
            self.sum_of_allocations += budget_allocation.amount
        return budget_allocations   

    def validate_create_input(self) :
        category_allocations = self._validate_category_allocations()
        if not category_allocations:
            raise TransactionError(message= "At least one category is required", code=status.HTTP_400_BAD_REQUEST)
        goal_allocations = self._validate_goal_allocations()
        budget_allocations = self._validate_budget_allocations()
        if self.sum_of_allocations != self.input.amount:
            raise TransactionError(message="The sum of allocations must be equal to the transaction amount", code=status.HTTP_400_BAD_REQUEST)
        return category_allocations, goal_allocations, budget_allocations
    
    def validate_update_input(self):
        category_allocations = self._validate_category_allocations()
        goal_allocations = self._validate_goal_allocations()
        budget_allocations = self._validate_budget_allocations()
        if self.sum_of_allocations != self.input.amount:
            raise TransactionError(message="The sum of allocations must be equal to the transaction amount", code=status.HTTP_400_BAD_REQUEST)
        return category_allocations, goal_allocations, budget_allocations
        

class TransactionQueryValidator(Validator):
    pass