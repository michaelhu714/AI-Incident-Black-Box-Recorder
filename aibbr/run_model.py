# run_model.py
import argparse
from main import AIBBRWrapper

# Example dummy backends
def dummy_upper(text):
    return text.upper()

def dummy_reverse(text):
    return text[::-1]

def dummy_fail(text):
    raise ValueError("Simulated failure")

# Backend registry
MODEL_BACKENDS = {
    "upper": dummy_upper,
    "reverse": dummy_reverse,
    "fail": dummy_fail,
}

def main():
    parser = argparse.ArgumentParser(description="Run a model with AIBBR logging.")
    parser.add_argument("--backend", choices=MODEL_BACKENDS.keys(), required=True, help="Which model backend to use")
    parser.add_argument("--input", required=True, help="Input string to send to the model")
    args = parser.parse_args()

    model_fn = MODEL_BACKENDS[args.backend]
    wrapped = AIBBRWrapper(model_fn, model_name=args.backend)

    print("\nMODEL OUTPUT:")
    print(wrapped.predict(args.input))

if __name__ == "__main__":
    main()
