# Views de autenticação
from .auth import LoginSuap, ExchangeSuapCode

# Views de usuários
from .usuarios import UsuarioViewSet, AlunoViewSet, AssistenteSocialViewSet

# Views de solicitações e benefícios
from .solicitacoes import SolicitacaoViewSet, BeneficioViewSet, AuxilioViewSet

# Views de formulários
from .formularios import (
    FormularioViewSet,
    FormularioQuestaoViewSet,
    FormularioQuestaoOpcaoViewSet,
    RespostaFormularioViewSet,
    RespostaQuestaoViewSet
)

# Views de chamados
from .chamados import ChamadoViewSet, ChamadoDetailViewSet

# Views de documentos
from .documentos import DocumentoViewSet

# Views de notificações

# Views de perguntas
from .perguntas import PerguntaViewSet

# Views de dashboard
from .dashboard import DashboardView

__all__ = [
    # Autenticação
    'LoginSuap',
    'ExchangeSuapCode',
    
    # Usuários
    'UsuarioViewSet',
    'AlunoViewSet',
    'AssistenteSocialViewSet',
    
    # Solicitações e benefícios
    'SolicitacaoViewSet',
    'BeneficioViewSet',
    'AuxilioViewSet',
    
    # Formulários
    'FormularioViewSet',
    'FormularioQuestaoViewSet',
    'FormularioQuestaoOpcaoViewSet',
    'RespostaFormularioViewSet',
    'RespostaQuestaoViewSet',
    
    # Outros
    'ChamadoViewSet',
    'ChamadoDetailViewSet',
    'DocumentoViewSet',
    'NotificacaoViewSet',
    'PerguntaViewSet',
    'DashboardView',
]