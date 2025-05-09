from .authentication.resolvers import AuthQuery
from .expense.resolvers import ExpenseQuery
import strawberry



@strawberry.type
class ProtectedQuery( ExpenseQuery):
    pass