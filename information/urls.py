from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.index, name='index'),

    # informational tools paths
    url('tools/youtube/', views.youtube, name='youtube'),
    url('tools/articles/', views.articles, name='articles'),
    url('tools/tutorials/', views.tutorials, name='tutorials'),
]
