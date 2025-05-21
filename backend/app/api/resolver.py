from .transaction.resolvers import TransactionQuery
from .category.resolvers import CategoryQuery
from .authentication.resolvers import AuthQuery
import strawberry



# @strawberry.type
# class ProtectedQuery( TransactionQuery, CategoryResolver):
#     pass

@strawberry.type
class Query:
    @strawberry.field
    def category(self) -> CategoryQuery:
        return CategoryQuery()
    
    @strawberry.field
    def transaction(self) -> TransactionQuery:
        return TransactionQuery()

    
    
    @strawberry.field
    def auth(self) -> AuthQuery:
        return AuthQuery()
    
    