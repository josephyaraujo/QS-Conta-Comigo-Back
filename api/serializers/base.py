from jsonschema import ValidationError
from rest_framework import serializers

from ..models import (
    Usuario, Aluno, AssistenteSocial, Notificacao, FormularioQuestao, Documento, Cursos, FormularioQuestaoOpcao
)
from django.apps import apps

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'email',
            'nome_completo',
            'tipo'
        ]

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'

class AlunoSerializer(serializers.ModelSerializer):
    documentos = serializers.SerializerMethodField()
    matricula = serializers.CharField(
        min_length=14,
        max_length=14,
        error_messages={
            'min_length': 'A matrícula do aluno deve ter 14 dígitos.',
            'max_length': 'A matrícula do aluno deve ter 14 dígitos.',
        }
    )
    
    def get_documentos(self, obj):
        documentos = DocumentoSerializer(obj.documentos_criados, many=True).data
        return documentos
    
    def validate(self, attrs):  
        instance = Aluno(**attrs)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return attrs

    class Meta:
        model = Aluno
        fields = (
            'id',
            'full_name',
            'usuario',
            'matricula',
            'cpf',
            'curso',
            'periodo',
            'status',
            'campus',
            'ingresso',
            'qtd_periodos',
            'documentos'
        )

class AlunoSimpleSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source = 'usuario.nome_completo')
    class Meta:
        model = Aluno
        fields = (
            'id',
            'nome',
            'matricula'
        )

class UsuarioAuthSerializer(serializers.Serializer):
    usuario = serializers.CharField()
    matricula = serializers.CharField()
    tipo_usuario = serializers.CharField()

class AssistenteSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistenteSocial
        fields = '__all__'

#serializer pra usar no perfil do aluno juntando usuario e aluno
class AlunoPerfilSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()  # Serializador aninhado para o usuário

    class Meta:
        model = Aluno
        fields = '__all__'

class AlunoReadOnlySerializer(serializers.ModelSerializer):
    # Acessa o nome completo do usuário relacionado ao Aluno
    nome_completo = serializers.CharField(source='usuario.nome_completo', read_only=True)
    
    class Meta:
        model = Aluno
        fields = ['matricula', 'curso', 'nome_completo']

class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = '__all__'

class FormularioQuestaoOpcaoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('api', 'FormularioQuestaoOpcao')  # Import será feito dinamicamente
        fields = ['id', 'alternativa']

class FormularioQuestaoSimpleSerializer(serializers.ModelSerializer):
    opcoes = serializers.SerializerMethodField()
    
    def get_opcoes(self, obj):
        opcoes = obj.opcoes.all()
        return [{'id': opcao.id, 'alternativa': opcao.alternativa} for opcao in opcoes]
    
    class Meta:
        model = FormularioQuestao
        fields = ['id', 'titulo_pergunta', 'tipo_pergunta', 'obrigatoriedade', 'ordem', 'opcoes']
        
class CursoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cursos
        fields = ['id', 'nome']


class AlunoChamadoSerializer(serializers.ModelSerializer):
    documentos = serializers.SerializerMethodField()
    def validate(self, attrs):  
        instance = Aluno(**attrs)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return attrs
    
    def get_documentos(self, obj):
        documentos = obj.documentos.filter(tipo_documento='anexo_chamado')
        return DocumentoSerializer(documentos, many=True).data

    class Meta:
        model = Aluno
        fields = (
            'id',
            'full_name',
            'usuario',
            'matricula',
            'cpf',
            'curso',
            'periodo',
            'status',
            'campus',
            'ingresso',
            'qtd_periodos',
            'documentos',
        )