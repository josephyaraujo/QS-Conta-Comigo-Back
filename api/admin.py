from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import (
    Usuario, Aluno, AssistenteSocial, Chamado, Formulario, 
    FormularioQuestao, FormularioQuestaoOpcao, RespostaFormulario, RespostaQuestao,
    Documento, Pergunta, Notificacao, Solicitacao, Beneficio, Auxilio, StatusSolicitacao
)
from django.contrib.admin.sites import AlreadyRegistered

# Configurações comuns para reutilização
class BaseAdmin(admin.ModelAdmin):
    search_fields = ()
    list_filter = ()
    raw_id_fields = ()
    date_hierarchy = None

# Formulários personalizados para o modelo de usuário
# class CustomUsuarioCreationForm(UserCreationForm):
#     class Meta:
#         model = Usuario
#         fields = ('username', 'email', 'nome')

# class CustomUsuarioChangeForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'nome', 'is_staff', 'is_active')

# # Configuração para o modelo de usuário
# class UsuarioAdmin(UserAdmin):
#     add_form = CustomUsuarioCreationForm
#     form = CustomUsuarioChangeForm
#     model = Usuario
#     list_display = ('username', 'email', 'nome', 'is_staff')
#     search_fields = ('username', 'nome', 'email')
#     list_filter = ('is_staff', 'is_superuser')
#     ordering = ('nome',)

#     # Campos exibidos ao editar um usuário
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Informações pessoais', {'fields': ('nome', 'email')}),
#         ('Permissões', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
#         ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
#     )

#     # Campos exibidos ao criar um novo usuário
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2', 'nome', 'email', 'is_staff', 'is_active')}
#         ),
#     )

# Configuração para o modelo de Aluno
class AlunoAdmin(BaseAdmin):
    list_display = ('id','matricula', 'usuario', 'curso', 'periodo', 'status')
    search_fields = ('matricula', 'usuario__nome', 'cpf')
    list_filter = ('curso', 'periodo', 'status')
    raw_id_fields = ('usuario',)

# Configuração para o modelo de Assistente Social
class AssistenteSocialAdmin(BaseAdmin):
    list_display = ('id','matricula', 'usuario')
    search_fields = ('matricula', 'usuario__nome')
    raw_id_fields = ('usuario',)

# Configuração para o modelo de Chamado
class ChamadoAdmin(BaseAdmin):
    date_hierarchy = 'data_abertura'
    list_display = ('id', 'aluno', 'tipo_de_chamado', 'data_abertura', 'status', 'assistente_social')
    list_filter = ('tipo_de_chamado', 'status')
    search_fields = ('aluno__usuario__nome', 'descricao')
    autocomplete_fields = ('aluno', 'assistente_social')

# Inline para FormularioQuestao
class FormularioQuestaoInline(admin.TabularInline):
    model = FormularioQuestao
    extra = 1

# Configuração para o modelo de Formulario
class FormularioAdmin(BaseAdmin):
    date_hierarchy = 'data_inicio'
    list_display = ('titulo', 'auxilio_alvo', 'data_inicio', 'data_fim')
    list_filter = ('auxilio_alvo', 'solicitados')
    search_fields = ('titulo', 'objetivo')
    inlines = [FormularioQuestaoInline]

# Configuração para o modelo de FormularioQuestao
class FormularioQuestaoAdmin(BaseAdmin):
    list_display = ('formulario', 'titulo_pergunta', 'tipo_pergunta', 'obrigatoriedade', 'ordem')
    list_filter = ('tipo_pergunta', 'obrigatoriedade')
    search_fields = ('titulo_pergunta',)
    list_editable = ('ordem',)

# Configuração para o modelo de FormularioQuestaoOpcao
class FormularioQuestaoOpcaoAdmin(BaseAdmin):
    list_display = ('questao', 'alternativa')
    search_fields = ('alternativa', 'questao__titulo_pergunta')

