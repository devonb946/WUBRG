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

    return render(request, 'browse/card_results.html', context)

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

    return render(request, 'browse/card_results.html', context)


def card_details(request, id):
    card = Card.objects.get(id=id)
    page = request.GET.get('page')
    name = request.GET.get('name')

    # filter decks to add the card to by editable decks only
    if request.user.is_authenticated:
        decks = request.user.decks.filter(creator=request.user.username)

    context = {
        'card': card,
        'decks': decks,
        'page': page,
        'name': name
    }

    return render(request, 'browse/card_details.html', context)

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
        'page': page,
        'title': 'All Decks'
    }

    return render(request, 'browse/deck_results.html', context)

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

    # limit some functionality for followed decks
    if user.username == deck.creator:
        can_edit = True
    else:
        can_edit = False

    mass_entry_string = build_mass_entry(deck_cards)

    context = {
        'deck': deck,
        'cards_data': cards_data,
        'art_card': art_card,
        'has_deck': has_deck,
        'can_edit': can_edit,
        'mass_entry_string': mass_entry_string,
        'page': page,
    }

    return render(request, 'browse/deck_details.html', context)

def decks_search(request):
    context = {}
    return render(request, 'browse/deck_search.html', context)

def decks_results(request):
    name = request.GET.get('name')
    page = request.GET.get('page')

    result_decks = Deck.objects.filter(name__icontains=name).order_by('date_created')

    if page == None:
        page = 1

    paginator = Paginator(result_decks, 42)
    decks = paginator.get_page(page)

    context = {
        'decks': decks,
        'page': page,
        'title': 'Search results for "{}"'.format(name),
        'name': name
    }

    return render(request, 'browse/deck_results.html', context)

def build_mass_entry(deck_cards):

    me_string = ""

    for deck_card in deck_cards:
        me_string += str(deck_card.count)

        name_words = deck_card.card.data['name'].split()
        for word in name_words:
            me_string += "%20"  # query string space
            me_string += word

        me_string += "||"

    return me_string
