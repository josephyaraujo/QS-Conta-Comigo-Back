from datetime import date, timedelta
from django.test import TestCase
from api.models import Formulario, FormularioQuestao, Auxilio
from api.serializers import FormularioQuestaoSerializer

class TestFormularioQuestaoSimpleSerializer(TestCase):
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
        self.questao_data = {
            'formulario': self.formulario.id,
            'titulo_pergunta': 'Qual a sua renda familiar parcial?',
            'tipo_pergunta': 'multipla_escolha',
            'obrigatoriedade': True
        }
        
        self.questao = FormularioQuestao.objects.create(
            formulario=self.formulario,
            titulo_pergunta='Qual a sua renda familiar parcial?',
            tipo_pergunta='multipla escolha',
            obrigatoriedade=True
        )

    def test_serializer_com_dados_validos(self):
        serializer = FormularioQuestaoSerializer(data=self.questao_data)
        self.assertTrue(serializer.is_valid(), msg=f"O serializer rejeitou os dados. Erros: {serializer.errors}")

    def test_serializer_com_dados_invalidos_falta_titulo(self):
        dados_invalidos = self.questao_data.copy()
        dados_invalidos.pop('titulo_pergunta')
        serializer = FormularioQuestaoSerializer(data=dados_invalidos)
        self.assertFalse(serializer.is_valid())
        self.assertIn('titulo_pergunta', serializer.errors)

    def test_serializer_com_dado_invalido_caracteres_maximos(self):
        dados_invalidos = self.questao_data.copy()
        dados_invalidos['titulo_pergunta'] = 'A' * 251
        serializer = FormularioQuestaoSerializer(data=dados_invalidos)
        self.assertFalse(serializer.is_valid())
        self.assertIn('titulo_pergunta', serializer.errors)

    def test_serializer_contem_campos_esperados(self):
        serializer = FormularioQuestaoSerializer(instance=self.questao)
        data = serializer.data
        campos_esperados = {
            'id', 'titulo_pergunta', 'tipo_pergunta', 'obrigatoriedade'
        }
        # Verifica se os campos gerados pelo serializer contêm pelo menos os campos base da questão
        self.assertTrue(campos_esperados.issubset(set(data.keys())))