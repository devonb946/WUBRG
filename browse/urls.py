from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # card paths
    path('cards/all', views.cards_all, name="All Cards"),
    path('details/<uuid:id>', views.details, name='Card Details'),
    path('cards/search', views.cards_search, name='Search Cards'),

    # deck paths
    path('decks/all', views.decks_all, name="all_decks"),
    path('deck_details/<uuid:id>', views.deck_details, name='deck_details'),
    #path('decks/search/', views.decks_search, name='decks_search'),
]
