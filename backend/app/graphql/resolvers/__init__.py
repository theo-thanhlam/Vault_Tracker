from .auth import *
from .expense import *

@strawberry.type
class Query(UserQuery, ExpenseQuery):
    pass