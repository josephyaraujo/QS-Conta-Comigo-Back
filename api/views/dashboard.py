from rest_framework.response import Response
from typing import List
from api.permission import OnlyAssistenteSocial
from ..services.dashboardService import DashboardService
from ..models import *
from ..serializers import *
from rest_framework.views import APIView

class DashboardView(APIView):
    permission_classes: List[type] = [OnlyAssistenteSocial]
    
    def get(self, request, *args, **kwargs):
        data = DashboardService.get_indicadores()
        
        return Response(data)

