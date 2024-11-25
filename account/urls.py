from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from account import views
from django.urls import path, include
from dj_rest_auth.views import LoginView
from django.contrib.auth import logout
from django.http import HttpResponseRedirect


def custom_logout(request):
    """Обрабатывает GET-запросы для выхода"""
    logout(request)  # Завершение сессии пользователя
    return HttpResponseRedirect('/')  # Редирект на главную страницу

router = DefaultRouter()
router.register('', views.UserViewSet)

urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('signup/', views.signup, name='signup'),
    path('logout/', custom_logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),

    # path('login/', LoginView.as_view()),    # These login and logout is only for backend
    # path('logout/', views.CustomLogoutView.as_view()),

    path('', include(router.urls)),
]