from django.conf import settings
import requests
import json  # Certifique-se de importar o módulo json

def fetch_wine_recommendations(preference):
    """
    Generates a natural language prompt based on user preferences and calls the external API
    to receive recommendations in JSON format.
    """
    # Create a natural language description based on user preferences
    prompt_text = (
        f"I am looking for a {preference['wine_type']} wine with a budget of ${preference['budget']:.2f}. "
        f"My preference is for wines from {preference['grape_region']}. I am interested in wines with "
        f"the following sensory characteristics: {', '.join(preference['sensory_perception'])}. "
        f"Additionally, I am looking for a wine that would suit a {preference['social_psychological']} setting. "
        "Please return at least 5 wine recommendations as a JSON object with each wine having fields: "
        "'wine_name', 'region', 'grape_variety', 'price'(in decimals), and 'description'."
    )
    
    api_url = settings.API_URL
    headers = {
        "x-api-key": settings.API_KEY,
        "Content-Type": "application/json",
    }

    # Make the POST request to the API
    response = requests.post(api_url, json={"prompt": prompt_text, "tokens": 1000}, headers=headers)
    response.raise_for_status()  # Raise an error if the status is not 200

    # Get the response text
    response_data_str = response.text  # Get the response text

    # Convert the response string to a JSON object
    try:
        response_data = json.loads(response_data_str)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return []  # Return an empty list if there is an error

    # Verificar se a chave 'message' está presente
    if 'message' in response_data:
        try:
            # Carregar a string JSON dentro de 'message'
            wine_info = json.loads(response_data['message'])
            # Retornar a lista de vinhos diretamente
            return wine_info.get('wines', [])  # Retorna a lista de vinhos ou uma lista vazia
        except json.JSONDecodeError as e:
            print("Error decoding JSON in 'message':", e)
            return []  # Retornar uma lista vazia se houver um erro
    else:
        print("No 'message' key in response data.")
        return []  # Retornar uma lista vazia se a chave não estiver presente