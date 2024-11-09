# preferences/forms.py

from django import forms
from django.forms.widgets import NumberInput
from preferences.models import GrapeRegion

class WinePreferenceForm(forms.Form):
    WINE_TYPE_CHOICES = [
        ('Red', 'Red'),
        ('White', 'White'),
        ('Rose', 'Rosé'),
    ]
    
    wine_type = forms.ChoiceField(choices=WINE_TYPE_CHOICES, widget=forms.RadioSelect)
    
    budget = forms.DecimalField(
        decimal_places=2,
        required=True,
        widget=NumberInput(attrs={
            'type': 'range',         
            'min': '10',
            'max': '1000',
            'step': '1',
            'class': 'form-range'
        })
    )

    grape_region = forms.ModelMultipleChoiceField(
        queryset=GrapeRegion.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    sensory_perception = forms.MultipleChoiceField(
        choices=[
            ('Taste', 'Taste'),
            ('Aroma', 'Aroma'),
            ('Appearance', 'Appearance'),
            ('Body', 'Body'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    
    social_psychological = forms.CharField(widget=forms.Textarea, required=True)
    save_selection = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')])
    selection_name = forms.CharField(required=False)