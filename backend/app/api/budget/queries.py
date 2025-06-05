import strawberry
from strawberry.types import Info
from .types import *
from ...utils import db

from .types import GetBudgetSuccess
from .session_query import get_all_budgets_query
from fastapi import status


@strawberry.type(description="Budget query type")
class BudgetQuery:
    
    @strawberry.field(description="Get all budgets")
    def getAllBudgets(self,info:Info) -> GetBudgetSuccess:
        session = db.get_session()
        user = info.context.get("user")
        budgets = get_all_budgets_query(session,user.id)
        return GetBudgetSuccess(message="Budgets fetched successfully",values=budgets,code=status.HTTP_200_OK)
    