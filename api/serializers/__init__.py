# seu_app/serializers/__init__.py

# Importa de base.py
from .base import (
    UsuarioSerializer, 
    AlunoSerializer, 
    AssistenteSocialSerializer, 
    AlunoReadOnlySerializer,
    NotificacaoSerializer,
    AlunoPerfilSerializer
)

# Importa de chamados.py 
from .chamados import (
    ChamadoSerializer, 
    DocumentoSerializer, 
)

# Importa de auxilio_beneficio.py 
from .auxilio_beneficio import (
    AuxilioSerializer, 
    BeneficioSerializer,
    SolicitacaoDetailsSerializer,
    SolicitacaoCreateSerializer,
    SolicitacaoSerializer,
    BeneficioCreateSerializer
)

# Importa de formularios.py
from .formularios import (
    FormularioQuestaoOpcaoSerializer, 
    FormularioQuestaoSerializer, 
    FormularioSerializer
)

# Importa de respostas.py
from .respostas import (
    RespostaQuestaoCreateSerializer,
    RespostaFormularioCreateSerializer,
    RespostaFormularioReadOnlySerializer,
    RespostaQuestaoReadOnlySerializer
)

from .perguntas import PerguntaSerializer

# Opcional: Você pode definir __all__ para controle mais estrito (melhor prática)
__all__ = [
    'AlunoPerfilSerializer',
    'UsuarioSerializer', 'AlunoSerializer', 'AssistenteSocialSerializer', 'AlunoReadOnlySerializer',
    'ChamadoSerializer',
    'AuxilioSerializer', 'BeneficioSerializer', 'SolicitacaoDetailsSerializer',
    'FormularioQuestaoOpcaoSerializer', 'FormularioQuestaoSerializer', 'FormularioSerializer',
    'RespostaQuestaoCreateSerializer', 'RespostaQuestaoReadOnlySerializer', 'RespostaFormularioCreateSerializer', 'RespostaFormularioReadOnlySerializer',
    'DocumentoSerializer', 'NotificacaoSerializer', 'SolicitacaoSerializer', 'PerguntaSerializer', 'SolicitacaoCreateSerializer', 'SolicitacaoSerializer', 'BeneficioCreateSerializer'
]