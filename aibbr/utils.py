# This file provides utility functions for generating IDs and timestamps.

import uuid
from datetime import datetime

def generate_id():
    return str(uuid.uuid4())

def get_timestamp():
    return datetime.utcnow().isoformat()
