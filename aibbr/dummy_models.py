# dummy_models.py

def uppercase_model(text):
    """Simple model that returns uppercase version of the input."""
    return text.upper()

def reverse_model(text):
    """Reverses the input text."""
    return text[::-1]

def failing_model(text):
    """Intentionally throws an error for testing purposes."""
    raise RuntimeError("This model always fails.")
