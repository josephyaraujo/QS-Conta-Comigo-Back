from rest_framework.response import Response
from api.permission import IsAlunoOrAssistenteSocial
from api.serializers.perguntas import PerguntaRespostaSerializer
from ..models import *
from ..serializers import *
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated 
from api.permission import OnlyAluno, OnlyAssistenteSocial
class PerguntaViewSet(viewsets.ModelViewSet):
    queryset = Pergunta.objects.all()
    serializer_class = PerguntaSerializer
    permission_classes = [IsAlunoOrAssistenteSocial]

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'put' or self.action == 'patch':
            return PerguntaRespostaSerializer
        
        return self.serializer_class
    
    def get_permissions(self):
        ACTIONS_ASSISTENTE = ['update', 'partial_update', 'responder_pergunta','list']
        ACTIONS_ALUNO = ['create', 'minhas_perguntas_proprio', 'minhas_perguntas']
        if self.action in ACTIONS_ASSISTENTE:
            return [IsAuthenticated(), OnlyAssistenteSocial()]
        if self.action in ACTIONS_ALUNO:
            return [IsAuthenticated(), OnlyAluno()]
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        # Obter o aluno associado ao usuário autenticado
        try:
            aluno = request.user.aluno
        except AttributeError:
            return Response(
                {'error': 'Usuário deve ser um aluno para criar perguntas'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Criar o serializer com os dados da requisição
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            pergunta = serializer.validated_data.get('enunciado')
            if not pergunta.strip():
                return Response(
                    {'error': 'Pergunta não pode ser vazia.'},
                    status=status.HTTP_400_BAD_REQUEST)
            # Salvar a pergunta associando ao aluno automaticamente
            pergunta = serializer.save(aluno=aluno, status='nao_respondida')
            
            # Retornar a resposta com os dados da pergunta criada
            response_serializer = self.get_serializer(pergunta)
            return Response(
                response_serializer.data, 
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True  # Força atualização parcial mesmo em PUT
        
        # Obter a instância atual da pergunta
        instance = self.get_object()
        
        # Obter o serializer com os novos dados
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            # Verificar se uma resposta está sendo fornecida
            resposta = serializer.validated_data.get('resposta')
            pergunta = Pergunta.objects.get(pk=instance.pk)  
            if pergunta.status == 'respondida' and resposta:
                return Response(
                    {'error': 'Pergunta já foi respondida. Não é possível alterar a resposta.'},
                    status=status.HTTP_400_BAD_REQUEST)
            if not resposta.strip():
                return Response(
                    {'error': 'Resposta não pode ser vazia.'},
                    status=status.HTTP_400_BAD_REQUEST)
            # Se há uma resposta e ela não está vazia, marcar como respondida
            if resposta and resposta.strip():
                from datetime import date
                serializer.validated_data['status'] = 'respondida'
                serializer.validated_data['data_resposta'] = date.today()
                
                # Se o usuário é um assistente social, associar à pergunta
                if hasattr(request.user, 'assistentesocial'):
                    serializer.validated_data['assistente_social'] = request.user.assistentesocial
            
            # Salvar as alterações
            pergunta_atualizada = serializer.save()
            
            # Retornar resposta com dados atualizados
            response_serializer = self.get_serializer(pergunta_atualizada)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(
        detail=False,
        methods=['get'],
        url_path='minhas-perguntas',
    )
    def minhas_perguntas_proprio(self, request):
        """
        Retorna as perguntas do aluno autenticado
        URL: /api/perguntas/minhas-perguntas/
        Filtros: ?respondida=true|false
        """
        try:
            aluno = request.user.aluno
        except AttributeError:
            return Response(
                {'error': 'Usuário deve ser um aluno'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Começar com todas as perguntas do aluno
        perguntas = Pergunta.objects.filter(aluno=aluno)        
        if not perguntas:
            return Response(
                {'message': 'Nenhuma pergunta encontrada para este aluno'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Aplicar filtro de status se fornecido
        respondida_param = request.query_params.get('respondida')
        if respondida_param is not None:
            if respondida_param.lower() == 'true':
                perguntas = perguntas.filter(status='respondida')
            elif respondida_param.lower() == 'false':
                perguntas = perguntas.filter(status='nao_respondida')
        
        # Ordenar por ID decrescente (mais recentes primeiro)
        perguntas = perguntas.order_by('-id')
        
        serializer = self.get_serializer(perguntas, many=True)
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(
        detail=True,
        methods=['get'],
        url_path='minhas-perguntas',
    )
    def minhas_perguntas(self, request, pk=None):
        """
        Retorna as perguntas de um aluno específico (apenas para staff)
        URL: /api/perguntas/{id}/minhas-perguntas/
        Filtros: ?respondida=true|false
        """
        # Verificar se o usuário tem permissão (staff ou superuser)
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {'error': 'Permissão negada. Apenas staff pode acessar perguntas de outros alunos'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Validar se pk é um número válido
        try:
            pk = int(pk)
        except (ValueError, TypeError):
            return Response(
                {'error': 'ID do aluno deve ser um número válido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Buscar o aluno com validação
        aluno = get_object_or_404(Aluno, pk=pk)

        # Começar com todas as perguntas do aluno
        perguntas = Pergunta.objects.filter(aluno=aluno)
        if not perguntas:
            return Response(
                {'message': 'Nenhuma pergunta encontrada para este aluno'},
                status=status.HTTP_200_OK
            )
        
        # Aplicar filtro de status se fornecido
        respondida_param = request.query_params.get('respondida')
        if respondida_param is not None:
            if respondida_param.lower() == 'true':
                perguntas = perguntas.filter(status='respondida')
            elif respondida_param.lower() == 'false':
                perguntas = perguntas.filter(status='nao_respondida')
        
        # Ordenar por ID decrescente (mais recentes primeiro)
        perguntas = perguntas.order_by('-id')
        
        serializer = self.get_serializer(perguntas, many=True)
        
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(
        detail=True,
        methods=['patch'],
        url_path='responder',
    )
    def responder_pergunta(self, request, pk=None):
        """
        Permite que assistente social responda uma pergunta específica
        URL: /api/perguntas/{id}/responder/
        """
        # Verificar se o usuário é um assistente social
        if not hasattr(request.user, 'assistentesocial'):
            return Response(
                {'error': 'Apenas assistentes sociais podem responder perguntas'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Validar se pk é um número válido
        try:
            pk = int(pk)
        except (ValueError, TypeError):
            return Response(
                {'error': 'ID da pergunta deve ser um número válido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Buscar a pergunta
        pergunta = get_object_or_404(Pergunta, pk=pk)
        
        # Verificar se a resposta foi fornecida
        resposta = request.data.get('resposta')
        if not resposta or not resposta.strip():
            return Response(
                {'error': 'Resposta é obrigatória'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Atualizar a pergunta
        from datetime import date
        pergunta.resposta = resposta.strip()
        pergunta.status = 'respondida'
        pergunta.data_resposta = date.today()
        pergunta.assistente_social = request.user.assistentesocial
        pergunta.save()
        
        # Retornar dados atualizados
        serializer = self.get_serializer(pergunta)
        return Response(
            {
                'message': 'Pergunta respondida com sucesso',
                'pergunta': serializer.data
            },
            status=status.HTTP_200_OK
        )