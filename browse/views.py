from django.shortcuts import render
from .models import Card
from builder.models import Deck
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
def deck_details(request, id):

    deck = Deck.objects.get(id=id)
    art_card = deck.art_card
    page = request.GET.get('page')

    user = request.user

    if user.is_authenticated:
        try:
            user_deck = user.decks.get(id=deck.id)
            has_deck = True
        except Deck.DoesNotExist:
            has_deck = False
    else:
        has_deck = False

    context = {
        'deck': deck,
        'art_card': art_card,
        'has_deck': has_deck,
        'page': page,
    }

    return render(request, 'browse/deck_details.html', context)

def decks_search(request):
    return render(request, 'browse/index.html')

def decks_featured(request):
    return render(request, 'browse/index.html')
