from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include

router = DefaultRouter()
router.register('', views.RoomViewSet)

urlpatterns = [
    path('create/', views.RoomCreateView.as_view()),
    # path('', include(router.urls)),
    path('', views.rooms, name='rooms'),
    path('<slug:slug>/', views.room, name='room')

]