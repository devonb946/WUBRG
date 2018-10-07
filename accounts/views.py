from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse


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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been created.')

            #TODO change to actual profile page
            return redirect('register')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

def user_page(request):
    return redirect(reverse('profile', args=[request.user.username]))

@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'accounts/profile.html', {'user': user})

# TODO display user decks
@login_required
def profile_decks(request):
    return render(request, 'accounts/base.html')

@login_required
def password_change_done(request):
    return render(request, 'accounts/change_password_done.html')

def remove_account(request, username):
    try:
        user = User.objects.get(username=username)
        user.delete()
        messages.success(request, 'User {username} has been deleted.')

    except User.DoesNotExist:
        messages.error(request, 'User {username} does not exist. Please try again')

    return render(request, 'accounts/base.html')
