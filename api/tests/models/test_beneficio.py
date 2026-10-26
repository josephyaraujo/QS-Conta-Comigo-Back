from datetime import date, timedelta
from django.core.exceptions import ValidationError
from api.tests.factories import criar_dados_beneficio
from api.models import (
    AssistenteSocial,
    Usuario,
    Cursos,
    Beneficio,
    Aluno,
    Solicitacao,
    Auxilio,
    StatusSolicitacao,
)
from django.test import TestCase


class TestBeneficioModel(TestCase):
    def setUp(self):
        dados = criar_dados_beneficio()
        for nome, valor in dados.items():
            setattr(self, nome, valor)

    def test_justificativa_abaixo_do_limite_valida(self):
        field = Beneficio._meta.get_field("justificativa_finalizacao")
        self.assertEqual(field.max_length, 200)

    def test_justificativa_acima_do_limite_invalida(self):
        beneficio = Beneficio(
            aluno=self.aluno,
            solicitacao=self.solicitacao,
            tipo_auxilio=self.tipo_auxilio,
            status=True,
            data_fim=date.today() + timedelta(days=30),
            data_finalizacao=date.today() + timedelta(days=30),
            justificativa_finalizacao="B" * 201,
        )
        with self.assertRaises(ValidationError):
            beneficio.full_clean()

    def test_data_fim_igual_data_inicio_valida(self):
        beneficio = Beneficio(
            aluno=self.aluno,
            solicitacao=self.solicitacao,
            tipo_auxilio=self.tipo_auxilio,
            status=True,
            data_fim=date.today(),
            data_finalizacao=date.today(),
            justificativa_finalizacao="B" * 200,
        )
        try:
            beneficio.full_clean()
        except ValidationError:
            self.fail("Benefício com data_fim igual a data_inicio deve ser válido.")

    def test_data_fim_menor_que_data_inicio_invalida(self):
        beneficio = Beneficio(
            aluno=self.aluno,
            solicitacao=self.solicitacao,
            tipo_auxilio=self.tipo_auxilio,
            status=True,
            data_inicio=date.today(),
            data_fim=date.today() - timedelta(days=1),
            data_finalizacao=date.today() + timedelta(days=30),
            justificativa_finalizacao="B" * 200,
        )
        with self.assertRaises(ValidationError) as ctx:
            beneficio.full_clean()

        self.assertIn("data_fim", ctx.exception.message_dict)

    def test_data_finalizacao_igual_data_inicio_valida(self):
        beneficio = Beneficio(
            aluno=self.aluno,
            solicitacao=self.solicitacao,
            tipo_auxilio=self.tipo_auxilio,
            status=True,
            data_fim=date.today() + timedelta(days=30),
            data_finalizacao=date.today(),
            justificativa_finalizacao="B" * 200,
        )
        try:
            beneficio.full_clean()
        except ValidationError:
            self.fail(
                "Benefício com data_finalizacao igual a data_inicio deve ser válido."
            )

    def test_data_finalizacao_menor_que_data_inicio_invalida(self):
        beneficio = Beneficio(
            aluno=self.aluno,
            solicitacao=self.solicitacao,
            tipo_auxilio=self.tipo_auxilio,
            status=True,
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30),
            data_finalizacao=date.today() - timedelta(days=1),
            justificativa_finalizacao="B" * 200,
        )
        with self.assertRaises(ValidationError) as ctx:
            beneficio.full_clean()

        self.assertIn("data_finalizacao", ctx.exception.message_dict)
