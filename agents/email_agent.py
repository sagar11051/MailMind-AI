import re
import json
from datetime import datetime
from typing import Dict, Any

class EmailAgent:
    def __init__(self, hf_token: str):
        self.hf_token = hf_token

    def process_email(self, email_text: str) -> Dict[str, Any]:
        """
        Processes email content to extract key information and generate a response.
        
        Args:
            email_text: The email content to process
            
        Returns:
            Dict containing extracted information and suggested response
        """
        try:
            # Extract sender information
            email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', email_text)
            sender_email = email_match.group(0) if email_match else "unknown@example.com"
            
            # Extract sender name if available
            name_match = re.search(r'(?i)(?:from|sender|sent by)[\s:]*([^<\n<]+)', email_text)
            sender_name = name_match.group(1).strip() if name_match else ""
            
            # Extract subject if available
            subject_match = re.search(r'(?i)subject:[\s]*(.*?)(?:\n|$)', email_text)
            subject = subject_match.group(1).strip() if subject_match else "No Subject"
            
            # Process email content
            intent = self._detect_intent(email_text)
            urgency = self._detect_urgency(email_text)
            body = self._extract_body(email_text)
            
            # Generate response based on intent
            response = self._generate_response(intent, sender_name, subject)
            
            return {
                "metadata": {
                    "sender_email": sender_email,
                    "sender_name": sender_name,
                    "subject": subject,
                    "intent": intent,
                    "urgency": urgency,
                    "received_at": datetime.now().isoformat()
                },
                "content": {
                    "body": body,
                    "response": response,
                    "suggested_actions": self._get_suggested_actions(intent)
                }
            }
            
        except Exception as e:
            return {
                "error": f"Error processing email: {str(e)}",
                "metadata": {
                    "sender_email": "",
                    "sender_name": "",
                    "subject": "Error Processing Email",
                    "intent": "Error",
                    "urgency": "High",
                    "received_at": datetime.now().isoformat()
                },
                "content": {
                    "body": email_text[:500] + ("..." if len(email_text) > 500 else ""),
                    "response": "We encountered an error processing your email. Our team has been notified.",
                    "suggested_actions": ["Review manually"]
                }
            }
    
    def _generate_response(self, intent: str, sender_name: str, subject: str) -> str:
        """Generate a response template based on the detected intent"""
        name = sender_name.split(' ')[0] if sender_name else "there"
        
        responses = {
            "Demo Request": (
                f"Hi {name},\n\n"
                "Thank you for your interest in our AI solutions! We'd be happy to schedule a demo for you. "
                "Our team will reach out shortly to find a convenient time.\n\n"
                "Best regards,\nThe AI Solutions Team"
            ),
            "Information Request": (
                f"Hello {name},\n\n"
                "Thank you for reaching out! We've attached our latest product brochure and pricing information. "
                "Please let us know if you have any specific questions.\n\n"
                "Best regards,\nThe AI Solutions Team"
            ),
            "Meeting Request": (
                f"Hi {name},\n\n"
                "We'd be happy to schedule a call to discuss {subject or 'this matter'}. "
                "Please let us know your availability for the next few days.\n\n"
                "Best regards,\nThe AI Solutions Team"
            ),
            "General Inquiry": (
                f"Hello {name},\n\n"
                "Thank you for your message. We've received your inquiry and will get back to you "
                "with more information soon.\n\n"
                "Best regards,\nThe AI Solutions Team"
            )
        }
        
        return responses.get(intent, responses["General Inquiry"])
    
    def _get_suggested_actions(self, intent: str) -> list:
        """Get suggested actions based on the email intent"""
        actions = {
            "Demo Request": ["Schedule demo", "Send product info", "Assign to sales"],
            "Information Request": ["Send brochure", "Share pricing", "Schedule call"],
            "Meeting Request": ["Check calendar", "Propose times", "Assign to team member"],
            "Support/Complaint": ["Create support ticket", "Escalate to manager", "Request more info"]
        }
        return actions.get(intent, ["Review manually"])
    
    def _detect_intent(self, text: str) -> str:
        """Enhanced intent detection based on keywords and patterns"""
        text = text.lower()
        
        # Check for specific patterns first
        if any(term in text for term in ['demo', 'demonstration', 'show me', 'show us']):
            return "Demo Request"
            
        if any(term in text for term in ['brochure', 'information', 'details', 'learn more']):
            return "Information Request"
            
        if any(term in text for term in ['invoice', 'payment', 'bill']):
            return "Invoice/Payment"
            
        if any(term in text for term in ['rfq', 'quote', 'pricing', 'how much']):
            return "Pricing Inquiry"
            
        if any(term in text for term in ['complaint', 'issue', 'problem', 'not working']):
            return "Support/Complaint"
            
        if any(term in text for term in ['meeting', 'schedule', 'appointment', 'call', 'discuss']):
            return "Meeting Request"
            
        if any(term in text for term in ['partnership', 'collaborate', 'work together']):
            return "Partnership Inquiry"
            
        if any(term in text for term in ['hi ', 'hello', 'dear', 'good morning', 'good afternoon']):
            return "General Inquiry"
            
        return "General Inquiry"
    
    def _detect_urgency(self, text: str) -> str:
        """Simple urgency detection based on keywords"""
        text = text.lower()
        if any(word in text for word in ['urgent', 'asap', 'immediately', 'right away']):
            return "High"
        elif any(word in text for word in ['soon', 'prompt', 'quick']):
            return "Medium"
        return "Low"
    
    def _extract_body(self, text: str) -> str:
        """Extract the main message body from email text"""
        # Simple approach: take first 200 chars or first paragraph
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith(('From:', 'To:', 'Subject:', 'Date:')):
                return '\n'.join(lines[i:i+5])[:500]  # Return first 5 lines or 500 chars
        return text[:500]  # Fallback to first 500 chars 