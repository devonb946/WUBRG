import json
import uuid
import re
from .models import Deck, DeckCard, SideboardCard
from browse.models import Card
from .forms import DeckCreationForm
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# builder views
def index(request):
    all_decks = Deck.objects.order_by('date_created')

    paginator = Paginator(all_decks, 12)

    page = request.GET.get('page')
    decks = paginator.get_page(page)

    context = {
        'decks': decks,
        'page': page
    }

    return render(request, 'builder/base.html', context)

@login_required
def create(request):
    user = request.user

    if request.method == 'POST':
        form = DeckCreationForm(request.POST)
        if form.is_valid():
            deck = form.save()

            # adding some implicit fields
            deck.creator = user.username
            deck.date_created = timezone.now()
            deck.colors = update_deck_colors(deck)
            deck.save()

            # adding deck to user's account
            user.decks.add(deck)
            messages.success(request, 'Deck has been created.')

            return redirect('create_success')
    else :
        form = DeckCreationForm()

    context = {
        'form': form
    }

    return render(request, 'builder/create_deck.html', context)

def create_success(request):
    return render(request, 'builder/create_deck_success.html')

@login_required
def add_card(request, card_id):
    if request.method == 'POST':
        deck_id = request.POST.get('deck_id')
        is_sideboard = request.POST.get('is_sideboard')
        is_commander = request.POST.get('is_commander')
        user = request.user
        card = Card.objects.get(id=card_id)
        deck = Deck.objects.get(id=deck_id)

        # prevent followers from editing decks
        if user.username == deck.creator:
            add(deck, card, is_sideboard, is_commander)
            messages.success(request, 'Card has been added.')

            page = request.GET.get('page')

            return HttpResponseRedirect('/browse/card_details/' + str(card_id))
        else:
            return HttpResponse(status=204)
    else:
        return HttpResponse(status=204)

@login_required
def remove_card(request, card_id):
    user = request.user
    deck_id = request.POST.get('deck_id')
    is_sideboard = request.POST.get('is_sideboard')
    deck = Deck.objects.get(id=deck_id)
    card = Card.objects.get(id=card_id)

    #prevent followers from editing decks
    if user.username == deck.creator:
        remove_count = parse_remove_count(request.POST.get('remove_count'))
        remove(deck, card, is_sideboard, remove_count)

        #page = request.GET.get('page')

        messages.success(request, 'Card has been removed.')

        return HttpResponseRedirect('/browse/deck_details/' + deck_id)
    else:
        return HttpResponse(status=204)

def update_deck_colors(deck):
    colors = set()


    for card in deck.cards.all():
        if "colors" in card.data:
            colors = colors.union(card.data['colors'])
        elif "card_faces" in card.data["card_faces"][0]:
            if "colors" in card.data:
                colors = card.data["card_faces"][0]["colors"] + card.data["card_faces"][1]["colors"]

    for card in deck.cards.all():
        if "colors" in card.data:
            colors = colors.union(card.data['colors'])
        elif "card_faces" in card.data["card_faces"][0]:
            if "colors" in card.data:
                colors = card.data["card_faces"][0]["colors"] + card.data["card_faces"][1]["colors"]

    order = {"W":0, "U": 1, "B": 2, "R": 3, "G": 4}
    colors = sorted(colors, key = lambda x: order[x])

    return ''.join(colors)

def parse_remove_count(count):
    if not count is None:
        count = count.strip()
        return int(count) if count else 1
    else:
        return 1

@login_required
def copy_deck(request, deck_id):
    user = request.user
    deck = Deck.objects.get(id=deck_id)

    # create new copy of deck
    new_deck_name = "{} ({}\'s copy)".format(deck.name, user.username)
    new_deck = Deck.objects.create_deck(
        new_deck_name,
        deck.description,
        deck.id,
        deck.format,
        deck.card_count,
        deck.sideboard_card_count,
        deck.colors,
        user.username,
        timezone.now(),
        deck.cards.all(),
        deck.sideboard_cards.all(),
        deck.art_card
    )

    user.decks.add(new_deck)
    messages.success(request, 'Deck has been successfully copied.')
    return render(request, 'builder/copy_deck_success.html')

