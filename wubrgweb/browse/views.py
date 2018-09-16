from django.shortcuts import render
from .models import Card

# Create your views here.
def index(request):
    cards = Card.objects.all()

    context = {
        'cards': cards
    }

    return render(request, 'browse/index.html', context)

def details(request, id):
    card = Card.objects.get(id=collector_number)

    context = {
        'card': card
    }

    return render(request, 'browse/details.html', context)
