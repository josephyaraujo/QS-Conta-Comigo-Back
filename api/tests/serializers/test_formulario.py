from datetime import date, timedelta
from django.test import TestCase
from api.models import Formulario, Auxilio
from api.serializers import FormularioSerializer

class TestFormularioSerializer(TestCase):
    def setUp(self):
        self.auxilio = Auxilio.objects.create()
        self.formulario_data = {
            'titulo': 'Formulário Teste',
            'objetivo': 'Objetivo de teste',
            'solicitados': 'todos',
            'auxilio_alvo': self.auxilio.id,
            'data_inicio': date.today(),
            'data_fim': date.today() + timedelta(days=5),
            'alunos_solicitados': 0,
            'status': 'rascunho',
            "questoes": [
                {
                    "titulo_pergunta": "Qual a sua cor favorita?",
                    "tipo_pergunta": "multipla_escolha", 
                    "obrigatoriedade": True, 
                    "ordem": 1
                },
                {
                    "titulo_pergunta": "Qual o seu curso?",
                    "tipo_pergunta": "paragrafo",
                    "obrigatoriedade": False,
                    "ordem": 2
                }
            ]
        }
        
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

    def test_serializer_com_dados_validos(self):
        serializer = FormularioSerializer(data=self.formulario_data)
        self.assertTrue(serializer.is_valid(),  msg=f"O serializer rejeitou os dados. Erros: {serializer.errors}")

    def test_serializer_com_dados_invalidos_falta_titulo(self):
        dados_invalidos = self.formulario_data.copy()
        dados_invalidos.pop('titulo')
        serializer = FormularioSerializer(data=dados_invalidos)
        self.assertFalse(serializer.is_valid())
        self.assertIn('titulo', serializer.errors)

    def test_serializer_com_dado_invalido_caracteres_maximos(self):
        dados_invalidos = self.formulario_data.copy()
        dados_invalidos['titulo'] = 'A' * 101
        serializer = FormularioSerializer(data=dados_invalidos)
        self.assertFalse(serializer.is_valid())
        self.assertIn('titulo', serializer.errors)

    def test_serializer_contem_campos_esperados(self):
        serializer = FormularioSerializer(instance=self.formulario)
        data = serializer.data
        campos_esperados = {
            'id', 'titulo', 'objetivo', 'solicitados', 'auxilio_alvo', 
            'alunos_selecionados', 'data_inicio', 'data_fim', 
            'alunos_solicitados', 'status'
        }
        # Verifica se os campos gerados pelo serializer contêm pelo menos os campos base do model
        self.assertTrue(campos_esperados.issubset(set(data.keys())))