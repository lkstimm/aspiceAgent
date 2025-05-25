"""
Project Orchestrator Agent - Manages overall project lifecycle and coordination
"""

from typing import Any, Dict, List
import json
from app.core.agent_base import AutonomousAgent, AgentContext, AgentResponse
from anthropic import AsyncAnthropic


class ProjectOrchestratorAgent(AutonomousAgent):
    """
    Autonomous agent responsible for orchestrating the entire ASPICE consulting project.
    This agent coordinates other agents and manages the project lifecycle.
    """
    
    def __init__(self, anthropic_client: AsyncAnthropic):
        system_prompt = """
        You are the Project Orchestrator Agent for an ASPICE consulting platform. Your role is to:
        
        1. AUTONOMOUS PROJECT MANAGEMENT:
           - Analyze incoming project data and automatically structure it
           - Identify key stakeholders, risks, and project parameters
           - Create project timelines and milestone plans
           - Coordinate with other specialized agents
        
        2. DECISION MAKING:
           - Determine which agents need to be involved for specific tasks
           - Prioritize activities based on project constraints and goals
           - Make autonomous decisions about project flow and next steps
        
        3. QUALITY ASSURANCE:
           - Ensure all project activities align with ASPICE standards
           - Monitor progress and identify potential issues early
           - Maintain project coherence across all activities
        
        4. COMMUNICATION:
           - Generate clear status updates and recommendations
           - Coordinate between consultant and client needs
           - Provide strategic guidance based on project analysis
        
        Always respond with structured JSON that includes:
        - analysis: Your analysis of the situation
        - decisions: Autonomous decisions you're making
        - next_actions: Specific next steps
        - agent_coordination: Which other agents to involve
        - timeline: Proposed timeline for activities
        - risks: Identified risks and mitigation strategies
        
        Be proactive, analytical, and focused on ASPICE consulting best practices.
        """
        
        super().__init__("ProjectOrchestrator", anthropic_client, system_prompt)
    
    async def process(self, input_data: Any, context: AgentContext) -> AgentResponse:
        """
        Process project-related requests and make autonomous decisions
        """
        try:
            # Determine the type of request
            if isinstance(input_data, dict):
                request_type = input_data.get("type", "general")
                data = input_data.get("data", {})
            else:
                request_type = "general"
                data = {"content": str(input_data)}
            
            if request_type == "project_creation":
                return await self._handle_project_creation(data, context)
            elif request_type == "project_analysis":
                return await self._handle_project_analysis(data, context)
            elif request_type == "workflow_coordination":
                return await self._handle_workflow_coordination(data, context)
            else:
                return await self._handle_general_request(data, context)
                
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Error in ProjectOrchestrator: {str(e)}"
            )
    
    async def _handle_project_creation(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Autonomously handle new project creation
        """
        prompt = f"""
        AUTONOMOUS PROJECT CREATION TASK:
        
        I need to analyze this new project data and create a comprehensive project structure:
        
        Project Data:
        {json.dumps(data, indent=2)}
        
        Please autonomously:
        1. Extract and structure all key project information
        2. Identify the ASPICE scope and process areas involved
        3. Analyze the risk landscape and technical challenges
        4. Create a project timeline with key milestones
        5. Determine which specialized agents need to be involved
        6. Generate initial project recommendations
        
        Provide a comprehensive project analysis and action plan.
        """
        
        response_text = await self._call_claude(prompt, context)
        
        try:
            # Try to parse as JSON, fallback to structured text
            if response_text.strip().startswith('{'):
                response_data = json.loads(response_text)
            else:
                response_data = {"analysis": response_text}
            
            return AgentResponse(
                success=True,
                data=response_data,
                message="Project creation analysis completed",
                confidence=0.9,
                reasoning="Analyzed project data and created comprehensive structure",
                next_actions=[
                    "Initialize knowledge graph with project entities",
                    "Schedule stakeholder interviews",
                    "Activate Gap Analysis Expert Agent",
                    "Set up project monitoring dashboard"
                ]
            )
            
        except json.JSONDecodeError:
            return AgentResponse(
                success=True,
                data={"analysis": response_text},
                message="Project analysis completed (text format)",
                confidence=0.8
            )
    
    async def _handle_project_analysis(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Analyze ongoing project status and make autonomous decisions
        """
        prompt = f"""
        AUTONOMOUS PROJECT ANALYSIS TASK:
        
        Current project status and data:
        {json.dumps(data, indent=2)}
        
        Please autonomously:
        1. Assess current project health and progress
        2. Identify any blockers or risks that need attention
        3. Determine if the project timeline needs adjustment
        4. Decide which activities should be prioritized next
        5. Evaluate if additional resources or expertise is needed
        6. Generate actionable recommendations
        
        Focus on maintaining ASPICE compliance and project success.
        """
        
        response_text = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={"analysis": response_text},
            message="Project analysis completed",
            confidence=0.85,
            reasoning="Analyzed current project status and identified optimization opportunities"
        )
    
    async def _handle_workflow_coordination(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Coordinate workflows between different agents
        """
        prompt = f"""
        AUTONOMOUS WORKFLOW COORDINATION TASK:
        
        Workflow coordination request:
        {json.dumps(data, indent=2)}
        
        Please autonomously:
        1. Analyze which agents need to be involved
        2. Determine the optimal sequence of agent activities
        3. Identify dependencies between different tasks
        4. Create a coordination plan with timelines
        5. Define success criteria for each workflow step
        6. Plan for error handling and contingencies
        
        Ensure efficient coordination while maintaining quality standards.
        """
        
        response_text = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={"coordination_plan": response_text},
            message="Workflow coordination plan created",
            confidence=0.9,
            reasoning="Analyzed workflow requirements and created optimal coordination strategy"
        )
    
    async def _handle_general_request(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Handle general project-related requests
        """
        prompt = f"""
        GENERAL PROJECT REQUEST:
        
        Request data:
        {json.dumps(data, indent=2)}
        
        Please analyze this request and provide:
        1. Your understanding of what's being asked
        2. Autonomous recommendations for how to proceed
        3. Which other agents might need to be involved
        4. Potential risks or considerations
        5. Next steps and timeline
        
        Maintain focus on ASPICE consulting excellence.
        """
        
        response_text = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={"response": response_text},
            message="General request processed",
            confidence=0.8,
            reasoning="Analyzed request and provided autonomous recommendations"
        )
    
    async def create_project_timeline(self, project_data: Dict, context: AgentContext) -> Dict:
        """
        Autonomously create a project timeline based on project data
        """
        prompt = f"""
        Create an autonomous project timeline for this ASPICE consulting project:
        
        {json.dumps(project_data, indent=2)}
        
        Generate a detailed timeline with:
        1. Project phases (Onboarding, Gap Analysis, Improvement Planning, Implementation, Verification)
        2. Key milestones and deliverables
        3. Estimated durations based on project complexity
        4. Dependencies between activities
        5. Risk buffers and contingency time
        6. Client interaction points
        
        Format as a structured timeline with dates and responsibilities.
        """
        
        timeline_response = await self._call_claude(prompt, context)
        return {"timeline": timeline_response}
    
    async def assess_project_risks(self, project_data: Dict, context: AgentContext) -> Dict:
        """
        Autonomously assess project risks and create mitigation strategies
        """
        prompt = f"""
        Perform autonomous risk assessment for this ASPICE project:
        
        {json.dumps(project_data, indent=2)}
        
        Identify and analyze:
        1. Technical risks (complexity, technology maturity, integration challenges)
        2. Organizational risks (team size, experience, change resistance)
        3. Timeline risks (scope creep, resource availability, dependencies)
        4. Compliance risks (ASPICE interpretation, audit readiness)
        5. Business risks (budget, stakeholder alignment, market pressures)
        
        For each risk, provide:
        - Risk level (High/Medium/Low)
        - Impact assessment
        - Probability assessment
        - Mitigation strategies
        - Monitoring approach
        """
        
        risk_response = await self._call_claude(prompt, context)
        return {"risk_assessment": risk_response}