from rest_framework.permissions import IsAuthenticated

from api.permission import OnlyAssistenteSocial, OnlyAluno, IsAlunoOrAssistenteSocial


def obter_permissoes_por_acao(
    acao,
    acoes_assistente=None,
    acoes_aluno=None,
    acoes_aluno_ou_assistente=None,
):
    if acoes_assistente and acao in acoes_assistente:
        return [IsAuthenticated(), OnlyAssistenteSocial()]

    if acoes_aluno and acao in acoes_aluno:
        return [IsAuthenticated(), OnlyAluno()]

    if acoes_aluno_ou_assistente and acao in acoes_aluno_ou_assistente:
        return [IsAuthenticated(), IsAlunoOrAssistenteSocial()]

    return [IsAuthenticated()]
