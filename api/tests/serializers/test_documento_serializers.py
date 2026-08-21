from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from api.models import Aluno, Documento, Usuario
from api.serializers.chamados import (
    DocumentoAlunoSerializer,
    DocumentoCreateSerializer,
    DocumentoSerializer,
)


def _choice_value(model, field_name, fallback=None):
    field = model._meta.get_field(field_name)
    if field.choices:
        return field.choices[0][0]
    return fallback


def criar_usuario_valido(**kwargs):
    field_names = {field.name for field in Usuario._meta.get_fields() if hasattr(field, "name")}

    data = {}

    if "username" in field_names:
        data["username"] = "usuario_teste"

    if "email" in field_names:
        data["email"] = "usuario@teste.com"

    if "cpf" in field_names:
        data["cpf"] = "12345678901"

    if "first_name" in field_names:
        data["first_name"] = "Usuario"

    if "last_name" in field_names:
        data["last_name"] = "Teste"

    data.update(kwargs)

    usuario = Usuario.objects.create(**data)

    if hasattr(usuario, "set_password"):
        usuario.set_password("123456")
        usuario.save()

    return usuario


def criar_aluno_valido(**kwargs):
    field_names = {field.name for field in Aluno._meta.get_fields() if hasattr(field, "name")}

    data = {}

    if "usuario" in field_names:
        identificador_usuario = kwargs.pop("identificador_usuario", "202600000")
        username_usuario = kwargs.pop("username_usuario", f"user_{identificador_usuario}")
        email_usuario = kwargs.pop("email_usuario", f"{username_usuario}@teste.com")

        data["usuario"] = criar_usuario_valido(
            username=username_usuario,
            email=email_usuario,
        )

    if "matricula" in field_names:
        data["matricula"] = "202600001"

    if "periodo" in field_names:
        data["periodo"] = 1

    if "campus" in field_names:
        data["campus"] = _choice_value(Aluno, "campus", "Natal-Central")

    if "curso" in field_names:
        curso_field = Aluno._meta.get_field("curso")
        if getattr(curso_field, "choices", None):
            data["curso"] = curso_field.choices[0][0]

    if "turno" in field_names:
        turno_field = Aluno._meta.get_field("turno")
        if getattr(turno_field, "choices", None):
            data["turno"] = turno_field.choices[0][0]

    if "cpf" in field_names:
        data["cpf"] = "12345678901"

    if "telefone" in field_names:
        data["telefone"] = "84999999999"

    data.update(kwargs)
    return Aluno.objects.create(**data)


class DocumentoSerializerTestCase(TestCase):
    def setUp(self):
        self.documento = Documento.objects.create(
            titulo="Documento serializer",
            tipo_documento=Documento._meta.get_field("tipo_documento").choices[0][0],
            descricao="Descrição",
            arquivo=SimpleUploadedFile(
                "documento.pdf",
                b"arquivo teste",
                content_type="application/pdf",
            ),
        )

    def test_deve_serializar_todos_os_campos(self):
        serializer = DocumentoSerializer(instance=self.documento)
        data = serializer.data

        self.assertIn("id", data)
        self.assertIn("titulo", data)
        self.assertIn("tipo_documento", data)
        self.assertIn("descricao", data)
        self.assertIn("aluno", data)
        self.assertIn("assistente_social", data)
        self.assertIn("solicitacao", data)
        self.assertIn("data_criacao", data)
        self.assertIn("arquivo", data)

    def test_deve_validar_dados_basicos(self):
        payload = {
            "titulo": "Novo documento",
            "tipo_documento": Documento._meta.get_field("tipo_documento").choices[0][0],
            "descricao": "Teste",
        }

        serializer = DocumentoSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)


class DocumentoAlunoSerializerTestCase(TestCase):
    def setUp(self):
        self.aluno = criar_aluno_valido(
            matricula="202600101",
            identificador_usuario="202600301",
            username_usuario="user_doc_aluno",
            email_usuario="user_doc_aluno@teste.com",
        )

        self.documento = Documento.objects.create(
            titulo="Documento do aluno",
            tipo_documento=Documento._meta.get_field("tipo_documento").choices[0][0],
            descricao="Documento com aluno",
            aluno=self.aluno,
            arquivo=SimpleUploadedFile(
                "aluno.pdf",
                b"arquivo aluno",
                content_type="application/pdf",
            ),
        )

    def test_deve_serializar_campos_esperados(self):
        serializer = DocumentoAlunoSerializer(instance=self.documento)
        data = serializer.data

        self.assertEqual(
            set(data.keys()),
            {"id", "tipo_documento", "arquivo", "aluno", "data_criacao"},
        )

    def test_campo_aluno_deve_vir_aninhado(self):
        serializer = DocumentoAlunoSerializer(instance=self.documento)
        data = serializer.data

        self.assertIsInstance(data["aluno"], dict)


class DocumentoCreateSerializerTestCase(TestCase):
    def setUp(self):
        self.aluno = criar_aluno_valido(
            matricula="202600202",
            identificador_usuario="202600302",
            username_usuario="user_doc_create",
            email_usuario="user_doc_create@teste.com",
        )

    def test_deve_validar_quando_aluno_id_existe(self):
        payload = {
            "aluno_id": self.aluno.id,
            "arquivo": SimpleUploadedFile(
                "create.pdf",
                b"conteudo",
                content_type="application/pdf",
            ),
            "tipo_documento": Documento._meta.get_field("tipo_documento").choices[0][0],
        }

        serializer = DocumentoCreateSerializer(data=payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_deve_invalidar_quando_aluno_id_nao_existe(self):
        payload = {
            "aluno_id": 999999,
            "arquivo": SimpleUploadedFile(
                "create.pdf",
                b"conteudo",
                content_type="application/pdf",
            ),
            "tipo_documento": Documento._meta.get_field("tipo_documento").choices[0][0],
        }

        serializer = DocumentoCreateSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertTrue(
            "aluno" in str(serializer.errors).lower()
            or "aluno_id" in str(serializer.errors).lower()
        )

    def test_deve_criar_documento_com_aluno_id(self):
        payload = {
            "aluno_id": self.aluno.id,
            "arquivo": SimpleUploadedFile(
                "create-ok.pdf",
                b"conteudo ok",
                content_type="application/pdf",
            ),
            "tipo_documento": Documento._meta.get_field("tipo_documento").choices[0][0],
        }

        serializer = DocumentoCreateSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        documento = serializer.save()

        self.assertIsNotNone(documento.id)
        self.assertEqual(documento.aluno.id, self.aluno.id)

    def test_tipo_documento_deve_assumir_default_quando_nao_for_informado(self):
        payload = {
            "aluno_id": self.aluno.id,
            "arquivo": SimpleUploadedFile(
                "default.pdf",
                b"default",
                content_type="application/pdf",
            ),
        }

        serializer = DocumentoCreateSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        documento = serializer.save()

        self.assertEqual(documento.tipo_documento, "outros")

    def test_campos_write_only_nao_devem_aparecer_na_saida(self):
        payload = {
            "aluno_id": self.aluno.id,
            "arquivo": SimpleUploadedFile(
                "writeonly.pdf",
                b"write only",
                content_type="application/pdf",
            ),
            "tipo_documento": Documento._meta.get_field("tipo_documento").choices[0][0],
        }

        serializer = DocumentoCreateSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        documento = serializer.save()

        output = DocumentoCreateSerializer(instance=documento).data

        self.assertNotIn("aluno_id", output)