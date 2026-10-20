from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mascota/nueva/', views.registrar_mascota, name='registrar_mascota'),
    path('cita/nueva/', views.crear_cita, name='crear_cita'),
    path('cita/<int:cita_id>/estado/<str:nuevo_estado>/', views.cambiar_estado_cita, name='cambiar_estado_cita'),
]