from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import WubrgUser

class WubrgUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = WubrgUser
        fields = ('username', 'email')


class WubrgUserChangeForm(UserChangeForm):
    class Meta:
        model = WubrgUser
        fields = ('username', 'email')
