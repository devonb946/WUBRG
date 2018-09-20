from django.conf.urls import url
from . import views

# This will house all of our urls for wubrgweb
urlpatterns = [
    url('', views.index, name='index'),

    # header tabs
    url('profile/{profileId}/', views.profile, name='profile'),
    url('browse/cards/', views.browse_cards, name='browse_cards'),
    url('tools/', views.tools, name='tools'),
    url('browse/decks/', views.browse_decks, name='browse_decks'),
    url('builder/', views.builder, name='builder'),
]
