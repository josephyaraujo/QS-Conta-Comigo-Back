from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from ..models import *
from ..serializers.base import UsuarioAuthSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from rest_framework.permissions import AllowAny
from datetime import datetime
from ..SuapServices.suap_service import PopulateUsuario
from ..SuapServices.serializer import SuapCodeSerializer
Usuario = get_user_model()

class LoginSuap(APIView):
    authentication_classes = [] # impede o jwt, verifica quem é o usuario, nesse caso fica anonimo msm
    permission_classes = (AllowAny,)  # endpoin public pq é de login, verifica se o usuario pode acessar
    """ 
    Retorna a URL de autenticação do SUAP para o frontend redirecionar o usuário.
    """
    def get(self, request):
        # URL de autorização do SUAP (vai ser onde o usuário faz login)
        authorization_url = (
            "https://suap.ifrn.edu.br/o/authorize/?"
            f"response_type=code"
            f"&client_id={settings.SOCIAL_AUTH_SUAP_KEY}"
            f"&redirect_uri={settings.SOCIAL_AUTH_SUAP_REDIRECT_URI}"
        )

        # o front vai redirecionar o usuário para esse link para fazer o login do suap
        return Response({"auth_url": authorization_url})
    

class ExchangeSuapCode(APIView):
    authentication_classes = [] # impede o jwt
    permission_classes = (AllowAny,)  # endpoin public pq é de login
    """
    Recebe o 'code' do SUAP, troca pelo access_token e autentica o usuário local.
    """
    @swagger_auto_schema(
        request_body=SuapCodeSerializer, 
        responses={200: "Autenticado com sucesso", 400: "Erro ao obter token do SUAP"},
    )
    def post(self, request):
        code = request.data.get("code")

        if not code:
            return Response({"error": "Código de autorização ausente."}, status=status.HTTP_400_BAD_REQUEST)

        # troca o code pelo access token
        token_url = "https://suap.ifrn.edu.br/o/token/"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.SOCIAL_AUTH_SUAP_REDIRECT_URI,  
            "client_id": settings.SOCIAL_AUTH_SUAP_KEY,
            "client_secret": settings.SOCIAL_AUTH_SUAP_SECRET,
        }
        print("data",data)

        # a requisição ao SUAP para pegar o access token
        token_response = requests.post(token_url, data=data)
        print("response",token_response.json())
        if token_response.status_code != 200:
            return Response({"error": "Falha ao obter token do SUAP."}, status=status.HTTP_400_BAD_REQUEST)
        access_token = token_response.json().get("access_token")

        # dados básicos do usuário no SUAP
        populador = PopulateUsuario()
        user_details, usuario = populador.get_user_suap(access_token)
        data_usuario, tipo_usuario = populador.populate_usuario(access_token, user_details, usuario)
        data_usuario.tipo_usuario = tipo_usuario
        usuario_serializer = UsuarioAuthSerializer(data_usuario)

        # gera tokens JWT para autenticação
        refresh = RefreshToken.for_user(usuario)
        # retorna tudo que o front precisa
        
        return Response({
            "user": usuario_serializer.data,
            "jwt": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
        }, status=status.HTTP_200_OK)

