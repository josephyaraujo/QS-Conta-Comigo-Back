from rest_framework import serializers
from ..models import (
    Aluno, Formulario, 
    FormularioQuestao, FormularioQuestaoOpcao, Auxilio
)
from .auxilio_beneficio import AuxilioSerializer
from .base import AlunoSerializer
from .respostas import RespostaFormularioReadOnlySerializer

from django.db import transaction

# ------- Serializers de Formulário e Questões -------
class FormularioQuestaoOpcaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormularioQuestaoOpcao
        fields = ['id', 'questao', 'alternativa']
        extra_kwargs = {
            'id': {'read_only': True},
            'questao': {'read_only': True},
        }

class FormularioQuestaoSerializer(serializers.ModelSerializer):
    formulario = serializers.PrimaryKeyRelatedField(
        queryset=Formulario.objects.all(),
        required=False,
        allow_null=True
    )
    
    opcoes = FormularioQuestaoOpcaoSerializer(many=True, required=False)

    class Meta:
        model = FormularioQuestao
        fields = ['id', 'formulario', 'titulo_pergunta', 'tipo_pergunta', 'obrigatoriedade', 'ordem', 'opcoes']
        extra_kwargs = {'id': {'read_only': True}}

# --- Formulario Serializer (Inclui tudo) ---

class FormularioSerializer(serializers.ModelSerializer):
    questoes = FormularioQuestaoSerializer(many=True)
    # Fonte: O related_name de RespostaFormulario para Formulario
    respostas = RespostaFormularioReadOnlySerializer(many=True, read_only=True, source='respostasformulario_set') 
    
    # Leitura: Retorna o objeto Auxilio
    auxilio_alvo = AuxilioSerializer(read_only=True)
    # Escrita: Recebe apenas o ID do Auxilio
    auxilio_alvo_id = serializers.PrimaryKeyRelatedField(
        queryset=Auxilio.objects.all(), 
        source='auxilio_alvo', 
        write_only=True, 
        required=False, 
        allow_null=True
    )

    alunos_selecionados = AlunoSerializer(many=True, read_only=True)
    # Escrita: Recebe a lista de IDs de alunos (para o M2M)
    alunos_selecionados_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Aluno.objects.all(), 
        source='alunos_selecionados', 
        write_only=True, 
        required=False
    )
    
    # Campo apenas de leitura para o frontend exibir
    modo_envio_display = serializers.CharField(source='get_solicitados_display', read_only=True)

    class Meta:
        model = Formulario
        fields = [
            'id', 'titulo', 'objetivo', 
            'solicitados', 'modo_envio_display',
            'auxilio_alvo', 'auxilio_alvo_id', 
            'alunos_selecionados', 'alunos_selecionados_ids',
            'data_inicio', 'data_fim', 'alunos_solicitados', 
            'status',
            'questoes', 'respostas'
        ]
        read_only_fields = ['alunos_solicitados']

    # Sobrescrever CREATE para lidar com aninhamento de Questões/Opções
    @transaction.atomic
    def create(self, validated_data):
        questoes_data = validated_data.pop('questoes', [])
        alunos_selecionados = validated_data.pop('alunos_selecionados', []) 
        
        # Crio o formulário
        formulario = Formulario.objects.create(**validated_data)
        
        # Adiciono os alunos selecionados (M2M)
        if alunos_selecionados:
            formulario.alunos_selecionados.set(alunos_selecionados)

        # Crio as questões e opções aninhadas
        for ordem, questao_data in enumerate(questoes_data, 1):
            opcoes_data = questao_data.pop('opcoes', [])
            # Injeto a ordem, garantindo que as questões sigam a ordem do array
            questao = FormularioQuestao.objects.create(formulario=formulario, ordem=ordem, **questao_data)
            for opcao_data in opcoes_data:
                FormularioQuestaoOpcao.objects.create(questao=questao, **opcao_data)
        
        return formulario
    
    # Sobrescrever UPDATE para lidar com aninhamento de Questões/Opções
    @transaction.atomic
    def update(self, instance, validated_data):
        questoes_data = validated_data.pop('questoes', None)
        alunos_selecionados = validated_data.pop('alunos_selecionados', None)
        print("entrou no update")
        
        # Atualiza campos simples do formulário
        for attr, value in validated_data.items():
            print(f"{attr}: {value}")
            setattr(instance, attr, value)
        instance.save()
        
        # Atualiza alunos selecionados (M2M) se fornecido
        if alunos_selecionados is not None:
            instance.alunos_selecionados.set(alunos_selecionados)
        
        # Atualiza questões se fornecidas
        if questoes_data is not None:
            # Remove questões antigas
            instance.questoes.all().delete()
            
            # Recria questões e opções
            for ordem, questao_data in enumerate(questoes_data, 1):
                opcoes_data = questao_data.pop('opcoes', [])
                questao = FormularioQuestao.objects.create(
                    formulario=instance, 
                    ordem=ordem, 
                    **questao_data
                )
                for opcao_data in opcoes_data:
                    FormularioQuestaoOpcao.objects.create(questao=questao, **opcao_data)
        
        return instance
