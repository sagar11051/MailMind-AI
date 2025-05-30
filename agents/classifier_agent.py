import os
import requests
import json

class ClassifierAgent:
    def __init__(self, hf_token: str):
        self.hf_token = hf_token
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

    def classify_and_route(self, input_data):
        prompt = f"""
You are an AI assistant for document triage. Given the following input, identify:
- The input format (PDF, JSON, or Email)
- The business intent (Invoice, RFQ, Complaint, Regulation, etc.)
- Which specialized agent should process it: \"json_agent\" for JSON, \"email_agent\" for Email, or \"pdf_agent\" for PDF.

Input:
{input_data}

Respond in JSON:
{{
  \"format\": \"<PDF|JSON|Email>\",
  \"intent\": \"<Intent>\",
  \"route_to\": \"<json_agent|email_agent|pdf_agent>\"
}}
"""
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        payload = {"inputs": prompt}
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            # The response is a list of dicts with 'generated_text'
            result = response.json()
            if isinstance(result, list):
                content = result[0].get('generated_text', '')
            else:
                content = result.get('generated_text', '')
            return json.loads(content)
        except Exception as e:
            return {'format': None, 'intent': None, 'route_to': None, 'error': str(e)} 