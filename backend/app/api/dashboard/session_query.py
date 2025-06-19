from sqlalchemy import func, case
from sqlalchemy.orm import Session
from uuid import UUID
from ...models.core import *

class DashboardSessionQuery:
        def __init__(self, session:Session, user_id:UUID):
                self.session = session
                self.user_id = user_id
                
        def get_sum_by_category(self):
                query = self.session.query(CategoryModel.type, func.sum(TransactionModel.amount).label("total"))\
                .join(CategoryModel, CategoryModel.id == TransactionModel.category_id)\
                .filter(TransactionModel.user_id == self.user_id)\
                .filter(TransactionModel.deleted_at == None)\
                .filter(CategoryModel.deleted_at == None)\
                .group_by(CategoryModel.type)
                result = query.all()
                
                return result
        
        def get_recent_transactions(self):
                query = self.session.query(TransactionModel.id,CategoryModel.type,TransactionModel.amount)\
                        .join(CategoryModel, CategoryModel.id == TransactionModel.category_id, isouter=True)\
                        .filter(TransactionModel.user_id == self.user_id)\
                        .filter(CategoryModel.user_id == self.user_id)\
                        .filter(TransactionModel.deleted_at==None)\
                        .filter(CategoryModel.deleted_at ==None)\
                        .limit(5)
                transactions = query.all()
                return transactions
        
        def get_cashflow(self):
                query = self.session.query(func.date_trunc('month', TransactionModel.date).label('month'), 
                                           func.sum( case((CategoryModel.type=='income', TransactionModel.amount),else_=0)).label("totalIncome"),
                                        func.sum( case((CategoryModel.type=='expense', TransactionModel.amount),else_=0)).label("totalExpense")
                                        )\
                        .join(CategoryModel, TransactionModel.category_id==CategoryModel.id)\
                        .filter(
                                TransactionModel.user_id==self.user_id,
                                TransactionModel.deleted_at==None
                        )\
                        .group_by(func.date_trunc('month', TransactionModel.date))
                cashflows = query.all()
                return cashflows
                





