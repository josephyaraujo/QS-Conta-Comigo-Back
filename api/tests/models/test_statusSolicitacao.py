from django.core.exceptions import ValidationError
from api.models import StatusSolicitacao
from django.test import TestCase

class TestStatusSolicitacaoModel(TestCase):
    def setUp(self):
        self.status_solicitacao = StatusSolicitacao.objects.create(
            codigo = 44, 
            descricao = 'A' * 100
        )
    
    def test_descricao_abaixo_do_limite_valida(self):
        field = StatusSolicitacao._meta.get_field('descricao')
        self.assertEqual(field.max_length, 100)

    def test_descricao_acima_do_limite_invalida(self):
        status = StatusSolicitacao(
            codigo = 45,
            descricao = 'A' * 101
        )
        with self.assertRaises(ValidationError):
            status.full_clean()

    def test_codigo_deve_ser_unico(self):
        status = StatusSolicitacao(
            codigo = self.status_solicitacao.codigo,
            descricao = 'Outro status'
        )
        with self.assertRaises(ValidationError):
            status.full_clean()

    def test_ordem_padrao_deve_ser_zero(self):
        self.assertEqual(self.status_solicitacao.ordem, 0)

    