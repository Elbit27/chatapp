from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework import serializers, permissions, generics
from dj_rest_auth.views import LogoutView
from account import serializers
from django.shortcuts import render

from rest_framework.response import Response
from django.core.cache import cache


class UserViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.UserListSerializer
        return serializers.UserDetailSerializer

    def list(self, request, *args, **kwargs):
        # Ключ для кэша
        cache_key = "user_list"
        cache_time = 300  # Кэш на 5 минут

        # Получение данных из кэша
        user_list = cache.get(cache_key)

        if not user_list:  # Если данных нет, запросить из БД
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            user_list = serializer.data

            # Сохранение данных в кэше
            cache.set(cache_key, user_list, cache_time)

        # Возвращение данных
        return Response(user_list)

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
