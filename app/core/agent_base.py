"""
Base class for all autonomous Claude AI agents in the ASPICE platform.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel
import asyncio
import logging
from anthropic import AsyncAnthropic
from datetime import datetime

logger = logging.getLogger(__name__)


class AgentContext(BaseModel):
    """Context information passed to agents"""
    project_id: str
    user_id: str
    session_id: str
    metadata: Dict[str, Any] = {}


class AgentResponse(BaseModel):
    """Standardized response from agents"""
    success: bool
    data: Any = None
    message: str = ""
    confidence: float = 0.0
    reasoning: str = ""
    next_actions: List[str] = []
    timestamp: datetime = datetime.now()


class AutonomousAgent(ABC):
    """
    Base class for all autonomous Claude AI agents.
    Each agent specializes in a specific aspect of ASPICE consulting.
    """
    
    def __init__(self, name: str, anthropic_client: AsyncAnthropic, system_prompt: str):
        self.name = name
        self.anthropic_client = anthropic_client
        self.system_prompt = system_prompt
        self.conversation_history: List[Dict[str, str]] = []
        
    @abstractmethod
    async def process(self, input_data: Any, context: AgentContext) -> AgentResponse:
        """
        Main processing method that each agent must implement.
        This is where the autonomous decision-making happens.
        """
        pass
    
    async def _call_claude(self, user_message: str, context: AgentContext) -> str:
        """
        Internal method to call Claude API with the agent's system prompt
        """
        try:
            # Build conversation with system prompt and history
            messages = []
            
            # Add conversation history
            for msg in self.conversation_history[-10:]:  # Keep last 10 messages
                messages.append(msg)
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": f"Context: {context.dict()}\n\nRequest: {user_message}"
            })
            
            response = await self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                system=self.system_prompt,
                messages=messages
            )
            
            assistant_response = response.content[0].text
            
            # Update conversation history
            self.conversation_history.append({
                "role": "user", 
                "content": user_message
            })
            self.conversation_history.append({
                "role": "assistant", 
                "content": assistant_response
            })
            
            return assistant_response
            
        except Exception as e:
            logger.error(f"Error calling Claude API in {self.name}: {str(e)}")
            raise
    
    async def think(self, problem: str, context: AgentContext) -> str:
        """
        Allow the agent to 'think' about a problem before taking action
        """
        thinking_prompt = f"""
        As the {self.name}, I need to think through this problem:
        
        {problem}
        
        Please provide your reasoning process, considering:
        1. What information do I have?
        2. What information do I need?
        3. What are the possible approaches?
        4. What is the best course of action?
        5. What are the potential risks or considerations?
        
        Provide a structured thinking process.
        """
        
        return await self._call_claude(thinking_prompt, context)
    
    async def collaborate(self, other_agent: 'AutonomousAgent', message: str, context: AgentContext) -> str:
        """
        Enable agents to collaborate with each other
        """
        collaboration_prompt = f"""
        I need to collaborate with the {other_agent.name} agent.
        
        Message to send: {message}
        
        Please format this as a clear, professional communication that includes:
        1. What I need from them
        2. What context they should know
        3. Any specific requirements or constraints
        4. Expected timeline or priority
        """
        
        formatted_message = await self._call_claude(collaboration_prompt, context)
        
        # The other agent processes this message
        response = await other_agent.process(formatted_message, context)
        
        return response.data if response.success else response.message
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the agent"""
        return {
            "name": self.name,
            "conversation_length": len(self.conversation_history),
            "last_activity": self.conversation_history[-1]["content"] if self.conversation_history else None
        }


class AgentOrchestrator:
    """
    Orchestrates multiple autonomous agents to work together on complex tasks
    """
    
    def __init__(self, anthropic_client: AsyncAnthropic):
        self.anthropic_client = anthropic_client
        self.agents: Dict[str, AutonomousAgent] = {}
        self.active_workflows: Dict[str, Dict] = {}
    
    def register_agent(self, agent: AutonomousAgent):
        """Register an agent with the orchestrator"""
        self.agents[agent.name] = agent
        logger.info(f"Registered agent: {agent.name}")
    
    async def execute_workflow(self, workflow_name: str, input_data: Any, context: AgentContext) -> AgentResponse:
        """
        Execute a predefined workflow involving multiple agents
        """
        workflow_id = f"{workflow_name}_{context.session_id}"
        
        try:
            if workflow_name == "project_onboarding":
                return await self._project_onboarding_workflow(input_data, context)
            elif workflow_name == "gap_analysis":
                return await self._gap_analysis_workflow(input_data, context)
            elif workflow_name == "report_generation":
                return await self._report_generation_workflow(input_data, context)
            elif workflow_name == "document_creation":
                return await self._document_creation_workflow(input_data, context)
            else:
                return AgentResponse(
                    success=False,
                    message=f"Unknown workflow: {workflow_name}"
                )
                
        except Exception as e:
            logger.error(f"Error executing workflow {workflow_name}: {str(e)}")
            return AgentResponse(
                success=False,
                message=f"Workflow execution failed: {str(e)}"
            )
    
    async def _project_onboarding_workflow(self, input_data: Any, context: AgentContext) -> AgentResponse:
        """Workflow for autonomous project onboarding"""
        # This will be implemented with specific agent coordination
        pass
    
    async def _gap_analysis_workflow(self, input_data: Any, context: AgentContext) -> AgentResponse:
        """Workflow for autonomous gap analysis"""
        # This will be implemented with specific agent coordination
        pass
    
    async def _report_generation_workflow(self, input_data: Any, context: AgentContext) -> AgentResponse:
        """Workflow for autonomous report generation"""
        # This will be implemented with specific agent coordination
        pass
    
    async def _document_creation_workflow(self, input_data: Any, context: AgentContext) -> AgentResponse:
        """Workflow for autonomous document creation"""
        # This will be implemented with specific agent coordination
        pass
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all registered agents"""
        return {name: agent.get_status() for name, agent in self.agents.items()}