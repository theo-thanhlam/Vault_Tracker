from .base import BaseType, strawberry

@strawberry.type
class TransactionType(BaseType):
    amount:float