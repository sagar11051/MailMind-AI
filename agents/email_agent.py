import openai

class EmailAgent:
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
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0
            )
            import json
            content = response['choices'][0]['message']['content']
            return json.loads(content)
        except Exception as e:
            return {'sender': None, 'intent': None, 'urgency': None, 'body': None, 'error': str(e)} 