@login_required
def follow_deck(request, deck_id):
    user = request.user
    deck = Deck.objects.get(id=deck_id)

    user.decks.add(deck)
    messages.success(request, 'Deck has been successfully followed.')
    return render(request, 'builder/follow_deck_success.html')

@login_required
def remove_deck(request, deck_id):
    user = request.user
    deck = Deck.objects.get(id=deck_id)

    # set draft to true to prevent it from showing up in browse
    deck.is_draft = True
    deck.save()

    user.decks.remove(deck)
    messages.success(request, 'Deck has been removed.')
    return render(request, 'builder/remove_deck_success.html')

@login_required
def unfollow_deck(request, deck_id):
    user = request.user
    deck = Deck.objects.get(id=deck_id)

    user.decks.remove(deck)
    messages.success(request, 'Deck has been unfollowed.')
    return render(request, 'builder/unfollow_deck_success.html')

@login_required
def update_art_card(request, card_id):
    user = request.user
    deck_id = request.POST.get('deck_id')

    deck = Deck.objects.get(id=deck_id)
    card = Card.objects.get(id=card_id)

    deck.art_card = card
    deck.save()

    messages.success(request, 'Art card has been successfully changed.')
    return HttpResponseRedirect('/browse/deck_details/' + deck_id)

@login_required
def validate_deck(request, deck_id):
    user = request.user
    deck = Deck.objects.get(id=deck_id)
    format = deck.format.lower()

    is_valid = validate(deck, format)
    if is_valid:
        deck.is_draft = False
        deck.save()
        messages.success(request, 'Deck {} has been successfully validated.'.format(deck_id))
        return HttpResponseRedirect('/browse/deck_details/' + str(deck_id))
    else:
        context = { 'deck_id': deck_id }
        return render(request, 'builder/validate_deck_failure.html', context)

def validate(deck, format):
    if format in ['standard', 'modern', 'legacy', 'vintage', 'brawl']:
        if deck.card_count < 60:
            return False
        if format != 'brawl' and deck.sideboard_card_count > 15:
            return False

    if format == 'commander':
        if deck.card_count < 100:
            return False

    # check for a commander card and color identity
    if format in ['commander', 'brawl']:
        deck_cards = DeckCard.objects.filter(deck=deck)
        is_legal = check_commander_identity(deck_cards)
        if not is_legal:
            return False

    for card in deck.cards.all():
        is_legal = check_card_legality(card, format)
        if not is_legal:
            return False

    return True

def check_card_legality(card, format):
    legality = card.data['legalities'][format]
    if legality != 'legal':
        return False
    else:
        return True

def check_commander_identity(deck_cards):
    commanders = all((card for card in deck_cards if card.is_commander), None)
    if commanders:
        color_identity = set()
        for commander in commanders:
            color_identity = color_identity.union(commander.data['color_identity'])
        color_identity = list(color_identity)
        for card in deck_cards:
            if card.data['color_identity'] not in color_identity:
                return False
        return True
    else:
        return False

