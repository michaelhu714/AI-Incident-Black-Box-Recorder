# Wrapper class to wrap any model

from logger import log_entry
from utils import get_timestamp, generate_id
import time

class AIBBRWrapper:
    def __init__(self, model, model_name="UnknownModel"):
        self.model = model
        self.model_name = model_name

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
