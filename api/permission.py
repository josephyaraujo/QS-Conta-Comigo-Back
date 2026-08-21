from rest_framework import permissions


def _is_assistente_social_mode(user):
    return user.groups.filter(name='AS').exists()


class OnlyAssistenteSocial(permissions.BasePermission):
    """Permissão de acesso para Assistente Social"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and _is_assistente_social_mode(request.user)
        )


class OnlyAluno(permissions.BasePermission):
    """Permissão de acesso para Aluno"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and not _is_assistente_social_mode(request.user)
            and hasattr(request.user, 'aluno')
        )
    
class IsAlunoOrAssistenteSocial(permissions.BasePermission):
    """Permissão para usuários autenticados com perfil no sistema"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                hasattr(request.user, 'aluno')
                or _is_assistente_social_mode(request.user)
            )
        )