from api.permission import IsAlunoOrAssistenteSocial, OnlyAluno, OnlyAssistenteSocial

from ..models import Cursos
from ..serializers.base import CursoSerializer
from rest_framework import viewsets, status


class CursosViewSet(viewsets.ModelViewSet):
    queryset = Cursos.objects.all()
    serializer_class = CursoSerializer
    pagination_class = None
    permission_classes = [IsAlunoOrAssistenteSocial]
    

