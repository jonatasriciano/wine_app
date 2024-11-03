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
    # Initialize variables for both POST and GET requests
    json_data = None  # To store JSON data sent to the API
    api_response = None  # To store API response
    api_url = None  # Define the API URL
    headers = {}  # Define headers for API request
    preference_data = None  # Placeholder for data sent to API

    if request.method == 'POST':
        # Retrieve data from the form
        wine_type = request.POST.get('wine_type').lower() if request.POST.get('wine_type') else None
        budget = request.POST.get('budget')
        grape_region = request.POST.get('grape_region')
        sensory_perception = request.POST.getlist('sensory_perception')
        social_psychological = request.POST.get('social_psychological')
        save_selection = request.POST.get('save_selection')
        selection_name = request.POST.get('selection_name')

        # Validate required fields
        if not wine_type or not budget or not grape_region:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'preferences/wine_preferences.html')

        # Convert budget to float and handle invalid entries
        try:
            budget = float(budget)
        except ValueError:
            messages.error(request, "Invalid budget value.")
            return render(request, 'preferences/wine_preferences.html')

        # Save the user's preferences to the database
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

        # Prepare JSON data for the external API
        preference_data = {
            "prompt": "Give me 3 wine recommendations based on my preferences",
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
        json_data = preference_data  # Store JSON data for display

        # Define the API URL and headers
        api_url = "http://ai-integration:3000/api/prompt-gpt"  # Ensure service name 'app' matches in Docker Compose
        headers = {
            "x-api-key": "7bc70fdb-fa87-4fd1-8914-971f5b8742aa",  # Replace with actual token
            "Content-Type": "application/json"
        }

        # Make API request
        try:
            response = requests.post(api_url, json=preference_data, headers=headers)
            response.raise_for_status()  # Trigger error for unsuccessful status codes
            api_response = response.json()  # Parse JSON response

            # Extract and save recommendations
            recommendations = api_response.get('recommendations', [])
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

        except requests.RequestException as e:
            messages.error(request, f"Failed to get recommendations: {e}")
            print("Error with Node.js API call:", e)  # Print error details for debugging

    # Render the template with context data
    return render(request, 'preferences/wine_preferences.html', {
        'json_data': json_data,  # JSON data sent to the API
        'api_response': api_response,  # Response received from the API
        'api_url': api_url,  # API URL for display
        'api_header': headers,  # API headers for display
        'api_data': preference_data  # Data payload for display
    })

@login_required
def view_preferences(request):
    """
    Displays the saved wine preferences and their corresponding recommendations for the logged-in user.
    """
    # Fetch all saved preferences and recommendations for the logged-in user
    preferences = WinePreference.objects.filter(user=request.user)
    return render(request, 'preferences/view_preferences.html', {'preferences': preferences})