from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from api.models import Pergunta
from api.tests.factories import criar_dados_pergunta


class TestPerguntaModel(TestCase):
    def setUp(self):
        dados = criar_dados_pergunta()
        for nome, valor in dados.items():
            setattr(self, nome, valor)

    # ----- Testes Enunciado ----------

    def test_enunciado_caracteres_maximo_valido(
        self,
    ):  # enunciado com quantidade de caracteres limite válido - VÁLIDA
        field = Pergunta._meta.get_field("enunciado")
        self.assertEqual(field.max_length, 900)

    def test_enunciado_caracteres_inferior_invalido(
        self,
    ):  # enunciado com a quantidade de caracteres inferior(vazio) - INVÁLIDA
        pergunta = Pergunta(enunciado="", status="nao_respondida", aluno=self.aluno)
        with self.assertRaises(ValidationError):
            pergunta.full_clean()

    def test_enunciado_caracteres_superior_invalido(
        self,
    ):  # enunciado com quantidade de caracteres maior do que o permitido - INVÁLIDA
        pergunta = Pergunta(
            enunciado="A" * 901, status="nao_respondida", aluno=self.aluno
        )
        with self.assertRaises(ValidationError):
            pergunta.full_clean()

    # ----- Testes Data Realização ----------
    def test_data_realizacao_futura_invalido(
        self,
    ):  # data de realização com valor futuro(maior que o dia atual) - INVÁLIDA
        pergunta = Pergunta(
            enunciado="A" * 900,
            status="nao_respondida",
            aluno=self.aluno,
            data_realizacao=date.today() + timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            pergunta.full_clean()

    def test_data_realizacao_limite_valida(
        self,
    ):  # data de realização com valor válido(dia atual) - VÁLIDA
        pergunta = self.pergunta
        try:
            pergunta.full_clean()
        except ValidationError:
            self.fail("data_realizacao válida não deveria lançar ValidationError.")

    def test_data_realizacao_passada_invalida(
        self,
    ):  # data de realização com valor passado(menor que o dia atual) - INVÁLIDA
        pergunta = Pergunta(
            enunciado="A" * 900,
            status="nao_respondida",
            aluno=self.aluno,
            data_realizacao=date.today() - timedelta(days=1),
        )
        self.assertLess(pergunta.data_realizacao, date.today())

    # ----- Testes Data Resposta ----------
    def test_data_resposta_limite_valida(
        self,
    ):  # data de resposta limite válido (dia atual, maior que a data de realização) - VÁLIDA
        pergunta = self.pergunta
        try:
            pergunta.full_clean()
        except ValidationError:
            self.fail("data_resposta válida não deveria lançar ValidationError.")

    def test_data_resposta_limite_futura_invalido(
        self,
    ):  # data de resposta com valor futuro(maior que o dia atual) - INVÁLIDA
        pergunta = Pergunta(
            enunciado="A" * 900,
            status="nao_respondida",
            aluno=self.aluno,
            data_resposta=date.today() + timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            pergunta.full_clean()

    def test_data_resposta_limite_passada_invalido(
        self,
    ):  # data de resposta com data passada (menor do que o dia atual) - INVÁLIDA
        pergunta = Pergunta(
            enunciado="A" * 900,
            status="nao_respondida",
            aluno=self.aluno,
            data_resposta=date.today() - timedelta(days=1),
            data_realizacao=date.today(),
        )
        with self.assertRaises(ValidationError):
            pergunta.full_clean()

    def test_data_resposta_menor_data_realizacao_invalida(
        self,
    ):  # data de resposta menor que a data de realização da pergunta - INVÁLIDA
        pergunta = Pergunta(
            enunciado="A" * 900,
            status="nao_respondida",
            aluno=self.aluno,
            data_resposta=date.today() - timedelta(days=1),
            data_realizacao=date.today(),
        )
        with self.assertRaises(ValidationError):
            pergunta.full_clean()

    def test_data_resposta_maior_data_realizacao_valida(
        self,
    ):  # data de resposta maior que a data de realização da pergunta - VÁLIDA
        pergunta = Pergunta(
            enunciado="A" * 900,
            status="nao_respondida",
            aluno=self.aluno,
            data_resposta=date.today(),
            data_realizacao=date.today() - timedelta(days=1),
        )
        try:
            pergunta.full_clean()
        except ValidationError:
            self.fail("Caso válido não deveria lançar ValidationError.")