def mass_entry(request):
    if request.method == 'POST' and request.user.is_authenticated:
        deck_id = request.POST.get('deck_id')
        is_sideboard = request.POST.get('is_sideboard')
        cards_text = request.POST.get('cards_text')
        deck = Deck.objects.get(id=deck_id)
        cards_text_lines = cards_text.strip().splitlines()

        for line in cards_text_lines:
            quantity_candidate = line.split(' ')[0].strip()
            # check if the word we pulled back is actually the quantity
            # and not the first word of the card name
            pattern = re.compile('[0-9]+x$')     # any number followed by x
            if pattern.match(quantity_candidate):  # can't input more than 999 of a card
                quantity = int(quantity_candidate[:-1])
                card_name = ' '.join(line.split(' ')[1:]).strip()
            else:
                quantity = 1
                card_name = line.strip()

            # check for special commander string
            if card_name[-1] == "__commander__":
                card_name = card_name[:-1]
                is_commander = True
            else:
                is_commander = False

            card_to_add = Card.objects.filter(data__name__icontains=card_name)[0]
            if card_to_add:     # ignore empty results
                for _ in range(min(quantity, 999)):
                    add(deck, card_to_add, is_sideboard, is_commander)

        context = { 'deck_id': deck_id }
        return render(request, 'builder/mass_entry_success.html', context)
    else:
        context = {}
        if request.user.is_authenticated:
            placeholder = "2x Negate\n1x Thunderclap Wyvern\nKiora, the Crashing Wave\n10x Island"
            decks = request.user.decks.filter(creator=request.user.username)
            context = {
                'placeholder': placeholder,
                'decks': decks
            }
        return render(request, 'builder/mass_entry.html', context)

def add(deck, card, is_sideboard, is_commander):
    if is_sideboard == "False":
        try:
            dc = DeckCard.objects.get(deck=deck, card=card)
        except DeckCard.DoesNotExist:
            dc = DeckCard(deck=deck, card=card, count=0)

        # check if card is eligible to be a commander
        is_eligible_commander = check_commander_status(dc.card)
        if is_commander == "True" and is_eligible_commander:
            dc.is_commander = True

        dc.count += 1
        # add a card by udpating the relationship model
        dc.save()

        if deck.card_count == 0:
            deck.art_card = card

        deck_cards = DeckCard.objects.filter(deck=deck)
        deck.card_count = deck_cards.aggregate(Sum('count'))['count__sum']
    else:
        try:
            sc = SideboardCard.objects.get(deck=deck, card=card)
        except SideboardCard.DoesNotExist:
            sc = SideboardCard(deck=deck, card=card, count=0)

        sc.count += 1
        sc.save()
        deck_sideboard_cards = SideboardCard.objects.filter(deck=deck)
        deck.sideboard_card_count = deck_sideboard_cards.aggregate(Sum('count'))['count__sum']

    deck.colors = update_deck_colors(deck)
    deck.save()

def remove(deck, card, is_sideboard, remove_count):
    if is_sideboard == "False":
        try:
            dc = DeckCard.objects.get(deck=deck, card=card)
        except DeckCard.DoesNotExist:
            dc = DeckCard(deck=deck, card=card, count=0)

        dc.count = dc.count - remove_count
        if dc.count <= 0:
            dc.delete()
        else:
            dc.save()

        deck_cards = DeckCard.objects.filter(deck=deck)
        deck.card_count = deck_cards.aggregate(Sum('count'))['count__sum']
        if not deck.card_count:     # aggregate will return None if 0
            deck.card_count = 0

    else:
        try:
            sc = SideboardCard.objects.get(deck=deck, card=card)
        except SideboardCard.DoesNotExist:
            sc = SideboardCard(deck=deck, card=card, count=0)

        sc.count = sc.count - remove_count
        if sc.count <= 0:
            sc.delete()
        else:
            sc.save()

        deck_sideboard_cards = SideboardCard.objects.filter(deck=deck)
        deck.sideboard_card_count = deck_sideboard_cards.aggregate(Sum('count'))['count__sum']
        if not deck.sideboard_card_count:   # aggregate will return None if 0
            deck.sideboard_card_count = 0

    deck.colors = update_deck_colors(deck)
    deck.save()

def check_commander_status(card):
    if hasattr(card.data, "card_faces"):
        card.data["type_line"] = card.data["card_faces"][0]["type_line"]
        card.data["oracle_text"] = card.data["card_faces"][0]["oracle_text"]
    if "legendary" in card.data['type_line'].lower() and "creature" in card.data['type_line'].lower():
        return True
    elif "can be your commander" in card.data['oracle_text'].lower():
        return True
    else:
        return False
