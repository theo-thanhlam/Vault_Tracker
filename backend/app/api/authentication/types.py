
from ..transaction.types import TransactionType
from ..base.types import *

from typing import List
import strawberry
from ...models.core import UserRoleEnum
from typing import Optional
from strawberry.scalars import JSON


@strawberry.type
class UserType(BaseType):
    """
    GraphQL type representing a user in the system.

    Inherits:
        BaseType: Includes standard metadata fields (id, created_at, updated_at, deleted_at).

    Fields:
        firstName (Optional[str]): User's first name.
        lastName (Optional[str]): User's last name.
        email (str): User's email address.
        role (UserRoleEnum): User's assigned role in the system.
        email_verified (bool): Whether the user's email has been verified.
        auth_provider_id (Optional[str]): ID from the external authentication provider (if applicable).
    """
    firstName:Optional[str] = None 
    lastName:Optional[str] = None
    email:str
    role:UserRoleEnum
    email_verified:bool
    auth_provider_id:Optional[str] = None 
    

@strawberry.type
class AuthSucess(BaseSuccess[JSON]):
    """
    Response type returned upon successful authentication.

    Inherits:
        BaseSuccess[JSON]: Generic success structure with additional token support.

    Fields:
        token (Optional[str]): Authentication token (e.g., JWT) used for future API access.
    """
    token: Optional[str] = strawberry.field(description="Authentication token", default=None)
    pass
    


class AuthError(BaseError):
    """
    Specific error type for authentication-related failures.

    Inherits:
        BaseError: Standardized error format including message, code, and detail.
    """
    pass

@strawberry.type
class GetUserSuccess(BaseSuccess[UserType]):
    """
    Success response for a "get user" operation.

    Inherits:
        BaseSuccess[UserType]: Standard success structure with `UserType` as the returned value.
    """
    pass
    

