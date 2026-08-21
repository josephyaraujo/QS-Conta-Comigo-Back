# from social_core.backends.oauth import BaseOAuth2
from ..models import *
import requests
from ..utils import formatar_nome_curso
from django.db import transaction

class PopulateUsuario():
    
    def __init__(self):
        self.USER_DATA_URL = "https://suap.ifrn.edu.br/api/rh/eu/" # dados geral do usuario
        self.EXTRA_USER_DATA_URL = "https://suap.ifrn.edu.br/api/rh/meus-dados/" # email e nome
        self.EXTRA_AS_DATA_URL = "https://suap.ifrn.edu.br/api/rh/servidores/" # dados detalhado da AS
        self.DATA_DETAILS_URL_ALUNO = "https://suap.ifrn.edu.br/api/ensino/meus-dados-aluno/" # dados detalhado aluno
        self.DEFAULT_SCOPE = ["identificacao", "email", "documentos_pessoais"]

    def get_user_suap(self, access_token):
        """ popula dados suap vindo do suap """
        method = "GET"
        data = {"scope": " ".join(self.DEFAULT_SCOPE)}
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(
            url=self.USER_DATA_URL,
            params=data,
            headers=headers,
        ).json()
        

        user_details = {
            "matricula": response.get("identificacao"),
            "nome_completo": (
                response.get("nome_social") or response.get("nome_registro")
            ),
            "cpf": response.get("cpf"),
            "campus": response.get("campus"),
            "email_pessoal": response.get("email_secundario"),
            "email_escolar": response.get("email_google_classroom"),
            "email_academico": response.get("email_academico"),
            "tipo_vinculo": response.get("tipo_usuario"),
        }

        usuario = Usuario.objects.filter(nome_completo=user_details["nome_completo"]).first()
        if not usuario: 
            usuario = Usuario.objects.create(
                nome_completo = user_details["nome_completo"],
                username = user_details["email_escolar"]
            )
        elif usuario.groups.filter(name='AS').exists():
            user_details["tipo_vinculo"] = 'assistente social'

        # primeiro_nome, *_, ultimo_nome = user_details["nome_completo"].split()

        return user_details, usuario
    
    def populate_usuario(self, access_token, user_details, usuario):
        """ função para popular banco com dados do usuário de acordo com seu vinculo """
        tipo_usuario = user_details['tipo_vinculo'].lower()

        if user_details['tipo_vinculo'].lower() == 'aluno': 
            """ criação ou update do aluno """
            data = {"scope": " ".join(self.DEFAULT_SCOPE)}
            method = "GET"
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Request dos dados de aluno
            response = requests.get(
                url=self.DATA_DETAILS_URL_ALUNO,
                headers=headers,
                params = data
            ).json()
            

            cpf_numerico = ''.join(filter(str.isdigit, user_details["cpf"]))
            matricula_aluno = str(user_details.get('matricula', '') or '')
            data_usuario, created = Aluno.objects.update_or_create(
                usuario=usuario,
                defaults= {
                    'cpf': cpf_numerico,
                    'curso' : formatar_nome_curso(response["curso"]),
                    'periodo' : response["periodo_referencia"],
                    'status' : response["situacao"],
                    'matricula' : matricula_aluno,
                    'campus': user_details['campus'],
                    'ingresso': response['ingresso'],
                    'qtd_periodos': response['qtd_periodos']
                }
            )

        elif user_details['tipo_vinculo'].lower() == 'assistente social': 
            """ criação ou update da AS """
            matricula_as = self._resolve_as_matricula(user_details, usuario)
            with transaction.atomic():
                # Evita conflito de unique(usuario): sempre atualiza pelo usuário.
                data_usuario, created = AssistenteSocial.objects.update_or_create(
                    usuario=usuario,
                    defaults={
                        'matricula': matricula_as,
                    }
                )
        # print(data_usuario or created)
        return data_usuario or created, tipo_usuario

    def _resolve_as_matricula(self, user_details, usuario):
        """Retorna uma matrícula AS válida (até 7 dígitos) e sem colisão."""
        raw = ''.join(filter(str.isdigit, str(user_details.get('matricula', '') or '')))
        candidate = raw[:7] if raw else ''

        # fallback determinístico para cenários em que o SUAP não fornece matrícula de servidor.
        if not candidate:
            candidate = f"9{usuario.id:06d}"[-7:]

        conflict = AssistenteSocial.objects.filter(matricula=candidate).exclude(usuario=usuario).exists()
        if not conflict:
            return candidate

        # Resolve colisão preservando 7 dígitos.
        base = int(candidate) if candidate.isdigit() else usuario.id
        for i in range(1, 1000):
            next_candidate = str((base + i) % 10_000_000).zfill(7)
            if not AssistenteSocial.objects.filter(matricula=next_candidate).exclude(usuario=usuario).exists():
                return next_candidate

        # Último fallback improvável.
        return str(usuario.id % 10_000_000).zfill(7)