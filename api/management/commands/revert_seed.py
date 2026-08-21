from django.core.management.base import BaseCommand
from api.models import (
    Usuario, Aluno, AssistenteSocial, Chamado, Formulario,
    FormularioQuestao, FormularioQuestaoOpcao, RespostaFormulario, RespostaQuestao,
    Documento, Pergunta, Notificacao, StatusSolicitacao, Solicitacao, Beneficio, Auxilio
)

class Command(BaseCommand):
    help = 'Remove os dados criados pela seed de desenvolvimento.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Revertendo dados da seed...'))

        # Remove notificações
        Notificacao.objects.all().delete()
        # Remove benefícios
        Beneficio.objects.all().delete()
        # Remove solicitações
        Solicitacao.objects.all().delete()
        # Remove perguntas
        Pergunta.objects.all().delete()
        # Remove formulários e suas questões/opções
        FormularioQuestaoOpcao.objects.all().delete()
        FormularioQuestao.objects.all().delete()
        Formulario.objects.all().delete()
        # Remove chamados
        Chamado.objects.all().delete()
        # Remove assistentes sociais
        AssistenteSocial.objects.all().delete()
        # Remove alunos
        Aluno.objects.all().delete()
        # Remove auxílios
        Auxilio.objects.all().delete()
        # Remove status de solicitação
        StatusSolicitacao.objects.all().delete()
        # Remove usuários criados pela seed (alunos e assistentes sociais)
        Usuario.objects.filter(username__in=[
            'joao.silva', 'maria.oliveira', 'pedro.santos', 'ana.costa', 'lucas.ferreira',
            'carla.mendes', 'roberto.lima'
        ]).delete()

        self.stdout.write(self.style.SUCCESS('Dados da seed revertidos com sucesso!'))
