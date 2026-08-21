from rest_framework import serializers

# from api.serializers.chamados import DocumentoSerializer
from ..models import (
    Auxilio, Beneficio, Solicitacao, StatusSolicitacao
)

from ..serializers.base import AlunoSerializer
from .base import *
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
class AuxilioSerializer(serializers.ModelSerializer):
    qtd_participantes = serializers.SerializerMethodField()

    def get_qtd_participantes(self, obj):
       return Beneficio.objects.filter(tipo_auxilio=obj).count()
    class Meta:
        model = Auxilio
        fields =  [
            'id',
            'nome',
            'descricao',
            'campus',
            'qtd_participantes',
            'qtd_chamados',
            'impedir_aluno',
            'exigir_comprov',
            'exigir_frequen',
            'disponibilidade',
            'edital'
        ]

class AuxilioListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auxilio
        fields =  [
            'id',
            'nome',
        ]

class BeneficioCreateSerializer(serializers.ModelSerializer):
    aluno_id = serializers.IntegerField()
    solicitacao_id = serializers.IntegerField()

    class Meta:
        model = Beneficio
        fields = ['id', 'aluno_id', 'solicitacao_id', 'data_fim']

    def validate(self, attrs):
        if not Aluno.objects.filter(id=attrs['aluno_id']).exists():
            raise serializers.ValidationError({
                'aluno_id': 'Aluno não encontrado.'
            })

        if not Solicitacao.objects.filter(id=attrs['solicitacao_id']).exists():
            raise serializers.ValidationError({
                'solicitacao_id': 'Solicitação não encontrada.'
            })

        if attrs['data_fim'] < datetime.now().date():
            raise serializers.ValidationError({
                'data_fim': 'Data de fim não pode ser menor que hoje.'
            })

        return attrs
    
    def create(self, validated_data):
        solicitacao = Solicitacao.objects.get(id=validated_data['solicitacao_id'])
        tipo_auxilio = solicitacao.tipo_auxilio
        aluno = Aluno.objects.get(id=validated_data['aluno_id'])
        return Beneficio.objects.create(
            tipo_auxilio=tipo_auxilio,
            aluno=aluno,
            solicitacao=solicitacao,
            data_fim=validated_data['data_fim']
        )

class BeneficioSerializer(serializers.ModelSerializer):
    aluno = AlunoSerializer()
    motivo_entrada = serializers.SerializerMethodField()
    # documentos = serializers.SerializerMethodField()
    tipo_auxilio = serializers.SerializerMethodField()
    parecer = serializers.SerializerMethodField()

    def get_motivo_entrada(self, obj):
        return obj.solicitacao.descricao
    
    def get_tipo_auxilio(self,obj):
        return {
            'id' : obj.tipo_auxilio.id,
            'titulo': obj.tipo_auxilio.descricao,
        }
    
    def get_parecer(self, obj):
        return obj.solicitacao.status.descricao
    
    # def get_documentos(self, obj):
    #     documentos = DocumentoSerializer(obj.aluno.documentos, many=True).data
    #     return documentos
    
    class Meta:
        model = Beneficio
        fields = [
            'id',
            'aluno',
            'status',
            'tipo_auxilio',
            'data_inicio',
            'data_fim',
            'data_finalizacao',
            'justificativa_finalizacao',
            'motivo_entrada',
            'parecer',
            # 'documentos'
        ]

class BeneficioAlunoSerializer(serializers.ModelSerializer):
    titulo = serializers.CharField(source='tipo_auxilio.nome')
    
    class Meta:
        model = Beneficio
        fields = [
            'id',
            'status',
            'titulo',
            'data_inicio',
        ]



class SolicitacaoDetailsSerializer(serializers.ModelSerializer):
    id_aluno = AlunoSerializer(read_only = True)
    programa = serializers.CharField(source='tipo_auxilio.descricao', read_only=True)
    class Meta:
        model = Solicitacao
        fields = [
            'status',
            'descricao',
            'data_deferimento',
            'id_aluno',
            'programa'
        ]


class SolicitacaoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Solicitacao
        fields = [
            'descricao',
            'tipo_auxilio'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        aluno = Aluno.objects.filter(usuario=user).first()
        status = StatusSolicitacao.objects.get(codigo=1)
        return Solicitacao.objects.create(id_aluno=aluno, status=status, **validated_data)

class SolicitacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Solicitacao
        fields = [
            'status',
            'descricao',
            'data_deferimento',
            'id_aluno',
            'data_criacao',
            'id_assistente_social',
            'tipo_auxilio'
        ]
        

class RelatorioCreateSerializer(serializers.Serializer):

    class Meta:
        model =  Solicitacao
        fields = [
            'status',
            'descricao',
            'data_deferimento',
            'id_aluno',
            'data_criacao',
            'id_assistente_social',
            'tipo_auxilio'
        ]
        


class RelatorioSerializer(serializers.Serializer):
    ano = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    titulo = serializers.CharField(required=True)
    programa = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    situacao_sistemica = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    ingresso = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    curso = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    periodo_referencia = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    situacao_periodo = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    turno = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    formato_relatorio = serializers.CharField(required=True)

    def validate_ano(self, value):
        if value in [None, '', 'null']:
            return None
        try:
            ano = int(value)
            if ano < 2000 or ano > datetime.now().year:
                raise serializers.ValidationError("Ano inválido.")
            return ano
        except (ValueError, TypeError):
            raise serializers.ValidationError("Ano deve ser um número inteiro válido.")

    def validate_programa(self, value):
        if value in [None, '', 'null']:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            raise serializers.ValidationError("Programa deve ser um número inteiro válido.")

    def validate_curso(self, value):
        if value in [None, '', 'null']:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            raise serializers.ValidationError("Curso deve ser um número inteiro válido.")

    def validate_formato_relatorio(self, value):
        formatos_validos = ["pdf", "docx", "excel"]
        if value not in formatos_validos:
            raise serializers.ValidationError("Formato inválido.")
        return value

class RelatorioGeradoSerializer(serializers.ModelSerializer):
    aluno = AlunoSerializer()
    curso = serializers.CharField(source='aluno.curso')
    tipo_auxilio = serializers.SerializerMethodField()
    motivo_entrada = serializers.SerializerMethodField()
    parecer = serializers.SerializerMethodField()

    def get_tipo_auxilio(self, obj):
        return obj.tipo_auxilio.nome if obj.tipo_auxilio else None

    def get_motivo_entrada(self, obj):
        return obj.solicitacao.descricao if obj.solicitacao else None

    def get_parecer(self, obj):
        return obj.solicitacao.status.descricao if obj.solicitacao and obj.solicitacao.status else None

    class Meta:
        model = Beneficio
        fields = [
            'aluno',
            'status',
            'tipo_auxilio',
            'data_inicio',
            'data_fim',
            'motivo_entrada',
            'parecer',
            'curso'
        ]