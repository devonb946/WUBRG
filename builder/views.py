import json
from .models import Deck, DeckCard
from browse.models import Card
from .forms import DeckCreationForm
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
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
            deck.data = json.dumps({ "cards" : [] })
            deck.creator = user.username
            deck.date_created = timezone.now()
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

        try:
            dc_relationship = DeckCard.objects.get(deck=deck, card=card)
        except DeckCard.DoesNotExist:
            dc_relationship = DeckCard(deck=deck, card=card, count=0)

        if deck.card_count == 0:
            deck.art_card = card

        dc_relationship.count += 1
        deck.card_count += 1

        # add a card by udpating the relationship model
        dc_relationship.save()
        deck.save()

        messages.success(request, 'Card has been added.')

        page = request.GET.get('page')

        context = {
            'card': card,
            'page': page,
        }

        return render(request, 'browse/details.html', context)

    return HttpResponse(status=204)

@login_required
def remove_card(request, card_id):
    user = request.user
    deck_id = request.POST.get('deck_id')
    deck = Deck.objects.get(id=deck_id)
    card = Card.objects.get(id=card_id)

    dc_relationship = DeckCard.objects.get(deck=deck, card=card)

    dc_relationship.count = dc_relationship.count - 1
    deck.card_count = deck.card_count - 1

    if dc_relationship.count <= 0:
        dc_relationship.delete()
    else:
        dc_relationship.save()

    deck.save()

    page = request.GET.get('page')

    messages.success(request, 'Card has been removed.')
    return HttpResponseRedirect(request.path_info)

@login_required
def add_deck(request, deck_id):
    if request.method == 'POST':
        user = request.user
        deck = Deck.objects.get(id=deck_id)

        user.decks.add(deck)
        messages.success(request, 'Deck has been added.')
        return render(request, 'browse/add_deck_success.html')

    return HttpResponse(status=204)

@login_required
def remove_deck(request, deck_id):
    user = request.user
    deck = Deck.objects.get(id=deck_id)

    user.decks.remove(deck)
    messages.success(request, 'Deck has been removed.')
    return render(request, 'browse/remove_deck_success.html')
