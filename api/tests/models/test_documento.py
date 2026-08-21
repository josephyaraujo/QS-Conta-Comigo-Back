from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from api.models import Documento


class DocumentoModelTestCase(TestCase):
    def make_documento(self, **kwargs):
        arquivo = SimpleUploadedFile(
            "teste.pdf",
            b"conteudo de teste",
            content_type="application/pdf",
        )

        data = {
            "titulo": "Documento de teste",
            "tipo_documento": Documento.TIPO_DOCUMENTO_CHOICES[0][0]
            if hasattr(Documento, "TIPO_DOCUMENTO_CHOICES")
            else "outros",
            "descricao": "Descrição do documento",
            "arquivo": arquivo,
            "aluno": None,
            "assistente_social": None,
            "solicitacao": None,
        }
        data.update(kwargs)
        return Documento.objects.create(**data)

    def test_deve_criar_documento_com_campos_basicos(self):
        documento = self.make_documento()

        self.assertIsNotNone(documento.id)
        self.assertEqual(documento.titulo, "Documento de teste")
        self.assertIsNotNone(documento.data_criacao)

    def test_descricao_pode_ser_nula(self):
        documento = self.make_documento(descricao=None)

        self.assertIsNone(documento.descricao)

    def test_aluno_pode_ser_nulo(self):
        documento = self.make_documento(aluno=None)

        self.assertIsNone(documento.aluno)

    def test_assistente_social_pode_ser_nulo(self):
        documento = self.make_documento(assistente_social=None)

        self.assertIsNone(documento.assistente_social)

    def test_solicitacao_pode_ser_nula(self):
        documento = self.make_documento(solicitacao=None)

        self.assertIsNone(documento.solicitacao)

    def test_arquivo_pode_ser_salvo(self):
        documento = self.make_documento()

        self.assertTrue(bool(documento.arquivo))
        self.assertIn("documentos/", documento.arquivo.name)

    def test_str_do_model_deve_existir(self):
        documento = self.make_documento()
        texto = str(documento)

        self.assertIsInstance(texto, str)
        self.assertNotEqual(texto.strip(), "")