from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from api.permission import IsAlunoOrAssistenteSocial
from ..models import *
from ..serializers import *


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # customização de swagger descrição e campos
    @swagger_auto_schema(
        request_body=UsuarioSerializer,
        operation_summary="Criar usuário",
        operation_description="Cria um novo usuário no sistema"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

    @swagger_auto_schema(
        operation_summary="Listar alunos",
        operation_description="Retorna todos os alunos cadastrados"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AssistenteSocialViewSet(viewsets.ModelViewSet):
    queryset = AssistenteSocial.objects.all()
    serializer_class = AssistenteSocialSerializer

class PerfilAlunoViewSet(viewsets.ViewSet):
    """
    ViewSet para visualizar o perfil do aluno logado.
    Retorna apenas os dados do aluno autenticado (somente leitura).
    Os dados são sincronizados com a API externa (SUAP).
    """
    permission_classes = [IsAlunoOrAssistenteSocial]
    
    @swagger_auto_schema(
        operation_summary="Obter perfil do aluno logado",
        operation_description="Retorna o perfil completo do aluno autenticado"
    )
    def list(self, request):
        """
        Retorna o perfil do aluno logado.
        Endpoint: GET /api/perfil_aluno/
        """
        try:
            # Verifica se o usuário logado tem um perfil de aluno
            aluno = request.user.aluno
            serializer = AlunoPerfilSerializer(aluno)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Aluno.DoesNotExist:
            return Response(
                {'error': 'Usuário logado não é um aluno.'}, 
                status=status.HTTP_404_NOT_FOUND
            )