# preferences/forms.py

from django import forms

class WinePreferenceForm(forms.Form):
    WINE_TYPE_CHOICES = [
        ('Red', 'Red'),
        ('White', 'White'),
        ('Rose', 'Rose'),
    ]
    
    wine_type = forms.ChoiceField(choices=WINE_TYPE_CHOICES, widget=forms.RadioSelect)
    budget = forms.DecimalField(decimal_places=2, required=True)
    grape_region = forms.CharField(widget=forms.Textarea, required=True)
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