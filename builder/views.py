import json
import uuid
from .models import Deck, DeckCard
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
        user = request.user
        card = Card.objects.get(id=card_id)
        deck = Deck.objects.get(id=deck_id)

        # prevent followers from editing decks
        if user.username == deck.creator:
            try:
                dc_relationship = DeckCard.objects.get(deck=deck, card=card)
            except DeckCard.DoesNotExist:
                dc_relationship = DeckCard(deck=deck, card=card, count=0)

            dc_relationship.count += 1

            # add a card by udpating the relationship model
            dc_relationship.save()

            if deck.card_count == 0:
                deck.art_card = card
            deck_cards = DeckCard.objects.filter(deck=deck)
            deck.card_count = deck_cards.aggregate(Sum('count'))['count__sum']
            deck.colors = update_deck_colors(deck)

            deck.save()

            messages.success(request, 'Card has been added.')

            page = request.GET.get('page')

            context = {
                'card': card,
                'page': page,
            }

            return render(request, 'browse/card_details.html', context)
        else:
            return HttpResponse(status=204)
    else:
        return HttpResponse(status=204)

@login_required
def remove_card(request, card_id):
    user = request.user
    deck_id = request.POST.get('deck_id')

    deck = Deck.objects.get(id=deck_id)
    card = Card.objects.get(id=card_id)

    #prevent followers from editing decks
    if user.username == deck.creator:
        remove_count = parse_remove_count(request.POST.get('remove_count'))

        dc_relationship = DeckCard.objects.get(deck=deck, card=card)

        dc_relationship.count = dc_relationship.count - remove_count

        if dc_relationship.count <= 0:
            dc_relationship.delete()
        else:
            dc_relationship.save()

        deck_cards = DeckCard.objects.filter(deck=deck)
        if not deck_cards:
            deck.card_count = 0
        else:
            deck.card_count = deck_cards.aggregate(Sum('count'))['count__sum']
        deck.colors = update_deck_colors(deck)

        deck.save()

        page = request.GET.get('page')

        messages.success(request, 'Card has been removed.')

        return HttpResponseRedirect('/browse/deck_details/' + deck_id)
    else:
        return HttpResponse(status=204)

def update_deck_colors(deck):
    colors = set()

    for card in deck.cards.all():
        colors = colors.union(card.data['colors'])

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

def validate_deck(request, deck_id):
    user = request.user
    deck = Deck.objects.get(id=deck_id)
    format = deck.format

    # logic bucket for various deck formats
    if format == 'Standard':
        is_valid = validate_standard(deck)
    elif format == 'Modern':
        is_valid = validate_modern(deck)
    elif format == 'Commander/EDH':
        is_valid = validate_commander(deck)
    elif format == 'Legacy':
        is_valid = validate_legacy(deck)
    elif format == 'Vintage':
        is_valid = validate_vintage(deck)
    elif format == 'Brawl':
        is_valid = validate_brawl(deck)
    else:
        is_valid = False

    if is_valid:
        deck.is_draft = False
        deck.save()

    return HttpResponse(status=204)

# -------------------------
# Deck validator functions
# -------------------------
def validate_standard(deck):
    return False

def validate_modern(deck):
    return False

def validate_commander(deck):
    return False

def validate_legacy(deck):
    return False

def validate_vintage(deck):
    return False

def validate_brawl(deck):
    return False
