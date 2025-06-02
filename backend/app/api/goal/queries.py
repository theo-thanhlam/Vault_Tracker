import strawberry
from strawberry.types import Info
from .types import *
from ...utils import db
from ...utils.handler import DatabaseHandler
from ..base.types import BaseInput
from .types import GetGoalSuccess
from .session_query import get_all_goals_query

@strawberry.type(description="Handles goal-related queries")
class GoalQuery:
    """
    Root-level GraphQL query class for interacting with goal data.
    """
    @strawberry.field
    def getAllGoals(self, info: Info) -> GetGoalSuccess:
        """
        Fetches all goals belonging to the authenticated user.
        """
        session = db.get_session()
        user = info.context.get("user")
        goals = get_all_goals_query(session, user.id)
        success_data = {
            "message": "Goals fetched successfully",
            "code": 200,
            "values": goals
        }
        
        return GetGoalSuccess(**success_data)
        