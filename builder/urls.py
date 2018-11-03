from django.urls import path
from builder import views

urlpatterns = [
    path('', views.index, name='index'),

    # builder paths
    path('create/', views.create, name='create'),
    path('create/success', views.create_success, name='create_success'),
    path('add/card/<uuid:card_id>', views.add_card, name='add_card'),
    path('remove/card/<uuid:card_id>', views.remove_card, name='remove_card'),
    path('add/deck/<uuid:deck_id>', views.add_deck, name='add_deck'),
    path('remove/deck/<uuid:deck_id>', views.remove_deck, name='remove_deck'),
    path('validate/deck/<uuid:deck_id>', views.validate_deck, name='validate_deck')
]
