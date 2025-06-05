from ...models.core import *
from typing import List
from uuid import UUID
from sqlalchemy import func
from .types import GoalType
from ...models.associative import CategoryGoalModel
from ..category.types import CategoryType
from ..category.queries import build_tree

def get_all_goals_query(session, user_id: UUID) -> List[GoalType]:
    """
    Get all goals for a user with their associated categories in tree view
    """
    goals_query = session.query(GoalModel, func.coalesce(func.sum(TransactionModel.amount),0).label('current_amount'))\
        .join(CategoryGoalModel, CategoryGoalModel.goal_id == GoalModel.id)\
        .join(CategoryModel, CategoryModel.id == CategoryGoalModel.category_id)\
        .join(TransactionModel, CategoryModel.id == TransactionModel.category_id, isouter=True)\
        .filter(GoalModel.user_id == user_id)\
        .filter(GoalModel.deleted_at == None)\
        .group_by(GoalModel.id)
    
    
    goals_records = goals_query.all()
    goals = []
    for record, current_amount in goals_records:
        goal_dict = record.to_dict()
        goal_dict['current_amount'] = current_amount
        categories = []
        for category_assoc in record.goal_category_association:
            if category_assoc.category_goal_association:
                category_dict = category_assoc.category_goal_association.to_dict()
                categories.append(CategoryType(**category_dict))
        goal_dict["categories"] = build_tree(categories)
        goals.append(GoalType(**goal_dict))
    
    return goals


