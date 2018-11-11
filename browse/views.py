from django.utils import timezone
from django.shortcuts import render
from .models import Card
from builder.models import Deck, DeckCard, SideboardCard
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
    query = request.META['QUERY_STRING']
    name = request.GET.get('name')
    page = request.GET.get('page')
    is_advanced = request.GET.get('is_advanced')

    result_cards = Card.objects.filter(data__name__icontains=name)

    if page == None:
        page = 1

    paginator = Paginator(result_cards, 42)
    cards = paginator.get_page(page)

    context = {
        'cards': cards,
        'page': page,
        'title': 'Search results for "{}"'.format(name),
        'name': name,
        'query': query
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

def cards_search(request):
    context = {}
    return render(request, 'browse/card_search.html', context)

def stat_relations(result_cards, attribute, relation, value):
    if attribute == "cmc":
        value = float(value)
        if relation == "eq":
            result_cards = result_cards.filter(data__cmc=value)
        elif relation == "gt":
            result_cards = result_cards.filter(data__cmc__gt=value)
        elif relation == "lt":
            result_cards = result_cards.filter(data__cmc__lt=value)
        elif relation == "gte":
            result_cards = result_cards.filter(data__cmc__gte=value)
        elif relation == "lte":
            result_cards = result_cards.filter(data__cmc__lte=value)
        elif relation == "ne":
            result_cards = result_cards.filter(data__cmc__ne=value)
    elif attribute == "power":
        value = str(value)
        if relation == "eq":
            result_cards = result_cards.filter(data__power=value)
        elif relation == "gt":
            result_cards = result_cards.filter(data__power__gt=value)
        elif relation == "lt":
            result_cards = result_cards.filter(data__power__lt=value)
        elif relation == "gte":
            result_cards = result_cards.filter(data__power__gte=value)
        elif relation == "lte":
            result_cards = result_cards.filter(data__power__lte=value)
        elif relation == "ne":
            result_cards = result_cards.filter(data__power__ne=value)
    elif attribute == "toughness":
        value = str(value)
        if relation == "eq":
            result_cards = result_cards.filter(data__toughness=value)
        elif relation == "gt":
            result_cards = result_cards.filter(data__toughness__gt=value)
        elif relation == "lt":
            result_cards = result_cards.filter(data__toughness__lt=value)
        elif relation == "gte":
            result_cards = result_cards.filter(data__toughness__gte=value)
        elif relation == "lte":
            result_cards = result_cards.filter(data__toughness__lte=value)
        elif relation == "ne":
            result_cards = result_cards.filter(data__toughness__ne=value)
    elif attribute == "loyalty":
        value = str(value)
        if relation == "eq":
            result_cards = result_cards.filter(data__loyalty=value)
        elif relation == "gt":
            result_cards = result_cards.filter(data__loyalty__gt=value)
        elif relation == "lt":
            result_cards = result_cards.filter(data__loyalty__lt=value)
        elif relation == "gte":
            result_cards = result_cards.filter(data__loyalty__gte=value)
        elif relation == "lte":
            result_cards = result_cards.filter(data__loyalty__lte=value)
        elif relation == "ne":
            result_cards = result_cards.filter(data__loyalty__ne=value)
    return result_cards

def legality_relations(result_cards, status, format):
    if format == "standard":
        if status == "legal":
            result_cards = result_cards.filter(data__legalities__standard=True)
        elif status == "illegal":
            result_cards = result_cards.filter(data__legalities__standard=False)
        elif status == "banned":
            result_cards = result_cards.filter(data__legalities__standard="banned")
        elif status == "restricted":
            result_cards = result_cards.filter(data__legalities__standard="restricted")
    elif format == "modern":
        if status == "legal":
            result_cards = result_cards.filter(data__legalities__modern=True)
        elif status == "illegal":
            result_cards = result_cards.filter(data__legalities__modern=False)
        elif status == "banned":
            result_cards = result_cards.filter(data__legalities__modern="banned")
        elif status == "restricted":
            result_cards = result_cards.filter(data__legalities__modern="restricted")
    elif format == "commander":
        if status == "legal":
            result_cards = result_cards.filter(data__legalities__commander=True)
        elif status == "illegal":
            result_cards = result_cards.filter(data__legalities__commander=False)
        elif status == "banned":
            result_cards = result_cards.filter(data__legalities__commander="banned")
        elif status == "restricted":
            result_cards = result_cards.filter(data__legalities__commander="restricted")
    elif format == "legacy":
        if status == "legal":
            result_cards = result_cards.filter(data__legalities__legacy=True)
        elif status == "illegal":
            result_cards = result_cards.filter(data__legalities__legacy=False)
        elif status == "banned":
            result_cards = result_cards.filter(data__legalities__legacy="banned")
        elif status == "restricted":
            result_cards = result_cards.filter(data__legalities__legacy="restricted")
    elif format == "vintage":
        if status == "legal":
            result_cards = result_cards.filter(data__legalities__vintage=True)
        elif status == "illegal":
            result_cards = result_cards.filter(data__legalities__vintage=False)
        elif status == "banned":
            result_cards = result_cards.filter(data__legalities__vintage="banned")
        elif status == "restricted":
            result_cards = result_cards.filter(data__legalities__vintage="restricted")
    elif format == "brawl":
        if status == "legal":
            result_cards = result_cards.filter(data__legalities__brawl=True)
        elif status == "illegal":
            result_cards = result_cards.filter(data__legalities__brawl=False)
        elif status == "banned":
            result_cards = result_cards.filter(data__legalities__brawl="banned")
        elif status == "restricted":
            result_cards = result_cards.filter(data__legalities__brawl="restricted")
    return result_cards


def cards_adv_results(request):

    query = request.META['QUERY_STRING']

    page = request.GET.get('page')
    name = request.GET.get('name')
    text = request.GET.get('text')
    type = request.GET.get('type')
    value = request.GET.get('value')
    status = request.GET.get('status')
    format = request.GET.get('format')
    set = request.GET.get('set')
    rarity = request.GET.get('rarity')
    artist = request.GET.get('artist')
    flavor = request.GET.get('flavor')
    language = request.GET.get('language')

    result_cards = Card.objects.all()

    if(name):
        result_cards = result_cards.filter(data__name__icontains=name)
    if(text):
        result_cards = result_cards.filter(data__oracle_text__icontains=text)
    if(type):
        result_cards = result_cards.filter(data__type_line__icontains=type)


    cols = []
    for i in 'WUBRGC':
        if bool(request.GET.get(i)):
            cols += [str(i).upper()]
    cols = sorted(cols)
    colors = request.GET.get('colors')

    if colors == 'e':
        result_cards = result_cards.filter(data__colors=cols)
    elif colors == 'g':
        for i in cols:
            result_cards = result_cards.filter(data__colors__contains=i)
    elif colors == 'l':
        newcolors = ["W", "U", "R", "B", "G", "C"]
        for i in cols:
            newcolors.remove(i)
        print(newcolors)
        for i in newcolors:
            result_cards = result_cards.exclude(data__colors__contains=i)

    comm_cols = []
    for i in 'WUBRGC':
        if bool(request.GET.get("C"+i)):
            comm_cols += [str(i).upper()]
    comm_cols = sorted(comm_cols)
    if comm_cols != []:
        result_cards = result_cards.filter(data__color_identity=comm_cols)


    if(value):
        attribute = request.GET.get('attribute')
        relation = request.GET.get('relation')
        result_cards = stat_relations(result_cards, attribute, relation, value)


    if(status and format):
        result_cards = legality_relations(result_cards, status, format)

    if(rarity):
        result_cards = result_cards.filter(data__rarity=rarity)

    if(artist):
        result_cards = result_cards.filter(data__artist__icontains=artist)

    if(flavor):
        result_cards = result_cards.filter(data__flavor_text__icontains=flavor)



    result_cards = result_cards.order_by("data__name")
    paginator = Paginator(result_cards, 42)
    cards = paginator.get_page(page)

    context = {
        'query': query,
        'cards': cards,
        'page': page,
        'title': 'Advanced Search Results',
    }

    return render(request, 'browse/card_results.html', context)


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

    sideboard_cards = deck.sideboard_cards.all()
    sideboard_deck_cards = SideboardCard.objects.filter(deck=deck)
    sideboard_cards_data = zip(sideboard_cards, sideboard_deck_cards)

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

    mass_buy_string = build_mass_buy(deck_cards, sideboard_deck_cards)

    context = {
        'deck': deck,
        'cards_data': cards_data,
        'sideboard_cards_data': sideboard_cards_data,
        'art_card': art_card,
        'has_deck': has_deck,
        'can_edit': can_edit,
        'mass_buy_string': mass_buy_string,
        'page': page,
    }

    return render(request, 'browse/deck_details.html', context)

def decks_search(request):
    context = {}
    return render(request, 'browse/deck_search.html', context)

def decks_results(request):
    name = request.GET.get('name')
    page = request.GET.get('page')
    is_advanced = request.GET.get('is_advanced')

    if is_advanced:
        format = request.GET.get('format')
        is_draft = request.GET.get('is_draft')
        date_created = request.GET.get('date_created')

        result_decks = Deck.objects.filter(
            name__icontains=name,
            format__iexact=format,
            is_draft__iexact=is_draft,
            colors__icontains=colors,
            creator__icontains=creator,
            date_created__gte=date_created,
        ).order_by('date_created')
    else:
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

def build_mass_buy(deck_cards, sideboard_deck_cards):

    mb_string = ""

    for deck_card in deck_cards:
        mb_string += str(deck_card.count)

        name_words = deck_card.card.data['name'].split()
        for word in name_words:
            mb_string += "%20"  # query string space
            mb_string += word

        mb_string += "||"

    for sideboard_deck_card in sideboard_deck_cards:
        mb_string += str(sideboard_deck_card.count)

        name_words = sideboard_deck_card.card.data['name'].split()
        for word in name_words:
            mb_string += "%20"  # query string space
            mb_string += word

        mb_string += "||"

    return mb_string
