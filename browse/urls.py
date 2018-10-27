from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # card paths
    path('cards/all', views.cards_all, name="All Cards"),
    path('details/<str:id>', views.details, name='Card Details'),
    path('cards/search', views.cards_search, name='Search Cards'),

    # deck paths
    #url('browse/decks/search/', views.decks_search, name='decks_search'),
    ##url('browse/decks/featured/', views.decks_featured, name='decks_featured'),
    #url('browse/decks/{deckId}/', views.deck, name='deck'),
]
