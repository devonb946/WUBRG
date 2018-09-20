from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.index, name='index'),

    # card paths
    url('details/(?P<id>\d+)/$', views.details, name='details'),
    url('browse/cards/search/', views.cards_search, name='cards_search'),
    url('browse/cards/suggested/', views.cards_suggested, name='cards_suggested'),

    # deck paths
    url('browse/decks/search/', views.decks_search, name='decks_search'),
    url('browse/decks/featured/', views.decks_featured, name='decks_featured'),
    url('browse/decks/{deckId}/', views.deck, name='deck'),
]
