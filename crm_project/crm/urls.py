from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(f'clients', views.ClientViewSet, basename='clients')
router.register(f'companies', views.CompanyViewSet, basename='companies')
router.register(f'tasks', views.TasksViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
]