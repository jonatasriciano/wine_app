from django import forms
from django.forms.widgets import SelectMultiple
from preferences.models import GrapeRegion


# Custom Widget for GrapeRegion to include flag SVGs
class FlagSelectWidget(SelectMultiple):
    def render_option(self, selected_choices, option_value, option_label):
        # Get the region based on the option_value (which is the primary key)
        region = GrapeRegion.objects.get(id=option_value)
        
        # Assuming the SVGs are located in static/images/flags/4x3/{country_code}.svg
        flag_svg_path = f"/static/images/flags/4x3/{region.country_code}.svg"  # Ensure this matches your static folder structure
        
        # Rendering the option with the flag image next to the label
        return f'''
            <option value="{option_value}" {"selected" if option_value in selected_choices else ""}>
                <img src="{flag_svg_path}" alt="{region.name}" style="width: 20px; height: 15px; margin-right: 10px;">
                {option_label} TESTE
            </option>
        '''

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
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': '10',
            'max': '1000',
            'step': '1',
            'class': 'form-range'
        })
    )

    grape_region = forms.ModelMultipleChoiceField(
        queryset=GrapeRegion.objects.all(),
        widget=FlagSelectWidget(attrs={'class': 'form-select', 'id': 'id_grape_region'})
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