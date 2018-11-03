from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from accounts import views

# urls for user accounts
urlpatterns = [
    path('', views.index, name='index'),

    # account paths
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('settings/changepass/', auth_views.PasswordChangeView.as_view(template_name='accounts/change_password.html'), name='change_password'),
    path('settings/changepass/done', views.password_change_done, name='password_change_done'),
    path('user_page/', views.user_page, name='user_page'),
    path('decks/', views.profile_decks, name='profile_decks'),
    path('settings/remove/<str:username>', views.remove_account, name='remove_account'),
    re_path('(?P<username>\w+)/', views.profile, name='profile'),    
]
