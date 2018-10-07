from . import views
from django.urls import path

# This will house all of our urls for wubrgweb
urlpatterns = [
    path('', views.index, name='index'),

    #TODO:
    # header tabs
    #path('profile/{profileId}/', views.profile, name='profile'),
    #path('browse/cards/', views.browse_cards, name='browse_cards'),
    #path('tools/', views.tools, name='tools'),
    #path('browse/decks/', views.browse_decks, name='browse_decks'),
    #path('builder/', views.builder, name='builder'),
]
