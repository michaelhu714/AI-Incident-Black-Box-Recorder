# web_input.py
import streamlit as st
from main import AIBBRWrapper

# Dummy backend models
def dummy_upper(text):
    return text.upper()

def dummy_reverse(text):
    return text[::-1]

def dummy_fail(text):
    raise ValueError("Simulated failure")

# Registry of models
MODEL_BACKENDS = {
    "Uppercase Model": dummy_upper,
    "Reverse Model": dummy_reverse,
    "Failing Model": dummy_fail,
}

# Streamlit app
st.set_page_config(page_title="Run AI Model", layout="centered")
st.title("Test an AI Model")

model_name = st.selectbox("Select a model backend", list(MODEL_BACKENDS.keys()))
user_input = st.text_area("Enter input text")

if st.button("Run Model") and user_input:
    model_fn = MODEL_BACKENDS[model_name]
    wrapped = AIBBRWrapper(model_fn, model_name=model_name)

    try:
        result = wrapped.predict(user_input)
        st.success("Model Output:")
        st.code(result, language="text")
    except Exception as e:
        st.error(f"Model error: {e}")
