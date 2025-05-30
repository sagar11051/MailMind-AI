from email import message_from_string
from typing import Dict

def parse_email(raw_email: str) -> Dict:
    msg = message_from_string(raw_email)
    return {
        'from': msg.get('From'),
        'to': msg.get('To'),
        'subject': msg.get('Subject'),
        'body': msg.get_payload()
    } 