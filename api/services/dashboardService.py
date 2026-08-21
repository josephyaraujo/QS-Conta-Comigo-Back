from django.db.models import Count, Q
from ..models import Auxilio, Solicitacao, Chamado, Pergunta, Documento, Aluno, Formulario
from django.utils import timezone
from datetime import timedelta

class DashboardService:
    
    @staticmethod
    def valor_percentual(semana_passada, atual):
        if semana_passada > 0:
            variacao = ((atual - semana_passada) / semana_passada) * 100
            return variacao
        elif atual > 0 and semana_passada == 0:
            return 100.0
        else:
            return 0.0
    
    @staticmethod
    def get_indicadores():
        hoje = timezone.now() 
        inicio_semana_atual = hoje - timedelta(days=7)
        inicio_semana_passada = hoje - timedelta(days=14)
        fim_semana_passada = inicio_semana_atual 
        
        raw_auxilios = (
            Auxilio.objects
            .annotate(
                calc_qtd_chamados=Count('chamados'),
                calc_qtd_participantes=Count('chamados__aluno', distinct=True)
            )
            .order_by('nome')
            .values('id', 'nome', 'calc_qtd_chamados', 'calc_qtd_participantes')
        )

        lista_indicadores_auxilio = [
            {
                'id': item['id'],
                'descricao': item['nome'],
                'qtd_chamados': item['calc_qtd_chamados'],      
                'qtd_participantes': item['calc_qtd_participantes']  
            }
            for item in raw_auxilios
        ]

        filtro_sol_pendente = Q(status__codigo=1) 
        
        agg_solicitacao = Solicitacao.objects.aggregate(
            total=Count('id', filter=filtro_sol_pendente),
            semana_atual=Count('id', 
                filter=filtro_sol_pendente & Q(data_criacao__gte=inicio_semana_atual)
            ),
            semana_passada=Count('id', 
                filter=filtro_sol_pendente & Q(data_criacao__gte=inicio_semana_passada, data_criacao__lt=fim_semana_passada)
            )
        )

        indicadores_solicitacao = {
            'solicitacoes_pendentes_total': agg_solicitacao['total'],
            'solicitacoes_pendentes_var_perc': DashboardService.valor_percentual(
                agg_solicitacao['semana_passada'], agg_solicitacao['semana_atual']
            )
        }

        filtro_chamado = Q(status="em_analise") 

        agg_chamado = Chamado.objects.aggregate(
            total=Count('id', filter=filtro_chamado),
            semana_atual=Count('id', 
                filter=filtro_chamado & Q(data_abertura__gte=inicio_semana_atual)
            ),
            semana_passada=Count('id', 
                filter=filtro_chamado & Q(data_abertura__gte=inicio_semana_passada, data_abertura__lt=fim_semana_passada)
            )
        )
        indicadores_chamado = {
            'total_chamados_total': agg_chamado['total'],
            'total_chamados_var_perc': DashboardService.valor_percentual(
                agg_chamado['semana_passada'], agg_chamado['semana_atual']
            )
        }

        agg_pergunta = Pergunta.objects.aggregate(
            total=Count('id'),
            semana_atual=Count('id', filter=Q(data_realizacao__gte=inicio_semana_atual)),
            semana_passada=Count('id', filter=Q(data_realizacao__gte=inicio_semana_passada, data_realizacao__lt=fim_semana_passada))
        )
        indicadores_pergunta = {
            'total_perguntas_total': agg_pergunta['total'],
            'total_perguntas_var_perc': DashboardService.valor_percentual(
                agg_pergunta['semana_passada'], agg_pergunta['semana_atual']
            )
        }
        
        alunos_trancados = Aluno.objects.aggregate(
            total_trancados=Count('id', filter=Q(status='trancado'))
        )
        
        try:
            data_corte = hoje.date().replace(year=hoje.year - 3)
        except ValueError:
            data_corte = hoje.date().replace(year=hoje.year - 3, day=28)
        
        documentacao_expirada = Documento.objects.aggregate(
            total_documentos=Count('id', filter=Q(data_criacao__lt=data_corte))
        )
        
        formularios_nao_respondidos = Formulario.objects.aggregate(
            total_formularios=Count('id', filter=Q(status='nao_respondido'))
        )

        indicadores_gerais = {
            **indicadores_solicitacao,
            **indicadores_chamado,
            **indicadores_pergunta,
            **alunos_trancados,
            **documentacao_expirada,
            **formularios_nao_respondidos,
        }
        
        data = {
            'auxilios': lista_indicadores_auxilio, 
            'indicadores_gerais': indicadores_gerais 
        }
        
        return data