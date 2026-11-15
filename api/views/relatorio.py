from typing import ClassVar

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Beneficio, Cursos
from api.permission import OnlyAssistenteSocial
from api.serializers.auxilio_beneficio import (
    RelatorioGeradoSerializer,
    RelatorioSerializer,
)

from ..services.relatorioService import gerar_docx, gerar_pdf, gerar_xlsx


class RelatorioView(APIView):
    permission_classes: ClassVar[list] = [OnlyAssistenteSocial]

    @swagger_auto_schema(request_body=RelatorioSerializer, security=[{"Bearer": []}])
    def post(self, request):
        serializer = RelatorioSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        dados_validados = serializer.validated_data

        titulo = dados_validados["titulo"]
        formato_relatorio = dados_validados["formato_relatorio"]

        ano = dados_validados.get("ano")
        programa = dados_validados.get("programa")
        ingresso = dados_validados.get("ingresso")
        curso = dados_validados.get("curso")
        periodo_referencia = dados_validados.get("periodo_referencia")
        situacao_periodo = dados_validados.get("situacao_periodo")

        filtros = {}

        if situacao_periodo:
            filtros["aluno__status"] = situacao_periodo

        if curso is not None:
            curso_nome = Cursos.objects.get(id=curso).nome
            filtros["aluno__curso"] = curso_nome

        if periodo_referencia:
            filtros["aluno__periodo"] = periodo_referencia

        if ingresso:
            filtros["aluno__ingresso"] = ingresso

        if ano is not None:
            filtros["data_inicio__year"] = ano

        if programa is not None:
            filtros["tipo_auxilio"] = programa

        dados = Beneficio.objects.filter(**filtros)
        serializer = RelatorioGeradoSerializer(dados, many=True)

        if formato_relatorio == "pdf":
            return gerar_pdf(titulo, serializer.data)
        elif formato_relatorio == "docx":
            return gerar_docx(titulo, serializer.data)
        elif formato_relatorio == "excel":
            return gerar_xlsx(titulo, serializer.data)

        return Response({"ok": True})
