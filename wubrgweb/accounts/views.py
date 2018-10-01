from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# profile views
def index(request):

    #TODO redirect to user profile page if they are signed in
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


# def login(request):
#     if request.method == 'POST':
#
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate()
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Login successful.')
#
#             #TODO change to actual profile page
#             return redirect('')
#     else:
#         #TODO create login form
#         form = UserCreationForm()
#
#     return render(request, 'accounts/login.html', {'form': form})


def profile_decks(request):
    return render(request, 'accounts/base.html')


def profile_settings(request):
    return render(request, 'accounts/base.html')


def change_username(request):
    return render(request, 'accounts/base.html')


def change_password(request):
    return render(request, 'accounts/base.html')


def remove_account(request):
    return render(request, 'accounts/base.html')