# Configuração para o modelo de RespostaFormulario
class RespostaFormularioAdmin(BaseAdmin):
    list_display = ('formulario', 'aluno', 'data_resposta', 'completo')
    list_filter = ('formulario', 'completo')
    search_fields = ('aluno__usuario__nome', 'formulario__titulo')
    raw_id_fields = ('aluno', 'formulario')

# Configuração para o modelo de RespostaQuestao
class RespostaQuestaoAdmin(BaseAdmin):
    list_display = ('resposta_formulario', 'questao', 'opcao_escolhida')
    search_fields = ('questao__titulo_pergunta', 'resposta_aberta')
    raw_id_fields = ('resposta_formulario', 'questao', 'opcao_escolhida')

# Configuração para o modelo de Documento
class DocumentoAdmin(BaseAdmin):
    list_display = ('tipo_documento', 'aluno', 'solicitacao')
    list_filter = ('tipo_documento',)
    raw_id_fields = ('aluno', 'solicitacao')

# Configuração para o modelo de Pergunta
class PerguntaAdmin(BaseAdmin):
    list_display = ('enunciado', 'status', 'data_realizacao', 'assistente_social')
    list_filter = ('status',)
    search_fields = ('enunciado', 'resposta')
class BeneficioAdmin(BaseAdmin):
    list_display = ('aluno', 'solicitacao')
    # list_filter = ('status',)
    # search_fields = ('enunciado', 'resposta')

# Configuração para o modelo de Notificacao
class NotificacaoAdmin(BaseAdmin):
    date_hierarchy = 'data_envio'
    list_display = ('titulo', 'mensagem', 'status', 'data_envio')
    list_filter = ('status',)
    search_fields = ('mensagem', 'destinatario')
# # Configuração para o modelo de Solicitacao
class SolicitacaoAdmin(BaseAdmin):
    date_hierarchy = 'data_criacao'
    list_display = ('get_aluno_matricula', 'get_tipo_auxilio_nome', 'status', 'data_criacao')
    list_filter = ('status', 'tipo_auxilio')
    search_fields = ('id_aluno__usuario__nome_completo', 'descricao')
    autocomplete_fields = ('id_aluno', 'tipo_auxilio', 'id_assistente_social')

    @admin.display(description='Matrícula do Aluno')
    def get_aluno_matricula(self, obj):
        return obj.id_aluno.matricula if obj.id_aluno else '-'

    @admin.display(description='Tipo de Auxílio')
    def get_tipo_auxilio_nome(self, obj):
        return obj.tipo_auxilio.nome if obj.tipo_auxilio else '-'

# Configuração para o modelo de Auxilio
class AuxilioAdmin(BaseAdmin):
    list_display = ('id', 'disponibilidade', 'edital')
    list_filter = ('disponibilidade',)
    search_fields = ('edital',)

class UsuarioAdmin(BaseAdmin):
    list_display = ('id','nome_completo',)
    list_filter = ('nome_completo',)


# Registro dos modelos no admin
admin.site.register(Usuario, UsuarioAdmin)
try:
    admin.site.register(Aluno, AlunoAdmin
                        )
except AlreadyRegistered:
    pass
admin.site.register(AssistenteSocial, AssistenteSocialAdmin)
admin.site.register(Chamado, ChamadoAdmin)
admin.site.register(Formulario, FormularioAdmin)
admin.site.register(FormularioQuestao, FormularioQuestaoAdmin)
admin.site.register(FormularioQuestaoOpcao, FormularioQuestaoOpcaoAdmin)
admin.site.register(RespostaFormulario, RespostaFormularioAdmin)
admin.site.register(RespostaQuestao, RespostaQuestaoAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Pergunta, PerguntaAdmin)
admin.site.register(Notificacao, NotificacaoAdmin)
admin.site.register(Solicitacao, SolicitacaoAdmin)
admin.site.register(Beneficio, BeneficioAdmin)
admin.site.register(Auxilio, AuxilioAdmin)
admin.site.register(StatusSolicitacao)
