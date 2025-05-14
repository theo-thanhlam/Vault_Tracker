import strawberry
import strawberry.exceptions
from ..baseType import BaseType, BaseError,BaseResponse
from datetime import datetime
from uuid import UUID
from typing import Optional, List
from fastapi import status

@strawberry.type
class TransactionType(BaseType):
    amount:float
    description:str
    category:str
    date:datetime 
    type:str
    user_id:UUID
    

@strawberry.type
class GetAllTransactionResponse(BaseResponse):
    transactions: List[TransactionType]


       
    
@strawberry.type
class TransactionOperationSuccess(BaseResponse):
    pass

class TransactionOperationError(BaseError):
   pass