from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import User, Token
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer, TokenSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    authentication_classes = []
    permission_classes = (AllowAny,)


class UserTokensList(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = TokenSerializer
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Token.objects.filter(user=self.request.user)
