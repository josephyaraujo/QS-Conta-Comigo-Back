
class SolicitacaoEnum:
    SOLICITACAO = {
        "EM_ANALISE": 1,
        "DEFERIDO": 2,
        "INDEFERIDO": 99,
        "DEFERIDO_SEM_RECURSO": 3,   
        "FINALIZADO": 4,   
    }


class ChamadoStatusEnum:
    CHAMADO = {
        "EM_ANALISE": "em_analise",
        "CONCLUIDO": "concluido",
        "FECHADO": "fechado",
    }