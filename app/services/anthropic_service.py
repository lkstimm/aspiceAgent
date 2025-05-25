"""
Anthropic Claude API service
"""

from anthropic import AsyncAnthropic
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)

# Global client instance
_anthropic_client = None


class AnthropicService:
    """Service for interacting with Anthropic Claude API"""
    
    def __init__(self):
        self.client = get_anthropic_client()
    
    async def generate_response(self, messages: list, system_prompt: str = "", model: str = "claude-3-sonnet-20240229") -> str:
        """Generate a response using Claude"""
        try:
            response = await self.client.messages.create(
                model=model,
                max_tokens=4000,
                system=system_prompt,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Error generating Claude response: {e}")
            return f"Error: {str(e)}"


def get_anthropic_client() -> AsyncAnthropic:
    """Get Anthropic client (singleton)"""
    global _anthropic_client
    
    if _anthropic_client is None:
        settings = get_settings()
        
        if not settings.anthropic_api_key:
            logger.warning("Anthropic API key not configured. Using mock client.")
            # In production, this should raise an error
            # For development, we'll create a mock client
            _anthropic_client = MockAnthropicClient()
        else:
            _anthropic_client = AsyncAnthropic(api_key=settings.anthropic_api_key)
            logger.info("Anthropic client initialized successfully")
    
    return _anthropic_client


class MockAnthropicClient:
    """Mock Anthropic client for development/testing"""
    
    class Messages:
        async def create(self, **kwargs):
            """Mock message creation"""
            model = kwargs.get("model", "claude-3-sonnet-20240229")
            messages = kwargs.get("messages", [])
            system = kwargs.get("system", "")
            
            # Extract the last user message
            user_message = ""
            for msg in reversed(messages):
                if msg.get("role") == "user":
                    user_message = msg.get("content", "")
                    break
            
            # Generate a mock response based on the request
            mock_response = self._generate_mock_response(user_message, system)
            
            class MockResponse:
                def __init__(self, content):
                    self.content = [MockContent(content)]
            
            class MockContent:
                def __init__(self, text):
                    self.text = text
            
            return MockResponse(mock_response)
    
    def __init__(self):
        self.messages = self.Messages()
    
    def _generate_mock_response(self, user_message: str, system_prompt: str) -> str:
        """Generate a mock response based on the request"""
        
        # Determine response type based on system prompt and user message
        if "ProjectOrchestrator" in system_prompt:
            return self._mock_project_orchestrator_response(user_message)
        elif "GapAnalysisExpert" in system_prompt:
            return self._mock_gap_analysis_response(user_message)
        elif "DocumentationStrategy" in system_prompt:
            return self._mock_documentation_response(user_message)
        elif "EntityExtraction" in system_prompt:
            return self._mock_entity_extraction_response(user_message)
        elif "ReportGeneration" in system_prompt:
            return self._mock_report_generation_response(user_message)
        else:
            return self._mock_general_response(user_message)
    
    def _mock_project_orchestrator_response(self, message: str) -> str:
        return """
        {
            "analysis": "Project analysis completed. Identified key stakeholders, ASPICE scope covering SYS.1-5 and SWE.1-6, and critical timeline constraints.",
            "decisions": [
                "Prioritize gap analysis for safety-critical process areas",
                "Schedule stakeholder interviews within 2 weeks",
                "Activate Gap Analysis Expert Agent for detailed assessment"
            ],
            "next_actions": [
                "Initialize knowledge graph with project entities",
                "Schedule stakeholder interviews",
                "Set up project monitoring dashboard"
            ],
            "agent_coordination": {
                "GapAnalysisExpert": "Conduct detailed process area assessment",
                "EntityExtraction": "Extract entities from project documentation"
            },
            "timeline": "4-week assessment phase with weekly milestones",
            "risks": [
                "Limited stakeholder availability may delay interviews",
                "Complex technical architecture may require additional expertise"
            ]
        }
        """
    
    def _mock_gap_analysis_response(self, message: str) -> str:
        return """
        **ASPICE Gap Analysis Results**
        
        ## Identified Gaps:
        - SYS.1: Missing system requirements specification template
        - SWE.2: Inadequate software design documentation
        - SUP.8: Limited configuration management procedures
        
        ## Process Area Mapping:
        - SYS: Strong coverage in SYS.1, gaps in SYS.3 and SYS.4
        - SWE: Good practices in SWE.1, improvements needed in SWE.2-4
        - SUP: Critical gaps in SUP.8 and SUP.9
        
        ## Capability Assessment:
        - Current average level: L1.5
        - Target level: L2
        - Critical gaps preventing L2 achievement identified
        
        ## Recommendations:
        1. Implement standardized requirements management process
        2. Develop comprehensive design documentation templates
        3. Establish formal configuration management procedures
        """
    
    def _mock_documentation_response(self, message: str) -> str:
        return """
        # ASPICE Process Improvement Strategy
        
        ## Executive Summary
        This strategy document outlines the approach for achieving ASPICE Level 2 compliance across targeted process areas.
        
        ## Current State Analysis
        - Capability Level 1 achieved in most process areas
        - Strong engineering practices but limited process documentation
        - Good tool infrastructure but inconsistent usage
        
        ## Target State Definition
        - ASPICE Level 2 compliance for SYS.1-5 and SWE.1-6
        - Standardized processes across all development teams
        - Comprehensive documentation and evidence management
        
        ## Implementation Roadmap
        ### Phase 1: Foundation (Weeks 1-4)
        - Establish process documentation framework
        - Implement requirements management procedures
        - Set up configuration management system
        
        ### Phase 2: Core Processes (Weeks 5-12)
        - Deploy software design processes
        - Implement verification and validation procedures
        - Establish quality assurance practices
        
        ### Phase 3: Optimization (Weeks 13-16)
        - Process refinement and optimization
        - Training and competency development
        - Continuous improvement implementation
        """
    
    def _mock_entity_extraction_response(self, message: str) -> str:
        return """
        [
            {
                "name": "John Smith",
                "type": "stakeholder",
                "confidence": 0.95,
                "properties": {
                    "role": "Software Architect",
                    "department": "Engineering",
                    "expertise": ["System Design", "ASPICE", "Automotive"]
                }
            },
            {
                "name": "SYS.1",
                "type": "process_area",
                "confidence": 0.98,
                "properties": {
                    "full_name": "System Requirements Analysis",
                    "current_level": "L1",
                    "target_level": "L2"
                }
            },
            {
                "name": "Requirements Specification",
                "type": "artifact",
                "confidence": 0.85,
                "properties": {
                    "document_type": "specification",
                    "process_area": "SYS.1",
                    "status": "incomplete"
                }
            }
        ]
        """
    
    def _mock_report_generation_response(self, message: str) -> str:
        return """
        # ASPICE Gap Analysis Report
        
        ## Executive Summary
        The ASPICE assessment identified significant opportunities for process improvement across system and software engineering process areas. Current capability levels average L1.3, with a clear path to achieve L2 compliance within 16 weeks.
        
        ## Key Findings
        - **Strengths**: Strong technical competency, good tool infrastructure
        - **Critical Gaps**: Process documentation, requirements traceability, configuration management
        - **Priority Areas**: SYS.1, SWE.2, SUP.8
        
        ## Detailed Findings by Process Area
        
        ### SYS.1 - System Requirements Analysis (Current: L1, Target: L2)
        **Strengths:**
        - Requirements are captured and analyzed
        - Stakeholder involvement in requirements definition
        
        **Gaps:**
        - Missing requirements specification template
        - Inadequate requirements traceability
        - Limited requirements validation procedures
        
        **Recommendations:**
        1. Implement standardized requirements specification template
        2. Establish requirements traceability matrix
        3. Define requirements validation procedures
        
        ## Implementation Roadmap
        - **Phase 1 (Weeks 1-4)**: Critical gap remediation
        - **Phase 2 (Weeks 5-12)**: Core process implementation
        - **Phase 3 (Weeks 13-16)**: Process optimization and validation
        
        ## Success Metrics
        - Process compliance rate > 90%
        - Documentation completeness > 95%
        - Stakeholder satisfaction > 4.0/5.0
        """
    
    def _mock_general_response(self, message: str) -> str:
        return f"""
        Thank you for your request. I've analyzed the provided information and generated a comprehensive response.
        
        **Analysis Summary:**
        Based on the input provided, I've identified key areas for attention and developed appropriate recommendations.
        
        **Key Insights:**
        - The request involves ASPICE consulting activities
        - Multiple process areas and stakeholders are involved
        - There are opportunities for process improvement and optimization
        
        **Recommendations:**
        1. Proceed with detailed analysis of identified areas
        2. Engage relevant stakeholders for validation
        3. Develop implementation plan with clear timelines
        4. Establish monitoring and measurement procedures
        
        **Next Steps:**
        - Review findings with project team
        - Refine recommendations based on feedback
        - Initiate implementation planning
        
        This is a mock response for development purposes. In production, this would be replaced with actual Claude AI responses.
        """