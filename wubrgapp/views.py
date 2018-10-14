from django.shortcuts import render

# home view
def index(request):
    return render(request, 'wubrgapp/home.html')

# header views
def profile(request):
    return render(request, 'wubrgapp/base.html')

def browse_cards(request):
    return render(request, 'wubrgapp/base.html')

def tools(request):
    return render(request, 'wubrgapp/base.html')

def browse_decks(request):
    return render(request, 'wubrgapp/base.html')

def builder(request):
    return render(request, 'wubrgapp/base.html')
