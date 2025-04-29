from .user import *
from .transaction import *

@strawberry.type
class Query(UserQuery, TransactionQuery):
    pass