
from datetime import date, timedelta

from api.models import (
    Aluno,
    AssistenteSocial,
    Auxilio,
    Beneficio,
    Cursos,
    Formulario,
    FormularioQuestao,
    FormularioQuestaoOpcao,
    Pergunta,
    Solicitacao,
    StatusSolicitacao,
    Usuario,
)


def criar_dados_beneficio():
    usuario = Usuario.objects.create(
        nome_completo="Pafinha Silva",
        email="pafinhaSilva@gmail.com",
    )
    status_solicitacao = StatusSolicitacao.objects.create(
        codigo=44,
        descricao="A" * 100,
    )
    curso = Cursos.objects.create(
        nome="Tecnologia em Análise e Desenvolvimento de Sistemas",
    )
    aluno = Aluno.objects.create(
        usuario=usuario,
        matricula="20241014040025",
        cpf="55284158024",
        curso=curso,
        periodo=4,
        status="Matriculado no SUAP",
        campus="Natal-Central",
        ingresso=None,
        qtd_periodos=6,
    )
    assistente_social = AssistenteSocial.objects.create(
        usuario=usuario,
        matricula="2024101",
    )
    tipo_auxilio = Auxilio.objects.create()
    solicitacao = Solicitacao.objects.create(
        status=status_solicitacao,
        descricao="B" * 100,
        id_assistente_social=assistente_social,
        id_aluno=aluno,
        tipo_auxilio=tipo_auxilio,
    )
    beneficio = Beneficio.objects.create(
        aluno=aluno,
        solicitacao=solicitacao,
        tipo_auxilio=tipo_auxilio,
        status=True,
        data_inicio=date.today(),
        data_fim=date.today() + timedelta(days=30),
        data_finalizacao=date.today() + timedelta(days=30),
        justificativa_finalizacao="B" * 200,
    )

    return {
        "usuario": usuario,
        "statusSolicitacao": status_solicitacao,
        "curso": curso,
        "aluno": aluno,
        "assistente_social": assistente_social,
        "tipo_auxilio": tipo_auxilio,
        "solicitacao": solicitacao,
        "beneficio": beneficio,
    }


def criar_dados_solicitacao(descricao_solicitacao="B" * 200):
    usuario = Usuario.objects.create(
        nome_completo="Pafinha Silva",
        email="pafinhaSilva@gmail.com",
    )
    status_solicitacao = StatusSolicitacao.objects.create(
        codigo=44,
        descricao="A" * 100,
    )
    curso = Cursos.objects.create(
        nome="Tecnologia em Análise e Desenvolvimento de Sistemas",
    )
    aluno = Aluno.objects.create(
        usuario=usuario,
        matricula="20241014040025",
        cpf="55284158024",
        curso=curso,
        periodo=4,
        status="Matriculado no SUAP",
        campus="Natal-Central",
        ingresso=None,
        qtd_periodos=6,
    )
    assistente_social = AssistenteSocial.objects.create(
        usuario=usuario,
        matricula="2024101",
    )
    tipo_auxilio = Auxilio.objects.create()
    solicitacao = Solicitacao.objects.create(
        status=status_solicitacao,
        descricao=descricao_solicitacao,
        id_assistente_social=assistente_social,
        id_aluno=aluno,
        tipo_auxilio=tipo_auxilio,
    )

    return {
        "usuario": usuario,
        "statusSolicitacao": status_solicitacao,
        "curso": curso,
        "aluno": aluno,
        "assistente_social": assistente_social,
        "tipo_auxilio": tipo_auxilio,
        "solicitacao": solicitacao,
    }


def criar_dados_formulario(
    titulo="Formulário Teste",
    solicitados="Todos",
):
    auxilio = Auxilio.objects.create()
    formulario = Formulario.objects.create(
        titulo=titulo,
        objetivo="Objetivo de teste",
        solicitados=solicitados,
        auxilio_alvo=auxilio,
        data_inicio=date.today(),
        data_fim=date.today() + timedelta(days=5),
        alunos_solicitados=0,
        status="rascunho",
    )

    return {
        "auxilio": auxilio,
        "formulario": formulario,
    }


def criar_dados_formulario_questao(
    titulo_pergunta="Qual a sua renda familiar parcial?",
    alternativa=None,
):
    dados = criar_dados_formulario()
    formulario = dados["formulario"]

    questao = FormularioQuestao.objects.create(
        formulario=formulario,
        titulo_pergunta=titulo_pergunta,
        tipo_pergunta="multipla escolha",
        obrigatoriedade=True,
    )

    dados["questao"] = questao

    if alternativa is not None:
        opcao = FormularioQuestaoOpcao.objects.create(
            questao=questao,
            alternativa=alternativa,
        )
        dados["opcao"] = opcao

    return dados

def criar_dados_aluno(
    nome_completo="Usuario Teste",
    email="userteste@gmail.com",
    criar_assistente_social=False,
):
    usuario = Usuario.objects.create(
        nome_completo=nome_completo,
        email=email,
    )
    curso = Cursos.objects.create(
        nome="Tecnologia em Análise e Desenvolvimento de Sistemas",
    )
    aluno = Aluno.objects.create(
        usuario=usuario,
        matricula="0" * 14,
        cpf="0" * 11,
        curso=curso,
        periodo=4,
        status="Matriculado no SUAP",
        campus="Natal-Central",
        ingresso=None,
        qtd_periodos=6,
    )

    dados = {
        "usuario": usuario,
        "curso": curso,
        "aluno": aluno,
    }

    if criar_assistente_social:
        dados["assistente_social"] = AssistenteSocial.objects.create(
            usuario=usuario,
            matricula="0" * 7,
        )

    return dados

def criar_dados_pergunta(cpf="55284158024"):
    dados_aluno = criar_dados_solicitacao()
    aluno = dados_aluno["aluno"]

    aluno.cpf = cpf
    aluno.save(update_fields=["cpf"])

    pergunta = Pergunta.objects.create(
        enunciado="A" * 900,
        resposta=None,
        status="nao_respondida",
        data_realizacao=date.today(),
        data_resposta=date.today(),
        assistente_social=None,
        aluno=aluno,
    )

    return {
        "usuario": dados_aluno["usuario"],
        "curso": dados_aluno["curso"],
        "aluno": aluno,
        "pergunta": pergunta,
    }

def criar_dados_assistente_social():
    usuario = Usuario.objects.create(
        nome_completo="Assistente Social Teste",
        email="usertest@gmail.com",
    )
    assistente_social = AssistenteSocial.objects.create(
        usuario=usuario,
        matricula="0" * 7,
    )

    return {
        "usuario": usuario,
        "assistente_social": assistente_social,
    }

def criar_dados_auxilio(**overrides):
    """Retorna dados padrão para testes de Auxilio."""
    from api.models import Auxilio

    dados = {
        "nome": Auxilio._meta.get_field("nome").choices[0][0],
        "campus": Auxilio._meta.get_field("campus").choices[0][0],
        "descricao": "Descrição de teste",
        "qtd_chamados": 0,
        "impedir_aluno": False,
        "exigir_comprov": False,
        "exigir_frequen": False,
        "disponibilidade": False,
        "edital": None,
    }
    dados.update(overrides)
    return dados