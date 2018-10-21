import json
from .models import Deck
from .forms import DeckCreationForm
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render
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
        form = DeckCreationForm(user, request.POST)
        if form_is_valid():
            deck = form.save()

            # adding some implicit fields
            deck.data = json.dumps({ "cards" : [] })
            deck.creator = user.username
            deck.date_created = timezone.now()
            deck.save()

            # adding deck to user's account
            user.decks.add(deck)

            messages.success(request, 'Deck has been created.')
    else :
        form = DeckCreationForm()

    context = {
        'form': form
    }

    return render(request, 'builder/create_deck.html', context)
