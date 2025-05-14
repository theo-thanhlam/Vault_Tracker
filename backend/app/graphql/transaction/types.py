import strawberry
from ..baseType import *
from datetime import datetime
from uuid import UUID
from typing import List
from ...models import TransactionTypeEnum 


@strawberry.type
class TransactionType(BaseType):
    amount:float
    description:str
    category_id:UUID
    date:datetime 
    type:TransactionTypeEnum
    user_id:UUID
    

@strawberry.type
class GetAllTransactionResponse(BaseResponse):
    transactions: List[TransactionType]


       
    
@strawberry.type
class TransactionOperationSuccess(BaseResponse):
    pass

class TransactionOperationError(BaseError):
   pass