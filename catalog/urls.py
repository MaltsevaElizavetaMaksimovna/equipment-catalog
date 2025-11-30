from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/add/', views.equipment_create, name='equipment_create'),
    path('equipment/<int:pk>/edit/', views.equipment_edit, name='equipment_edit'),
    path('equipment/<int:pk>/delete/', views.equipment_delete, name='equipment_delete'),
]
