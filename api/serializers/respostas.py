from rest_framework import serializers
from ..models import (
    RespostaQuestao, FormularioQuestao, RespostaFormulario, Formulario
)
from .base import FormularioQuestaoSimpleSerializer
from .base import AlunoReadOnlySerializer
from django.utils import timezone

class RespostaQuestaoCreateSerializer(serializers.ModelSerializer):
    # O ID da questão é recebido para que a validação possa buscar o TIPO da pergunta
    questao_id = serializers.IntegerField(write_only=True) 

    class Meta:
        model = RespostaQuestao
        fields = ['questao_id', 'opcao_escolhida', 'resposta_aberta'] 

    # Implementação da Validação de Regra de Negócio (Texto vs Opções)
    def validate(self, data):
        questao_id = data.get('questao_id')
        opcao_escolhida = data.get('opcao_escolhida')
        resposta_aberta = data.get('resposta_aberta')

        try:
            questao = FormularioQuestao.objects.get(pk=questao_id)
        except FormularioQuestao.DoesNotExist:
            raise serializers.ValidationError({"questao_id": "Questão do formulário não encontrada."})
            
        tipo_pergunta = questao.tipo_pergunta

        if tipo_pergunta == 'paragrafo':
            if not resposta_aberta:
                raise serializers.ValidationError(
                    {"resposta_aberta": "Este campo é obrigatório para perguntas de parágrafo."},
                    code='required'
                )

        elif tipo_pergunta in ['multipla_escolha', 'caixa_selecao']:
            if not opcao_escolhida:
                raise serializers.ValidationError(
                    {"opcao_escolhida": "É necessário selecionar uma opção para este tipo de pergunta."},
                    code='required'
                )
            
            
            if opcao_escolhida and opcao_escolhida.questao.id != questao_id:
                 raise serializers.ValidationError(
                    {"opcao_escolhida": "A opção escolhida não pertence à questão fornecida."},
                    code='option_mismatch'
                )

        # 4. Adiciona o objeto Questão validado para uso na View/Create
        data['questao'] = questao 
        return data

class RespostaQuestaoReadOnlySerializer(serializers.ModelSerializer):
    """ Serializer de LEITURA para uma Resposta de Questão individual. """
    # 1. Informações da Questão (para saber o que foi respondido)
    questao_info = FormularioQuestaoSimpleSerializer(source='questao', read_only=True)
    
    # 2. Alternativa escolhida (se for múltipla escolha/seleção)
    opcao_alternativa = serializers.CharField(source='opcao_escolhida.alternativa', read_only=True, allow_null=True)

    class Meta:
        model = RespostaQuestao
        fields = ['id', 'questao_info', 'opcao_alternativa', 'resposta_aberta']


class RespostaFormularioReadOnlySerializer(serializers.ModelSerializer):
    """ Serializer de LEITURA para um RespostaFormulario (usado no FormularioSerializer). """
    aluno_info = AlunoReadOnlySerializer(source='aluno', read_only=True)
    
    respostas_questoes = RespostaQuestaoReadOnlySerializer(many=True, read_only=True)

    class Meta:
        model = RespostaFormulario
        fields = ['id', 'aluno_info', 'data_resposta', 'completo', 'respostas_questoes']

class RespostaFormularioCreateSerializer(serializers.ModelSerializer):
    """ Serializer de ESCRITA usado pelo Aluno para submeter todas as respostas. """
    
    formulario_id = serializers.IntegerField(write_only=True, required=True)
    
    respostas_questoes = RespostaQuestaoCreateSerializer(many=True, write_only=True) 

    class Meta:
        model = RespostaFormulario
        # Inclui apenas campos que o aluno envia. O 'aluno' e 'formulario' são injetados na View.
        fields = ['formulario_id', 'respostas_questoes', 'completo'] 
        read_only_fields = ['data_resposta']

    # Método de validação extra para garantir que o Formulario ID existe
    def validate_formulario_id(self, value):
        try:
            Formulario.objects.get(pk=value)
        except Formulario.DoesNotExist:
            raise serializers.ValidationError("Formulário não encontrado.")
        return value
    
    def create(self, validated_data):
        from django.db import transaction
        
        formulario_id = validated_data.pop('formulario_id')
        respostas_questoes_data = validated_data.pop('respostas_questoes', [])
        
        # Pega o aluno do contexto (injetado pela view)
        aluno = self.context.get('aluno')
        if not aluno:
            raise serializers.ValidationError("Aluno não identificado no contexto.")
        
        formulario = Formulario.objects.get(pk=formulario_id)
        
        with transaction.atomic():
            # Cria ou atualiza a RespostaFormulario
            resposta_formulario, created = RespostaFormulario.objects.get_or_create(
                formulario=formulario,
                aluno=aluno,
                defaults={'completo': validated_data.get('completo', False)}
            )
            
            # Se já existia, atualiza o campo completo
            if not created:
                completo = validated_data.get('completo', resposta_formulario.completo)

                resposta_formulario.completo = completo

                if completo:
                    resposta_formulario.data_resposta = timezone.now()
                resposta_formulario.save()
            
            # Remove respostas antigas se estiver reenviando
            RespostaQuestao.objects.filter(resposta_formulario=resposta_formulario).delete()
            
            # Cria as respostas das questões
            for resposta_questao_data in respostas_questoes_data:
                questao = resposta_questao_data.pop('questao')
                RespostaQuestao.objects.create(
                    resposta_formulario=resposta_formulario,
                    questao=questao,
                    **resposta_questao_data
                )
        
        return resposta_formulario
        