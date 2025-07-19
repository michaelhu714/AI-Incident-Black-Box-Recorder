# run_model.py

from aibbr_wrapper import AIBBRWrapper
from dummy_models import uppercase_model, reverse_model, failing_model
from openai_backend import call_openai
from huggingface_backend import hf_sentiment
import sys

# Registry of available models
MODELS = {
    "uppercase": uppercase_model,
    "reverse": reverse_model,
    "fail": failing_model,
    "openai": call_openai,
    "huggingface": hf_sentiment,
}

def main():
    if len(sys.argv) < 3:
        print("Usage: python run_model.py <model_name> <input_text>")
        print("Available models:", list(MODELS.keys()))
        return

    model_name = sys.argv[1].lower()
    input_text = " ".join(sys.argv[2:])

    model_fn = MODELS.get(model_name)
    if not model_fn:
        print(f"Model '{model_name}' not found.")
        return

    wrapper = AIBBRWrapper(model_fn, model_name=model_name)
    result = wrapper(input_text)
    print("Output:", result)

if __name__ == "__main__":
    main()
