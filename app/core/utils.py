import json
import re
from datetime import datetime


def preprocess_for_json(data):
    if isinstance(data, dict):
        return {k: preprocess_for_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [preprocess_for_json(v) for v in data]
    elif isinstance(data, ValueError):
        return str(data)
    return data


def convert_to_readable(text):
    # Add a space before each capital letter followed by a lowercase letter
    readable_text = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)
    # Add a space before each capital letter preceded by a lowercase letter
    readable_text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', readable_text)
    # Convert to title case
    readable_text = readable_text.title()
    return readable_text


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
