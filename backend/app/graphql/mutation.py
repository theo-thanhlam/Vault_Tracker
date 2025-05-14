import strawberry
from .authentication.mutations import AuthMutation
from .transaction.mutations import TransactionMutation




@strawberry.type
class ProtectedMutation(TransactionMutation):
    pass