from main import AIBBRWrapper

def dummy_model(text):
    if "error" in text:
        raise ValueError("Model failed")
    return text.upper()

if __name__ == "__main__":
    wrapped = AIBBRWrapper(dummy_model, model_name="DummyUpper")

    print(wrapped.predict("hello"))
    print(wrapped.predict("cause error"))
    wrapped.tag_last("manual_crash")
