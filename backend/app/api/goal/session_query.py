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
    query = session.query(GoalModel)\
        .outerjoin(CategoryGoalModel, CategoryGoalModel.goal_id == GoalModel.id)\
        .outerjoin(CategoryModel, CategoryModel.id == CategoryGoalModel.category_id)\
        .filter(GoalModel.user_id == user_id)\
        .filter(GoalModel.deleted_at == None)
    records = query.all()
    goals = []
    for goal in records:
        goal_dict = goal.to_dict()
        # Get categories for this goal through the association
        categories = []
        for category_assoc in goal.goal_category_association:
            if category_assoc.category_goal_association:
                category_dict = category_assoc.category_goal_association.to_dict()
                categories.append(CategoryType(**category_dict))
        # Build tree structure for categories
        goal_dict["categories"] = build_tree(categories)
        goals.append(GoalType(**goal_dict))
    
    return goals


