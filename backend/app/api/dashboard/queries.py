import strawberry
from uuid import UUID
import strawberry.resolvers
from strawberry.types import Info
from .types import *
from ...utils import db
from ...utils.handler import DatabaseHandler
from ..base.types import BaseInput
from .session_query import *


@strawberry.type(description="Handle dashboard data")
class DashboardQuery():
    
    @strawberry.field
    def getSumByCategoryType(self, info:Info) -> DashboardSuccess:
        """
        Returns the total amounts grouped by category type (e.g., total income or expense).

        Args:
            info (Info): GraphQL context containing user.
            input (TypeInput): Input object specifying the category `type`.

        Returns:
            DashboardSuccess: Success object with a dict showing total sums.

        
        Example response:
        ```
        {
            "data": {
                "getSumByCategoryType": {
                    "code": 200,
                    "message": "Here is sum by category's type",
                    "values": {
                        CategoryTypeSum{
                            "INCOME": 3000.0,
                            "EXPENSE": 1500.0
                        }
                    }
                }
            }
        }

        ```
        """
        session = db.get_session()
        user = info.context.get("user")
        query = DashboardSessionQuery(session, user.id)
        
        
        type_sum = query.get_sum_by_category()
        type_sum_dict = {k:v for k,v in type_sum}
        type_sum_dict['expense'] = -type_sum_dict['expense']
        
        recent_transactions = query.get_recent_transactions()
        cashflows = query.get_cashflow()
        cashflow_list = [CashFlowType(month=row.month, totalIncome=row.totalIncome, totalExpense=row.totalExpense) for row in cashflows]
        DashboardValues = DashboardType(CategoryTypeSum=type_sum_dict, RecentTransactions=recent_transactions, Cashflow=cashflow_list)
        
        
        return DashboardSuccess(values=DashboardValues, message="Dashboard Values", code=200)
        
        