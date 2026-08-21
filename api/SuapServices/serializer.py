from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import serializers

class SuapCodeSerializer(serializers.Serializer):
    code = serializers.CharField(help_text="Código de autorização retornado pelo SUAP")