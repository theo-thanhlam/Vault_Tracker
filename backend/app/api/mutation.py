import strawberry
from .transaction.mutations import TransactionMutation
from .category.mutations import CategoryMutation
from .authentication.mutations import AuthMutation



# @strawberry.type
# class ProtectedMutation:
#     # category: CategoryMutation
    
#     @strawberry.field
#     def category(self) -> CategoryMutation:
#         return CategoryMutation()
    
#     @strawberry.field
#     def transaction(self) -> TransactionMutation:
#         return TransactionMutation()


@strawberry.type
class Mutation():
    
    @strawberry.field
    def category(self) -> CategoryMutation:
        return CategoryMutation()
    
    @strawberry.field
    def transaction(self) -> TransactionMutation:
        return TransactionMutation()

    
    
    @strawberry.field
    def auth(self) -> AuthMutation:
        return AuthMutation()
    
    
        
    