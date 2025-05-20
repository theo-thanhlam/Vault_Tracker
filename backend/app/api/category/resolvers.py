import strawberry
from uuid import UUID
import strawberry.resolvers
from strawberry.types import Info
from .types import *



@strawberry.type(description="Handles category-related mutations")
class CategoryQuery:
    @strawberry.field
    def getCategory(self) -> CategorySuccess:
        return CategorySuccess(code=200, message="Get Category successfully")
    