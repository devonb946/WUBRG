from django.shortcuts import render
from .models import Card
from builder.models import Deck, DeckCard
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

def index(request):
    cards = Card.objects.all().exclude(data__layout = 'token').exclude(data__layout = 'double_faced_token').exclude(data__layout = 'emblem').filter(data__lang = 'en').order_by('?')[:5]
    context = {
        'cards': cards
    }
    return render(request, "browse/landing.html", context)

def cards_all(request):
    all_cards = Card.objects.order_by('data__name').exclude(data__layout = 'token').exclude(data__layout = 'double_faced_token').exclude(data__layout = 'emblem').filter(data__lang = 'en').filter(data__reprint = False)
    paginator = Paginator(all_cards, 42)# Show 42 cards (not tokens) per page

    page = request.GET.get('page')
    cards = paginator.get_page(page)

    context = {
        'cards': cards,
        'page': page,
        'title': 'All Cards',
    }

    return render(request, 'browse/results.html', context)

def cards_results(request):
    name = request.GET.get('name')
    page = request.GET.get('page')

    result_cards = Card.objects.filter(data__name__icontains=name).order_by('data__name')

    if page == None:
        page = 1

    paginator = Paginator(result_cards, 42)
    cards = paginator.get_page(page)

    context = {
        'cards': cards,
        'page': page,
        'title': 'Search results for "{}"'.format(name),
        'name': name
    }

    return render(request, 'browse/results.html', context)


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


# deck views
def decks_all(request):
    all_decks = Deck.objects.order_by('date_created')
    paginator = Paginator(all_decks, 42)

    page = request.GET.get('page')
    decks = paginator.get_page(page)

    context = {
        'decks': decks,
        'page': page
    }

    return render(request, 'browse/all_decks.html', context)

def deck_details(request, id):

    deck = Deck.objects.get(id=id)

    cards = deck.cards.all()
    deck_cards = DeckCard.objects.filter(deck=deck)
    cards_data = zip(cards, deck_cards)

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
        'cards_data': cards_data,
        'art_card': art_card,
        'has_deck': has_deck,
        'page': page,
    }

    return render(request, 'browse/deck_details.html', context)

def decks_search(request):
    return render(request, 'browse/index.html')
