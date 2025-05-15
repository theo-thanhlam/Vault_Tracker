import strawberry
from .types import *
from ...models.base import BaseModel
from typing import TypeVar,Generic,Type
from fastapi import status
from ...utils import db
from sqlalchemy import sql





# class BaseMutation(Generic[TModel, TSuccess, TType]):
#     model: Type[TModel]
#     success_type: Type[TSuccess]
#     type_class: Type[TType]
    
#     def _update_existing(self, input:TUpdateInput):
#         parsed_input = input.to_dict()
    
#         for k,v in parsed_input.items():
#             if v is not None:
#                 setattr(self.model, k, v)
#         self.model.updated_at = sql.func.now()
#         return self.model
    
#     def create(self, input:TCreateInput, info:strawberry.Info)->TSuccess:
#         session = db.get_session()
#         parsed_input = input.to_dict()
#         user = info.context.get("user")
#         new_instance = self.model(user_id=user.id, **parsed_input)
#         session.add(new_instance)
#         session.commit()

#         return self.success_type(
#             code=status.HTTP_201_CREATED,
#             message=f"Created {self.model.__name__} successfully",
#             category=self.type_class(**new_instance.to_dict())
#         )
        
    
#     def update(self, input:TUpdateInput, info:strawberry.Info)->TSuccess:
#         session =db.get_session()
#         user = info.context.get("user")
#         existing= session.get(TModel, input.id)
        
#         if user.id != existing.user_id:
#             raise TError(message="Unauthorized", code=status.HTTP_401_UNAUTHORIZED, detail="You are not the person who creates this category")
#         if not existing or existing.deleted_at:
#             raise TError(message="Not Found", code=status.HTTP_404_NOT_FOUND)
        
#         existing = self._update_existing(input=input)
#         session.commit()
        
#         success_data = {
#             "code":status.HTTP_200_OK,
#             "message":f"Updated {self.model.__name__} successfully",
#             "category":TType(**existing.to_dict())
#         }
#         print("UPDATE IN BASEMUTATION")
        
#         return TSuccess(**success_data)
    
#     def delete(self, input:TDeleteInput, info:strawberry.Info)->TSuccess:
#         pass


TModel = TypeVar("TModel", bound=BaseModel)
TCreateInput = TypeVar("TCreateInput", bound=BaseInput)
TUpdateInput = TypeVar("TUpdateInput", bound = BaseInput)
TDeleteInput = TypeVar("TDeleteInput", bound=BaseInput)
TSuccess = TypeVar("TSuccess", bound=BaseSuccess)
TType = TypeVar("TType", bound=BaseType)
TError = TypeVar("TError", bound=BaseError)


class BaseMutation(Generic[TCreateInput, TSuccess]):
    

    def _create(self, input:TCreateInput, info:strawberry.Info) -> TSuccess:
        print("CREATE IN BASE")
        return TSuccess