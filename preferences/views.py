# Path: /app/preferences/views.py

import requests
from .models import WinePreference, WineRecommendation
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def wine_preferences(request):
    """
    Collects user preferences, saves them, and calls an external API to get wine recommendations.
    """
    if request.method == 'POST':
        wine_type = request.POST.get('wine_type').lower()  # Assuming API expects lowercase values
        budget = float(request.POST.get('budget'))
        grape_region = request.POST.get('grape_region')
        sensory_perception = request.POST.getlist('sensory_perception')
        social_psychological = request.POST.get('social_psychological')
        save_selection = request.POST.get('save_selection')
        selection_name = request.POST.get('selection_name')

        # Save preferences to the database
        preference = WinePreference(
            user=request.user,
            wine_type=wine_type,
            budget=budget,
            grape_region=grape_region,
            sensory_perception=sensory_perception,
            social_psychological=social_psychological,
            selection_name=selection_name if save_selection == 'yes' else ''
        )
        preference.save()

        # Prepare data to send to the external API in the required JSON format
        preference_data = {
            "preference": {
                "type": wine_type,
                "budget": budget,
                "details": {
                    "grape_region": grape_region,
                    "sensory": sensory_perception,
                    "psychology": social_psychological
                },
                "user_id": str(request.user.id)
            }
        }

        # Print the JSON data for debugging
        print("Sending JSON data to API:", preference_data)

        # Define the API URL and headers
        api_url = "http://localhost:3000/api/prompt-gpt"  # Replace with your actual API endpoint
        headers = {
            "x-api-key": "7bc70fdb-fa87-4fd1-8914-971f5b8742aa",  # Replace with your actual token
            "Content-Type": "application/json"  # Define content type as JSON
        }

        # Call the external API
        try:
            response = requests.post(api_url, json=preference_data, headers=headers)
            response.raise_for_status()  # Check if the request was successful
            recommendations = response.json().get('recommendations', [])  # Get the list of recommendations

            # Save each recommendation in the database
            for rec in recommendations:
                WineRecommendation.objects.create(
                    preference=preference,
                    wine_name=rec['wine_name'],
                    region=rec['region'],
                    grape_variety=rec['grape_variety'],
                    price=rec['price'],
                    description=rec['description']
                )

            messages.success(request, 'Preferences saved and recommendations retrieved successfully.')

        except requests.exceptions.RequestException as e:
            messages.error(request, f"Failed to get recommendations: {e}")

        # Redirect to the saved preferences page
        return redirect('view_preferences')  

    return render(request, 'preferences/wine_preferences.html')

@login_required
def view_preferences(request):
    """
    Displays the saved wine preferences and their corresponding recommendations for the logged-in user.
    """
    preferences = WinePreference.objects.filter(user=request.user)  # Fetch preferences for the logged-in user
    return render(request, 'preferences/view_preferences.html', {'preferences': preferences})