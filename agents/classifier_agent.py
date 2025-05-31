import json
from typing import Dict, Any
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

class ClassifierAgent:
    def __init__(self, hf_token: str):
        self.hf_token = hf_token
        self.device = "cpu"  # Force CPU to avoid CUDA memory issues
        # Use a much smaller model
        self.model_name = "google/electra-small-discriminator"
        self.tokenizer = None
        self.model = None
        try:
            self._load_model()
        except Exception as e:
            print(f"Warning: Could not load model: {e}")
            self.model = None
    
    def _load_model(self):
        """Load the model and tokenizer"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name,
                num_labels=3,  # JSON, Email, Text
                id2label={0: "JSON", 1: "Email", 2: "Text"},
                label2id={"JSON": 0, "Email": 1, "Text": 2}
            ).to(self.device)
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

    def classify_and_route(self, input_data) -> Dict[str, Any]:
        """
        Classify the input data and determine the appropriate route.
        
        Args:
            input_data: The input data to classify
            
        Returns:
            Dict containing classification results
        """
        # Simple heuristic fallback if model loading failed
        if self.model is None:
            return self._fallback_classification(input_data)
        
        try:
            # Convert input to string if it's a dictionary
            if isinstance(input_data, dict):
                text = json.dumps(input_data)
            else:
                text = str(input_data)
            
            # Tokenize and predict
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(self.device)
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Get predicted class
            predicted_class = torch.argmax(outputs.logits, dim=1).item()
            format_type = self.model.config.id2label.get(predicted_class, "Text")
            
            # Determine route and intent based on format
            if format_type == "JSON":
                return {
                    "format": "JSON",
                    "intent": "Data Processing",
                    "route_to": "json_agent"
                }
            elif format_type == "Email":
                return {
                    "format": "Email",
                    "intent": "Communication",
                    "route_to": "email_agent"
                }
            else:
                return {
                    "format": "Text",
                    "intent": "General Processing",
                    "route_to": "json_agent"
                }
                
        except Exception as e:
            print(f"Classification error: {e}")
            return self._fallback_classification(input_data)
    
    def _fallback_classification(self, input_data) -> Dict[str, str]:
        """Fallback classification using simple heuristics"""
        text = str(input_data).lower()
        
        # Check for email patterns
        if any(term in text for term in ['@', 'subject:', 'dear', 'hi ', 'hello', 'regards', 'thanks', 'thank you', 'sincerely']):
            return {
                "format": "Email",
                "intent": "Communication",
                "route_to": "email_agent"
            }
            
        # Check for JSON-like content
        if isinstance(input_data, dict) or (text.strip().startswith('{') and text.strip().endswith('}')):
            return {
                "format": "JSON",
                "intent": "Data Processing",
                "route_to": "json_agent"
            }
            
        # Default to text processing
        return {
            "format": "Text",
            "intent": "General Processing",
            "route_to": "json_agent"
        } 