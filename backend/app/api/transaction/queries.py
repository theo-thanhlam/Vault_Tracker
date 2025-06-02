import strawberry
from uuid import UUID
from .types import *
from ...utils import db
from ...models.core import UserModel
from ...utils.handler import DatabaseHandler
from fastapi import HTTPException,status
from strawberry import Info
from ...models.core import TransactionModel, CategoryModel
from ...models.associative import TransactionCategoryModel
from collections import defaultdict

@strawberry.input(description="Input object for retrieving a single transaction")
class GetTransactionInput:
    """
    Input object for retrieving a single transaction.

    Attributes:
        transaction_id (UUID): The unique identifier of the transaction.
    """
    transaction_id:UUID = strawberry.field(description="The unique identifier of the transaction.")
    
@strawberry.input(description="Input object for retrieving all transactions associated with the current user")
class GetAllTransactionsInput(BaseInput):
    """
    Input object for retrieving all transactions associated with the current user.

    Attributes:
        limit (Optional[int]): The maximum number of transactions to retrieve. Defaults to 10.
    """
    limit: Optional[int] = strawberry.field(default=10, description="The maximum number of transactions to retrieve. Defaults to 10.")
    offset: Optional[int] = strawberry.field(default=0, description="The maximum number of transactions to retrieve. Defaults to 10.")
    

@strawberry.type
class TransactionQuery:
    """
    GraphQL Query class for handling transaction-related queries.
    """
    @strawberry.field(description="Retrieve a list of transactions associated with the authenticated user.")
    def getTransactions(self, info: Info, input: GetAllTransactionsInput) -> GetAllTransactionsResponse:
        """
        Get all transactions for the authenticated user.

        Args:
            info (Info): GraphQL resolver info, containing context including the authenticated user.
            input (GetAllTransactionsInput): Input parameters including the limit on number of results.

        Returns:
            GetAllTransactionsResponse: A response object containing the list of transactions,
                                        a success message, and a status code.
        """
        user = info.context.get("user")
        session = db.get_session()
        user_transactions = []
        # user_transactions = DatabaseHandler.get_all_transactions_by_user_id(session=session, user_id=user.id, limit=input.limit, offset=input.offset)
        query = (
            session.query(
                TransactionModel,
                CategoryModel
            )
            .join(TransactionCategoryModel, TransactionModel.id == TransactionCategoryModel.transaction_id)
            .join(CategoryModel, TransactionCategoryModel.category_id == CategoryModel.id)
            .filter(
                TransactionModel.user_id == user.id,
                TransactionModel.deleted_at.is_(None),
                # TransactionCategoryModel.deleted_at.is_(None),
                CategoryModel.deleted_at.is_(None)
            )
        )
        rows = query.all()
        # Step 2: Group categories per transaction
        
        transactions_map = {}
        categories_group = defaultdict(list)

        for txn, cat in rows:
            if txn.id not in transactions_map:
                transactions_map[txn.id] = txn
            categories_group[txn.id].append({
                "id": str(cat.id),
                "name": cat.name,
                # Add more fields if needed
            })
            # Step 3: Format output
        result = []
        for txn_id, txn in transactions_map.items():
            txn_dict = {
                "id": str(txn.id),
                "amount": txn.amount,
                "description": txn.description,
                "date": txn.date.isoformat(),
                # Add more fields as needed from TransactionModel
                "categories": categories_group[txn_id],
            }
            result.append(txn_dict)

        # Step 4: Include total count of unique transactions
        output = {
            "data": result,
            "total": len(result)
        }
        print(output)
        
        # total_count = DatabaseHandler.get_total_transactions_count(session=session, user_id=user.id)
        return GetAllTransactionsResponse(transactions=output['data'], message=f"Here are all {user.firstName} {user.lastName}'s transactions", code=status.HTTP_200_OK,totalCount=output['total'])
    
    
    @strawberry.field(description="Retrieve details of a specific transaction by its ID.")
    def getTransaction(self, input: GetTransactionInput, info: Info) -> TransactionType:
        """
        Get a specific transaction by its ID.

        Args:
            input (GetTransactionInput): Input object containing the transaction ID.
            info (Info): GraphQL resolver info.

        Returns:
            TransactionType: The transaction object corresponding to the provided ID.
        """
        session = db.get_session()
        user_transactions = DatabaseHandler.get_transaction_by_id(session=session, id=input.transaction_id)
        return TransactionType(user_transactions)
        