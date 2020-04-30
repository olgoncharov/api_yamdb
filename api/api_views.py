from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import EmailCodeTokenObtainPairSerializer


class EmailCodeTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailCodeTokenObtainPairSerializer
