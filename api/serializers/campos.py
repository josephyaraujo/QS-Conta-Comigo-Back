CAMPOS_FORMULARIO_QUESTAO = (
    "formulario",
    "titulo_pergunta",
    "tipo_pergunta",
    "obrigatoriedade",
    "ordem",
)

CAMPOS_FORMULARIO_QUESTAO_COM_OPCOES = (
    "id",
    *CAMPOS_FORMULARIO_QUESTAO[1:],
    "opcoes",
)