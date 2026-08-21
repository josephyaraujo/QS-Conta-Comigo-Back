"""
Views for the main project.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    API root endpoint that provides information about the Conta Comigo Backend API.
    """
    return Response({
        'message': 'Bem-vindo à API do Sistema de Apoio à Formação Estudantil - Conta Comigo',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'api_v1': '/api/v1/',
            'api_auth': '/api-auth/',
        },
        'documentation': 'Esta é a API REST do sistema Conta Comigo para apoio à formação estudantil.'
    }, status=status.HTTP_200_OK)