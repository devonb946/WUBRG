import uuid
from django.forms import ModelForm, Textarea, Select
from builder.models import Deck

class DeckCreationForm(ModelForm):
    class Meta:
        FORMATS = (
            ('Standard', 'Standard'),
            ('Modern', 'Modern'),
            ('Commander', 'Commander'),
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
