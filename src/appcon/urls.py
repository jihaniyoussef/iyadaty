from django.urls import path
from . import views

urlpatterns = [
    path('consultation-detail/<int:id>/', views.consultation_detail,
        name='consultation_detail'),
    path('edit-consultation-detail/<int:pk>/', views.edit_consultation_detail,
        name='edit_consultation_detail'),
    path('consultation-services/<int:pk>/', views.consultation_services,
        name='consultation_services'),
    path('delete-consultation-service/<int:pk>/', views.delete_consultation_service,
        name='delete_consultation_service'),
    path('add-consultation-service/<int:pk>/', views.add_consultation_service,
        name='add_consultation_service'),
    ]
