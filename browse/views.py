from django.utils import timezone
from django.shortcuts import render
from django.contrib import messages
from .models import Card
from builder.models import Deck, DeckCard, SideboardCard
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


#browse views
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

def other_printings(request):
    name = request.GET.get('name', None)
    page = request.GET.get('page', 1)

    result_cards = Card.objects.filter(data__name__contains=name)

    paginator = Paginator(result_cards, 42)
    cards = paginator.get_page(page)

    context = {
        'cards': cards,
        'page': page,
        'title': 'All printings for "{}"'.format(name),
        'name': name,
    }

    return render(request, 'browse/card_results.html', context)


def cards_results(request):
    name = request.GET.get('name', None)
    page = request.GET.get('page', 1)

    query = request.META['QUERY_STRING']
    if "page" in query:
        query = query[query.find("&"):]
    if query[0] != "&":
        query = "&" + query

    result_cards = Card.objects.filter(data__name__icontains=name)

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
    page = request.GET.get('page', None)
    name = request.GET.get('name', None)
    query = request.META['QUERY_STRING']
    if "page" in query:
        query = query[query.find("&"):]
    if query != "" and query[0] != "&":
        query = "&" + query

    if page == None:
        page = 1

    #pretty mana cost for details desplay
    pmc = card.data["mana_cost"] if "mana_cost" in card.data else []
    if("//" in pmc):
        temp = "".join([i for i in pmc.split("//") if i != ""]).split("  ")
        pmc = []
        for i in temp:
            instance = i.split("}")
            pmc.append([j[1:] for j in instance if j != ""])
        pmc = [pmc[0]] + [["//"]] + [pmc[1]]
        pmc = [item for sublist in pmc for item in sublist]
    elif "card_faces" in card.data:
            pmc = card.data["card_faces"][0]["mana_cost"] + card.data["card_faces"][1]["mana_cost"]
            pmc = pmc.split("}")
            pmc = [i[1:] for i in pmc if i != ""]
    else:
        pmc = pmc.split("}")
        pmc = [i[1:] for i in pmc if i != ""]


    if "oracle_text" in card.data:
        formatted_oracle = card.data["oracle_text"].replace("\n", "<br />").replace("(", "<i>(").replace(")", ")</i>")
    else:
        if "card_faces" in card.data:
            formatted_oracle = card.data["card_faces"][0]["oracle_text"].replace("\n", "<br />").replace("(", "<i>(").replace(")", ")</i>") + "</p><hr /><p>" + card.data["card_faces"][1]["oracle_text"].replace("\n", "<br />").replace("(", "<i>(").replace(")", ")</i>")

    #mana symbols
    for i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,"W","U","B","R","G","C","X"]:
        formatted_oracle = formatted_oracle.replace("{%s}" % i, '<span style="display:inline"><i class="ms ms-%s"></i></span>' % str(i).lower() )
    #Phyrexean mana
    for i in ["W/P","U/P","B/P","R/P","G/P"]:
        formatted_oracle = formatted_oracle.replace("{%s}" % i, '<span style="display:inline"><i class="ms ms-%s ms-p"></i></span>' % i[0].lower() )
    #hybrid mana
    for i in ["W/U", "U/B", "B/R", "R/G", "G/W", "W/B", "U/R", "B/G", "R/W", "G/U"]:
        formatted_oracle = formatted_oracle.replace("{%s}" % i, '<img src="http://gatherer.wizards.com/Handlers/Image.ashx?size=medium&name={}{}&type=symbol" />'.format(i[0], i[-1]))
    for i in "WUBRG":
        formatted_oracle = formatted_oracle.replace("{" + "2/{}".format(i) + "}", '<img src="http://gatherer.wizards.com/Handlers/Image.ashx?size=medium&name=2{}&type=symbol" />'.format(i))

    #Phyrexean, snow, tap, energy, untap, chaos
    formatted_oracle = formatted_oracle.replace("{P}", '<span style="display:inline"><i class="ms ms-p" style="background:none;border:0px;"></i></span>')
    formatted_oracle = formatted_oracle.replace("{S}", '<span style="display:inline"><i class="ms ms-s" style="background:none;border:0px;"></i></span>')
    formatted_oracle = formatted_oracle.replace("{T}", '<span style="display:inline"><i class="ms ms-tap" style="background:none;border:0px;"></i></span>')
    formatted_oracle = formatted_oracle.replace("{E}", '<span style="display:inline"><i class="ms ms-e" style="background:none;border:0px;"></i></span>')
    formatted_oracle = formatted_oracle.replace("{Q}", '<span style="display:inline"><i class="ms ms-untap" style="background:none;border:0px;"></i></span>')
    formatted_oracle = formatted_oracle.replace("{CHAOS}", '<span style="display:inline"><i class="ms ms-chaos" style="background:none;border:0px;"></i></span>')


    # filter decks to add the card to by editable decks only
    if request.user.is_authenticated:
        decks = request.user.decks.filter(creator=request.user.username)
    else:
        decks = []

    context = {
        'card': card,
        'decks': decks,
        'page': page,
        'name': name,
        'query': query,
        'pmc': pmc,
        'formatted_oracle': formatted_oracle,
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
            result_cards = result_cards.filter(data__legalities__standard="legal")
        elif status == "illegal":
            result_cards = result_cards.filter(data__legalities__standard="not_legal")
        elif status == "banned":
            result_cards = result_cards.filter(data__legalities__standard="banned")
        elif status == "restricted":
            result_cards = result_cards.filter(data__legalities__standard="restricted")
    elif format == "modern":
        if status == "legal":
            result_cards = result_cards.filter(data__legalities__modern="legal")
        elif status == "illegal":
            result_cards = result_cards.filter(data__legalities__modern="not_legal")
        elif status == "banned":
            result_cards = result_cards.filter(data__legalities__modern="banned")
        elif status == "restricted":
            result_cards = result_cards.filter(data__legalities__modern="restricted")
    elif format == "commander":
        if status == "legal":
            result_cards = result_cards.filter(data__legalities__commander="legal")
        elif status == "illegal":
            result_cards = result_cards.filter(data__legalities__commander="not_legal")
        elif status == "banned":
            result_cards = result_cards.filter(data__legalities__commander="banned")
        elif status == "restricted":
            result_cards = result_cards.filter(data__legalities__commander="restricted")
    elif format == "legacy":
        if status == "legal":
            result_cards = result_cards.filter(data__legalities__legacy="legal")
        elif status == "illegal":
            result_cards = result_cards.filter(data__legalities__legacy="not_legal")
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

    page = request.GET.get('page', 1)
    name = request.GET.get('name', None)
    text = request.GET.get('text', None)
    type = request.GET.get('type', None)
    value = request.GET.get('value', None)
    status = request.GET.get('status', None)
    format = request.GET.get('format', None)
    set = request.GET.get('set', None)
    rarity = request.GET.get('rarity', None)
    artist = request.GET.get('artist', None)
    flavor = request.GET.get('flavor', None)
    language = request.GET.get('language', None)

    query = request.META['QUERY_STRING']
    if "page" in query:
        query = query[query.find("&"):]
    if query[0] != "&":
        query = "&" + query

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

    if(set):
        result_cards = result_cards.filter(data__set_name__icontains=set)

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
    all_decks = Deck.objects.order_by('date_created').filter(is_draft=False)
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

    if deck.parent_id:
        parent_deck = Deck.objects.get(id=deck.parent_id)
    else:
        parent_deck = None

    cards = deck.cards.all().order_by('data__name')
    deck_cards = DeckCard.objects.filter(deck=deck).order_by('card__data__name')
    cards_data = zip(cards, deck_cards)

    sideboard_cards = deck.sideboard_cards.all().order_by('data__name')
    sideboard_deck_cards = SideboardCard.objects.filter(deck=deck).order_by('card__data__name')
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
        'parent_deck': parent_deck,
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
    draft = request.GET.get('draft')

    if(draft == "True"):
        result_decks = Deck.objects.filter(name__icontains=name).order_by('date_created')
    else:
        result_decks = Deck.objects.filter(name__icontains=name).order_by('date_created').filter(is_draft=False)

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
