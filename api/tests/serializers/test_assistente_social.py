from api.models import AssistenteSocial, Usuario
from api.serializers.base import (AssistenteSocialSerializer)
from django.test import TestCase

class TestAssistenteSocialSerializer(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(nome_completo = 'Assistente Social Teste', email = 'usertest@gmail.com')
        self.assistente_social = AssistenteSocial.objects.create(
            usuario = self.usuario,
            matricula = '0' * 7,
        )
    
    def test_AS_serializer_leitura_retorna_campos_esperados(self):
        data = AssistenteSocialSerializer(instance = self.assistente_social).data
        self.assertIn('id', data)
        self.assertIn('usuario', data)
        self.assertIn('matricula', data)
