import os
import requests
import json

class EmailAgent:
    def __init__(self, hf_token: str):
        self.hf_token = hf_token
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

    def process_email(self, email_text):
        """
        Extracts sender, intent, urgency from email content, formats for CRM.
        """
        prompt = f"""
You are an email processing agent for a CRM system. Given the following email text, extract:
- Sender's email address
- Intent (e.g., Invoice, RFQ, Complaint, Regulation, etc.)
- Urgency (High, Medium, Low)
- Main message body

Input Email:
{email_text}

Respond in JSON:
{{
  \"sender\": \"<email address>\",
  \"intent\": \"<Intent>\",
  \"urgency\": \"<High|Medium|Low>\",
  \"body\": \"<main message>\"
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
            return {'sender': None, 'intent': None, 'urgency': None, 'body': None, 'error': str(e)} 