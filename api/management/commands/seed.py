from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from api.models import (
    Usuario, Aluno, AssistenteSocial, Chamado, Formulario,
    FormularioQuestao, FormularioQuestaoOpcao, RespostaFormulario, RespostaQuestao,
    Documento, Pergunta, Notificacao, StatusSolicitacao, Solicitacao, Beneficio, Auxilio
)


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais para desenvolvimento'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Iniciando seed do banco de dados...'))
        
        self.create_usuarios()
        self.create_status_solicitacao()
        self.create_auxilios()
        self.create_alunos()
        self.create_assistentes_sociais()
        self.create_chamados()
        self.create_formularios()
        self.create_perguntas()
        self.create_solicitacoes()
        self.create_beneficios()
        self.create_notificacoes()
        
        self.stdout.write(self.style.SUCCESS('Seed concluído com sucesso!'))

    def create_usuarios(self):
        self.stdout.write('Criando usuários...')
        
        # Usuários para alunos
        self.aluno_users = []
        alunos_data = [
            ('joao.silva', 'João Pedro Silva Santos', 'joao.silva@escolar.ifrn.edu.br'),
            ('maria.oliveira', 'Maria Eduarda Oliveira Lima', 'maria.oliveira@escolar.ifrn.edu.br'),
            ('pedro.santos', 'Pedro Henrique Santos Costa', 'pedro.santos@escolar.ifrn.edu.br'),
            ('ana.costa', 'Ana Carolina Costa Ferreira', 'ana.costa@escolar.ifrn.edu.br'),
            ('lucas.ferreira', 'Lucas Gabriel Ferreira Souza', 'lucas.ferreira@escolar.ifrn.edu.br'),
        ]
        
        for username, nome, email in alunos_data:
            user, _ = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    'nome_completo': nome,
                    'email': email,
                }
            )
            user.set_password('aluno123')
            user.save()
            self.aluno_users.append(user)

        # Usuários para assistentes sociais
        self.as_users = []
        as_data = [
            ('carla.mendes', 'Carla Regina Mendes Almeida', 'carla.mendes@ifrn.edu.br'),
            ('roberto.lima', 'Roberto Carlos Lima Pereira', 'roberto.lima@ifrn.edu.br'),
        ]
        
        for username, nome, email in as_data:
            user, _ = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    'nome_completo': nome,
                    'email': email,
                    'is_staff': True,
                }
            )
            user.set_password('as123456')
            user.save()
            self.as_users.append(user)

        self.stdout.write(self.style.SUCCESS(f'  ✓ {Usuario.objects.count()} usuários criados'))

    def create_status_solicitacao(self):
        self.stdout.write('Criando status de solicitação...')
        
        status_data = [
            {'codigo': 1, 'descricao': 'Em análise', 'ordem': 1},
            {'codigo': 2, 'descricao': 'Deferido sem recurso', 'ordem': 3},
            {'codigo': 3, 'descricao': 'Deferido', 'ordem': 2},
            {'codigo': 4, 'descricao': 'Indeferido', 'ordem': 99},
            {'codigo': 5, 'descricao': 'Finalizado', 'ordem': 4},
        ]
        self.status_list = []
        for data in status_data:
            status, _ = StatusSolicitacao.objects.get_or_create(
                codigo=data['codigo'],
                defaults={'descricao': data['descricao'], 'ordem': data['ordem']}
            )
            self.status_list.append(status)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {StatusSolicitacao.objects.count()} status criados'))

    def create_auxilios(self):
        self.stdout.write('Criando auxílios...')
        
        auxilios_data = [
            {
                'nome': 'Auxílio Transporte',
                'descricao': 'Oferece suporte financeiro para custear despesas com deslocamento do estudante entre sua residência e o campus, garantindo o acesso e a permanência nas atividades acadêmicas.',
                'disponibilidade': True,
                'edital': 'Edital 01/2026 - Auxílio Transporte',
                'exigir_frequen': True,
                'exigir_comprov': True,
            },
            {
                'nome': 'Auxílio Moradia',
                'descricao': 'Concede apoio financeiro a estudantes que necessitam residir fora de seu domicílio de origem para frequentar o IFRN, auxiliando nos custos com moradia durante o período de estudos.',
                'disponibilidade': True,
                'edital': 'Edital 02/2026 - Auxílio Moradia',
                'exigir_frequen': True,
                'exigir_comprov': True,
            },
            {
                'nome': 'Auxílio Alimentação',
                'descricao': 'Destinado a contribuir com as despesas alimentares do estudante, assegurando condições adequadas de permanência e aproveitamento acadêmico durante o período letivo.',
                'disponibilidade': True,
                'edital': 'Edital 03/2026 - Auxílio Alimentação Estudantil',
                'exigir_frequen': True,
                'exigir_comprov': False,
            },
            {
                'nome': 'Apoio Formação Estudantil',
                'descricao': 'Visa apoiar financeiramente estudantes em atividades relacionadas à formação acadêmica, como aquisição de materiais didáticos, participação em eventos, cursos, projetos ou outras ações que contribuam para o desenvolvimento educacional.',
                'disponibilidade': False,
                'edital': None,
                'exigir_frequen': False,
                'exigir_comprov': False,
            },
            {
                'nome': 'Auxílios Eventuais',
                'descricao': 'Destinados a atender situações emergenciais e imprevistas que possam comprometer a permanência do estudante no IFRN, mediante avaliação socioeconômica.',
                'disponibilidade': True,
                'edital': 'Edital 05/2026 - Auxílios Eventuais',
                'exigir_frequen': True,
                'exigir_comprov': True,
            },
            {
                'nome': 'Cursos de Idiomas',
                'descricao': 'Concede apoio financeiro para participação em cursos de idiomas, contribuindo para a ampliação da formação acadêmica, cultural e profissional do estudante.',
                'disponibilidade': True,
                'edital': 'Edital 06/2026 - Cursos de Idiomas',
                'exigir_frequen': True,
                'exigir_comprov': True,
            },
        ]
        
        self.auxilios = []
        for data in auxilios_data:
            auxilio, _ = Auxilio.objects.get_or_create(
                nome=data['nome'],
                defaults=data
            )
            self.auxilios.append(auxilio)
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ {Auxilio.objects.count()} auxílios criados'))

    def create_alunos(self):
        self.stdout.write('Criando alunos...')
        
        alunos_data = [
            ('20231014010001', '12345678901', 'tecnologia_ads', 3, 'Ativo'),
            ('20231014010002', '12345678902', 'informatica_internet', 2, 'Ativo'),
            ('20231014010003', '12345678903', 'engenharia_civil', 4, 'Ativo'),
            ('20231014010004', '12345678904', 'administracao', 1, 'Ativo'),
            ('20231014010005', '12345678905', 'eletrotecnica', 3, 'Trancado'),
        ]
        
        self.alunos = []
        for i, (matricula, cpf, curso, periodo, status) in enumerate(alunos_data):
            aluno, _ = Aluno.objects.get_or_create(
                matricula=matricula,
                defaults={
                    'usuario': self.aluno_users[i],
                    'cpf': cpf,
                    'curso': curso,
                    'periodo': periodo,
                    'status': status,
                    'campus': 'Natal-Central',
                }
            )
            self.alunos.append(aluno)
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ {Aluno.objects.count()} alunos criados'))

    def create_assistentes_sociais(self):
        self.stdout.write('Criando assistentes sociais...')
        
        as_data = [
            ('1234567',),
            ('7654321',),
        ]
        
        self.assistentes = []
        for i, (matricula,) in enumerate(as_data):
            assistente, _ = AssistenteSocial.objects.get_or_create(
                matricula=matricula,
                defaults={'usuario': self.as_users[i]}
            )
            self.assistentes.append(assistente)
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ {AssistenteSocial.objects.count()} assistentes sociais criados'))

    def create_chamados(self):
        self.stdout.write('Criando chamados...')
        
        chamados_data = [
            {
                'descricao': 'Solicito alteração do comprovante de residência enviado anteriormente.',
                'tipo_de_chamado': 'alteracao_documentos',
                'tipo_de_auxilio': self.auxilios[0], # auxilio_transporte
                'status': 'em_analise',
                'aluno': self.alunos[0],
                'assistente_social': self.assistentes[0],
            },
            {
                'descricao': 'Preciso enviar documentos pendentes referentes ao auxílio moradia.',
                'tipo_de_chamado': 'arquivos_pendentes',
                'tipo_de_auxilio': self.auxilios[1], # auxilio_moradia
                'status': 'em_analise',
                'aluno': self.alunos[1],
                'assistente_social': self.assistentes[0],
            },
            {
                'descricao': 'Justificativa de falta no dia 15/01/2026 por motivo de saúde.',
                'tipo_de_chamado': 'justificacao',
                'tipo_de_auxilio': self.auxilios[2], # alimentacao_estudantil
                'status': 'concluido',
                'aluno': self.alunos[2],
                'assistente_social': self.assistentes[1],
            },
        ]
        for data in chamados_data:
            Chamado.objects.get_or_create(
                descricao=data['descricao'],
                aluno=data['aluno'],
                defaults=data
            )
        self.stdout.write(self.style.SUCCESS(f'  ✓ {Chamado.objects.count()} chamados criados'))

    def create_formularios(self):
        self.stdout.write('Criando formulários...')
        
        hoje = timezone.now().date()
        
        # Formulário 1 - Aberto
        form1, created = Formulario.objects.get_or_create(
            titulo='Pesquisa de Satisfação - Auxílio Transporte 2026',
            defaults={
                'objetivo': 'Avaliar a satisfação dos alunos beneficiários do auxílio transporte.',
                'solicitados': 'auxilio',
                'auxilio_alvo': self.auxilios[0],
                'data_inicio': hoje - timedelta(days=5),
                'data_fim': hoje + timedelta(days=25),
                'status': 'aberto',
            }
        )
        
        if created:
            # Questões do formulário 1
            q1 = FormularioQuestao.objects.create(
                formulario=form1,
                titulo_pergunta='Como você avalia o valor do auxílio transporte?',
                tipo_pergunta='multipla_escolha',
                obrigatoriedade=True,
                ordem=1
            )
            FormularioQuestaoOpcao.objects.bulk_create([
                FormularioQuestaoOpcao(questao=q1, alternativa='Excelente'),
                FormularioQuestaoOpcao(questao=q1, alternativa='Bom'),
                FormularioQuestaoOpcao(questao=q1, alternativa='Regular'),
                FormularioQuestaoOpcao(questao=q1, alternativa='Ruim'),
            ])
            
            q2 = FormularioQuestao.objects.create(
                formulario=form1,
                titulo_pergunta='O auxílio cobre suas despesas de transporte?',
                tipo_pergunta='multipla_escolha',
                obrigatoriedade=True,
                ordem=2
            )
            FormularioQuestaoOpcao.objects.bulk_create([
                FormularioQuestaoOpcao(questao=q2, alternativa='Sim, completamente'),
                FormularioQuestaoOpcao(questao=q2, alternativa='Sim, parcialmente'),
                FormularioQuestaoOpcao(questao=q2, alternativa='Não'),
            ])
            
            q3 = FormularioQuestao.objects.create(
                formulario=form1,
                titulo_pergunta='Deixe suas sugestões ou comentários:',
                tipo_pergunta='paragrafo',
                obrigatoriedade=False,
                ordem=3
            )

        # Formulário 2 - Rascunho
        form2, created = Formulario.objects.get_or_create(
            titulo='Levantamento Socioeconômico 2026.1',
            defaults={
                'objetivo': 'Coletar informações socioeconômicas dos estudantes para análise.',
                'solicitados': 'todos',
                'data_inicio': hoje + timedelta(days=30),
                'data_fim': hoje + timedelta(days=60),
                'status': 'rascunho',
            }
        )
        
        if created:
            q1 = FormularioQuestao.objects.create(
                formulario=form2,
                titulo_pergunta='Qual a renda familiar mensal?',
                tipo_pergunta='multipla_escolha',
                obrigatoriedade=True,
                ordem=1
            )
            FormularioQuestaoOpcao.objects.bulk_create([
                FormularioQuestaoOpcao(questao=q1, alternativa='Até 1 salário mínimo'),
                FormularioQuestaoOpcao(questao=q1, alternativa='1 a 2 salários mínimos'),
                FormularioQuestaoOpcao(questao=q1, alternativa='2 a 3 salários mínimos'),
                FormularioQuestaoOpcao(questao=q1, alternativa='Acima de 3 salários mínimos'),
            ])

        # Formulário 3 - Concluído
        form3, created = Formulario.objects.get_or_create(
            titulo='Avaliação do Restaurante Estudantil 2025',
            defaults={
                'objetivo': 'Avaliar a qualidade do serviço do restaurante estudantil.',
                'solicitados': 'auxilio',
                'auxilio_alvo': self.auxilios[2],
                'data_inicio': hoje - timedelta(days=60),
                'data_fim': hoje - timedelta(days=30),
                'status': 'concluido',
            }
        )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ {Formulario.objects.count()} formulários criados'))
        self.stdout.write(self.style.SUCCESS(f'  ✓ {FormularioQuestao.objects.count()} questões criadas'))
        self.stdout.write(self.style.SUCCESS(f'  ✓ {FormularioQuestaoOpcao.objects.count()} opções criadas'))

    def create_perguntas(self):
        self.stdout.write('Criando perguntas (FAQ)...')
        
        perguntas_data = [
            {
                'enunciado': 'Quais documentos são necessários para solicitar o auxílio transporte?',
                'resposta': 'São necessários: RG, CPF, comprovante de residência, comprovante de matrícula e declaração de renda familiar.',
                'status': 'respondida',
                'aluno': self.alunos[0],
                'assistente_social': self.assistentes[0],
            },
            {
                'enunciado': 'Qual o prazo para análise da solicitação de auxílio moradia?',
                'resposta': 'O prazo para análise é de até 30 dias úteis após a entrega de toda documentação.',
                'status': 'respondida',
                'aluno': self.alunos[1],
                'assistente_social': self.assistentes[0],
            },
            {
                'enunciado': 'Posso acumular mais de um tipo de auxílio?',
                'resposta': None,
                'status': 'nao_respondida',
                'aluno': self.alunos[2],
                'assistente_social': None,
            },
            {
                'enunciado': 'Como faço para renovar meu auxílio alimentação?',
                'resposta': None,
                'status': 'nao_respondida',
                'aluno': self.alunos[3],
                'assistente_social': None,
            },
        ]
        
        hoje = timezone.now().date()
        for data in perguntas_data:
            Pergunta.objects.get_or_create(
                enunciado=data['enunciado'],
                aluno=data['aluno'],
                defaults={
                    **data,
                    'data_resposta': hoje - timedelta(days=2) if data['resposta'] else None,
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ {Pergunta.objects.count()} perguntas criadas'))

    def create_solicitacoes(self):
        self.stdout.write('Criando solicitações...')
        
        solicitacoes_data = [
            {
                'status': self.status_list[2],  # Deferido
                'descricao': 'Solicitação de auxílio transporte para o semestre 2026.1',
                'id_aluno': self.alunos[0],
                'tipo_auxilio': self.auxilios[0],
                'id_assistente_social': self.assistentes[0],
                'data_deferimento': timezone.now().date() - timedelta(days=10),
            },
            {
                'status': self.status_list[0],  # Em análise
                'descricao': 'Solicitação de auxílio moradia para o semestre 2026.1',
                'id_aluno': self.alunos[1],
                'tipo_auxilio': self.auxilios[1],
                'id_assistente_social': None,
                'data_deferimento': None,
            },
            {
                'status': self.status_list[1],  # Documentação pendente
                'descricao': 'Solicitação de alimentação estudantil',
                'id_aluno': self.alunos[2],
                'tipo_auxilio': self.auxilios[2],
                'id_assistente_social': self.assistentes[1],
                'data_deferimento': None,
            },
            {
                'status': self.status_list[3],  # Indeferido
                'descricao': 'Solicitação de auxílio transporte',
                'id_aluno': self.alunos[3],
                'tipo_auxilio': self.auxilios[0],
                'id_assistente_social': self.assistentes[0],
                'data_deferimento': None,
            },
        ]
        
        self.solicitacoes = []
        for data in solicitacoes_data:
            solicitacao, _ = Solicitacao.objects.get_or_create(
                descricao=data['descricao'],
                id_aluno=data['id_aluno'],
                tipo_auxilio=data['tipo_auxilio'],
                defaults=data
            )
            self.solicitacoes.append(solicitacao)
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ {Solicitacao.objects.count()} solicitações criadas'))

    def create_beneficios(self):
        self.stdout.write('Criando benefícios...')
        
        hoje = timezone.now().date()
        
        # Benefício ativo para o aluno que teve solicitação deferida
        Beneficio.objects.get_or_create(
            aluno=self.alunos[0],
            solicitacao=self.solicitacoes[0],
            tipo_auxilio=self.auxilios[0],
            defaults={
                'status': True,
                'data_fim': hoje + timedelta(days=180),
            }
        )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ {Beneficio.objects.count()} benefícios criados'))

    def create_notificacoes(self):
        self.stdout.write('Criando notificações...')
        
        notificacoes_data = [
            {
                'titulo': 'Solicitação Deferida',
                'mensagem': 'Sua solicitação de auxílio transporte foi deferida! Parabéns!',
                'status': 'lida',
            },
            {
                'titulo': 'Documentação Pendente',
                'mensagem': 'Sua solicitação de alimentação estudantil está com documentação pendente. Por favor, envie os documentos faltantes.',
                'status': 'nao_lida',
            },
            {
                'titulo': 'Novo Formulário Disponível',
                'mensagem': 'Um novo formulário de pesquisa está disponível. Por favor, responda até o prazo final.',
                'status': 'enviada',
            },
            {
                'titulo': 'Lembrete de Prazo',
                'mensagem': 'O prazo para entrega de documentos do auxílio moradia termina em 5 dias.',
                'status': 'nao_lida',
            },
        ]
        
        usuarios_notif = [
            [self.aluno_users[0]],
            [self.aluno_users[2]],
            self.aluno_users,  # Todos os alunos
            [self.aluno_users[1]],
        ]
        
        for i, data in enumerate(notificacoes_data):
            notif, created = Notificacao.objects.get_or_create(
                titulo=data['titulo'],
                mensagem=data['mensagem'],
                defaults={'status': data['status']}
            )
            if created:
                notif.usuario.set(usuarios_notif[i])
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ {Notificacao.objects.count()} notificações criadas'))
