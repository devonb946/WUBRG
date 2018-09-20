from django.conf.urls import url
from accounts import views

# urls for user accounts
urlpatterns = [
    url('', views.index, name='index'),

    # account paths
    url('profile/decks/', views.profile_decks, name='profile_decks'),
    url('profile/settings/', views.profile_settings, name='profile_settings'),
    url('profile/settings/changename/', views.change_username, name='change_username'),
    url('profile/settings/changepass/', views.change_password, name='change_password'),
    url('profile/settings/remove/', views.remove_account, name='remove_account'),
]
