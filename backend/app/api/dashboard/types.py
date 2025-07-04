import strawberry
from ..base.types import *
from typing import List
from ...models.core import CategoryTypeEnum



@strawberry.type
class getSumByCategoryTypeSuccess(BaseSuccess[JSON]):
    pass

@strawberry.type
class RecentTransactionsType:
    id:UUID
    type:CategoryTypeEnum
    amount:float
    
@strawberry.type
class CashFlowType:
    month:datetime
    totalIncome:float
    totalExpense:float


   
@strawberry.type
class DashboardType:
    CategoryTypeSum:Optional[JSON] 
    RecentTransactions:List[RecentTransactionsType]
    Cashflow:List[CashFlowType]


@strawberry.type
class DashboardSuccess(BaseSuccess[DashboardType]):
    pass