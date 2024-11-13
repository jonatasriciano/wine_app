import json
import requests
from django.conf import settings

def fetch_wine_recommendations(preference):
    """
    Generate a natural language prompt based on user preferences and request wine recommendations
    from an external API. Returns a list of wine recommendations in JSON format.
    """
    prompt_text = (
        f"I am looking for a {preference['wine_type']} wine with a budget of ${preference['budget']:.2f}. "
        f"My preference is for wines from {preference['grape_region']}. I am interested in wines with "
        f"the following sensory characteristics: {', '.join(preference['sensory_perception'])}. "
        f"Additionally, I am looking for a wine that would suit a {preference['social_psychological']} setting. "
        "Please return at least 5 wine recommendations as a JSON object with each wine having fields: "
        "'wine_name', 'region', 'grape_variety', 'price' (in decimals), 'description', 'link'. "
        "IMPORTANT: Only send the information 'link' if the link is real and functional."
    )

    # Define headers and API URL
    api_url = settings.API_URL
    headers = {
        "x-api-key": settings.API_KEY,
        "Content-Type": "application/json",
    }

    # Make the POST request to the API
    try:
        response = requests.post(api_url, json={"prompt": prompt_text, "tokens": 1000}, headers=headers)
        response.raise_for_status()  # Ensure the request was successful
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []  # Return empty list on request error

    # Parse the response JSON
    try:
        response_data = response.json()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return []  # Return empty list if JSON decoding fails

    # Check if the response contains the 'message' key and process it
    if 'message' in response_data:
        try:
            wine_info = json.loads(response_data['message'])  # Parse the 'message' field
            return wine_info.get('wines', [])  # Return the wine list or an empty list if not found
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in 'message': {e}")
            return []  # Return an empty list if there's a decoding issue in 'message'
    else:
        print("No 'message' key found in response data.")
        return []  # Return empty list if 'message' key is absent