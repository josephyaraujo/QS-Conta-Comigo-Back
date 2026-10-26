from datetime import date, timedelta

from api.models import (
    Aluno,
    AssistenteSocial,
    Auxilio,
    Beneficio,
    Cursos,
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
