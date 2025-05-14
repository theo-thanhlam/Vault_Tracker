import strawberry
from uuid import UUID
from strawberry.types import Info
from .types import *



@strawberry.type(description="Handles category-related mutations")
class CategoryResolver:
    pass