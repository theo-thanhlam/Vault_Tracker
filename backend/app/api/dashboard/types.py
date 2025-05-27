import strawberry
from ..base.types import *




@strawberry.type
class getSumByCategoryTypeSuccess(BaseSuccess[JSON]):
    pass
   
   
@strawberry.type
class DashboardType:
    CategoryTypeSum:Optional[JSON] = strawberry.field(default=None, description="Total expenses groupby category type")


@strawberry.type
class DashboardSuccess(BaseSuccess[DashboardType]):
    pass