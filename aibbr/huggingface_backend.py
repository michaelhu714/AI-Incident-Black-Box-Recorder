# huggingface_backend.py
from transformers import pipeline

# Example model: sentiment analysis
pipe = pipeline("sentiment-analysis")

def hf_sentiment(text):
    result = pipe(text)
    return f"Label: {result[0]['label']}, Score: {result[0]['score']:.3f}"
