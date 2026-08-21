from datetime import date, timedelta
from django.core.exceptions import ValidationError
from api.models import Aluno, Usuario, Cursos, Aluno
from django.test import TestCase

class TestAlunoModel(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(nome_completo = 'Aluno Teste', email = 'usertest@gmail.com')
        self.curso = 'tecnologia_ads'
        self.aluno = Aluno.objects.create(
            usuario = self.usuario,
            matricula = '20241014040025',
            cpf = '0'* 11,
            curso = self.curso,
            periodo = 4,
            status = 'Matriculado no SUAP',
            campus = 'Natal Central',
            ingresso = None,
            qtd_periodos = 6
        )

    def test_cria_aluno_valido(self):
        aluno = self.aluno
        try:
            aluno.full_clean()
        except ValidationError:
            self.fail("Criação aluno válido não deveria lançar ValidationError")

    # ----- Testes CPF ----------     
    def test_cpf_limite_maximo_invalido(self):
        self.aluno.cpf = '0' * 12
        with self.assertRaises(ValidationError):
            self.aluno.full_clean()

    def test_cpf_limite_minimo_invalido(self):
        self.aluno.cpf = '0'
        with self.assertRaises(ValidationError):
            self.aluno.full_clean()

    def test_cpf_caracteres_invalidos(self):
        self.aluno.cpf = 'abcde12345f'
        with self.assertRaises(ValidationError):
            self.aluno.full_clean()

    def test_cpf_string_vazia(self):
        self.aluno.cpf = ''
        with self.assertRaises(ValidationError):
            self.aluno.full_clean()

    # ----- Testes matricula ----------    
    def test_matricula_limite_minimo_invalido(self):
        self.aluno.matricula = '0'
        with self.assertRaises(ValidationError):
            self.aluno.full_clean()

    def test_matricula_limite_maximo_invalido(self):
        self.aluno.matricula = '0' * 15
        with self.assertRaises(ValidationError):
            self.aluno.full_clean()

    # ----- Testes matricula ----------   
    def test_periodo_limite_inferior_invalido(self):
        periodo = Aluno(
            periodo = -1,
            usuario = self.usuario
        )
        with self.assertRaises(ValidationError):
            periodo.full_clean()

    def test_periodo_tipo_invalido(self):
        self.aluno.periodo = 'um'
        with self.assertRaises(ValidationError):
            self.aluno.full_clean()

    # ----- Testes status ---------- 
    def test_status_qtd_caracteres_limite_superior_invalido(self):
        self.aluno.status = 'a' * 101
        with self.assertRaises(ValidationError):
            self.aluno.full_clean()

    def test_string_vazia_invalido(self):
        self.aluno.status = ''
        with self.assertRaises(ValidationError):
            self.aluno.full_clean()

    # ----- Testes campus ---------- 
    def test_campus_limite_caracteres_superior_invalido(self): 
        self.aluno.campus = 'a' * 101
        with self.assertRaises(ValidationError):
            self.aluno.full_clean()

    def test_campus_string_vazia_invalido(self): 
        self.aluno.campus = ''
        with self.assertRaises(ValidationError):
            self.aluno.full_clean()
    
    # ----- Testes curso ---------- 
    def test_curso_limite_caracteres_superior_invalido(self):
        self.aluno.curso = 'a' * 101
        with self.assertRaises(ValidationError):
            self.aluno.full_clean()

    def test_curso_string_vazia_invalido(self):
        self.aluno.curso = ''
        with self.assertRaises(ValidationError):
            self.aluno.full_clean()
    
    def test_curso_existe_no_choice(self): # informação existente no choice
        field = Aluno._meta.get_field('curso')
        choices = [choice[0] for choice in field.choices]
        self.assertIn('tecnologia_ads', choices)
    