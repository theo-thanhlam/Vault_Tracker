from .authentication.resolvers import AuthQuery
from .transaction.resolvers import TransactionQuery
import strawberry



@strawberry.type
class ProtectedQuery( TransactionQuery):
    pass