from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from .forms import WubrgUserCreationForm, WubrgUserChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

User = get_user_model()

# profile views
def index(request):
    username = None
    # redirect to user's actual profile page if they are logged in
    if request.user.is_authenticated:
        return redirect(reverse('profile', args=[request.user.username]))
    else:
        return render(request, 'accounts/base.html')

def register(request):
    if request.method == 'POST':
        form = WubrgUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts/index')
    else:
        form = WubrgUserCreationForm()

    context = {
        'form': form
    }

    return render(request, 'accounts/register.html', context)

def user_page(request):
    return redirect(reverse('profile', args=[request.user.username]))

@login_required
def profile(request, username):
    user = request.user
    # restrict decks to 3 on front page of profile
    decks = user.decks.all().order_by('-date_created')[:3]

    context = {
        'user': user,
        'decks' : decks,
    }

    return render(request, 'accounts/profile.html', context)

# TODO display user decks
@login_required
def profile_decks(request):
    user = request.user
    user_decks = user.decks.all().order_by('-date_created')

    paginator = Paginator(user_decks, 12)

    page = request.GET.get('page')
    decks = paginator.get_page(page)

    context = {
        'user': user,
        'decks': decks,
        'page': page,
    }

    return render(request, 'accounts/user_decks.html', context)

@login_required
def password_change_done(request):
    return render(request, 'accounts/change_password_done.html')

@login_required
def remove_account(request, username):
    try:
        user = User.objects.get(username=username)
        user.is_active = False
        user.save()
        messages.success(request, 'User {username} has been removed successfully.')
    except User.DoesNotExist:
        messages.error(request, 'User {username} does not exist. Please try again.')
    return redirect('logout')
