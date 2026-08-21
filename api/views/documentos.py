from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser, FormParser
from api.models import Documento
from api.permission import IsAlunoOrAssistenteSocial
from api.serializers.chamados import DocumentoAlunoSerializer, DocumentoCreateSerializer

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoAlunoSerializer
    permission_classes = [IsAlunoOrAssistenteSocial]  

    def get_serializer_class(self):
        if self.action == 'envia':
            return DocumentoCreateSerializer
        return self.serializer_class

    @action(
        detail=True,
        methods=['post'],
        url_path='envia',
        parser_classes=[MultiPartParser, FormParser]
    )
    def envia(self, request, pk=None):
        arquivo = request.FILES.get('arquivo')

        if not arquivo:
            return Response(
                {'arquivo': 'Arquivo não enviado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        caminho = default_storage.save(
            f'documentos/{arquivo.name}',
            ContentFile(arquivo.read())
        )

        data = request.data.copy()
        data['aluno_id'] = pk
        data['url_documento'] = caminho  # 🔹 string

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"mensagem": "Documento enviado com sucesso."},
            status=status.HTTP_201_CREATED
        )

