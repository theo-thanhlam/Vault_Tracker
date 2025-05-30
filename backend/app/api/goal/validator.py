from ..base.validator import Validator
from ..goal.types import GoalError
from fastapi import status
from ...models.core.goal import GoalModel
from ...models.core.user import UserModel
from ...utils import db
from sqlalchemy import sql

class GoalMutationValidator(Validator):
    def validate_create_input(self):
        category_ids = self.input.categories
        if not category_ids:
            raise GoalError(message="At least one category is required", code=status.HTTP_400_BAD_REQUEST)
        categories = self._get_categories(category_ids)
        if len(categories) != len(category_ids):
            raise GoalError(message="Some categories are not found", code=status.HTTP_404_NOT_FOUND)
        return categories

    def validate_update_input(self):
        goal_id = self.input.id
        if not goal_id:
            raise GoalError(message="Goal ID is required", code=status.HTTP_400_BAD_REQUEST)
        goal = self.session.query(GoalModel).filter(
            GoalModel.id == goal_id,
            GoalModel.user_id == self.user.id,
            GoalModel.deleted_at == None
        ).first()
        if not goal:
            raise GoalError(message="Goal not found", code=status.HTTP_404_NOT_FOUND)
        category_ids = self.input.categories if self.input.categories else [category.category_id for category in goal.categories]
        categories = self._get_categories(category_ids)
        if len(categories) != len(category_ids):
            raise GoalError(message="Some categories are not found", code=status.HTTP_404_NOT_FOUND)
        return goal, categories

    def validate_delete_input(self):
        goal_id = self.input.id
        if not goal_id:
            raise GoalError(message="Goal ID is required", code=status.HTTP_400_BAD_REQUEST)
        goal = self.session.query(GoalModel).filter(
            GoalModel.id == goal_id,
            GoalModel.user_id == self.user.id,
            GoalModel.deleted_at == None
        ).first()
        if not goal:
            raise GoalError(message="Goal not found", code=status.HTTP_404_NOT_FOUND)
        return goal