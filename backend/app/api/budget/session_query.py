from ...models import *
from typing import List
from uuid import UUID
from .types import BudgetType
from ..category.types import CategoryType
from ..category.queries import build_tree


def get_all_budgets_query(session,user_id:UUID) -> List[BudgetType]:
    """
    Get all budgets for a user
    """
    pass