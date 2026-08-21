from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError


Usuario = get_user_model()


class Command(BaseCommand):
    help = 'Alterna o modo de login entre AS e Aluno para um usuário identificado pelo e-mail.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--role',
            choices=['as', 'aluno'],
            help='Perfil que o usuário deve assumir no próximo login via SUAP.',
        )
        parser.add_argument(
            '--email',
            help='E-mail retornado pelo SUAP para localizar o usuário local.',
        )

    def handle(self, *args, **options):
        try:
            role = self._resolve_role(options.get('role'))
            email = self._resolve_email(options.get('email'))
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nOperação cancelada pelo usuário.'))
            return

        usuario = self._find_usuario(email)

        if not usuario:
            raise CommandError(
                f'Nenhum usuário encontrado para "{email}". '
                'Verifique se o e-mail está correto e se o usuário já foi criado no sistema.'
            )

        as_group, _ = Group.objects.get_or_create(name='AS')
        aluno_group, _ = Group.objects.get_or_create(name='Aluno')

        if role == 'as':
            usuario.groups.add(as_group)
            usuario.groups.remove(aluno_group)
            mensagem = 'modo AS'
        else:
            usuario.groups.remove(as_group)
            usuario.groups.add(aluno_group)
            mensagem = 'modo Aluno'

        self.stdout.write(
            self.style.SUCCESS(
                f'Usuário {usuario.nome_completo} ({usuario.username}) ajustado para {mensagem}. '
                'Agora faça o login via SUAP novamente.'
            )
        )

    def _resolve_role(self, role):
        if role:
            return role

        self.stdout.write('Escolha o perfil de login:')
        self.stdout.write('  1 - AS')
        self.stdout.write('  2 - Aluno')
        choice = input('Opção: ').strip().lower()

        if choice in {'1', 'as', 'assistente social', 'assistente_social'}:
            return 'as'
        if choice in {'2', 'aluno'}:
            return 'aluno'

        raise CommandError('Opção inválida. Use AS ou Aluno.')

    def _resolve_email(self, email):
        if email:
            return email.strip()

        email = input('E-mail retornado pelo SUAP: ').strip()
        if not email:
            raise CommandError('O e-mail não pode ficar vazio.')
        return email

    def _find_usuario(self, email):
        return (
            Usuario.objects.filter(email__iexact=email).first()
            or Usuario.objects.filter(username__iexact=email).first()
        )