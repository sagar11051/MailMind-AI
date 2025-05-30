import openai

class JSONAgent:
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
            return {'reformatted': {}, 'anomalies': [str(e)]} 