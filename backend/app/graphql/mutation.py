import strawberry
from .transaction.mutations import TransactionMutation
from .category.mutations import CategoryMutation




@strawberry.type
class ProtectedMutation:
    # category: CategoryMutation
    
    @strawberry.field
    def category(self) -> CategoryMutation:
        return CategoryMutation()
    
    @strawberry.field
    def transaction(self) -> TransactionMutation:
        return TransactionMutation()
    