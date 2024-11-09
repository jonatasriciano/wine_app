# preferences/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import WinePreferenceForm
from .services import fetch_wine_recommendations
from .models import WinePreference, WineRecommendation, GrapeRegion

@login_required
def wine_preferences(request):
    if request.method == 'POST':
        form = WinePreferenceForm(request.POST)
        
        if form.is_valid():
            preferences_data = form.cleaned_data
            recommendations = fetch_wine_recommendations(preferences_data)

            wine_preference = WinePreference.objects.create(
                user=request.user,
                wine_type=preferences_data['wine_type'],
                budget=preferences_data['budget'],
                sensory_perception=preferences_data['sensory_perception'],
                social_psychological=preferences_data['social_psychological'],
                selection_name=form.cleaned_data['selection_name']
            )
            wine_preference.grape_region.set(preferences_data['grape_region'])  # Salva as grape_regions selecionadas

            if isinstance(recommendations, list) and recommendations:
                for wine_data in recommendations:
                    if isinstance(wine_data, dict) and 'wine_name' in wine_data:
                        WineRecommendation.objects.create(
                            preference=wine_preference,
                            wine_name=wine_data.get('wine_name'),
                            region=wine_data.get('region'),
                            grape_variety=wine_data.get('grape_variety'),
                            price=wine_data.get('price'),
                            description=wine_data.get('description')
                        )
            else:
                return JsonResponse({'status': 'error', 'message': 'No valid recommendations received from the API.'}, status=400)

            return JsonResponse({'status': 'success', 'recommendations': recommendations}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data.'}, status=400)

    else:
        form = WinePreferenceForm()

    # Passamos grape_regions manualmente para o template
    return render(request, 'preferences/wine_preferences.html', {
        'form': form,
        'grape_regions': GrapeRegion.objects.all(),
    })

@login_required
def view_preferences(request):
    preferences = WinePreference.objects.filter(user=request.user)
    return render(request, 'preferences/view_preferences.html', {'preferences': preferences})