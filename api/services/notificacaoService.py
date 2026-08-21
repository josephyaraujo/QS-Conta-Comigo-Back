from ..models import Usuario, Notificacao
from datetime import datetime

"""CDU006. Consultar notificações
Ator principal: Usuário logado
Resumo: O Usuário logado poderá ver suas notificações
Pré-condição:
Ter feito o login
Estar na área do usuário logado
Pós-condição: O sistema deve exibir as notificações (se houver) do Usuário logado."""

class ConsultarNotificacao:
    
    @staticmethod
    def listar_notificacoes(usuario, status):
        return Notificacao.objects.filter(usuario=usuario, status=status)
    
    @staticmethod
    def marcar_como_lida(usuario, notificacoes_ids):
        Notificacao.objects.filter(id=notificacoes_ids, usuario=usuario).update(data_visualizacao=datetime.now())
        
    @staticmethod
    def excluir_notificacao(usuario, notificacoes_ids):
        for n in Notificacao.objects.filter(id__in=notificacoes_ids):
            if usuario in n.usuario.all():
                n.delete()
        
    @staticmethod
    def criar_notificacao(titulo, mensagem):
        notificacao = Notificacao.objects.create(
            titulo=titulo,
            mensagem=mensagem,
            status="nao_lida"
        )
        print(notificacao)
        
        return notificacao