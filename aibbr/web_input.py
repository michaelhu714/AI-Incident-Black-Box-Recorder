# web_input.py (updated with backend dropdown)
import streamlit as st
from aibbr_wrapper import AIBBRWrapper
from dummy_models import uppercase_model, reverse_model, failing_model
from openai_backend import call_openai
from huggingface_backend import hf_sentiment

# Model registry
MODELS = {
    "Uppercase": uppercase_model,
    "Reverse": reverse_model,
    "Failing Model": failing_model,
    "OpenAI GPT": call_openai,
    "HuggingFace Sentiment": hf_sentiment,
}

st.title("AIBBR: AI Behavior BlackBox Recorder")
st.write("Test various models and log their behavior.")

model_name = st.selectbox("Choose a model backend:", list(MODELS.keys()))
user_input = st.text_area("Enter your input:", "Hello world!")

if st.button("Run Model"):
    model_fn = MODELS[model_name]
    wrapper = AIBBRWrapper(model_fn, model_name=model_name)
    output = wrapper(user_input)
    st.subheader("Output")
    st.write(output)
