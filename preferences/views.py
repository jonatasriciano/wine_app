from django.shortcuts import render
from django.http import JsonResponse
from .forms import WinePreferenceForm
from .services import fetch_wine_recommendations
from django.contrib.auth.decorators import login_required
from .models import WinePreference, WineRecommendation

@login_required
def wine_preferences(request):
    """
    View for submitting wine preferences.
    Expects a POST request with user preferences in the form.
    Returns a JSON response with recommended wines.
    """
    if request.method == 'POST':
        form = WinePreferenceForm(request.POST)
        
        if form.is_valid():
            # Get cleaned data from the form
            preferences_data = form.cleaned_data
            
            # Call the service with the preferences dictionary
            recommendations = fetch_wine_recommendations(preferences_data)

            # Create a WinePreference object
            wine_preference = WinePreference.objects.create(
                user=request.user,
                wine_type=preferences_data['wine_type'],
                budget=preferences_data['budget'],
                grape_region=preferences_data['grape_region'],
                sensory_perception=preferences_data['sensory_perception'],
                social_psychological=preferences_data['social_psychological'],
                selection_name=form.cleaned_data['selection_name']
            )
            
            if isinstance(recommendations, list) and recommendations:  # Verifique se é uma lista e não vazia
                # Salvar cada recomendação em WineRecommendation
                for wine_data in recommendations:
                    # Verificar se wine_data é um dicionário e contém a chave 'wine_name'
                    if isinstance(wine_data, dict) and 'wine_name' in wine_data:
                        WineRecommendation.objects.create(
                            preference=wine_preference,
                            wine_name=wine_data.get('wine_name'),
                            region=wine_data.get('region'),
                            grape_variety=wine_data.get('grape_variety'),
                            price=wine_data.get('price'),  # Certifique-se de que o preço está no formato correto
                            description=wine_data.get('description')
                        )
                    else:
                        print("Invalid wine data format or missing 'wine_name':", wine_data)
            else:
                return JsonResponse({'status': 'error', 'message': 'No valid recommendations received from the API.'}, status=400)

            return JsonResponse({'status': 'success', 'recommendations': recommendations}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data.'}, status=400)

    else:
        # Create a new form instance for GET requests
        form = WinePreferenceForm()

    # Render the form in the template for GET requests
    return render(request, 'preferences/wine_preferences.html', {'form': form})

@login_required
def view_preferences(request):
    """
    Displays the saved wine preferences and their corresponding recommendations for the logged-in user.
    """
    # Fetch all saved preferences for the logged-in user
    preferences = WinePreference.objects.filter(user=request.user)
    return render(request, 'preferences/view_preferences.html', {'preferences': preferences})