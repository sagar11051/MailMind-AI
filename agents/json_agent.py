import os
import requests
import json

class JSONAgent:
    def __init__(self, hf_token: str):
        self.hf_token = hf_token
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

    def process_json(self, json_payload):
        """
        Processes JSON payload, reformats to target schema, flags anomalies.
        """
        prompt = f"""
You are a data validation and transformation agent. Given the following JSON payload, extract and reformat the data to match this target schema:
{{
  \"customer\": ...,
  \"request_type\": ...,
  \"details\": ...
}}
If any required fields are missing or anomalous, flag them in an \"anomalies\" field.

Input JSON:
{json_payload}

Respond in JSON:
{{
  \"reformatted\": {{ ... }},
  \"anomalies\": [ ... ]
}}
"""
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        payload = {"inputs": prompt}
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            if isinstance(result, list):
                content = result[0].get('generated_text', '')
            else:
                content = result.get('generated_text', '')
            return json.loads(content)
        except Exception as e:
            return {'reformatted': {}, 'anomalies': [str(e)]} 