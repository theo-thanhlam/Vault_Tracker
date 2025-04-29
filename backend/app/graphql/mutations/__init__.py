from .user import *
from .expense import *

@strawberry.type
class Mutation(UserMutation, ExpenseMutation):
    pass