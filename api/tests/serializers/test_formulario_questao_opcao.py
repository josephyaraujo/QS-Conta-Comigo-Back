from datetime import date, timedelta
from django.test import TestCase
from api.models import Formulario, FormularioQuestao, FormularioQuestaoOpcao, Auxilio
from api.serializers import FormularioQuestaoOpcaoSerializer

class TestFormularioQuestaoOpcaoSerializer(TestCase):
    def setUp(self):
        self.auxilio = Auxilio.objects.create()
        self.formulario = Formulario.objects.create(
            titulo='Formulário Teste',
            objetivo='Objetivo de teste',
            solicitados='Todos',
            auxilio_alvo=self.auxilio,
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=5),
            alunos_solicitados=0,
            status='rascunho'
        )
        self.questao = FormularioQuestao.objects.create(
            formulario=self.formulario,
            titulo_pergunta='Qual a sua renda familiar parcial?',
            tipo_pergunta='multipla escolha',
            obrigatoriedade=True
        )
        self.opcao_data = {
            'questao': self.questao.id,
            'alternativa': 'Opção de teste'
        }
        
        self.opcao = FormularioQuestaoOpcao.objects.create(
            questao=self.questao,
            alternativa='Opção de teste'
        )

    def test_serializer_com_dados_validos(self):
        serializer = FormularioQuestaoOpcaoSerializer(data=self.opcao_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_com_dados_invalidos_falta_alternativa(self):
        dados_invalidos = self.opcao_data.copy()
        dados_invalidos.pop('alternativa')
        serializer = FormularioQuestaoOpcaoSerializer(data=dados_invalidos)
        self.assertFalse(serializer.is_valid())
        self.assertIn('alternativa', serializer.errors)

    def test_serializer_com_dado_invalido_caracteres_maximos(self):
        dados_invalidos = self.opcao_data.copy()
        dados_invalidos['alternativa'] = 'A' * 251
        serializer = FormularioQuestaoOpcaoSerializer(data=dados_invalidos)
        self.assertFalse(serializer.is_valid())
        self.assertIn('alternativa', serializer.errors)

    def test_serializer_contem_campos_esperados(self):
        serializer = FormularioQuestaoOpcaoSerializer(instance=self.opcao)
        data = serializer.data
        campos_esperados = {
            'id', 'alternativa'
        }
        # Verifica se os campos gerados pelo serializer contêm pelo menos os campos base da opção
        self.assertTrue(campos_esperados.issubset(set(data.keys())))
        