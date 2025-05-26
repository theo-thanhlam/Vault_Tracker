import strawberry
from uuid import UUID
import strawberry.resolvers
from strawberry.types import Info
from .types import *
from ...utils import db
from ...utils.handler import DatabaseHandler
from ..base.types import BaseInput


@strawberry.type(description="Handle dashboard data")
class DashboardQuery():
    
    @strawberry.field
    def getOverview(self, info:Info) -> GetOverview:
        return GetOverview(total=1)
        