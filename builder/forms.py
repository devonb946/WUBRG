import uuid
from django.forms import ModelForm, Textarea, Select
from builder.models import Deck


class DeckCreationForm(ModelForm):

    #
    # # User-defined fields
    # name = forms.CharField(max_length=100)
    # format = forms.CharField(
    #     label = 'Select a format',
    #     max_length=50,
    #     widget=forms.Select(choices=FORMATS)
    # )
    # description = forms.CharField(max_length=10000)

    class Meta:
        FORMATS = (
            ('Standard', 'Standard'),
            ('Modern', 'Modern'),
            ('Commander/EDH', 'Commander/EDH'),
            ('Legacy', 'Legacy'),
            ('Vintage', 'Vintage'),
            ('Brawl', 'Brawl'),
        )

        model = Deck
        fields = ('name', 'format', 'description')
        widgets = {
            'format': Select(choices=FORMATS),
            'description': Textarea(attrs={'cols': 50, 'rows': 5}),
        }
