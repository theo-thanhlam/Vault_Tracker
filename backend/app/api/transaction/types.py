import strawberry
from ..base.types import *
from datetime import datetime
from uuid import UUID
from typing import List
from typing import Optional


@strawberry.type
class TransactionType(BaseType):
    amount:float
    description:str
    category_id:UUID
    date:datetime 
    # type:TransactionTypeEnum
    user_id:UUID
    

@strawberry.type
class GetAllTransactionResponse(BaseResponse):
    transactions: List[TransactionType]


       
    
@strawberry.type
class TransactionSuccess(BaseSuccess[TransactionType]):
    # result:Optional[TransactionType]=None
    pass
    
    

class TransactionError(BaseError):
   pass