import strawberry
from .types import *
from ...models.base import BaseModel
from typing import TypeVar,Generic,Type
from fastapi import status
from ...utils import db
from sqlalchemy import sql
from ...utils.handler import login_required



# Type variables for generic class
TModel = TypeVar("TModel", bound=BaseModel)           # ORM model type
TCreateInput = TypeVar("TCreateInput", bound=BaseInput)  # Input schema for creating instances
TUpdateInput = TypeVar("TUpdateInput", bound=BaseInput)  # Input schema for updating instances
TDeleteInput = TypeVar("TDeleteInput", bound=BaseInput)  # Input schema for deleting instances
TSuccess = TypeVar("TSuccess", bound=BaseSuccess)        # Response success type
TType = TypeVar("TType", bound=BaseType)                 # Output type used for response values




class BaseAuthenticatedMutation(Generic[TModel, TCreateInput, TUpdateInput, TDeleteInput, TSuccess, TType]):
    """
    A generic base class for implementing authenticated GraphQL mutations.
    
    This class provides reusable `create` and `update` methods for any model-based GraphQL operation.
    It ensures authentication and basic ownership checks.
    
    Type Parameters:
    - TModel: The SQLAlchemy model class.
    - TCreateInput: Input class used for creation.
    - TUpdateInput: Input class used for update (must include an ID).
    - TDeleteInput: Input class used for deletion (not used in this snippet).
    - TSuccess: Type used to represent a successful response.
    - TType: GraphQL output type used for wrapping the returned model.
    """
    model: Type[TModel]
    success_type: Type[TSuccess]
    
    type: Type[TType]
    
    def __update_instance(self, instance:TModel,input:TUpdateInput) ->TModel:
        """
        Internal method to update model instance fields using the provided input.

        Only non-None fields from the input are updated. Also updates the `updated_at` timestamp.

        Args:
            instance (TModel): The existing model instance to be updated.
            input (TUpdateInput): The validated input containing new values.

        Returns:
            TModel: The updated model instance.
        """
        parsed_input = input.to_dict()
    
        for k,v in parsed_input.items():
            if v is not None:
                setattr(instance, k, v)
        instance.updated_at = sql.func.now()
        return instance
    
    @login_required
    def create(self,  input: TCreateInput,info:strawberry.Info) -> TSuccess:
        """
        Create a new instance of the model with the given input.

        Args:
            input (TCreateInput): Input data for the new instance.
            info (strawberry.Info): GraphQL resolver info containing context (e.g., user).

        Returns:
            TSuccess: A success response wrapping the created instance.
        """
        session = db.get_session()
        parsed_input = input.to_dict()
        user = info.context.get("user")
        new_instance = self.model(user_id=user.id, **parsed_input)
        session.add(new_instance)
        session.commit()
        return self.success_type(
            code=status.HTTP_201_CREATED,
            message=f"Created successfully",
            values= self.type(**new_instance.to_dict())
        )
    
    @login_required
    def update(self, input:TUpdateInput, info:strawberry.Info) -> TSuccess:
        """
        Update an existing instance of the model based on the input ID.

        This method checks for existence, ownership, and soft deletion before performing the update.

        Args:
            input (TUpdateInput): Input data containing the ID and new values.
            info (strawberry.Info): GraphQL resolver info containing context (e.g., user).

        Returns:
            TSuccess: A success response wrapping the updated instance.
        """
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
            values= self.type(**instance.to_dict())
        )
    
    @login_required
    def delete(self, input:TUpdateInput, info:strawberry.Info) -> TSuccess:
        """
        Soft-delete an existing instance of the model by setting `deleted_at` timestamp.

        This method performs the following checks:
        - Verifies that the instance exists and is not already deleted.
        - Ensures the authenticated user is the owner of the instance.
        
        Args:
            input (TUpdateInput): Input containing the ID of the instance to delete.
            info (strawberry.Info): GraphQL resolver info containing context (e.g., user).

        Returns:
            TSuccess: A success response indicating the resource was deleted.
        """
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