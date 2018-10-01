from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views

# urls for user accounts
urlpatterns = [
    path('', views.index, name='index'),

    # account paths
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('decks/', views.profile_decks, name='profile_decks'),
    path('settings/', views.profile_settings, name='profile_settings'),
    path('settings/changepass/', auth_views.PasswordChangeView.as_view(template_name='accounts/change_password.html'), name='change_password'),
    path('settings/remove/', views.remove_account, name='remove_account'),
]
