try:
    from rest_framework.permissions import AllowAny
except ImportError:
    from rest_framework.permissions import OnlyAssistenteSocialAllowAny as AllowAny
