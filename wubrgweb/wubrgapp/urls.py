from django.urls import path
from wubrgapp import views

# This will house all of our urls for wubrgweb
urlpatterns = [
    path('', views.index, name='index'),

    # header tabs
    path('profile/{profileId}/', views.profile, name='profile'),
    path('browse/cards/', views.browse_cards, name='browse_cards'),
    path('tools/', views.tools, name='tools'),
    path('browse/decks/', views.browse_decks, name='browse_decks'),
    path('builder/', views.builder, name='builder'),

    # profile paths
    path('profile/decks/', views.profile_decks, name='profile_decks'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('profile/settings/changename/', views.change_username, name='change_username'),
    path('profile/settings/changepass/', views.change_password, name='change_password'),
    path('profile/settings/remove/', views.remove_account, name='remove_account'),

    # card paths
    path('browse/cards/search/', views.cards_search, name='cards_search'),
    path('browse/cards/suggested/', views.cards_suggested, name='cards_suggested'),
    path('browse/cards/{cardId}', views.card, name='card'),

    # informational tools paths
    path('tools/youtube/', views.youtube, name='youtube'),
    path('tools/articles/', views.articles, name='articles'),
    path('tools/tutorials/', views.tutorials, name='tutorials'),

    # deck paths
    path('browse/decks/search/', views.decks_search, name='decks_search'),
    path('browse/decks/featured/', views.decks_featured, name='decks_featured'),
    path('browse/decks/{deckId}/', views.deck, name='deck'),

    # builder paths
    path('builder/create/', views.create, name='create'),
]
