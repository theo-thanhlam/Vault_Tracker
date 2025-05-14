from .transaction.resolvers import TransactionQuery
from .category.resolvers import CategoryResolver
import strawberry



@strawberry.type
class ProtectedQuery( TransactionQuery, CategoryResolver):
    pass