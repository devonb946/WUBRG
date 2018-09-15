from django.shortcuts import render

# home view
def index(request):
    return render(request, 'base.html')


# header views
def profile(request):
    return render(request, 'base.html')

def browse_cards(request):
    return render(request, 'base.html')

def tools(request):
    return render(request, 'base.html')

def browse_decks(request):
    return render(request, 'base.html')

def builder(request):
    return render(request, 'base.html')


# profile views
def profile_decks(request):
    return render(request, 'base.html')

def profile_settings(request):
    return render(request, 'base.html')

def change_username(request):
    return render(request, 'base.html')

def change_password(request):
    return render(request, 'base.html')

def remove_account(request):
    return render(request, 'base.html')


# card views
def cards_search(request):
    return render(request, 'base.html')

def cards_suggested(request):
    return render(request, 'base.html')

def card(request):
    return render(request, 'base.html')


# informational tools views
def youtube(request):
    return render(request, 'base.html')

def articles(request):
    return render(request, 'base.html')

def tutorials(request):
    return render(request, 'base.html')


# deck views
def decks_search(request):
    return render(request, 'base.html')

def decks_featured(request):
    return render(request, 'base.html')

def deck(request):
    return render(request, 'base.html')


# builder views
def create(request):
    return render(request, 'base.html')
