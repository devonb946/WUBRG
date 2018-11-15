from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # informational tools paths
    path('mtgrss/', views.mtgrss, name='mtgrss'),
    path('youtube/', views.youtube, name='youtube'),
]
