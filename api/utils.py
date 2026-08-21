import re

class Utilitaria:
    @staticmethod
    def formatar_cpf(cpf: str) -> str:
        """Formata o CPF para o padrão XXX.XXX.XXX-XX."""
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("CPF deve conter 11 dígitos numéricos.")
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    @staticmethod
    def validar_cpf(cpf: str) -> bool:
        cpf_numerico = ''.join(filter(str.isdigit, cpf)) # remove os caracteres que não são digitos

        if len(set(cpf_numerico)) == 1: # verifica se todos os digitos são iguais
            return False

        # cálculo do primeiro dígito verificador
        soma_digito1 = 0
        # multiplicadores de 10 a 2 para os 9 primeiros dígitos
        for i in range(9):
            soma_digito1 += int(cpf_numerico[i]) * (10 - i)

        resto_digito1 = soma_digito1 % 11
        
        if resto_digito1 < 2:
            digito_verificador1 = 0
        else:
            digito_verificador1 = 11 - resto_digito1
        
        if digito_verificador1 != int(cpf_numerico[9]): # compara o dígito calculado com o dígito real (10º dígito do CPF)
            return False

        # cálculo do segundo dígito verificador
        soma_digito2 = 0
        
        for i in range(10): # multiplicadores de 11 a 2 para os 10 primeiros dígitos
            soma_digito2 += int(cpf_numerico[i]) * (11 - i)
            
        resto_digito2 = soma_digito2 % 11

        if resto_digito2 < 2:
            digito_verificador2 = 0
        else:
            digito_verificador2 = 11 - resto_digito2

        if digito_verificador2 != int(cpf_numerico[10]): # compara o dígito calculado com o dígito real (11º dígito do CPF)
            return False
            
        # 5. Se passou por todas as verificações, o CPF é válido
        return True



def formatar_nome_curso(curso_raw):
        if not curso_raw:
            return "Não informado"
        
        # remove o código no início (ex: "01404 - ")
        curso_sem_codigo = re.sub(r'^\d+\s*-\s*', '', curso_raw)

        # remove o trecho do campus
        curso_sem_campus = re.sub(r'\s*-\s*Campus.*$', '', curso_sem_codigo)

        # remove o ano entre parênteses
        curso_final = re.sub(r'\(\d{4}\)', '', curso_sem_campus).strip()

        return curso_final

def proxima_AS(ultimo_chamado, assistentes):
    ultimo_id = ultimo_chamado.assistente_social.id
    lista_ids = list(assistentes.values_list('id', flat=True))
    try:
        indice_atual = lista_ids.index(ultimo_id)
        proximo_indice = (indice_atual + 1) % len(lista_ids)
        proximo_assistente = assistentes.get(id=lista_ids[proximo_indice])
    except ValueError:
        proximo_assistente = assistentes.first()
    return proximo_assistente


def enviar_notificacao(mensagem, usuario,titulo, tipo):
    from api.models import Notificacao
    try:
        nova_notificacao = Notificacao.objects.create(
            titulo=titulo,
            mensagem=mensagem,
            status="nao_lida" ,
            usuario = usuario,
            tipo = tipo
        )
    except Exception as e:
        print(f"Erro ao criar notificação: {e}")