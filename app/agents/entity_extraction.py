"""
Entity Extraction Agent - Extracts and tags entities from various inputs
"""

from typing import Any, Dict, List, Tuple
import json
import re
from app.core.agent_base import AutonomousAgent, AgentContext, AgentResponse
from anthropic import AsyncAnthropic


class EntityExtractionAgent(AutonomousAgent):
    """
    Autonomous agent specialized in extracting and tagging entities from various inputs.
    Identifies stakeholders, process areas, risks, artifacts, and other ASPICE-relevant entities.
    """
    
    def __init__(self, anthropic_client: AsyncAnthropic):
        system_prompt = """
        You are the Entity Extraction Agent for ASPICE consulting. Your expertise includes:
        
        1. ENTITY IDENTIFICATION:
           - Stakeholders (roles, names, responsibilities)
           - ASPICE Process Areas and Base Practices
           - Artifacts and Work Products
           - Risks and Issues
           - Technologies and Tools
           - Requirements and Specifications
           - Organizational Units and Teams
        
        2. INTELLIGENT TAGGING:
           - Categorize entities by type and relevance
           - Assign confidence scores to extractions
           - Identify relationships between entities
           - Tag entities with ASPICE process area associations
        
        3. CONTEXT UNDERSTANDING:
           - Understand domain-specific terminology
           - Recognize implicit references and abbreviations
           - Extract entities from various formats (text, documents, transcripts)
           - Maintain consistency across extractions
        
        4. KNOWLEDGE GRAPH PREPARATION:
           - Structure entities for knowledge graph integration
           - Define entity relationships and properties
           - Ensure traceability and linkage
           - Support semantic search and retrieval
        
        Always provide structured output with:
        - entities: List of extracted entities with types and properties
        - relationships: Connections between entities
        - confidence_scores: Reliability assessment for each extraction
        - tags: Categorization and classification tags
        - metadata: Additional context and properties
        
        Focus on accuracy, completeness, and ASPICE domain relevance.
        """
        
        super().__init__("EntityExtraction", anthropic_client, system_prompt)
        
        # Entity types and patterns
        self.entity_types = {
            "stakeholder": ["manager", "engineer", "architect", "tester", "analyst", "lead", "director"],
            "process_area": ["SYS", "SWE", "SUP", "MAN", "ACQ", "SPL"],
            "artifact": ["document", "specification", "plan", "report", "model", "code", "test"],
            "risk": ["risk", "issue", "concern", "challenge", "problem", "threat"],
            "technology": ["tool", "platform", "framework", "language", "system", "environment"],
            "requirement": ["requirement", "feature", "function", "constraint", "criteria"]
        }
    
    async def process(self, input_data: Any, context: AgentContext) -> AgentResponse:
        """
        Process entity extraction requests autonomously
        """
        try:
            if isinstance(input_data, dict):
                request_type = input_data.get("type", "general")
                data = input_data.get("data", {})
            else:
                request_type = "general"
                data = {"content": str(input_data)}
            
            if request_type == "text_extraction":
                return await self._extract_from_text(data, context)
            elif request_type == "document_extraction":
                return await self._extract_from_documents(data, context)
            elif request_type == "interview_extraction":
                return await self._extract_from_interview(data, context)
            elif request_type == "project_extraction":
                return await self._extract_from_project_data(data, context)
            elif request_type == "relationship_analysis":
                return await self._analyze_entity_relationships(data, context)
            else:
                return await self._general_extraction(data, context)
                
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Error in EntityExtraction: {str(e)}"
            )
    
    async def _extract_from_text(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Extract entities from free text
        """
        text = data.get("text", "")
        focus_types = data.get("focus_types", [])
        
        prompt = f"""
        AUTONOMOUS ENTITY EXTRACTION FROM TEXT:
        
        Text to analyze:
        {text}
        
        Focus on these entity types: {focus_types if focus_types else "all relevant entities"}
        
        Please extract and categorize entities:
        
        1. STAKEHOLDERS:
           - Names, roles, titles, responsibilities
           - Organizational units and teams
           - Contact information if available
           - Expertise areas and domains
        
        2. ASPICE PROCESS AREAS:
           - Explicit mentions of process areas (SYS.1, SWE.2, etc.)
           - Implicit references to ASPICE activities
           - Base practices and work products mentioned
           - Capability level indicators
        
        3. ARTIFACTS AND WORK PRODUCTS:
           - Documents, specifications, plans
           - Models, diagrams, code
           - Test artifacts and reports
           - Tools and templates
        
        4. RISKS AND ISSUES:
           - Identified problems or concerns
           - Potential risks and threats
           - Challenges and obstacles
           - Mitigation strategies mentioned
        
        5. TECHNOLOGIES AND TOOLS:
           - Software tools and platforms
           - Programming languages and frameworks
           - Development environments
           - Testing and analysis tools
        
        6. REQUIREMENTS AND CONSTRAINTS:
           - Functional and non-functional requirements
           - Business constraints and limitations
           - Regulatory and compliance requirements
           - Quality criteria and standards
        
        For each entity, provide:
        - Entity name and type
        - Confidence score (0.0-1.0)
        - Context where it was found
        - Relevant properties and attributes
        - ASPICE process area associations
        
        Format as structured JSON for knowledge graph integration.
        """
        
        extraction_result = await self._call_claude(prompt, context)
        
        # Parse and structure the results
        entities = self._parse_extraction_result(extraction_result)
        
        return AgentResponse(
            success=True,
            data={
                "entities": entities,
                "extraction_result": extraction_result,
                "text_length": len(text),
                "entity_count": len(entities)
            },
            message="Entity extraction from text completed",
            confidence=0.9,
            reasoning="Extracted and categorized entities from provided text",
            next_actions=[
                "Add entities to knowledge graph",
                "Analyze entity relationships",
                "Update project entity database",
                "Generate entity summary report"
            ]
        )
    
    async def _extract_from_documents(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Extract entities from document collections
        """
        documents = data.get("documents", [])
        document_types = data.get("document_types", [])
        
        prompt = f"""
        AUTONOMOUS ENTITY EXTRACTION FROM DOCUMENTS:
        
        Document Types: {document_types}
        Number of Documents: {len(documents)}
        
        Documents to analyze:
        {json.dumps(documents, indent=2)}
        
        Please extract entities across all documents:
        
        1. CROSS-DOCUMENT ENTITY IDENTIFICATION:
           - Identify entities mentioned across multiple documents
           - Resolve entity references and aliases
           - Track entity evolution and changes
           - Identify document-specific entities
        
        2. DOCUMENT METADATA EXTRACTION:
           - Authors, reviewers, approvers
           - Creation and modification dates
           - Version information and status
           - Document relationships and dependencies
        
        3. CONTENT ENTITY EXTRACTION:
           - Technical entities (components, interfaces, requirements)
           - Process entities (activities, roles, deliverables)
           - Quality entities (metrics, criteria, standards)
           - Risk entities (issues, assumptions, constraints)
        
        4. TRACEABILITY INFORMATION:
           - Links between requirements and implementations
           - Test coverage and verification relationships
           - Process flow and dependency chains
           - Change impact relationships
        
        5. ASPICE COMPLIANCE ENTITIES:
           - Work products and their characteristics
           - Process area coverage and gaps
           - Evidence and supporting artifacts
           - Compliance indicators and measures
        
        Provide comprehensive entity extraction with document source tracking.
        """
        
        extraction_result = await self._call_claude(prompt, context)
        entities = self._parse_extraction_result(extraction_result)
        
        return AgentResponse(
            success=True,
            data={
                "entities": entities,
                "documents_analyzed": len(documents),
                "document_types": document_types,
                "extraction_result": extraction_result
            },
            message="Entity extraction from documents completed",
            confidence=0.85,
            reasoning="Extracted entities from document collection with cross-document analysis"
        )
    
    async def _extract_from_interview(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Extract entities from interview transcripts
        """
        transcript = data.get("transcript", "")
        interviewer = data.get("interviewer", "")
        interviewee = data.get("interviewee", "")
        interview_focus = data.get("focus", "")
        
        prompt = f"""
        AUTONOMOUS ENTITY EXTRACTION FROM INTERVIEW:
        
        Interviewer: {interviewer}
        Interviewee: {interviewee}
        Interview Focus: {interview_focus}
        
        Transcript:
        {transcript}
        
        Please extract entities with interview-specific context:
        
        1. PARTICIPANT ENTITIES:
           - Interviewer and interviewee details
           - Mentioned colleagues and stakeholders
           - Organizational context and relationships
           - Expertise areas and responsibilities
        
        2. PROCESS AND PRACTICE ENTITIES:
           - Current processes described
           - Tools and methods mentioned
           - Work products and deliverables discussed
           - Process gaps and improvement areas
        
        3. OPINION AND SENTIMENT ENTITIES:
           - Positive and negative sentiments
           - Concerns and satisfaction areas
           - Suggestions and recommendations
           - Confidence levels and uncertainties
        
        4. FACTUAL ENTITIES:
           - Concrete examples and cases
           - Specific tools and technologies
           - Timelines and schedules mentioned
           - Metrics and measurements discussed
        
        5. ASPICE-SPECIFIC ENTITIES:
           - Process areas explicitly or implicitly discussed
           - Evidence and work products mentioned
           - Capability level indicators
           - Compliance gaps and strengths
        
        Include speaker attribution and context for each entity.
        """
        
        extraction_result = await self._call_claude(prompt, context)
        entities = self._parse_extraction_result(extraction_result)
        
        return AgentResponse(
            success=True,
            data={
                "entities": entities,
                "interviewer": interviewer,
                "interviewee": interviewee,
                "transcript_length": len(transcript),
                "extraction_result": extraction_result
            },
            message="Entity extraction from interview completed",
            confidence=0.9,
            reasoning="Extracted entities from interview with speaker attribution and context"
        )
    
    async def _extract_from_project_data(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Extract entities from comprehensive project data
        """
        project_info = data.get("project_info", {})
        stakeholder_data = data.get("stakeholders", [])
        technical_data = data.get("technical_info", {})
        
        prompt = f"""
        AUTONOMOUS ENTITY EXTRACTION FROM PROJECT DATA:
        
        Project Information:
        {json.dumps(project_info, indent=2)}
        
        Stakeholder Data:
        {json.dumps(stakeholder_data, indent=2)}
        
        Technical Information:
        {json.dumps(technical_data, indent=2)}
        
        Please extract and structure all project entities:
        
        1. PROJECT ENTITIES:
           - Project name, ID, and classification
           - Scope, objectives, and deliverables
           - Timeline, milestones, and phases
           - Budget, resources, and constraints
        
        2. ORGANIZATIONAL ENTITIES:
           - Client organization and structure
           - Project team and roles
           - Stakeholder groups and interests
           - Decision makers and influencers
        
        3. TECHNICAL ENTITIES:
           - Product and system components
           - Technologies and platforms
           - Development tools and environments
           - Standards and regulations
        
        4. PROCESS ENTITIES:
           - Current development processes
           - Quality assurance practices
           - Configuration management approaches
           - Risk management procedures
        
        5. ASPICE SCOPE ENTITIES:
           - Target process areas and levels
           - Assessment scope and boundaries
           - Compliance requirements and criteria
           - Improvement goals and objectives
        
        Create a comprehensive entity map for the entire project.
        """
        
        extraction_result = await self._call_claude(prompt, context)
        entities = self._parse_extraction_result(extraction_result)
        
        return AgentResponse(
            success=True,
            data={
                "entities": entities,
                "project_id": project_info.get("id", "unknown"),
                "stakeholder_count": len(stakeholder_data),
                "extraction_result": extraction_result
            },
            message="Entity extraction from project data completed",
            confidence=0.95,
            reasoning="Extracted comprehensive entity map from project data"
        )
    
    async def _analyze_entity_relationships(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Analyze relationships between extracted entities
        """
        entities = data.get("entities", [])
        relationship_types = data.get("relationship_types", [])
        
        prompt = f"""
        AUTONOMOUS ENTITY RELATIONSHIP ANALYSIS:
        
        Entities to analyze:
        {json.dumps(entities, indent=2)}
        
        Focus on these relationship types: {relationship_types if relationship_types else "all relevant relationships"}
        
        Please analyze and identify relationships:
        
        1. HIERARCHICAL RELATIONSHIPS:
           - Organizational reporting structures
           - Process area hierarchies and dependencies
           - Document and artifact hierarchies
           - System and component structures
        
        2. FUNCTIONAL RELATIONSHIPS:
           - Role and responsibility assignments
           - Process input/output relationships
           - Tool and artifact usage patterns
           - Stakeholder interaction patterns
        
        3. TEMPORAL RELATIONSHIPS:
           - Process sequence and dependencies
           - Timeline and milestone relationships
           - Version and evolution relationships
           - Cause and effect relationships
        
        4. ASPICE-SPECIFIC RELATIONSHIPS:
           - Process area to work product mappings
           - Evidence to base practice relationships
           - Stakeholder to process area responsibilities
           - Gap to improvement action relationships
        
        5. SEMANTIC RELATIONSHIPS:
           - Conceptual similarities and differences
           - Synonym and alias relationships
           - Category and classification relationships
           - Context and domain relationships
        
        For each relationship, provide:
        - Source and target entities
        - Relationship type and strength
        - Confidence score
        - Supporting evidence
        - ASPICE relevance
        
        Format for knowledge graph integration.
        """
        
        relationship_analysis = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "relationship_analysis": relationship_analysis,
                "entities_analyzed": len(entities),
                "relationship_types": relationship_types
            },
            message="Entity relationship analysis completed",
            confidence=0.85,
            reasoning="Analyzed relationships between entities for knowledge graph integration"
        )
    
    async def _general_extraction(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Handle general entity extraction requests
        """
        content = data.get("content", "")
        
        prompt = f"""
        GENERAL ENTITY EXTRACTION REQUEST:
        
        Content to analyze:
        {content}
        
        Please perform comprehensive entity extraction:
        1. Identify all relevant entities
        2. Categorize by type and importance
        3. Assess confidence and quality
        4. Determine ASPICE relevance
        5. Suggest relationships and connections
        
        Focus on entities that support ASPICE consulting activities.
        """
        
        extraction_result = await self._call_claude(prompt, context)
        entities = self._parse_extraction_result(extraction_result)
        
        return AgentResponse(
            success=True,
            data={
                "entities": entities,
                "extraction_result": extraction_result
            },
            message="General entity extraction completed",
            confidence=0.8,
            reasoning="Performed general entity extraction and categorization"
        )
    
    def _parse_extraction_result(self, extraction_text: str) -> List[Dict]:
        """
        Parse extraction results into structured entity list
        """
        entities = []
        
        try:
            # Try to parse as JSON first
            if extraction_text.strip().startswith('[') or extraction_text.strip().startswith('{'):
                parsed = json.loads(extraction_text)
                if isinstance(parsed, list):
                    entities = parsed
                elif isinstance(parsed, dict) and 'entities' in parsed:
                    entities = parsed['entities']
        except json.JSONDecodeError:
            # Fallback to text parsing
            entities = self._extract_entities_from_text(extraction_text)
        
        return entities
    
    def _extract_entities_from_text(self, text: str) -> List[Dict]:
        """
        Extract entities from text using pattern matching
        """
        entities = []
        lines = text.split('\n')
        
        current_entity = {}
        for line in lines:
            line = line.strip()
            if not line:
                if current_entity:
                    entities.append(current_entity)
                    current_entity = {}
                continue
            
            # Simple pattern matching for entity extraction
            if line.startswith('- ') or line.startswith('* '):
                if current_entity:
                    entities.append(current_entity)
                current_entity = {
                    "name": line[2:].strip(),
                    "type": "unknown",
                    "confidence": 0.7,
                    "properties": {}
                }
            elif ':' in line and current_entity:
                key, value = line.split(':', 1)
                current_entity["properties"][key.strip().lower()] = value.strip()
        
        if current_entity:
            entities.append(current_entity)
        
        return entities