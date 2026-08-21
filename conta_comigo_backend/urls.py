from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny
# from .views import api_root
from api.views import auth, chamados, dashboard, documentos, formularios, listagem, notificacoes, perguntas, relatorio,solicitacoes, usuarios, relatorio
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Conta Comigo API",
        default_version='v2',
        description="Conta Comigo API with Swagger",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,  # mantém a documentação visível
        permission_classes=(AllowAny,),  # não esconde os endpoints
    authentication_classes=[],  # não usa login do Django admin
)


router = DefaultRouter()
router.register(r'usuarios', usuarios.UsuarioViewSet)
router.register(r'alunos', usuarios.AlunoViewSet)
router.register(r'auxilios', solicitacoes.AuxilioViewSet)
router.register(r'beneficios', solicitacoes.BeneficioViewSet)
router.register(r'documentos', documentos.DocumentoViewSet)
router.register(r'solicitacoes', solicitacoes.SolicitacaoViewSet)
router.register(r'perguntas', perguntas.PerguntaViewSet)
router.register(r'chamados', chamados.ChamadoViewSet)
router.register(r'chamados_chat', chamados.ChamadoDetailViewSet)
router.register(r'formularios', formularios.FormularioViewSet)
router.register(r'formulario_questao', formularios.FormularioQuestaoViewSet)
router.register(r'formulario_questao_opcao', formularios.FormularioQuestaoOpcaoViewSet)
router.register(r'resposta_formulario', formularios.RespostaFormularioViewSet)
router.register(r'resposta_questao', formularios.RespostaQuestaoViewSet)
router.register(r'cursos', listagem.CursosViewSet)
router.register(r'perfil_aluno', usuarios.PerfilAlunoViewSet, basename='perfil_aluno')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("api/auth/login/", auth.LoginSuap.as_view(), name="auth-login-suap"),
    path("api/auth/exchange/", auth.ExchangeSuapCode.as_view(), name="auth-exchange-suap"),
    path('api/dashboard/', dashboard.DashboardView.as_view(), name='dashboard-indicadores'),
    path('api/auxilios/list/', solicitacoes.AuxilioListView.as_view(), name='auxilio-list'),
    path('api/relatorio/', relatorio.RelatorioView.as_view(), name='relatorio'),
    path('api/notificacoes/', notificacoes.NotificacaoView.as_view(), name='notificacoes'),
    path('api/notificacoes/<int:pk>/', notificacoes.NotificacaoView.as_view(), name='notificacoes-detail'),
    path('api/', include(router.urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
