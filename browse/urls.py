from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # card paths
    path('details/<uuid:id>', views.details, name='Card Details'),

    #TODO: Fully implement URLs
    path('cards/search', views.cards_search, name='cards_search'),
    #url('cards/suggested/', views.cards_suggested, name='cards_suggested'),

    # deck paths
    path('deck_details/<uuid:id>', views.deck_details, name='deck_details'),
    #path('decks/search/', views.decks_search, name='decks_search'),
    #path('decks/featured/', views.decks_featured, name='decks_featured'),
]
