import strawberry
from .types import *
from ...models.base import BaseModel
from typing import TypeVar,Generic,Type
from fastapi import status
from ...utils import db
from sqlalchemy import sql
from ...utils.handler import login_required



TModel = TypeVar("TModel", bound=BaseModel)
TCreateInput = TypeVar("TCreateInput", bound=BaseInput)
TUpdateInput = TypeVar("TUpdateInput", bound = BaseInput)
TDeleteInput = TypeVar("TDeleteInput", bound=BaseInput)
TSuccess = TypeVar("TSuccess", bound=BaseSuccess)
TType = TypeVar("TType", bound=BaseType)




class BaseAuthenticatedMutation(Generic[TModel, TCreateInput, TUpdateInput, TDeleteInput, TSuccess, TType]):
    model: Type[TModel]
    success_type: Type[TSuccess]
    
    type: Type[TType]
    
    def __update_instance(self, instance:TModel,input:TUpdateInput) ->TModel:
        parsed_input = input.to_dict()
    
        for k,v in parsed_input.items():
            if v is not None:
                setattr(instance, k, v)
        instance.updated_at = sql.func.now()
        return instance
    
    @login_required
    def create(self,  input: TCreateInput,info:strawberry.Info) -> TSuccess:
        session = db.get_session()
        parsed_input = input.to_dict()
        user = info.context.get("user")
        new_instance = self.model(user_id=user.id, **parsed_input)
        session.add(new_instance)
        session.commit()
        return self.success_type(
            code=status.HTTP_201_CREATED,
            message=f"Created successfully",
            result= self.type(**new_instance.to_dict())
        )
    
    @login_required
    def update(self, input:TUpdateInput, info:strawberry.Info) -> TSuccess:
        session = db.get_session()
        user = info.context.get("user")
        instance = session.get(self.model, input.id)
        
        if not instance or instance.deleted_at:
            raise BaseError(message="Not Found", code=status.HTTP_404_NOT_FOUND)
        if user.id != instance.user_id:
            raise BaseError(message = "Unauthorized", code=status.HTTP_401_UNAUTHORIZED)
        instance = self.__update_instance(instance, input)
        session.commit()
        
        return self.success_type(
            code=status.HTTP_200_OK,
            message='Updated successfully',
            result= self.type(**instance.to_dict())
        )
    
    @login_required
    def delete(self, input:TUpdateInput, info:strawberry.Info) -> TSuccess:
        session = db.get_session()
        user = info.context.get("user")
        instance = session.get(self.model, input.id)
        
        if not instance or instance.deleted_at:
            
            raise BaseError(message="Not Found", code=status.HTTP_404_NOT_FOUND)
        if user.id != instance.user_id:
            raise BaseError(message = "Unauthorized", code=status.HTTP_401_UNAUTHORIZED)
        
        instance.deleted_at = sql.func.now()
        session.commit()
        return self.success_type(
            message="Deleted successfully",
            code = status.HTTP_204_NO_CONTENT,
        
        )