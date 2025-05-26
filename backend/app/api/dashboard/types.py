import strawberry
from ..base.types import *





@strawberry.type(description="Return overview dashboard data")
class GetOverview:
    total: int