from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters as drf_filters
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend

from api.permission import IsAlunoOrAssistenteSocial, OnlyAssistenteSocial, OnlyAluno
from ..models import *
from ..serializers import *
from ..filters import FormularioFilter
from rest_framework.permissions import IsAuthenticated

class FormularioViewSet(viewsets.ModelViewSet):
    queryset = Formulario.objects.all().order_by('-data_inicio')
    serializer_class = FormularioSerializer
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = FormularioFilter
    search_fields = ['titulo', 'objetivo', 'auxilio_alvo__descricao']
    ordering_fields = ['data_inicio', 'data_fim', 'alunos_solicitados']

    def get_permissions(self):
        ACTIONS_ASSISTENTE = [
            'create', 'update', 'partial_update', 'destroy',
            'envio', 'estatisticas'
        ]
        ACTIONS_ALUNO_OU_ASSISTENTE = ['list', 'retrieve']

        if self.action in ACTIONS_ASSISTENTE:
            return [IsAuthenticated(), OnlyAssistenteSocial()]

        if self.action in ACTIONS_ALUNO_OU_ASSISTENTE:
            return [IsAuthenticated(), IsAlunoOrAssistenteSocial()]

        return [IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def envio(self, request, pk=None):
        formulario = self.get_object()
        
        # Valida se pode ser enviado
        if formulario.status == 'concluido':
            return Response(
                {'mensagem': 'Formulários concluídos não podem ser enviados.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.utils import timezone
        hoje = timezone.now().date()
        
        if formulario.data_fim < hoje:
            return Response(
                {'mensagem': 'Não é possível enviar um formulário com data de término no passado.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        modo = formulario.solicitados
        alunos_query = Aluno.objects.all()

        if modo == 'todos':
            # Todos os alunos cadastrados
            pass

        elif modo == 'auxilio':
            if not formulario.auxilio_alvo:
                return Response({'mensagem': 'O modo Auxílio exige a seleção de um auxílio alvo.'}, status=status.HTTP_400_BAD_REQUEST)

            auxilio = formulario.auxilio_alvo

            # Filtra alunos relacionados ao auxílio (se houver relação por solicitacao/beneficio)
            # Aqui usamos a tabela Beneficio/Solicitacao para encontrar alunos com o auxílio
            alunos_por_beneficio = Aluno.objects.filter(beneficio__tipo_auxilio=auxilio).distinct()
            alunos_query = alunos_por_beneficio

        #pensar melhor essa parte depois  
        elif modo == 'individual':
            if not formulario.alunos_selecionados.exists():
                return Response({'mensagem': 'O modo Individual exige a seleção de pelo menos um aluno.'}, status=status.HTTP_400_BAD_REQUEST)

            # Filtra pelos alunos selecionados na relação M2M
            alunos_query = formulario.alunos_selecionados.all()
        
        else:
            return Response({'mensagem': 'Modo de envio inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        
        alunos_finais = list(alunos_query)
        
        if not alunos_finais:
            return Response({'mensagem': 'Nenhum aluno encontrado para os critérios de envio.'}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic(): #se todas as operações dentro desse bloco forem bem-sucedidas, as mudanças serão salvas no banco de dados. 
            #Se ocorrer algum erro, todas as mudanças serão revertidas.

            formulario.alunos_solicitados = len(alunos_finais)
            # Se estava em rascunho, muda para aberto ao enviar
            if formulario.status == 'rascunho':
                formulario.status = 'aberto'
            formulario.save(update_fields=['alunos_solicitados', 'status'])
            
            # Criar instâncias de RespostaFormulario para cada aluno
            respostas_formulario = []
            for aluno in alunos_finais:
                # Verificar se já existe uma resposta para evitar duplicatas
                resposta_existente = RespostaFormulario.objects.filter(
                    formulario=formulario,
                    aluno=aluno
                ).exists()
                
                if not resposta_existente:
                    resposta_formulario = RespostaFormulario(
                        formulario=formulario,
                        aluno=aluno,
                        completo=False  # marca como não completo inicialmente
                    )
                    respostas_formulario.append(resposta_formulario)
            
            # Criar todas as respostas de uma vez para otimizar
            if respostas_formulario:
                RespostaFormulario.objects.bulk_create(respostas_formulario)
            
            titulo_notificacao = f"Novo Formulário: {formulario.titulo}"
            mensagem_notificacao = f"Acesse e responda o formulário {formulario.titulo} antes de {formulario.data_fim.strftime('%d/%m/%Y')}."

            nova_notificacao = Notificacao.objects.create(
                titulo=titulo_notificacao,
                mensagem=mensagem_notificacao,
                status='nao_lida',
                tipo = 'formulario'
            )
            
            usuarios_alvo = Usuario.objects.filter(aluno__in=alunos_finais)
            nova_notificacao.usuario.set(usuarios_alvo)

        return Response(
            {
            'status': 'sucesso',
            'mensagem': f'Formulário "{formulario.titulo}" enviado para {len(alunos_finais)} alunos.',
            'alunos_notificados_count': len(alunos_finais),
            'respostas_criadas_count': len(respostas_formulario),
            'alunos_notificados_count': len(alunos_finais),
            'status_formulario': formulario.status
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        estatisticas = {
            'total_formularios': Formulario.objects.count(),
            'formularios_rascunho': Formulario.objects.filter(status='rascunho').count(),
            'formularios_abertos': Formulario.objects.filter(status='aberto').count(),
            'formularios_concluidos': Formulario.objects.filter(status='concluido').count(),
        }
        return Response(estatisticas, status=status.HTTP_200_OK)
    
class FormularioQuestaoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAlunoOrAssistenteSocial]  
    queryset = FormularioQuestao.objects.all()
    serializer_class = FormularioQuestaoSerializer

class FormularioQuestaoOpcaoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAlunoOrAssistenteSocial]  
    queryset = FormularioQuestaoOpcao.objects.all()
    serializer_class = FormularioQuestaoOpcaoSerializer

class RespostaFormularioViewSet(viewsets.ModelViewSet):
    queryset = RespostaFormulario.objects.all()
    serializer_class = RespostaFormularioCreateSerializer
    permission_classes = [IsAlunoOrAssistenteSocial]  

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'formulario',
        'aluno',
        'completo'
    ]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RespostaFormularioReadOnlySerializer
        return RespostaFormularioCreateSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Injeta o aluno no contexto para o serializer
        if self.request.user.is_authenticated and hasattr(self.request.user, 'aluno'):
            context['aluno'] = self.request.user.aluno
        return context


class RespostaQuestaoViewSet(viewsets.ModelViewSet):
    queryset = RespostaQuestao.objects.all()
    serializer_class = RespostaQuestaoCreateSerializer
