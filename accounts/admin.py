from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import WubrgUserCreationForm, WubrgUserChangeForm
from .models import WubrgUser

# Register your models here.

class WubrgUserAdmin(UserAdmin):
    add_form = WubrgUserCreationForm
    form = WubrgUserChangeForm
    model = WubrgUser
    list_display = ['username', 'email',]

admin.site.register(WubrgUser, WubrgUserAdmin)
