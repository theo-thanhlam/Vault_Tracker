import strawberry
from .transaction.mutations import TransactionMutation
from .category.mutations import CategoryMutation




@strawberry.type
class ProtectedMutation(TransactionMutation, CategoryMutation):
    pass