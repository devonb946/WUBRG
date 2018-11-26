from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # card paths
    path('cards/all', views.cards_all, name='All Cards'),
    path('card_details/<uuid:id>', views.card_details, name='Card Details'),
    path('cards/search', views.cards_search, name='Search Cards'),
    path('cards/results', views.cards_results, name='Card Results'),
    path('cards/adv_results', views.cards_adv_results, name='Advanced Card Results'),
    path('cards/printings', views.other_printings, name='Printings'),
    # deck paths
    path('decks/all', views.decks_all, name='All Decks'),
    path('deck_details/<uuid:id>', views.deck_details, name='Deck Details'),
    path('decks/search', views.decks_search, name='Search Decks'),
    path('decks/results', views.decks_results, name='Deck Results'),
]
