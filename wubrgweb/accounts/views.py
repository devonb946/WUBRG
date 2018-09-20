from django.shortcuts import render

# profile views
def index(request):
    return render(request, 'accounts/base.html')

def profile_decks(request):
    return render(request, 'accounts/base.html')

def profile_settings(request):
    return render(request, 'accounts/base.html')

def change_username(request):
    return render(request, 'accounts/base.html')

def change_password(request):
    return render(request, 'accounts/base.html')

def remove_account(request):
    return render(request, 'accounts/base.html')
