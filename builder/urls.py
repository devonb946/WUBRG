from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.index, name='index'),

    # builder paths
    url('builder/create/', views.create, name='create'),
]
