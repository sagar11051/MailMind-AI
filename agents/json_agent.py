import json
from typing import Dict, Any, Union, List

class JSONAgent:
    def __init__(self, hf_token: str = None):
        # Token is kept for backward compatibility but not used
        self.hf_token = hf_token

    def process_json(self, json_payload: Union[Dict, str]) -> Dict[str, Any]:
        """
        Processes JSON payload, reformats to target schema, flags anomalies.
        
        Args:
            json_payload: The JSON data to process (can be dict or JSON string)
            
        Returns:
            Dict containing reformatted data and any anomalies found
        """
        try:
            # Parse JSON string if needed
            if isinstance(json_payload, str):
                try:
                    data = json.loads(json_payload)
                except json.JSONDecodeError:
                    return {
                        'reformatted': {},
                        'anomalies': ['Invalid JSON format']
                    }
            else:
                data = json_payload
                
            # Initialize result structure
            result = {
                'reformatted': {},
                'anomalies': []
            }
            
            # Simple reformatting logic
            if isinstance(data, dict):
                # Try to extract common fields
                result['reformatted']['customer'] = data.get('customer') or data.get('user') or 'Unknown'
                result['reformatted']['request_type'] = data.get('type') or data.get('request_type') or 'general'
                
                # Include all other top-level fields in details
                result['reformatted']['details'] = {
                    k: v for k, v in data.items() 
                    if k not in ['customer', 'user', 'type', 'request_type']
                }
                
                # Check for required fields
                if not result['reformatted']['customer']:
                    result['anomalies'].append('Missing customer information')
                    
            else:
                # If it's a list or other JSON type, put it in details
                result['reformatted'] = {
                    'customer': 'Unknown',
                    'request_type': 'data_processing',
                    'details': data
                }
                
            return result
            
        except Exception as e:
            return {
                'reformatted': {},
                'anomalies': [f'Error processing JSON: {str(e)}']
            } 