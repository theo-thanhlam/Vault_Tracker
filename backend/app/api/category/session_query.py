from ...models.core.category import CategoryModel

def get_categories_by_type(session, user_id, type):
    return session.query(CategoryModel).filter(CategoryModel.user_id == user_id, CategoryModel.type == type, CategoryModel.deleted_at == None).all()