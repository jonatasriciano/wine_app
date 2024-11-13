from django import forms
from preferences.models import GrapeRegion
from django.forms.widgets import SelectMultiple

# Custom Widget for BsMultiSelect with flags
class FlagBsMultiSelectWidget(forms.SelectMultiple):
    def render_option(self, selected_choices, option_value, option_label):
        try:
            region = GrapeRegion.objects.get(id=option_value)
            flag_svg_path = f"/static/images/flags/4x3/{region.country_code}.svg" if region.country_code else "/static/images/flags/default.svg"
        except GrapeRegion.DoesNotExist:
            flag_svg_path = "/static/images/flags/default.svg"

        # Render HTML for BsMultiSelect options
        return f'''
            <option value="{option_value}" {"selected" if option_value in selected_choices else ""}>
                <img src="{flag_svg_path}" alt="{region.name}" style="width: 20px; height: 15px; margin-right: 10px;">
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
        widget=FlagBsMultiSelectWidget(attrs={'class': 'form-select', 'id': 'id_grape_region'}),
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