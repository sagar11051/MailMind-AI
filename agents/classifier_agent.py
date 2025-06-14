from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class ClassifierAgent:
    def __init__(self, hf_token: str = None):
        self.llm = Ollama(
            model="llama2",
            temperature=0,
            base_url="http://localhost:11434"
        )
        
        # Define tools for the agent
        self.tools = [
            Tool(
                name="classify_content",
                func=self._classify_content,
                description="Classifies the content type and determines the appropriate route"
            ),
            Tool(
                name="extract_metadata",
                func=self._extract_metadata,
                description="Extracts relevant metadata from the content"
            )
        ]
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert content classifier and router. Your task is to:
            1. Analyze the input content
            2. Determine its type (email, JSON, text, etc.)
            3. Extract relevant metadata
            4. Route it to the appropriate processing agent
            
            Available routes:
            - json_agent: For structured JSON data
            - email_agent: For email content
            - text_agent: For plain text content
            
            Provide detailed reasoning for your classification."""),
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

    def _classify_content(self, content: str) -> Dict[str, Any]:
        """Helper function to classify content type"""
        if isinstance(content, dict):
            return {"type": "json", "confidence": 0.95}
        elif "@" in content and ("Subject:" in content or "From:" in content):
            return {"type": "email", "confidence": 0.95}
        else:
            return {"type": "text", "confidence": 0.95}

    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Helper function to extract metadata"""
        metadata = {
            "content_length": len(str(content)),
            "has_attachments": False,
            "is_structured": isinstance(content, dict)
        }
        return metadata

    def classify_and_route(self, input_data: Any) -> Dict[str, Any]:
        """
        Classifies the input data and determines the appropriate route
        """
        try:
            # Prepare the input for the agent
            agent_input = {
                "input": f"Please analyze and classify this content: {str(input_data)}"
            }
            
            # Run the agent
            result = self.agent_executor.invoke(agent_input)
            
            # Process the agent's response
            classification = result.get("output", {})
            
            # Determine the route based on classification
            if isinstance(input_data, dict):
                route = "json_agent"
            elif "@" in str(input_data) and ("Subject:" in str(input_data) or "From:" in str(input_data)):
                route = "email_agent"
            else:
                route = "text_agent"
            
            return {
                "route_to": route,
                "classification": classification,
                "confidence": 0.95,
                "metadata": self._extract_metadata(input_data)
            }
            
        except Exception as e:
            return {
                "route_to": "text_agent",  # Default route
                "error": str(e),
                "confidence": 0.0
            } 