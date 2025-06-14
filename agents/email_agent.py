from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from typing import Dict, Any, List
import os
from dotenv import load_dotenv
import re
from datetime import datetime

load_dotenv()

class EmailAgent:
    def __init__(self, hf_token: str = None):
        self.llm = Ollama(
            model="llama2",
            temperature=0.7,
            base_url="http://localhost:11434"
        )
        
        # Define tools for the agent
        self.tools = [
            Tool(
                name="extract_email_metadata",
                func=self._extract_email_metadata,
                description="Extracts metadata from email content"
            ),
            Tool(
                name="analyze_email_intent",
                func=self._analyze_email_intent,
                description="Analyzes the intent and urgency of the email"
            ),
            Tool(
                name="generate_response",
                func=self._generate_response,
                description="Generates an appropriate response to the email"
            )
        ]
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert email processing agent. Your task is to:
            1. Extract and analyze email metadata
            2. Determine the email's intent and urgency
            3. Generate appropriate responses
            4. Suggest follow-up actions
            
            Be professional, concise, and helpful in your responses."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Create the agent
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Create the agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True
        )

    def _extract_email_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from email content"""
        metadata = {
            "subject": "",
            "sender": "",
            "date": datetime.now().isoformat(),
            "recipients": [],
            "has_attachments": False
        }
        
        # Extract subject
        subject_match = re.search(r"Subject:\s*(.*?)(?:\n|$)", content)
        if subject_match:
            metadata["subject"] = subject_match.group(1).strip()
        
        # Extract sender
        sender_match = re.search(r"From:\s*(.*?)(?:\n|$)", content)
        if sender_match:
            metadata["sender"] = sender_match.group(1).strip()
        
        # Extract recipients
        to_match = re.search(r"To:\s*(.*?)(?:\n|$)", content)
        if to_match:
            metadata["recipients"] = [r.strip() for r in to_match.group(1).split(",")]
        
        # Check for attachments
        metadata["has_attachments"] = "attachment" in content.lower() or "attached" in content.lower()
        
        return metadata

    def _analyze_email_intent(self, content: str) -> Dict[str, Any]:
        """Analyze email intent and urgency"""
        # Use the LLM to analyze intent
        prompt = f"""Analyze this email and determine:
        1. Primary intent (e.g., inquiry, request, complaint, meeting)
        2. Urgency level (low, medium, high)
        3. Required actions
        
        Email content:
        {content}
        """
        
        response = self.llm.invoke(prompt)
        
        return {
            "intent": response.content,
            "urgency": "medium",  # Default urgency
            "required_actions": []
        }

    def _generate_response(self, content: str, metadata: Dict[str, Any], intent: Dict[str, Any]) -> str:
        """Generate an appropriate response to the email"""
        prompt = f"""Generate a professional email response based on:
        - Original email: {content}
        - Metadata: {metadata}
        - Intent analysis: {intent}
        
        The response should be:
        1. Professional and courteous
        2. Address all points in the original email
        3. Clear and concise
        4. Include appropriate next steps if needed
        """
        
        response = self.llm.invoke(prompt)
        return response.content

    def process_email(self, email_content: str) -> Dict[str, Any]:
        """
        Process an email and generate appropriate response
        """
        try:
            # Extract metadata
            metadata = self._extract_email_metadata(email_content)
            
            # Analyze intent
            intent_analysis = self._analyze_email_intent(email_content)
            
            # Generate response
            response = self._generate_response(email_content, metadata, intent_analysis)
            
            # Prepare the final result
            result = {
                "metadata": metadata,
                "intent_analysis": intent_analysis,
                "response": response,
                "suggested_actions": self._get_suggested_actions(intent_analysis)
            }
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "metadata": self._extract_email_metadata(email_content),
                "response": "I apologize, but I encountered an error processing this email. Please try again or contact support."
            }

    def _get_suggested_actions(self, intent_analysis: Dict[str, Any]) -> List[str]:
        """Generate suggested actions based on intent analysis"""
        actions = []
        
        if intent_analysis["urgency"] == "high":
            actions.append("Schedule immediate follow-up")
        
        if "meeting" in intent_analysis["intent"].lower():
            actions.append("Check calendar availability")
            actions.append("Prepare meeting agenda")
        
        if "inquiry" in intent_analysis["intent"].lower():
            actions.append("Gather relevant information")
            actions.append("Prepare detailed response")
        
        return actions 