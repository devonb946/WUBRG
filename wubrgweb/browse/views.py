from django.shortcuts import render
from .models import Card
from django.http import HttpResponse

# Create your views here.
def index(request):
    cards = Card.objects.all()[:25]

    context = {
        'cards': cards
    }

    return render(request, 'browse/index.html', context)

def details(request, id):
    card = Card.objects.get(collector_number=id)

    context = {
        'card': card,
    }

    return render(request, 'browse/details.html', context)







# TODO: Implement all of this
def cards_search(request):

    return render(request, 'browse/index.html')

def cards_suggested(request):

    return render(request, 'browse/index.html')


# deck views
def decks_search(request):
    return render(request, 'browse/index.html')

def decks_featured(request):
    return render(request, 'browse/index.html')

def deck(request):
    return render(request, 'browse/index.html')
