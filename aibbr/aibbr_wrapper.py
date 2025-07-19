# Wrapper class to wrap any model

from logger import log_entry, log_interaction
from utils import get_timestamp, generate_id
import time

class AIBBRWrapper:
    def __init__(self, model_fn, model_name="unknown"):
        self.model_fn = model_fn
        self.model_name = model_name

    def __call__(self, input_text):
        return self.run(input_text)

    def run(self, input_text):
        try:
            result = self.model_fn(input_text)
            log_interaction(input_text, result, self.model_name, status="success")
            return result
        except Exception as e:
            error_msg = f"Model error: {e}"
            log_interaction(input_text, error_msg, self.model_name, status="error")
            return error_msg

    def predict(self, input_data):
        start = time.time()
        try:
            output = self.model(input_data)
            success = True
        except Exception as e:
            output = str(e)
            success = False

        log_entry({
            "id": generate_id(),
            "timestamp": get_timestamp(),
            "model_name": self.model_name,
            "input": input_data,
            "output": output,
            "success": success,
            "latency_sec": round(time.time() - start, 4),
            "tags": []
        })

        return output

    def tag_last(self, tag):
        from logger import tag_last_entry
        tag_last_entry(tag)
