from django.test import TestCase
from datetime import date, timedelta

from api.tests.factories import criar_dados_beneficio
from api.models import (
    Beneficio,
    AssistenteSocial,
    Usuario,
    Aluno,
    Auxilio,
    Solicitacao,
    StatusSolicitacao,
    Cursos,
)
from api.serializers.auxilio_beneficio import (
    BeneficioCreateSerializer,
    BeneficioSerializer,
    BeneficioAlunoSerializer,
)


class TestBeneficioSerializers(TestCase):
    def setUp(self):
        dados = criar_dados_beneficio()
        for nome, valor in dados.items():
            setattr(self, nome, valor)

    def test_beneficio_create_serializer_valida_dados_corretos(self):
        serializer = BeneficioCreateSerializer(
            data={
                "aluno_id": self.aluno.id,
                "solicitacao_id": self.solicitacao.id,
                "tipo_auxilio": self.tipo_auxilio.id,
                "status": True,
                "data_fim": date.today() + timedelta(days=30),
                "data_finalizacao": date.today() + timedelta(days=30),
                "justificativa_finalizacao": "B" * 200,
                "data_inicio": date.today(),
            }
        )
        self.assertTrue(serializer.is_valid())

    def test_beneficio_serializer_retorna_campos_esperados(self):
        data = BeneficioSerializer(instance=self.beneficio).data

        self.assertIn("aluno", data)
        self.assertIn("tipo_auxilio", data)
        self.assertIn("status", data)
        self.assertIn("data_fim", data)
        self.assertIn("data_finalizacao", data)
        self.assertIn("data_inicio", data)
        self.assertIn("justificativa_finalizacao", data)
        self.assertIn("motivo_entrada", data)
        self.assertIn("parecer", data)

    def test_beneficio_aluno_serializer_retorna_campos_esperados(self):
        data = BeneficioAlunoSerializer(instance=self.beneficio).data

        self.assertIn("id", data)
        self.assertIn("status", data)
        self.assertIn("titulo", data)
        self.assertIn("data_inicio", data)
