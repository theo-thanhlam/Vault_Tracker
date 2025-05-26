from .transaction.queries import TransactionQuery
from .category.queries import CategoryQuery
from .authentication.queries import AuthQuery
from .dashboard.queries import DashboardQuery
import strawberry



# @strawberry.type
# class ProtectedQuery( TransactionQuery, CategoryResolver):
#     pass

@strawberry.type(description="Root query object that provides access to all main query groups.")
class Query:
    """
    Root GraphQL query class. Acts as the entry point for all top-level query groups
    such as categories, transactions, authentication, and dashboards.
    """
    
    @strawberry.field(description="Access category-related queries.")
    def category(self) -> CategoryQuery:
        """
        Returns:
            CategoryQuery: An object that exposes category-related query fields.
        """
        return CategoryQuery()
    
    @strawberry.field(description="Access transaction-related queries.")
    def transaction(self) -> TransactionQuery:
        """
        Returns:
            TransactionQuery: An object that exposes transaction-related query fields.
        """
        return TransactionQuery()
    
    @strawberry.field(description="Access authentication-related queries.")
    def auth(self) -> AuthQuery:
        """
        Returns:
            AuthQuery: An object that exposes authentication-related query fields.
        """
        return AuthQuery()
    
    @strawberry.field(description="Access dashboard-related queries.")
    def dashboard(self) -> DashboardQuery:
        """
        Returns:
            DashboardQuery: An object that exposes dashboard analytics and statistics queries.
        """
        return DashboardQuery()
    
    