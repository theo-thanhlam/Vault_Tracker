from ...models.core import *
from typing import List
from uuid import UUID
from sqlalchemy import func
from .types import GoalType
from ...models.associative import TransactionGoalModel

def get_all_goals_query(session, user_id: UUID) -> List[GoalType]:
    """
    Get all goals for a user
    """
    # goals = session.query(GoalModel).filter(GoalModel.user_id == user_id).filter(GoalModel.deleted_at == None).all()
    query = session.query(
        GoalModel, 
        ((func.coalesce(func.sum(TransactionGoalModel.amount), 0.00) / GoalModel.target) * 100).label("progress"),
        (func.coalesce(func.sum(TransactionGoalModel.amount), 0.00)).label("current_amount")
        )\
        .outerjoin(
            TransactionGoalModel,
            TransactionGoalModel.goal_id == GoalModel.id
        )\
        .filter(GoalModel.user_id == user_id)\
        .filter(GoalModel.deleted_at == None)\
        .group_by(GoalModel.id)
    records = query.all()
    goals = [GoalType(**goal.to_dict(), progress=round(progress, 2), current_amount=round(current_amount, 2)) for goal, progress, current_amount in records]
    return goals