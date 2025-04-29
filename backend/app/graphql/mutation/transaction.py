import strawberry
from uuid import UUID
from ..types import UserType
from ...utils import db
from ...models import UserModel
from fastapi import HTTPException

@strawberry.type
class TransactionMutation:
    pass