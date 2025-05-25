"""
Documentation & Strategy Agent - Creates professional documents and strategies
"""

from typing import Any, Dict, List
import json
from app.core.agent_base import AutonomousAgent, AgentContext, AgentResponse
from anthropic import AsyncAnthropic


class DocumentationStrategyAgent(AutonomousAgent):
    """
    Autonomous agent specialized in creating professional ASPICE documentation and strategies.
    Generates strategy documents, process descriptions, work instructions, and training materials.
    """
    
    def __init__(self, anthropic_client: AsyncAnthropic):
        system_prompt = """
        You are the Documentation & Strategy Agent for ASPICE consulting. Your expertise includes:
        
        1. PROFESSIONAL DOCUMENT CREATION:
           - Strategy documents with executive summaries and detailed plans
           - Process descriptions aligned with ASPICE requirements
           - Work instructions and procedures
           - Training materials and presentations
           - Assessment reports and gap analysis documents
        
        2. ASPICE DOCUMENTATION STANDARDS:
           - Deep knowledge of ASPICE work product requirements
           - Understanding of documentation hierarchies and relationships
           - Knowledge of traceability and configuration management
           - Expertise in document templates and formatting standards
        
        3. STRATEGIC PLANNING:
           - ASPICE improvement roadmaps and implementation strategies
           - Process optimization and maturity advancement plans
           - Risk mitigation strategies and contingency planning
           - Resource allocation and timeline planning
        
        4. AUTONOMOUS CONTENT GENERATION:
           - Analyze input data and automatically generate appropriate content
           - Ensure consistency across all documentation
           - Maintain professional formatting and structure
           - Include relevant references and traceability
        
        Always generate documents with:
        - Professional formatting and structure
        - Clear executive summaries
        - Detailed content with proper sections
        - References to ASPICE standards
        - Actionable recommendations
        - Proper version control and metadata
        
        Focus on creating high-quality, professional documents that meet ASPICE standards.
        """
        
        super().__init__("DocumentationStrategy", anthropic_client, system_prompt)
        
        # Document templates and structures
        self.document_templates = {
            "strategy": {
                "sections": ["Executive Summary", "Current State Analysis", "Target State Definition", 
                           "Gap Analysis", "Implementation Roadmap", "Risk Management", "Success Metrics"],
                "format": "professional_report"
            },
            "process_description": {
                "sections": ["Purpose", "Scope", "Process Flow", "Roles and Responsibilities", 
                           "Work Products", "Entry/Exit Criteria", "Metrics"],
                "format": "technical_document"
            },
            "work_instruction": {
                "sections": ["Objective", "Scope", "Prerequisites", "Step-by-Step Procedure", 
                           "Quality Checks", "Documentation Requirements", "References"],
                "format": "procedural_guide"
            },
            "training_material": {
                "sections": ["Learning Objectives", "Content Overview", "Key Concepts", 
                           "Practical Examples", "Exercises", "Assessment", "Resources"],
                "format": "educational_content"
            }
        }
    
    async def process(self, input_data: Any, context: AgentContext) -> AgentResponse:
        """
        Process documentation and strategy requests autonomously
        """
        try:
            if isinstance(input_data, dict):
                request_type = input_data.get("type", "general")
                data = input_data.get("data", {})
            else:
                request_type = "general"
                data = {"content": str(input_data)}
            
            if request_type == "strategy_document":
                return await self._create_strategy_document(data, context)
            elif request_type == "process_description":
                return await self._create_process_description(data, context)
            elif request_type == "work_instruction":
                return await self._create_work_instruction(data, context)
            elif request_type == "training_material":
                return await self._create_training_material(data, context)
            elif request_type == "assessment_report":
                return await self._create_assessment_report(data, context)
            elif request_type == "improvement_plan":
                return await self._create_improvement_plan(data, context)
            else:
                return await self._general_documentation_request(data, context)
                
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Error in DocumentationStrategy: {str(e)}"
            )
    
    async def _create_strategy_document(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Autonomously create a comprehensive ASPICE strategy document
        """
        project_data = data.get("project_data", {})
        gap_analysis = data.get("gap_analysis", {})
        target_levels = data.get("target_levels", {})
        constraints = data.get("constraints", {})
        
        prompt = f"""
        AUTONOMOUS ASPICE STRATEGY DOCUMENT CREATION:
        
        Project Information:
        {json.dumps(project_data, indent=2)}
        
        Gap Analysis Results:
        {json.dumps(gap_analysis, indent=2)}
        
        Target Capability Levels:
        {json.dumps(target_levels, indent=2)}
        
        Project Constraints:
        {json.dumps(constraints, indent=2)}
        
        Please create a comprehensive ASPICE improvement strategy document with:
        
        1. EXECUTIVE SUMMARY:
           - High-level overview of current state and target state
           - Key challenges and opportunities
           - Strategic recommendations and expected outcomes
           - Investment requirements and timeline overview
        
        2. CURRENT STATE ANALYSIS:
           - Detailed assessment of current ASPICE capability levels
           - Strengths and weaknesses by process area
           - Risk assessment and compliance gaps
           - Organizational readiness evaluation
        
        3. TARGET STATE DEFINITION:
           - Desired capability levels for each process area
           - Business justification for target levels
           - Success criteria and metrics
           - Alignment with business objectives
        
        4. IMPLEMENTATION ROADMAP:
           - Phased approach with clear milestones
           - Dependencies and critical path analysis
           - Resource requirements and allocation
           - Timeline with realistic estimates
        
        5. RISK MANAGEMENT:
           - Identified risks and mitigation strategies
           - Contingency planning
           - Change management considerations
           - Success factors and potential obstacles
        
        6. SUCCESS METRICS AND MONITORING:
           - KPIs for measuring progress
           - Monitoring and reporting framework
           - Review and adjustment mechanisms
           - Long-term sustainability planning
        
        Format as a professional strategy document with proper structure, formatting, and references.
        """
        
        strategy_document = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "document": strategy_document,
                "document_type": "strategy",
                "sections": self.document_templates["strategy"]["sections"],
                "metadata": {
                    "project_id": context.project_id,
                    "created_by": "DocumentationStrategy Agent",
                    "version": "1.0",
                    "status": "draft"
                }
            },
            message="ASPICE strategy document created",
            confidence=0.9,
            reasoning="Generated comprehensive strategy document based on project data and gap analysis",
            next_actions=[
                "Review document with stakeholders",
                "Refine based on feedback",
                "Create detailed implementation plans",
                "Develop supporting documentation"
            ]
        )
    
    async def _create_process_description(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Autonomously create detailed process descriptions
        """
        process_area = data.get("process_area", "")
        current_practices = data.get("current_practices", {})
        target_level = data.get("target_level", "L1")
        
        prompt = f"""
        AUTONOMOUS ASPICE PROCESS DESCRIPTION CREATION:
        
        Process Area: {process_area}
        Current Practices: {json.dumps(current_practices, indent=2)}
        Target Capability Level: {target_level}
        
        Please create a detailed process description document with:
        
        1. PURPOSE AND SCOPE:
           - Clear statement of process purpose
           - Scope and boundaries definition
           - Relationship to other processes
           - ASPICE compliance objectives
        
        2. PROCESS FLOW:
           - Detailed process flow diagram (described textually)
           - Input and output specifications
           - Decision points and alternative paths
           - Feedback loops and iterations
        
        3. ROLES AND RESPONSIBILITIES:
           - Key roles involved in the process
           - Specific responsibilities for each role
           - Authority and accountability matrix
           - Escalation procedures
        
        4. WORK PRODUCTS:
           - Required input work products
           - Generated output work products
           - Work product characteristics and quality criteria
           - Templates and examples
        
        5. ENTRY AND EXIT CRITERIA:
           - Clear entry criteria for process initiation
           - Exit criteria for process completion
           - Quality gates and checkpoints
           - Approval requirements
        
        6. METRICS AND MEASUREMENT:
           - Process performance indicators
           - Quality metrics and targets
           - Measurement procedures
           - Reporting and review mechanisms
        
        7. TOOLS AND TECHNIQUES:
           - Recommended tools and technologies
           - Methods and techniques to be used
           - Training requirements
           - Support resources
        
        Ensure alignment with ASPICE {target_level} requirements and industry best practices.
        """
        
        process_description = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "document": process_description,
                "document_type": "process_description",
                "process_area": process_area,
                "target_level": target_level
            },
            message=f"Process description for {process_area} created",
            confidence=0.9,
            reasoning="Generated detailed process description aligned with ASPICE requirements"
        )
    
    async def _create_work_instruction(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Autonomously create detailed work instructions
        """
        activity = data.get("activity", "")
        process_area = data.get("process_area", "")
        tools = data.get("tools", [])
        roles = data.get("roles", [])
        
        prompt = f"""
        AUTONOMOUS WORK INSTRUCTION CREATION:
        
        Activity: {activity}
        Process Area: {process_area}
        Tools: {tools}
        Involved Roles: {roles}
        
        Please create detailed work instructions with:
        
        1. OBJECTIVE:
           - Clear statement of what the instruction achieves
           - Expected outcomes and deliverables
           - Quality standards and criteria
        
        2. SCOPE AND APPLICABILITY:
           - When to use this instruction
           - Applicable scenarios and contexts
           - Exceptions and special cases
        
        3. PREREQUISITES:
           - Required skills and knowledge
           - Necessary tools and resources
           - Input work products and information
           - Environmental requirements
        
        4. STEP-BY-STEP PROCEDURE:
           - Detailed, numbered steps
           - Decision points and alternatives
           - Quality checks at each step
           - Error handling and troubleshooting
        
        5. QUALITY ASSURANCE:
           - Verification and validation steps
           - Review and approval requirements
           - Common mistakes to avoid
           - Quality criteria and acceptance tests
        
        6. DOCUMENTATION REQUIREMENTS:
           - What to document during execution
           - Required records and evidence
           - Templates and forms to use
           - Traceability requirements
        
        7. REFERENCES AND RESOURCES:
           - Related procedures and guidelines
           - Standards and regulations
           - Training materials
           - Support contacts
        
        Make instructions clear, actionable, and suitable for practitioners at different experience levels.
        """
        
        work_instruction = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "document": work_instruction,
                "document_type": "work_instruction",
                "activity": activity,
                "process_area": process_area
            },
            message=f"Work instruction for {activity} created",
            confidence=0.85,
            reasoning="Generated detailed work instruction with step-by-step procedures"
        )
    
    async def _create_training_material(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Autonomously create training materials
        """
        topic = data.get("topic", "")
        audience = data.get("audience", "")
        duration = data.get("duration", "")
        format_type = data.get("format", "presentation")
        
        prompt = f"""
        AUTONOMOUS TRAINING MATERIAL CREATION:
        
        Topic: {topic}
        Target Audience: {audience}
        Duration: {duration}
        Format: {format_type}
        
        Please create comprehensive training materials with:
        
        1. LEARNING OBJECTIVES:
           - Clear, measurable learning outcomes
           - Skills and knowledge to be acquired
           - Competency levels to be achieved
           - Assessment criteria
        
        2. CONTENT STRUCTURE:
           - Logical flow of topics
           - Key concepts and principles
           - Practical examples and case studies
           - Interactive elements and exercises
        
        3. DETAILED CONTENT:
           - Introduction and context setting
           - Core content with explanations
           - Real-world examples and scenarios
           - Best practices and common pitfalls
        
        4. PRACTICAL EXERCISES:
           - Hands-on activities and workshops
           - Group discussions and case studies
           - Problem-solving scenarios
           - Skill practice opportunities
        
        5. ASSESSMENT METHODS:
           - Knowledge checks and quizzes
           - Practical assessments
           - Competency evaluations
           - Feedback mechanisms
        
        6. RESOURCES AND REFERENCES:
           - Additional reading materials
           - Standards and guidelines
           - Tools and templates
           - Support resources
        
        7. DELIVERY GUIDANCE:
           - Instructor notes and tips
           - Timing and pacing guidance
           - Equipment and setup requirements
           - Troubleshooting common issues
        
        Tailor content to the {audience} audience and ensure engagement and practical applicability.
        """
        
        training_material = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "document": training_material,
                "document_type": "training_material",
                "topic": topic,
                "audience": audience,
                "format": format_type
            },
            message=f"Training material for {topic} created",
            confidence=0.85,
            reasoning="Generated comprehensive training material tailored to target audience"
        )
    
    async def _create_assessment_report(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Autonomously create ASPICE assessment reports
        """
        assessment_data = data.get("assessment_data", {})
        findings = data.get("findings", [])
        recommendations = data.get("recommendations", [])
        
        prompt = f"""
        AUTONOMOUS ASPICE ASSESSMENT REPORT CREATION:
        
        Assessment Data:
        {json.dumps(assessment_data, indent=2)}
        
        Key Findings:
        {json.dumps(findings, indent=2)}
        
        Recommendations:
        {json.dumps(recommendations, indent=2)}
        
        Please create a professional ASPICE assessment report with:
        
        1. EXECUTIVE SUMMARY:
           - Assessment scope and objectives
           - Key findings and overall rating
           - Critical recommendations
           - Next steps and timeline
        
        2. ASSESSMENT METHODOLOGY:
           - Assessment approach and standards used
           - Evidence collection methods
           - Evaluation criteria and rating scale
           - Limitations and assumptions
        
        3. DETAILED FINDINGS:
           - Process area by process area analysis
           - Capability level assessments with justification
           - Strengths and weaknesses identified
           - Evidence quality and completeness
        
        4. GAP ANALYSIS:
           - Critical gaps preventing compliance
           - Missing processes and practices
           - Documentation and evidence gaps
           - Organizational and cultural gaps
        
        5. RECOMMENDATIONS:
           - Prioritized improvement recommendations
           - Implementation approach and timeline
           - Resource requirements and costs
           - Risk mitigation strategies
        
        6. IMPROVEMENT ROADMAP:
           - Phased implementation plan
           - Quick wins and long-term improvements
           - Dependencies and critical path
           - Success metrics and monitoring
        
        Format as a professional assessment report suitable for executive and technical audiences.
        """
        
        assessment_report = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "document": assessment_report,
                "document_type": "assessment_report",
                "assessment_scope": assessment_data.get("scope", ""),
                "findings_count": len(findings)
            },
            message="ASPICE assessment report created",
            confidence=0.9,
            reasoning="Generated comprehensive assessment report with findings and recommendations"
        )
    
    async def _create_improvement_plan(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Autonomously create detailed improvement plans
        """
        gaps = data.get("gaps", [])
        priorities = data.get("priorities", {})
        resources = data.get("resources", {})
        timeline = data.get("timeline", "")
        
        prompt = f"""
        AUTONOMOUS ASPICE IMPROVEMENT PLAN CREATION:
        
        Identified Gaps:
        {json.dumps(gaps, indent=2)}
        
        Priorities:
        {json.dumps(priorities, indent=2)}
        
        Available Resources:
        {json.dumps(resources, indent=2)}
        
        Timeline: {timeline}
        
        Please create a detailed improvement plan with:
        
        1. IMPROVEMENT OBJECTIVES:
           - Clear, measurable improvement goals
           - Target capability levels for each process area
           - Success criteria and metrics
           - Business benefits and ROI
        
        2. PRIORITIZED ACTION ITEMS:
           - Critical, high, medium, and low priority items
           - Effort estimation and resource requirements
           - Dependencies and sequencing
           - Risk assessment for each item
        
        3. IMPLEMENTATION PHASES:
           - Phase 1: Critical improvements and quick wins
           - Phase 2: Core process improvements
           - Phase 3: Optimization and maturity advancement
           - Phase 4: Continuous improvement and monitoring
        
        4. DETAILED WORK PACKAGES:
           - Specific tasks and deliverables
           - Assigned responsibilities and roles
           - Timeline and milestones
           - Quality gates and checkpoints
        
        5. RESOURCE ALLOCATION:
           - Human resource requirements
           - Training and skill development needs
           - Tool and technology requirements
           - Budget allocation and cost estimates
        
        6. RISK MANAGEMENT:
           - Implementation risks and mitigation strategies
           - Change management considerations
           - Contingency planning
           - Success factors and enablers
        
        7. MONITORING AND CONTROL:
           - Progress tracking mechanisms
           - Regular review and adjustment processes
           - Escalation procedures
           - Communication and reporting framework
        
        Create a practical, actionable plan that can be executed within the given constraints.
        """
        
        improvement_plan = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "document": improvement_plan,
                "document_type": "improvement_plan",
                "gaps_addressed": len(gaps),
                "timeline": timeline
            },
            message="ASPICE improvement plan created",
            confidence=0.9,
            reasoning="Generated detailed improvement plan with prioritized actions and implementation strategy"
        )
    
    async def _general_documentation_request(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Handle general documentation requests
        """
        content = data.get("content", "")
        document_type = data.get("document_type", "general")
        
        prompt = f"""
        GENERAL DOCUMENTATION REQUEST:
        
        Document Type: {document_type}
        Request: {content}
        
        Please create appropriate documentation based on this request:
        1. Analyze what type of document is needed
        2. Determine appropriate structure and content
        3. Generate professional, well-structured content
        4. Include relevant ASPICE considerations
        5. Provide actionable recommendations
        
        Focus on creating high-quality, professional documentation.
        """
        
        document = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "document": document,
                "document_type": document_type
            },
            message="Documentation created",
            confidence=0.8,
            reasoning="Generated documentation based on general request"
        )