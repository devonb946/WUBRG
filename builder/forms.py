import uuid
from django import forms
from builder.models import Deck


class DeckCreationForm(forms.Form):
    FORMATS = (
        ('Standard', 'Standard'),
        ('Modern', 'Modern'),
        ('Commander/EDH', 'Commander/EDH'),
        ('Legacy', 'Legacy'),
        ('Vintage', 'Vintage'),
        ('Brawl', 'Brawl'),
    )

    # User-defined fields
    name = forms.CharField(max_length=100)
    format = forms.CharField(
        label = 'Select a format',
        max_length=50,
        widget=forms.Select(choices=FORMATS)
    )
    description = forms.CharField(max_length=10000)
