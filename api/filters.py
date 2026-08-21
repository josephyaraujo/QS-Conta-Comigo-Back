from django_filters import rest_framework as filters
from .models import Formulario, Auxilio, Beneficio, Solicitacao


class FormularioFilter(filters.FilterSet):
    # Filtrar por id do auxílio alvo
    auxilio_alvo = filters.ModelChoiceFilter(field_name='auxilio_alvo', queryset=Auxilio.objects.all())

    # Filtrar por descrição do auxílio (ex.: 'auxilio transporte')
    auxilio_nome = filters.CharFilter(field_name='auxilio_alvo__nome', lookup_expr='icontains')

    # Filtrar pelo modo de solicitados (choices do campo solicitados)
    solicitados = filters.CharFilter(field_name='solicitados', lookup_expr='iexact')
    
    # Filtrar por status
    status = filters.CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = Formulario
        fields = ['solicitados', 'auxilio_alvo', 'auxilio_nome', 'data_inicio', 'data_fim', 'status']

class BeneficioFilter(filters.FilterSet):
    status = filters.CharFilter(field_name='status', lookup_expr='exact')
    matricula = filters.CharFilter(field_name='id_aluno__matricula', lookup_expr='icontains')
    campus = filters.CharFilter(field_name='id_aluno__campus', lookup_expr='icontains')
    nome_aluno = filters.CharFilter(field_name='id_aluno__usuario__nome_completo', lookup_expr='icontains')

    class Meta:
        model = Beneficio
        # deixamos fields vazio porque declaramos filtros manualmente
        fields = []


class SolicitacaoFilter(filters.FilterSet):
    status = filters.CharFilter(field_name='status', lookup_expr='exact')
    matricula = filters.CharFilter(field_name='id_aluno__matricula', lookup_expr='icontains')
    campus = filters.CharFilter(field_name='id_aluno__campus', lookup_expr='icontains')
    nome_aluno = filters.CharFilter(field_name='id_aluno__usuario__nome_completo', lookup_expr='icontains')

    class Meta:
        model = Solicitacao
        fields = []
