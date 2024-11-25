from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework import serializers, permissions, generics
from dj_rest_auth.views import LogoutView
from account import serializers
from django.shortcuts import render


class UserViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.UserListSerializer
        return serializers.UserDetailSerializer

# We need to create view, that registers the user
class UserRegisterView(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer

def signup(request):
    if request.method == 'POST':
        print(request.POST)
        serializer = serializers.UserRegisterSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return render(request, 'core/frontpage.html')  # Перенаправление после успешной регистрации
        else:
            print(serializer.errors)
    return render(request, 'core/signup.html', {'serializer': UserRegisterView.serializer_class})

class CustomLogoutView(LogoutView):
    permission_classes = (permissions.IsAuthenticated, )
