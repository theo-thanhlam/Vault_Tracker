from .auth import *
from .expense import *

@strawberry.type
class Mutation(AuthMutation, ExpenseMutation):
    pass