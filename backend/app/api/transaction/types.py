import strawberry
from ..base.types import *
from datetime import datetime
from uuid import UUID
from typing import List
from typing import Optional
from ..category.types import CategoryTypeEnum,CategoryType
from ..goal.types import GoalType
from ..budget.types import BudgetType

@strawberry.type(description="Represents a single transaction made by a user.")
class TransactionType(BaseType):
    """
    GraphQL type representing a transaction.

    Attributes:
        amount (float): The amount of the transaction.
        description (str): A short description of the transaction.
        category_id (UUID): The unique identifier for the transaction's category.
        categoryName (Optional[str]): The name of the category (if available).
        date (datetime): The date and time the transaction occurred.
        categoryType (Optional[str]): The type of category, such as 'expense' or 'income' (if available).
        user_id (UUID): The unique identifier of the user who made the transaction.
    """
    amount:float
    description:str
    # category_id:UUID
    # categoryName:Optional[str] = None
    # categoryType:Optional[str] = None
    date:datetime 
    
    # type:TransactionTypeEnum
    user_id:UUID
    categories:Optional[List[CategoryType]] = None
    goals:Optional[List[GoalType]] = None
    budgets:Optional[List[BudgetType]] = None
    

    

@strawberry.type(description="A response object containing a list of transactions.")
class GetAllTransactionsResponse(BaseResponse):
    """
    GraphQL response type for a list of transactions.

    Attributes:
        transactions (List[TransactionType]): A list of TransactionType objects.
    """
    transactions: List[TransactionType]
    totalCount: int


       
    
@strawberry.type(description="Represents a successful response for a single transaction query.")
class TransactionSuccess(BaseSuccess[TransactionType]):
    """
    Response wrapper for a successful transaction-related GraphQL operation.

    Inherits:
        BaseSuccess[TransactionType]: Provides fields like 'data', 'code', and 'message'.
    """
    pass
    
    

class TransactionError(BaseError):
    """
    Represents an error during a transaction-related GraphQL operation.

    Inherits:
        BaseError: Contains fields such as 'code', 'message', and potentially additional error metadata.
    """
    pass