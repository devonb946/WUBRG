from django.urls import path
from builder import views

urlpatterns = [
    path('', views.index, name='index'),

    # builder paths
    path('create/', views.create, name='create'),
    path('create/success', views.create_success, name='create_success'),
]
