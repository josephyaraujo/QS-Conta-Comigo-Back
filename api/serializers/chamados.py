from rest_framework import serializers
from ..models import Chamado, Chamado_chat, Documento, Auxilio, Aluno
from .base import AlunoSerializer, AlunoSimpleSerializer, UsuarioSerializer

class ChamadoSerializer(serializers.ModelSerializer):
    aluno = AlunoSerializer(read_only=True)
    assistente_social = UsuarioSerializer(source='assistente_social.usuario', read_only=True)
    class Meta:
        model = Chamado
        fields = [
            'id',
            'descricao',
            'tipo_de_chamado',
            'tipo_de_auxilio',
            'status',
            'data_abertura',
            'data_analise',
            'aluno',
            'assistente_social',
            'documentos',
            'justificativa_chamado'
        ]
        read_only_fields = ['aluno', 'assistente_social', 'data_abertura', 'status', 'documentos']
        
    def to_internal_value(self, data):
        data = data.copy()

        if 'tipo_de_auxilio' in data and isinstance(data['tipo_de_auxilio'], str):
            texto_recebido = data['tipo_de_auxilio']
            
            if texto_recebido.isdigit():
                pass 
            else:
                try:
                    auxilio = Auxilio.objects.get(descricao__iexact=texto_recebido)
                    data['tipo_de_auxilio'] = auxilio.id
                except Auxilio.DoesNotExist:
                    raise serializers.ValidationError({
                        "tipo_de_auxilio": f"O auxílio '{texto_recebido}' não foi encontrado no banco de dados."
                    })

        return super().to_internal_value(data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if instance.tipo_de_auxilio:
            representation['tipo_de_auxilio'] = instance.tipo_de_auxilio.nome
        
        return representation

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'


class DocumentoAlunoSerializer(serializers.ModelSerializer):
    aluno = AlunoSimpleSerializer()
    class Meta:
        model = Documento
        fields = (
            'id',
            'tipo_documento',
            'arquivo',
            'aluno',
            'data_criacao'
        )
class DocumentoCreateSerializer(serializers.ModelSerializer):
    aluno_id = serializers.IntegerField(write_only=True)
    tipo_documento = serializers.CharField(default="outros")
    arquivo = serializers.FileField(write_only=True)

    class Meta:
        model = Documento
        fields = ['id', 'aluno_id', 'arquivo', 'tipo_documento']

    def validate(self, attrs):
        if not Aluno.objects.filter(id=attrs['aluno_id']).exists():
            raise serializers.ValidationError({
                'aluno_id': 'Aluno não encontrado.'
            })
        return attrs

    def create(self, validated_data):
        aluno = Aluno.objects.get(id=validated_data['aluno_id'])

        return Documento.objects.create(
            aluno=aluno,
            tipo_documento=validated_data.get('tipo_documento', 'outros'),
            arquivo=validated_data['arquivo'] 
        )



class ChamadoChatCreateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if not attrs.get('mensagem') and not self.context['request'].FILES.get('arquivos'):
            raise serializers.ValidationError({
                'mensagem': 'A mensagem não pode ser vazia.'
            })
        return attrs  
    class Meta:
        model = Chamado_chat
        fields = [
            'chamado',
            'mensagem',
            'arquivo'
        ]

class ChamadoChatDetailSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
        
    class Meta:
        model = Chamado_chat
        fields = [
            'id',
            'chamado',
            'usuario',
            'mensagem',
            'arquivo',
            'data_envio',
            'lida',
        ]

class ChamadoEncerrarSerializer(serializers.Serializer):
    justificativa = serializers.CharField()



class ChamadoDetalheSerializer(serializers.ModelSerializer):
    aluno = AlunoSerializer(read_only=True)
    assistente_social = UsuarioSerializer(source='assistente_social.usuario', read_only=True)
    documentos = serializers.SerializerMethodField()
    tipo_de_auxilio = serializers.CharField(source='tipo_de_auxilio.nome', read_only=True)


    def get_documentos(self, obj):
        documentos = obj.documentos.filter(tipo_documento='anexo_chamado')
        return DocumentoSerializer(documentos, many=True).data

    class Meta:
        model = Chamado
        fields = [
            'id',
            'descricao',
            'tipo_de_chamado',
            'tipo_de_auxilio',
            'status',
            'data_abertura',
            'data_analise',
            'aluno',
            'assistente_social',
            'documentos',
            'justificativa_chamado'
        ]
        read_only_fields = ['aluno', 'assistente_social', 'data_abertura', 'status', 'documentos']
        