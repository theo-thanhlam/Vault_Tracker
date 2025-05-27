import strawberry
from uuid import UUID
import strawberry.resolvers
from strawberry.types import Info
from .types import *
from ...utils import db
from ...utils.handler import DatabaseHandler
from ..base.types import BaseInput


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
            getSumByCategoryTypeSuccess: Success object with a dict showing total sums.

        
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
        
        
        type_sum = DatabaseHandler.get_total_by_category_type(session=session, user_id=user.id)
        type_sum_dict = {k:v for k,v in type_sum}
        
        DashboardValues = DashboardType(CategoryTypeSum=type_sum_dict)
        
        
        return DashboardSuccess(values=DashboardValues, message="Dashboard Values", code=200)
        
        