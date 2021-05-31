from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(f'clients', views.ClientViewSet, basename='clients')




urlpatterns = [
    path('', include(router.urls)),
]