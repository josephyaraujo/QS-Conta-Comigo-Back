from typing import ClassVar

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.base import NotificacaoSerializer
from ..services.notificacaoService import ConsultarNotificacao


class NotificacaoView(APIView):
    permission_classes: ClassVar[list] = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        usuario = request.user

        lidas_qs = ConsultarNotificacao.listar_notificacoes(usuario, "lida")
        nao_lidas_qs = ConsultarNotificacao.listar_notificacoes(usuario, "nao_lida")

        data_nao_lidas = NotificacaoSerializer(nao_lidas_qs, many=True).data
        data_lidas = NotificacaoSerializer(lidas_qs, many=True).data

        return Response({"nao_lidas": data_nao_lidas, "lidas": data_lidas})

    def patch(self, request, pk=None, *args, **kwargs):
        usuario = request.user
        notificacao_id = pk or request.query_params.get("id")

        if not notificacao_id:
            return Response(
                {"error": "ID da notificação não fornecido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ConsultarNotificacao.marcar_como_lida(usuario, notificacao_id)

        return Response(
            {"message": "Notificação marcada como lida com sucesso."},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk=None):
        usuario = request.user

        if not pk:
            return Response(
                {"error": "ID não fornecido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ConsultarNotificacao.excluir_notificacao(usuario, [pk])

        return Response(status=status.HTTP_204_NO_CONTENT)
