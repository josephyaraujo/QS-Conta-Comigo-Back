from django.core.exceptions import ValidationError
from api.models import AssistenteSocial, Usuario
from django.test import TestCase

class TestAssistenteSocialModel(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(nome_completo = 'Assistente Social Teste', email = 'usertest@gmail.com')
        self.assistente_social = AssistenteSocial.objects.create(
            usuario = self.usuario,
            matricula = '0' * 7,
        )

    def test_cria_AS_valido(self):
        assistente_social = self.assistente_social
        try:
            assistente_social.full_clean()
        except ValidationError:
            self.fail("Criação Assistente Social válido não deveria lançar ValidationError")

    # ----- Testes matricula ----------    
    def test_matricula_limite_minimo_invalido(self):
        self.assistente_social.matricula = '0'
        with self.assertRaises(ValidationError):
            self.assistente_social.full_clean()

    def test_matricula_limite_maximo_invalido(self):
        self.assistente_social.matricula = '0' * 8
        with self.assertRaises(ValidationError):
            self.assistente_social.full_clean()

    def test_matricula_string_vazia_invalido(self):
        self.assistente_social.matricula = ''
        with self.assertRaises(ValidationError):
            self.assistente_social.full_clean()