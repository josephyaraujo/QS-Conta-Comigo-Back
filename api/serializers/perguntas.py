from rest_framework import serializers

from api.serializers.base import AlunoSerializer
from ..models import Pergunta

class PerguntaSerializer(serializers.ModelSerializer):
    aluno = AlunoSerializer(read_only=True)
    class Meta:
        model = Pergunta
        fields = (
            'id',
            'enunciado',
            'resposta',
            'status',
            'data_realizacao',
            'data_resposta',
            'assistente_social',
            'aluno'
        )
class PerguntaRespostaSerializer(serializers.ModelSerializer):
    enunciado = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    assistente_social = serializers.CharField(required=True)
    class Meta:
        model = Pergunta
        fields = (
            'id',
            'resposta',
            'enunciado',
            'status',
            'assistente_social',
        )


