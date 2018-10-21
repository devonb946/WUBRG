from django.shortcuts import render
from .models import Card
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.


def index(request):
    all_cards = Card.objects.order_by('data__name').exclude(data__layout = 'token').exclude(data__layout = 'double_faced_token').filter(data__lang = 'en').filter(data__reprint = False)
    paginator = Paginator(all_cards, 42)# Show 40 cards (not tokens) per page

    page = request.GET.get('page')
    cards = paginator.get_page(page)

    context = {
        'cards': cards,
        'page': page
    }

    return render(request, 'browse/base.html', context)


def details(request, id):
    card = Card.objects.get(id=id)
    page = request.GET.get('page')

    context = {
        'card': card,
        'page': page
    }

    return render(request, 'browse/details.html', context)

# TODO: Implement all of this
def cards_search(request):

    context = {}

    return render(request, 'browse/card_search.html', context)

def cards_suggested(request):

    return render(request, 'browse/index.html')


# deck views
def decks_search(request):
    return render(request, 'browse/index.html')

def decks_featured(request):
    return render(request, 'browse/index.html')

def deck(request):
    return render(request, 'browse/index.html')
