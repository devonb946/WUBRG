import json
from .models import Deck
from browse.models import Card
from .forms import DeckCreationForm
from django.utils import timezone
from django.http import HttpResponse
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

        deck.data['cards'].append(card)
        messages.success(request, 'Deck has been added.')
        return render(request, 'browse/add_card_success.html')

    return HttpResponse(status=204)

@login_required
def remove_card(request, card_id):
    if request.method == 'POST':
        deck_id = request.POST.get('deck_id')
        user = request.user
        deck = Deck.objects.get(id=deck_id)

        deck.data['cards'] = [x for x in deck.data['cards'] if x['id'] != card_id]
        deck.save(update_fields=['data'])
        messages.success(request, 'Card has been removed.')
        return render(request, 'browse/remove_card_success.html')

    return HttpResponse(status=204)

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
    if request.method == 'POST':
        user = request.user
        deck = Deck.objects.get(id=deck_id)

        user.decks.remove(deck)
        messages.success(request, 'Deck has been removed.')
        return render(request, 'browse/remove_deck_success.html')

    return HttpResponse(status=204)
