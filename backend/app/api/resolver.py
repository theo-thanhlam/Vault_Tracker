from .transaction.resolvers import TransactionQuery
from .category.resolvers import CategoryQuery
from .authentication.resolvers import AuthQuery
import strawberry



# @strawberry.type
# class ProtectedQuery( TransactionQuery, CategoryResolver):
#     pass

@strawberry.type
class Query:
    auth: AuthQuery
    transaction: TransactionQuery
    category: CategoryQuery
    
    