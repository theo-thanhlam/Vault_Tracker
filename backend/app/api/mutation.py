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


@strawberry.type(description="Root mutation object that provides access to all mutation groups.")
class Mutation():
    """
    Root GraphQL mutation class. Acts as the entry point for all top-level mutation groups
    such as categories, transactions, and authentication.
    """
    
    @strawberry.field(description="Access category-related mutations.")
    def category(self) -> CategoryMutation:
        """
        Returns:
            CategoryMutation: An object that exposes category-related mutation fields.
        """
        return CategoryMutation()
    
    @strawberry.field(description="Access transaction-related mutations.")
    def transaction(self) -> TransactionMutation:
        """
        Returns:
            TransactionMutation: An object that exposes transaction-related mutation fields.
        """
        return TransactionMutation()

    
    
    @strawberry.field(description="Access authentication-related mutations.")
    def auth(self) -> AuthMutation:
        """
        Returns:
            AuthMutation: An object that exposes authentication-related mutation fields.
        """
        return AuthMutation()
    
    
        
    