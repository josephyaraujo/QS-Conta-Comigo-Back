from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

from api.permission import OnlyAluno, OnlyAssistenteSocial
from api.serializers.auxilio_beneficio import AuxilioListSerializer, BeneficioAlunoSerializer
from ..models import *
from ..serializers import *
from django.contrib.auth import get_user_model
from ..constants import SolicitacaoEnum
from datetime import datetime
from rest_framework.permissions import IsAuthenticated, AllowAny
  

class SolicitacaoViewSet(viewsets.ModelViewSet):
    queryset = Solicitacao.objects.all()
    serializer_class = SolicitacaoSerializer
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'create':
            return SolicitacaoCreateSerializer
        return  super().get_serializer_class()

@swagger_auto_schema(security=[{'Bearer': []}])
class BeneficioViewSet(viewsets.ModelViewSet):
    queryset = Beneficio.objects.all()
    serializer_class = BeneficioSerializer
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'create':
            return BeneficioCreateSerializer
        if self.action == 'meus_beneficios':
            return BeneficioAlunoSerializer
        return  super().get_serializer_class()

    def get_permissions(self):
        ACTIONS_ASSISTENTE = ['list', 'retrieve', 'create', 'update', 
                            'partial_update', 'destroy', 
                            'details_programa', 'finaliza_beneficio']
        ACTIONS_ALUNO = ['meus_beneficios']

        if self.action in ACTIONS_ASSISTENTE:
            return [IsAuthenticated(), OnlyAssistenteSocial()]
        if self.action in ACTIONS_ALUNO:
            return [IsAuthenticated(), OnlyAluno()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['get'])
    def details_programa(self, request, pk = None): 
        """ endpoint que recebe o id e mostra os inscritos (tela de programa de programas) """
        envolvidos_programa = Beneficio.objects.filter(tipo_auxilio__id = pk) 
        if not envolvidos_programa.exists():
            return Response({'mensagem': 'Nenhum aluno encontrado nesse programa'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BeneficioSerializer(envolvidos_programa, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    @action(detail=True, methods=['patch'], url_path='finalizacao', url_name='finalizacao-solicitacao') 
    def finaliza_beneficio(self, request, pk = None): # finaliza o beneficio do aluno
        justificativa_finalizacao = request.data.get('motivo_finalizacao')
        solicitacao = Solicitacao.objects.filter(
            id = pk, 
            status__ordem__in = [SolicitacaoEnum.SOLICITACAO["DEFERIDO"], SolicitacaoEnum.SOLICITACAO["DEFERIDO_SEM_RECURSO"]]
        ).exists()

        beneficio = Beneficio.objects.filter(id=pk).first()

        if not solicitacao:
            return Response({"success":False,"mensagem": 'Beneficios só podem ser finalizados em status de deferimento. '}, status=status.HTTP_400_BAD_REQUEST)
        
        if not justificativa_finalizacao:
            return Response({"success":False,"mensagem": 'Para finalizar o benefício do aluno é necessário uma justificativa. '}, status=status.HTTP_400_BAD_REQUEST)
        
        if not beneficio:
            return Response({"success":False,"mensagem": 'Benefício não encontrado. '}, status=status.HTTP_404_NOT_FOUND)

        beneficio.justificativa_finalizacao = justificativa_finalizacao
        beneficio.solicitacao.status = StatusSolicitacao.objects.get(ordem=SolicitacaoEnum.SOLICITACAO["FINALIZADO"])
        beneficio.data_finalizacao = datetime.now()
        beneficio.status = False
        beneficio.save()

        return Response({"success":True,"mensagem": 'Beneficio finalizado com sucesso. '}, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['get'], url_path='meus-beneficios', url_name='meus-beneficios')
    def meus_beneficios(self, request): 
        """ lista os auxilios do aluno logado """
        usuario = request.user
        aluno = Aluno.objects.filter(usuario=usuario).first()
        
        if not aluno:
            return Response({'mensagem': 'Aluno não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        beneficios = Beneficio.objects.filter(aluno=aluno)
        serializer = BeneficioAlunoSerializer(beneficios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AuxilioViewSet(viewsets.ModelViewSet):
    queryset = Auxilio.objects.all()
    serializer_class = AuxilioSerializer
    pagination_class = None
    permission_classes = [AllowAny]


class AuxilioListView(ListAPIView):
    queryset = Auxilio.objects.all()
    serializer_class = AuxilioListSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    authentication_classes = []



