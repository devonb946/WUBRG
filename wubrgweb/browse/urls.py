from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # card paths
    path('details/<int:id>', views.details, name='Card Details'),

    #TODO: Fully implement URLs
    #url('browse/cards/search/', views.cards_search, name='cards_search'),
    #url('browse/cards/suggested/', views.cards_suggested, name='cards_suggested'),

    # deck paths
    #url('browse/decks/search/', views.decks_search, name='decks_search'),
    ##url('browse/decks/featured/', views.decks_featured, name='decks_featured'),
    #url('browse/decks/{deckId}/', views.deck, name='deck'),
]
