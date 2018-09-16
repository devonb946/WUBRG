from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.index, name='index'),
    url('details/(?P<id>\d+)/$', views.details, name='details')
]
