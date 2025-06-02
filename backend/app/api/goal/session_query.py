from ...models.core import *
from typing import List
from uuid import UUID


def get_all_goals_query(session, user_id: UUID) -> List[GoalModel]:
    """
    Get all goals for a user
    """
    return session.query(GoalModel).filter(GoalModel.user_id == user_id).filter(GoalModel.deleted_at == None).all()