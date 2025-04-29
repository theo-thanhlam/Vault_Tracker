from .user import *
from .transaction import *

@strawberry.type
class Mutation(UserMutation, TransactionMutation):
    pass