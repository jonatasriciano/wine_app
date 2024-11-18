from django import forms
from django.forms.widgets import SelectMultiple
from preferences.models import GrapeRegion

# Custom Widget for GrapeRegion to include flag SVGs and the data-mdb-icon attribute
class FlagSelectWidget(SelectMultiple):
    def render_option(self, selected_choices, option_value, option_label):
        # Get the region object based on the option_value
        region = GrapeRegion.objects.get(id=option_value)
        
        # Path to the flag SVG based on the country code
        flag_svg_path = f"/static/images/flags/4x3/{region.country_code}.svg"
        
        # Add data-mdb-icon with the flag URL and the region name
        return f'''
            <option oi value="{option_value}" 
                    {"selected" if option_value in selected_choices else ""} 
                    data-mdb-icon="{flag_svg_path}">
                {option_label}
            </option>
        '''

class WinePreferenceForm(forms.Form):
    WINE_TYPE_CHOICES = [
        ('Red', 'Red'),
        ('White', 'White'),
        ('Rose', 'Rosé'),
    ]

    wine_type = forms.ChoiceField(
        choices=WINE_TYPE_CHOICES,
        widget=forms.RadioSelect,
        error_messages={'required': 'Please select a wine type.'}
    )
    
    budget = forms.DecimalField(
        decimal_places=2,
        required=True,
        initial=50, 
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': '10',
            'max': '1000',
            'step': '1',
            'class': 'form-range'
        }),
        error_messages={'required': 'Please select your budget.'}
    )

    grape_region = forms.ModelMultipleChoiceField(
        queryset=GrapeRegion.objects.all(),
        widget=FlagSelectWidget(attrs={'class': 'form-select', 'id': 'id_grape_region'}),
        error_messages={'required': 'Please select at least one grape region.'}
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
    
    social_psychological = forms.CharField(
        widget=forms.Textarea,
        required=True,
        error_messages={'required': 'Please enter some thoughts on your social/psychological wine preferences.'}
    )
    
    save_selection = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        error_messages={'required': 'Please indicate if you want to save this selection.'}
    )
    
    selection_name = forms.CharField(
        required=False,
        max_length=50,
        error_messages={'max_length': 'The selection name must be less than 50 characters.'}
    )