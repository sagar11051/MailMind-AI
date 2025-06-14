from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from typing import Dict, Any, List
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

class JSONAgent:
    def __init__(self, hf_token: str = None):
        self.llm = Ollama(
            model="llama2",
            temperature=0,
            base_url="http://localhost:11434"
        )
        
        # Define tools for the agent
        self.tools = [
            Tool(
                name="validate_json",
                func=self._validate_json,
                description="Validates JSON structure and content"
            ),
            Tool(
                name="extract_json_metadata",
                func=self._extract_json_metadata,
                description="Extracts metadata from JSON content"
            ),
            Tool(
                name="process_json_content",
                func=self._process_json_content,
                description="Processes and analyzes JSON content"
            )
        ]
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert JSON processing agent. Your task is to:
            1. Validate JSON structure and content
            2. Extract and analyze metadata
            3. Process and transform JSON data
            4. Generate insights and recommendations
            
            Be thorough and precise in your analysis."""),
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

    def _validate_json(self, content: Any) -> Dict[str, Any]:
        """Validate JSON structure and content"""
        try:
            if isinstance(content, str):
                json.loads(content)
                return {"is_valid": True, "error": None}
            elif isinstance(content, dict):
                json.dumps(content)
                return {"is_valid": True, "error": None}
            else:
                return {"is_valid": False, "error": "Content is not JSON"}
        except json.JSONDecodeError as e:
            return {"is_valid": False, "error": str(e)}

    def _extract_json_metadata(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metadata from JSON content"""
        metadata = {
            "keys": list(content.keys()),
            "depth": self._get_json_depth(content),
            "size": len(str(content)),
            "has_nested": self._has_nested_structures(content),
            "data_types": self._get_data_types(content)
        }
        return metadata

    def _process_json_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Process and analyze JSON content"""
        # Use the LLM to analyze the content
        prompt = f"""Analyze this JSON content and provide:
        1. Main purpose/type of data
        2. Key insights
        3. Potential issues or improvements
        4. Recommended actions
        
        JSON content:
        {json.dumps(content, indent=2)}
        """
        
        response = self.llm.invoke(prompt)
        
        return {
            "analysis": response.content,
            "timestamp": datetime.now().isoformat(),
            "recommendations": self._generate_recommendations(content)
        }

    def _get_json_depth(self, obj: Any, current_depth: int = 0) -> int:
        """Calculate the maximum depth of JSON structure"""
        if not isinstance(obj, dict):
            return current_depth
        
        max_depth = current_depth
        for value in obj.values():
            if isinstance(value, dict):
                depth = self._get_json_depth(value, current_depth + 1)
                max_depth = max(max_depth, depth)
        
        return max_depth

    def _has_nested_structures(self, obj: Any) -> bool:
        """Check if JSON has nested structures"""
        if not isinstance(obj, dict):
            return False
        
        return any(isinstance(value, (dict, list)) for value in obj.values())

    def _get_data_types(self, obj: Any) -> Dict[str, List[str]]:
        """Get unique data types in JSON structure"""
        types = {
            "primitives": set(),
            "complex": set()
        }
        
        def analyze_types(value):
            if isinstance(value, (str, int, float, bool)):
                types["primitives"].add(type(value).__name__)
            elif isinstance(value, (dict, list)):
                types["complex"].add(type(value).__name__)
                if isinstance(value, dict):
                    for v in value.values():
                        analyze_types(v)
                elif isinstance(value, list):
                    for v in value:
                        analyze_types(v)
        
        analyze_types(obj)
        return {k: list(v) for k, v in types.items()}

    def _generate_recommendations(self, content: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on JSON content"""
        recommendations = []
        
        # Check for common issues
        if not content:
            recommendations.append("Empty JSON object - consider adding required fields")
        
        if self._get_json_depth(content) > 3:
            recommendations.append("Deep nesting detected - consider flattening structure")
        
        if len(str(content)) > 10000:
            recommendations.append("Large JSON object - consider splitting into smaller chunks")
        
        # Use LLM for more specific recommendations
        prompt = f"""Based on this JSON content, provide specific recommendations for:
        1. Data structure improvements
        2. Validation rules
        3. Performance optimizations
        
        JSON content:
        {json.dumps(content, indent=2)}
        """
        
        response = self.llm.invoke(prompt)
        recommendations.extend(response.content.split('\n'))
        
        return recommendations

    def process_json(self, json_data: Any) -> Dict[str, Any]:
        """
        Process JSON data and provide analysis
        """
        try:
            # Validate JSON
            validation = self._validate_json(json_data)
            if not validation["is_valid"]:
                return {
                    "error": validation["error"],
                    "status": "error"
                }
            
            # Convert string to dict if needed
            if isinstance(json_data, str):
                json_data = json.loads(json_data)
            
            # Extract metadata
            metadata = self._extract_json_metadata(json_data)
            
            # Process content
            analysis = self._process_json_content(json_data)
            
            return {
                "status": "success",
                "metadata": metadata,
                "analysis": analysis,
                "validation": validation
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "metadata": {},
                "analysis": {}
            } 