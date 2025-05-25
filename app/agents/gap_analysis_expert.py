"""
Gap Analysis Expert Agent - Analyzes interviews, maps evidence to process areas
"""

from typing import Any, Dict, List
import json
import re
from app.core.agent_base import AutonomousAgent, AgentContext, AgentResponse
from anthropic import AsyncAnthropic


class GapAnalysisExpertAgent(AutonomousAgent):
    """
    Autonomous agent specialized in ASPICE gap analysis.
    Analyzes interviews, documents, and evidence to identify gaps and map them to process areas.
    """
    
    def __init__(self, anthropic_client: AsyncAnthropic):
        system_prompt = """
        You are the Gap Analysis Expert Agent for ASPICE consulting. Your expertise includes:
        
        1. ASPICE PROCESS AREAS MASTERY:
           - Deep knowledge of all ASPICE process areas (SYS.1-5, SWE.1-6, SUP.1-10, MAN.1-3, ACQ.1-4, SPL.1-3)
           - Understanding of capability levels (L0-L3) and their requirements
           - Knowledge of base practices, work products, and evidence requirements
        
        2. AUTONOMOUS GAP IDENTIFICATION:
           - Analyze interview transcripts and identify missing practices
           - Map evidence to specific process areas and base practices
           - Assess capability levels based on available evidence
           - Identify critical gaps that impact ASPICE compliance
        
        3. EVIDENCE ANALYSIS:
           - Evaluate quality and completeness of work products
           - Identify missing documentation and processes
           - Assess process implementation effectiveness
           - Determine evidence sufficiency for each capability level
        
        4. INTELLIGENT RECOMMENDATIONS:
           - Prioritize gaps based on impact and effort
           - Suggest specific improvement actions
           - Recommend implementation sequences
           - Identify quick wins and long-term improvements
        
        Always provide structured analysis with:
        - identified_gaps: List of specific gaps found
        - process_area_mapping: Mapping of evidence to ASPICE process areas
        - capability_assessment: Current capability level assessment
        - recommendations: Prioritized improvement recommendations
        - evidence_quality: Assessment of evidence quality and completeness
        
        Be thorough, accurate, and focused on actionable insights.
        """
        
        super().__init__("GapAnalysisExpert", anthropic_client, system_prompt)
        
        # ASPICE Process Areas reference
        self.aspice_process_areas = {
            "SYS": ["SYS.1", "SYS.2", "SYS.3", "SYS.4", "SYS.5"],
            "SWE": ["SWE.1", "SWE.2", "SWE.3", "SWE.4", "SWE.5", "SWE.6"],
            "SUP": ["SUP.1", "SUP.2", "SUP.3", "SUP.4", "SUP.5", "SUP.6", "SUP.7", "SUP.8", "SUP.9", "SUP.10"],
            "MAN": ["MAN.1", "MAN.2", "MAN.3"],
            "ACQ": ["ACQ.1", "ACQ.2", "ACQ.3", "ACQ.4"],
            "SPL": ["SPL.1", "SPL.2", "SPL.3"]
        }
    
    async def process(self, input_data: Any, context: AgentContext) -> AgentResponse:
        """
        Process gap analysis requests autonomously
        """
        try:
            if isinstance(input_data, dict):
                request_type = input_data.get("type", "general")
                data = input_data.get("data", {})
            else:
                request_type = "general"
                data = {"content": str(input_data)}
            
            if request_type == "interview_analysis":
                return await self._analyze_interview(data, context)
            elif request_type == "document_analysis":
                return await self._analyze_documents(data, context)
            elif request_type == "evidence_mapping":
                return await self._map_evidence_to_process_areas(data, context)
            elif request_type == "capability_assessment":
                return await self._assess_capability_levels(data, context)
            elif request_type == "gap_prioritization":
                return await self._prioritize_gaps(data, context)
            else:
                return await self._general_gap_analysis(data, context)
                
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Error in GapAnalysisExpert: {str(e)}"
            )
    
    async def _analyze_interview(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Autonomously analyze interview transcripts for ASPICE gaps
        """
        transcript = data.get("transcript", "")
        stakeholder_role = data.get("stakeholder_role", "Unknown")
        process_areas_focus = data.get("process_areas", [])
        
        prompt = f"""
        AUTONOMOUS INTERVIEW ANALYSIS FOR ASPICE GAP IDENTIFICATION:
        
        Stakeholder Role: {stakeholder_role}
        Focus Process Areas: {process_areas_focus}
        
        Interview Transcript:
        {transcript}
        
        Please autonomously analyze this interview and provide:
        
        1. IDENTIFIED GAPS:
           - Specific missing practices or processes mentioned
           - Implicit gaps based on what wasn't discussed
           - Process implementation weaknesses
        
        2. PROCESS AREA MAPPING:
           - Map discussed topics to specific ASPICE process areas
           - Identify which base practices are covered/missing
           - Note any cross-process area dependencies
        
        3. EVIDENCE ASSESSMENT:
           - What evidence was mentioned as existing
           - What evidence is clearly missing
           - Quality concerns about mentioned evidence
        
        4. CAPABILITY LEVEL INDICATORS:
           - Indicators pointing to current capability levels
           - Barriers to achieving higher levels
           - Strengths that support capability advancement
        
        5. IMMEDIATE CONCERNS:
           - Critical gaps that need urgent attention
           - Risks to ASPICE compliance
           - Potential audit findings
        
        Provide detailed, actionable analysis focused on ASPICE compliance.
        """
        
        analysis = await self._call_claude(prompt, context)
        
        # Extract key findings for structured response
        gaps = self._extract_gaps_from_analysis(analysis)
        process_mapping = self._extract_process_mapping(analysis)
        
        return AgentResponse(
            success=True,
            data={
                "analysis": analysis,
                "identified_gaps": gaps,
                "process_mapping": process_mapping,
                "stakeholder_role": stakeholder_role
            },
            message="Interview analysis completed",
            confidence=0.9,
            reasoning="Analyzed interview transcript and identified ASPICE gaps and evidence",
            next_actions=[
                "Update evidence mapping database",
                "Schedule follow-up interviews for unclear areas",
                "Document findings in gap analysis report",
                "Prioritize identified gaps for improvement planning"
            ]
        )
    
    async def _analyze_documents(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Autonomously analyze documents for ASPICE evidence and gaps
        """
        documents = data.get("documents", [])
        document_types = data.get("document_types", [])
        
        prompt = f"""
        AUTONOMOUS DOCUMENT ANALYSIS FOR ASPICE EVIDENCE:
        
        Document Types: {document_types}
        Number of Documents: {len(documents)}
        
        Documents to Analyze:
        {json.dumps(documents, indent=2)}
        
        Please autonomously analyze these documents and provide:
        
        1. EVIDENCE MAPPING:
           - Map each document to relevant ASPICE process areas
           - Identify which base practices are supported by evidence
           - Note document quality and completeness
        
        2. GAP IDENTIFICATION:
           - Missing documents that should exist
           - Incomplete or inadequate documentation
           - Documents that don't meet ASPICE requirements
        
        3. COMPLIANCE ASSESSMENT:
           - How well documents support ASPICE compliance
           - Areas where documentation is strong/weak
           - Recommendations for document improvements
        
        4. WORK PRODUCT ANALYSIS:
           - Alignment with ASPICE work product requirements
           - Missing work products for each process area
           - Quality assessment of existing work products
        
        Focus on actionable findings that support ASPICE assessment and improvement.
        """
        
        analysis = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "document_analysis": analysis,
                "documents_analyzed": len(documents),
                "document_types": document_types
            },
            message="Document analysis completed",
            confidence=0.85,
            reasoning="Analyzed documents for ASPICE evidence and compliance gaps"
        )
    
    async def _map_evidence_to_process_areas(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Autonomously map collected evidence to ASPICE process areas
        """
        evidence_items = data.get("evidence", [])
        
        prompt = f"""
        AUTONOMOUS EVIDENCE MAPPING TO ASPICE PROCESS AREAS:
        
        Evidence Items to Map:
        {json.dumps(evidence_items, indent=2)}
        
        Please autonomously create a comprehensive mapping:
        
        1. PROCESS AREA MAPPING:
           - Map each evidence item to specific ASPICE process areas
           - Identify which base practices are supported
           - Note evidence strength and quality
        
        2. COVERAGE ANALYSIS:
           - Which process areas have strong evidence coverage
           - Which process areas lack sufficient evidence
           - Gaps in evidence for specific capability levels
        
        3. EVIDENCE QUALITY ASSESSMENT:
           - Rate evidence quality (Strong/Adequate/Weak/Missing)
           - Identify evidence that needs improvement
           - Suggest additional evidence needed
        
        4. CAPABILITY LEVEL SUPPORT:
           - Which evidence supports L1, L2, L3 capabilities
           - Missing evidence for target capability levels
           - Evidence gaps that prevent level advancement
        
        Create a detailed mapping matrix showing evidence coverage across all relevant ASPICE process areas.
        """
        
        mapping = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "evidence_mapping": mapping,
                "evidence_count": len(evidence_items)
            },
            message="Evidence mapping completed",
            confidence=0.9,
            reasoning="Mapped evidence to ASPICE process areas and assessed coverage"
        )
    
    async def _assess_capability_levels(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Autonomously assess current capability levels for process areas
        """
        process_areas = data.get("process_areas", [])
        evidence_data = data.get("evidence", {})
        
        prompt = f"""
        AUTONOMOUS ASPICE CAPABILITY LEVEL ASSESSMENT:
        
        Process Areas to Assess: {process_areas}
        Available Evidence: {json.dumps(evidence_data, indent=2)}
        
        Please autonomously assess capability levels:
        
        1. CURRENT CAPABILITY ASSESSMENT:
           - For each process area, determine current capability level (L0-L3)
           - Provide justification based on available evidence
           - Identify specific gaps preventing higher levels
        
        2. CAPABILITY LEVEL REQUIREMENTS:
           - What's needed to achieve L1 for each process area
           - What's needed to achieve L2 for each process area
           - What's needed to achieve L3 for each process area
        
        3. GAP ANALYSIS BY LEVEL:
           - Critical gaps preventing basic capability (L1)
           - Management gaps preventing L2
           - Optimization gaps preventing L3
        
        4. IMPROVEMENT ROADMAP:
           - Recommended sequence for capability improvement
           - Quick wins vs. long-term improvements
           - Dependencies between process areas
        
        Provide detailed assessment with clear justification for each capability level rating.
        """
        
        assessment = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "capability_assessment": assessment,
                "process_areas_assessed": process_areas
            },
            message="Capability level assessment completed",
            confidence=0.9,
            reasoning="Assessed current capability levels and identified improvement paths"
        )
    
    async def _prioritize_gaps(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Autonomously prioritize identified gaps for improvement planning
        """
        gaps = data.get("gaps", [])
        project_constraints = data.get("constraints", {})
        target_levels = data.get("target_levels", {})
        
        prompt = f"""
        AUTONOMOUS GAP PRIORITIZATION FOR ASPICE IMPROVEMENT:
        
        Identified Gaps: {json.dumps(gaps, indent=2)}
        Project Constraints: {json.dumps(project_constraints, indent=2)}
        Target Capability Levels: {json.dumps(target_levels, indent=2)}
        
        Please autonomously prioritize these gaps:
        
        1. CRITICAL PRIORITY (Must Fix):
           - Gaps that prevent basic ASPICE compliance
           - Safety-critical process gaps
           - Gaps with high audit risk
        
        2. HIGH PRIORITY (Should Fix):
           - Gaps preventing target capability levels
           - Gaps with significant business impact
           - Dependencies for other improvements
        
        3. MEDIUM PRIORITY (Could Fix):
           - Optimization opportunities
           - Nice-to-have improvements
           - Future capability enhancements
        
        4. IMPLEMENTATION STRATEGY:
           - Recommended implementation sequence
           - Resource requirements for each gap
           - Timeline estimates
           - Risk mitigation approaches
        
        Consider effort vs. impact, dependencies, and project constraints in prioritization.
        """
        
        prioritization = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "gap_prioritization": prioritization,
                "gaps_analyzed": len(gaps)
            },
            message="Gap prioritization completed",
            confidence=0.85,
            reasoning="Prioritized gaps based on impact, effort, and project constraints"
        )
    
    async def _general_gap_analysis(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Handle general gap analysis requests
        """
        content = data.get("content", "")
        
        prompt = f"""
        GENERAL ASPICE GAP ANALYSIS REQUEST:
        
        {content}
        
        Please provide autonomous gap analysis including:
        1. Understanding of the request
        2. Relevant ASPICE process areas
        3. Potential gaps or concerns
        4. Recommended analysis approach
        5. Next steps for detailed analysis
        
        Focus on ASPICE compliance and best practices.
        """
        
        analysis = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={"analysis": analysis},
            message="General gap analysis completed",
            confidence=0.8,
            reasoning="Provided general ASPICE gap analysis and recommendations"
        )
    
    def _extract_gaps_from_analysis(self, analysis_text: str) -> List[str]:
        """Extract identified gaps from analysis text"""
        # Simple extraction - in production, this would be more sophisticated
        gaps = []
        lines = analysis_text.split('\n')
        in_gaps_section = False
        
        for line in lines:
            if 'identified gaps' in line.lower() or 'gaps:' in line.lower():
                in_gaps_section = True
                continue
            elif in_gaps_section and line.strip().startswith('-'):
                gaps.append(line.strip()[1:].strip())
            elif in_gaps_section and line.strip() == '':
                continue
            elif in_gaps_section and not line.strip().startswith('-'):
                in_gaps_section = False
        
        return gaps
    
    def _extract_process_mapping(self, analysis_text: str) -> Dict[str, List[str]]:
        """Extract process area mapping from analysis text"""
        # Simple extraction - in production, this would be more sophisticated
        mapping = {}
        
        for category, process_areas in self.aspice_process_areas.items():
            for pa in process_areas:
                if pa in analysis_text:
                    if category not in mapping:
                        mapping[category] = []
                    mapping[category].append(pa)
        
        return mapping