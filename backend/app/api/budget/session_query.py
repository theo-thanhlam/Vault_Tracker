from ...models import *
from typing import List
from uuid import UUID
from .types import BudgetType
from ..category.types import CategoryType
from ..category.queries import build_tree
from sqlalchemy import func

def get_all_budgets_query(session,user_id:UUID) -> List[BudgetType]:
    """
    Get all budgets for a user
    """
    budgets_query = session.query(BudgetModel, func.coalesce(func.sum(TransactionModel.amount),0).label('current_amount'))\
        .join(CategoryBudgetModel, CategoryBudgetModel.budget_id == BudgetModel.id)\
        .join(CategoryModel, CategoryModel.id == CategoryBudgetModel.category_id)\
        .join(TransactionModel, CategoryModel.id == TransactionModel.category_id, isouter=True)\
        .filter(BudgetModel.user_id == user_id)\
        .filter(BudgetModel.deleted_at == None)\
        .group_by(BudgetModel.id)
    
    
    budgets_records = budgets_query.all()
    budgets = []
    for record, current_amount in budgets_records:
        budget_dict = record.to_dict()
        budget_dict['current_amount'] = current_amount
        categories = []
        for category_assoc in record.budget_category_association:
            if category_assoc.category_budget_association:
                category_dict = category_assoc.category_budget_association.to_dict()
                categories.append(CategoryType(**category_dict))
        budget_dict["categories"] = categories
        budgets.append(BudgetType(**budget_dict))
    
    return budgets