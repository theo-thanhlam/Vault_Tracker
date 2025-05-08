import strawberry
from .authentication.mutations import AuthMutation
from .expense.mutations import ExpenseMutation

@strawberry.type
class Mutation(AuthMutation, ExpenseMutation):
    pass