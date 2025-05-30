import openai
from typing import Any, Dict

class ClassifierAgent:
    def __init__(self, openai_api_key: str):
        openai.api_key = openai_api_key

    def classify_and_route(self, input_data: Any) -> Dict[str, Any]:
        """
        Classifies the input format and intent, and determines routing.
        Returns a dict with 'format', 'intent', and 'route_to'.
        """
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
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0
            )
            import json
            content = response['choices'][0]['message']['content']
            return json.loads(content)
        except Exception as e:
            return {'format': None, 'intent': None, 'route_to': None, 'error': str(e)} 