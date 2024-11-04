from django.contrib import messages

def validate_and_parse_budget(budget):
    """
    Validates and parses the budget field.
    """
    try:
        return float(budget)
    except (ValueError, TypeError):
        raise ValueError("Invalid budget value. Please enter a number.")