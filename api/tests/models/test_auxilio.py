from django.core.exceptions import ValidationError
from django.test import TestCase

from api.models import Auxilio


class AuxilioModelTestCase(TestCase):
    def make_auxilio(self, **kwargs):
        nome_valido = Auxilio._meta.get_field("nome").choices[0][0]
        campus_valido = Auxilio._meta.get_field("campus").choices[0][0]

        data = {
            "nome": nome_valido,
            "campus": campus_valido,
            "descricao": "Descrição de teste",
            "qtd_chamados": 0,
            "impedir_aluno": False,
            "exigir_comprov": False,
            "exigir_frequen": False,
            "disponibilidade": False,
            "edital": None,
        }
        data.update(kwargs)
        return Auxilio(**data)

    def test_deve_criar_auxilio_valido_quando_indisponivel(self):
        auxilio = self.make_auxilio()
        auxilio.full_clean()

    def test_nao_deve_aceitar_qtd_chamados_negativa(self):
        auxilio = self.make_auxilio(qtd_chamados=-1)

        with self.assertRaises(ValidationError) as exc:
            auxilio.full_clean()

        self.assertIn("qtd_chamados", exc.exception.message_dict)

    def test_auxilio_disponivel_deve_exigir_edital(self):
        auxilio = self.make_auxilio(
            disponibilidade=True,
            exigir_frequen=True,
            edital=None,
        )

        with self.assertRaises(ValidationError) as exc:
            auxilio.full_clean()

        self.assertIn("edital", str(exc.exception).lower())

    def test_auxilio_disponivel_deve_exigir_frequencia(self):
        auxilio = self.make_auxilio(
            disponibilidade=True,
            exigir_frequen=False,
            edital="Edital 001/2026",
        )

        with self.assertRaises(ValidationError) as exc:
            auxilio.full_clean()

        self.assertTrue(
            "frequen" in str(exc.exception).lower()
            or "frequ" in str(exc.exception).lower()
        )

    def test_auxilio_disponivel_com_edital_e_frequencia_deve_ser_valido(self):
        auxilio = self.make_auxilio(
            disponibilidade=True,
            exigir_frequen=True,
            edital="Edital 001/2026",
            exigir_comprov=True,
            impedir_aluno=True,
        )

        auxilio.full_clean()

    def test_auxilio_indisponivel_nao_deve_exigir_frequencia(self):
        auxilio = self.make_auxilio(
            disponibilidade=False,
            exigir_frequen=True,
        )

        with self.assertRaises(ValidationError) as exc:
            auxilio.full_clean()

        self.assertTrue(
            "frequen" in str(exc.exception).lower()
            or "frequ" in str(exc.exception).lower()
        )

    def test_auxilio_indisponivel_nao_deve_exigir_comprovante(self):
        auxilio = self.make_auxilio(
            disponibilidade=False,
            exigir_comprov=True,
        )

        with self.assertRaises(ValidationError) as exc:
            auxilio.full_clean()

        self.assertIn("comprov", str(exc.exception).lower())

    def test_auxilio_indisponivel_nao_deve_impedir_aluno(self):
        auxilio = self.make_auxilio(
            disponibilidade=False,
            impedir_aluno=True,
        )

        with self.assertRaises(ValidationError) as exc:
            auxilio.full_clean()

        self.assertIn("aluno", str(exc.exception).lower())

    def test_str_do_model_deve_existir(self):
        auxilio = self.make_auxilio()
        texto = str(auxilio)
        self.assertIsInstance(texto, str)
        self.assertNotEqual(texto.strip(), "")