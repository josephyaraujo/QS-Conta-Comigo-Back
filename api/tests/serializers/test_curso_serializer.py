from django.test import TestCase

from api.models import Cursos
from api.serializers.base import CursoSerializer


class CursoSerializerTestCase(TestCase):
    def setUp(self):
        self.curso = Cursos.objects.create(
            nome=Cursos._meta.get_field("nome").choices[0][0]
        )

    def test_deve_serializar_apenas_id_e_nome(self):
        serializer = CursoSerializer(instance=self.curso)
        data = serializer.data

        self.assertEqual(set(data.keys()), {"id", "nome"})

    def test_deve_serializar_multiplos_cursos(self):
        serializer = CursoSerializer(instance=[self.curso], many=True)

        self.assertEqual(len(serializer.data), 1)
        self.assertEqual(set(serializer.data[0].keys()), {"id", "nome"})

    def test_deve_validar_dados_para_criacao(self):
        payload = {"nome": Cursos._meta.get_field("nome").choices[0][0]}
        serializer = CursoSerializer(data=payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_deve_criar_curso_via_serializer(self):
        payload = {"nome": Cursos._meta.get_field("nome").choices[0][0]}
        serializer = CursoSerializer(data=payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        curso = serializer.save()

        self.assertIsNotNone(curso.id)
        self.assertEqual(curso.nome, payload["nome"])