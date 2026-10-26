from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from api.models import Formulario
from api.tests.factories import criar_dados_formulario

class TestFormularioModel(TestCase):
    def setUp(self):
        dados = criar_dados_formulario(
            titulo="A" * 100,
            solicitados="todos",
        )
        self.auxilio = dados["auxilio"]
        self.formulario = dados["formulario"]

    # ----- Testes Titulo ----------
    def test_titulo_caracteres_maximo_valido(self):
        field = Formulario._meta.get_field("titulo")
        self.assertEqual(field.max_length, 100)

    def test_titulo_caracteres_superior_invalido(self):
        formulario = Formulario(
            titulo="A" * 101,
            objetivo="Objetivo de teste",
            solicitados="todos",
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=5),
        )
        with self.assertRaises(ValidationError):
            formulario.full_clean()

    def test_titulo_vazio_invalido(self):
        formulario = Formulario(
            titulo="",
            objetivo="Objetivo de teste",
            solicitados="todos",
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=5),
        )
        with self.assertRaises(ValidationError):
            formulario.full_clean()

    # ----- Testes Datas ----------
    def test_data_fim_maior_data_inicio_valida(self):
        formulario = self.formulario
        try:
            formulario.full_clean()
        except ValidationError:
            self.fail(
                "Formulário com data_fim maior que data_inicio não deveria lançar ValidationError."
            )

    def test_data_fim_igual_data_inicio_valida(self):
        formulario = Formulario(
            titulo="A" * 50,
            objetivo="Objetivo de teste",
            solicitados="todos",
            data_inicio=date.today(),
            data_fim=date.today(),
        )
        try:
            formulario.full_clean()
        except ValidationError:
            self.fail(
                "Formulário com data_fim igual a data_inicio não deveria lançar ValidationError."
            )

    def test_data_fim_menor_data_inicio_invalida(self):
        formulario = Formulario(
            titulo="A" * 50,
            objetivo="Objetivo de teste",
            solicitados="todos",
            data_inicio=date.today(),
            data_fim=date.today() - timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            formulario.full_clean()
