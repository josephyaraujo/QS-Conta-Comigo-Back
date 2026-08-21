from django.test import TestCase

from api.models import Cursos


class CursosModelTestCase(TestCase):
    def test_deve_criar_curso_com_nome_valido(self):
        nome_valido = Cursos._meta.get_field("nome").choices[0][0]
        curso = Cursos.objects.create(nome=nome_valido)

        self.assertIsNotNone(curso.id)
        self.assertEqual(curso.nome, nome_valido)

    def test_nome_deve_pertencer_as_choices(self):
        field = Cursos._meta.get_field("nome")
        choices = [choice[0] for choice in field.choices]

        self.assertGreater(len(choices), 0)

    def test_str_do_model_deve_existir(self):
        nome_valido = Cursos._meta.get_field("nome").choices[0][0]
        curso = Cursos.objects.create(nome=nome_valido)

        texto = str(curso)
        self.assertIsInstance(texto, str)
        self.assertNotEqual(texto.strip(), "")