from rest_framework.response import Response
from rest_framework import mixins, status, viewsets, serializers
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from api.constants import ChamadoStatusEnum
from api.constants import ChamadoStatusEnum
from api.permission import OnlyAssistenteSocial
from api.serializers.base import AlunoChamadoSerializer
from api.utils import proxima_AS, enviar_notificacao
from ..models import Chamado, Aluno, AssistenteSocial, Chamado_chat, Documento, Notificacao, Usuario
from rest_framework.permissions import IsAuthenticated
from ..serializers.chamados import ChamadoChatCreateSerializer, ChamadoChatDetailSerializer, ChamadoDetalheSerializer, ChamadoEncerrarSerializer, ChamadoSerializer 
from rest_framework.decorators import action
from api.permission import IsAlunoOrAssistenteSocial, OnlyAssistenteSocial, OnlyAluno
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

class ChamadoViewSet(viewsets.ModelViewSet):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_permissions(self):
        ACTIONS_ASSISTENTE = [
            'concluir_chamado'
        ]
        ACTIONS_ALUNO_OU_ASSISTENTE = ['create', 'update', 'partial_update', 'perform_create', 'fechar_chamado']
        if self.action in ACTIONS_ASSISTENTE:
            return [IsAuthenticated(), OnlyAssistenteSocial()]

        if self.action in ACTIONS_ALUNO_OU_ASSISTENTE:
            return [IsAuthenticated(), IsAlunoOrAssistenteSocial()]

        return [IsAuthenticated()]
    
    def get_queryset(self):
        usuario = Usuario.objects.get(id=self.request.user.id)
        if usuario.tipo == 'aluno':
            return Chamado.objects.filter(aluno__usuario=self.request.user)
        elif usuario.tipo == 'assistente_social':
            return Chamado.objects.filter(assistente_social__usuario=usuario)
        return Chamado.objects.filter(assistente_social__usuario=usuario)

    def get_authenticate_header(self, request):
        return super().get_authenticate_header(request)

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'fechar_chamado':            
            return ChamadoEncerrarSerializer
        if self.action == 'concluir_chamado':
            pass
        if self.action in ['retrieve', 'get', 'list']:
            return ChamadoDetalheSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        usuario_logado = self.request.user
        try:
            perfil_aluno = Aluno.objects.get(usuario=usuario_logado)
        except Aluno.DoesNotExist:
            raise serializers.ValidationError({"aluno": "Usuário logado não é um aluno."})
        
        assistentes = AssistenteSocial.objects.order_by('id')
        if not assistentes.exists():
            raise serializers.ValidationError({"assistente_social": "Não há assistentes disponíveis."})

        ultimo_chamado = Chamado.objects.order_by('-id').first()
        proximo_assistente = None

        if not ultimo_chamado or not ultimo_chamado.assistente_social:
            proximo_assistente = assistentes.first()
        else:
            proximo_assistente = proxima_AS(ultimo_chamado, assistentes)
        chamado = serializer.save(aluno=perfil_aluno, assistente_social=proximo_assistente)
        
        mensagem = serializer.validated_data.get('descricao', '')
        usuario = Usuario.objects.get(id=usuario_logado.id)
        chamado_chat = Chamado_chat.objects.create(
                chamado = chamado,
                usuario = usuario,
                mensagem = mensagem,
                data_envio = timezone.now(),
            )

        try:
            nova_notificacao = Notificacao.objects.create(
                titulo="Novo Chamado Atribuído",
                mensagem=f"O aluno {perfil_aluno.usuario.first_name} abriu um chamado de {chamado.tipo_de_chamado}.",
                status="nao_lida" 
            )
            
            nova_notificacao.usuario.add(proximo_assistente.usuario)

        except Exception as e:
            print(f"Erro ao criar notificação: {e}")
            
        arquivos = self.request.FILES.getlist('arquivos') 
        
        descricoes = self.request.POST.getlist('descricoes_arquivos')

        if arquivos:
            for i, arquivo in enumerate(arquivos):
                descricao_doc = descricoes[i] if i < len(descricoes) else f"Anexo do chamado {chamado.id}"
                
                novo_doc = Documento.objects.create(
                    aluno=perfil_aluno,
                    arquivo=arquivo,
                    tipo_documento="anexo_chamado", 
                    descricao=descricao_doc 
                )
                
                chamado.documentos.add(novo_doc)



    @action(detail=True, methods=['put'], url_path='concluir_chamado', url_name='conclusao-chamado') 
    def concluir_chamado(self, request, pk = None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            chamado = Chamado.objects.get(id=serializer.validated_data.get('chamado', None).id)
            usuario = Usuario.objects.get(id = request.user.id)

            if chamado.aluno.usuario != usuario and chamado.assistente_social.usuario != usuario:
                return Response({"success":False,"mensagem": 'Você não tem permissão para responder a este chamado.'}, status=status.HTTP_403_FORBIDDEN)

            if chamado.status in [ChamadoStatusEnum.CHAMADO["FECHADO"], ChamadoStatusEnum.CHAMADO["CONCLUIDO"]]:
                return Response({"success":False,"mensagem": 'Não é possível concluir um chamado que já foi concluído ou fechado.'}, status=status.HTTP_400_BAD_REQUEST)
            chamado.status = ChamadoStatusEnum.CHAMADO["CONCLUIDO"]
            chamado.save()
            enviar_notificacao(
                mensagem = f"O chamado de {chamado.tipo_de_chamado} foi concluído por {usuario.groups.name} {usuario.first_name}.",
                usuario = chamado.aluno.usuario,
                titulo = "Chamado Concluído"
            )
            return Response({"success":True,"mensagem": 'Chamado concluído com sucesso.'}, status=status.HTTP_200_OK)
        except Chamado.DoesNotExist:
            return Response({"success":False,"mensagem": 'Ocorreu um erro inesperado! Tente novamente.'}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=True, methods=['put', 'patch'], url_path='fechar_chamado', url_name='fechamento-chamado')
    def fechar_chamado(self, request, pk = None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            chamado = Chamado.objects.get(id=pk)
            usuario = Usuario.objects.get(id = request.user.id)
            justificativa = serializer.validated_data.get('justificativa', '')

            if chamado.aluno.usuario != usuario and chamado.assistente_social.usuario != usuario:
                return Response({"success":False,"mensagem": 'Você não tem permissão para responder a este chamado.'}, status=status.HTTP_403_FORBIDDEN)

            if chamado.status in [ChamadoStatusEnum.CHAMADO["FECHADO"], ChamadoStatusEnum.CHAMADO["CONCLUIDO"]]:
                return Response({"success":False,"mensagem": 'Não é possível concluir um chamado que já foi concluído ou fechado.'}, status=status.HTTP_400_BAD_REQUEST)

            if not justificativa:
                return Response({"success":False,"mensagem": 'A justificativa é obrigatória para fechar o chamado.'}, status=status.HTTP_400_BAD_REQUEST)

            chamado.status = ChamadoStatusEnum.CHAMADO["FECHADO"]
            chamado.justificativa_chamado = justificativa
            
            enviar_notificacao(
                mensagem = f"O chamado de {chamado.tipo_de_chamado} foi fechado por {usuario.groups.name} {usuario.first_name}.",
                usuario = chamado.aluno.usuario,
                titulo = "Chamado Fechado",
                tipo = 'chamado'
            )
            chamado.save()
            return Response({"success":True,"mensagem": 'Chamado fechado com sucesso.'}, status=status.HTTP_200_OK)
        except Chamado.DoesNotExist:
            return Response({"success":False,"mensagem": 'Ocorreu um erro inesperado! Tente novamente.'}, status=status.HTTP_404_NOT_FOUND)
        pass


class ChamadoDetailViewSet(mixins.RetrieveModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = ChamadoChatDetailSerializer
    queryset = Chamado_chat.objects.all()

    def get_permissions(self):
        ACTIONS_ALUNO_OU_ASSISTENTE = ['create', 'update', 'partial_update', 'responder']

        if self.action in ACTIONS_ALUNO_OU_ASSISTENTE:
            return [IsAuthenticated(), IsAlunoOrAssistenteSocial()]

        return [IsAuthenticated()]

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'responder':
            return ChamadoChatCreateSerializer
        return super().get_serializer_class()

    def retrieve(self, request, pk=None):
        mensagens = Chamado_chat.objects.filter(chamado_id=pk)
        serializer = self.get_serializer(mensagens, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='responder', url_name='reposta-chamado') 
    def responder(self, request, pk = None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            mensagem = serializer.validated_data.get('mensagem', None)
            chamado = Chamado.objects.get(id=serializer.validated_data.get('chamado', None).id)
            arquivos = self.request.FILES.getlist('arquivos') 
            descricoes = self.request.POST.getlist('descricoes_arquivos')
            usuario = Usuario.objects.get(id = request.user.id)


            if chamado.aluno.usuario != usuario and chamado.assistente_social.usuario != usuario:
                return Response({"success":False,"mensagem": 'Você não tem permissão para responder a este chamado.'}, status=status.HTTP_403_FORBIDDEN)

            if chamado.status in [ChamadoStatusEnum.CHAMADO["FECHADO"], ChamadoStatusEnum.CHAMADO["CONCLUIDO"]]:
                return Response({"success":False,"mensagem": 'Não é possível responder a um chamado que já foi concluído ou fechado.'}, status=status.HTTP_400_BAD_REQUEST)
            
            
            chamado_chat = Chamado_chat.objects.create(
                chamado = chamado,
                usuario = usuario,
                mensagem = mensagem,
                data_envio = timezone.now(),
            )
            
            if arquivos:
                if hasattr(request.user, 'aluno'):
                    doc_kwargs = {'aluno': Aluno.objects.get(usuario=usuario.id)}
                else:
                    doc_kwargs = {'assistente_social': AssistenteSocial.objects.get(usuario=usuario.id)}
                for i, arquivo in enumerate(arquivos):
                    descricao_doc = descricoes[i] if i < len(descricoes) else f"Anexo do chamado {chamado.id}"
                    novo_doc = Documento.objects.create(
                        arquivo=arquivo,
                        tipo_documento="anexo_chamado",
                        descricao=descricao_doc,
                        **doc_kwargs
                    )
                    chamado_chat.arquivo = novo_doc
            chamado_chat.save()
            enviar_notificacao(
                titulo="Nova resposta no chamado",
                mensagem=f"O(a) {usuario.groups.name} {usuario.first_name} respondeu o chamado de {chamado.tipo_de_chamado}. id:{chamado.id}",
                usuario = usuario,
                tipo = 'chamado'
            )
            return Response({"success":True,"mensagem": 'Mensagem enviada com sucesso. '}, status=status.HTTP_200_OK)
        except Chamado.DoesNotExist:
            return Response({"success":False,"mensagem": 'Ocorreu um erro inesperado! Tente novamente.'}, status=status.HTTP_404_NOT_FOUND)