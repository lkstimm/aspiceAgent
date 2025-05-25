"""
Autonomous Onboarding Service - Orchestrates the complete project onboarding workflow
"""

import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime, timedelta
import uuid

from app.core.agent_base import AgentOrchestrator, AgentContext
from app.agents.project_orchestrator import ProjectOrchestratorAgent
from app.agents.entity_extraction import EntityExtractionAgent
from app.agents.gap_analysis_expert import GapAnalysisExpertAgent
from app.agents.documentation_strategy import DocumentationStrategyAgent
from app.agents.report_generation import ReportGenerationAgent
from app.services.anthropic_service import AnthropicService
from app.services.knowledge_graph import KnowledgeGraph


class AutonomousOnboardingService:
    """
    Manages the complete autonomous onboarding workflow for new ASPICE projects.
    This service coordinates multiple AI agents to automatically set up and initialize projects.
    """
    
    def __init__(self):
        self.anthropic_service = AnthropicService()
        self.knowledge_graph = KnowledgeGraph()
        self.orchestrator = AgentOrchestrator()
        
        # Initialize agents
        self.project_orchestrator = ProjectOrchestratorAgent(self.anthropic_service.client)
        self.entity_extraction = EntityExtractionAgent(self.anthropic_service.client)
        self.gap_analysis_expert = GapAnalysisExpertAgent(self.anthropic_service.client)
        self.documentation_strategy = DocumentationStrategyAgent(self.anthropic_service.client)
        self.report_generation = ReportGenerationAgent(self.anthropic_service.client)
        
        # Register agents with orchestrator
        self.orchestrator.register_agent("ProjectOrchestrator", self.project_orchestrator)
        self.orchestrator.register_agent("EntityExtraction", self.entity_extraction)
        self.orchestrator.register_agent("GapAnalysisExpert", self.gap_analysis_expert)
        self.orchestrator.register_agent("DocumentationStrategy", self.documentation_strategy)
        self.orchestrator.register_agent("ReportGeneration", self.report_generation)
    
    async def initiate_autonomous_onboarding(self, project_id: str, onboarding_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Initiate the complete autonomous onboarding workflow
        """
        try:
            # Create agent context
            context = AgentContext(
                project_id=project_id,
                user_id="system",
                session_id=str(uuid.uuid4()),
                metadata={
                    "workflow": "autonomous_onboarding",
                    "timestamp": datetime.utcnow().isoformat(),
                    "onboarding_data": onboarding_data
                }
            )
            
            # Phase 1: Project Analysis and Structure Creation
            print(f"🎯 Phase 1: Project Analysis for {project_id}")
            project_analysis = await self._phase_1_project_analysis(onboarding_data, context)
            
            # Phase 2: Knowledge Graph Creation
            print(f"🧠 Phase 2: Knowledge Graph Creation for {project_id}")
            knowledge_graph_result = await self._phase_2_knowledge_graph_creation(onboarding_data, context)
            
            # Phase 3: Stakeholder Analysis and Interview Preparation
            print(f"👥 Phase 3: Stakeholder Analysis for {project_id}")
            stakeholder_analysis = await self._phase_3_stakeholder_analysis(onboarding_data, context)
            
            # Phase 4: Assessment Framework Setup
            print(f"📋 Phase 4: Assessment Framework Setup for {project_id}")
            assessment_framework = await self._phase_4_assessment_framework(onboarding_data, context)
            
            # Phase 5: Monitoring and Reporting Setup
            print(f"📊 Phase 5: Monitoring Setup for {project_id}")
            monitoring_setup = await self._phase_5_monitoring_setup(onboarding_data, context)
            
            # Compile onboarding results
            onboarding_result = {
                "project_id": project_id,
                "status": "completed",
                "timestamp": datetime.utcnow().isoformat(),
                "phases": {
                    "project_analysis": project_analysis,
                    "knowledge_graph": knowledge_graph_result,
                    "stakeholder_analysis": stakeholder_analysis,
                    "assessment_framework": assessment_framework,
                    "monitoring_setup": monitoring_setup
                },
                "next_actions": self._generate_next_actions(onboarding_data),
                "estimated_timeline": self._generate_project_timeline(onboarding_data),
                "success_metrics": self._define_success_metrics(onboarding_data)
            }
            
            print(f"✅ Autonomous onboarding completed for project {project_id}")
            return onboarding_result
            
        except Exception as e:
            print(f"❌ Error in autonomous onboarding for project {project_id}: {str(e)}")
            return {
                "project_id": project_id,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _phase_1_project_analysis(self, onboarding_data: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """
        Phase 1: Comprehensive project analysis and structure creation
        """
        try:
            # Use ProjectOrchestrator to analyze the project
            analysis_request = {
                "type": "project_creation",
                "data": onboarding_data
            }
            
            response = await self.project_orchestrator.process(analysis_request, context)
            
            if response.success:
                return {
                    "status": "completed",
                    "analysis": response.data,
                    "confidence": response.confidence,
                    "recommendations": response.next_actions
                }
            else:
                return {
                    "status": "error",
                    "error": response.message
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _phase_2_knowledge_graph_creation(self, onboarding_data: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """
        Phase 2: Create knowledge graph from project data
        """
        try:
            # Extract entities from onboarding data
            extraction_request = {
                "type": "project_onboarding",
                "data": onboarding_data
            }
            
            response = await self.entity_extraction.process(extraction_request, context)
            
            if response.success:
                # Store entities in knowledge graph
                entities = response.data.get("entities", [])
                for entity in entities:
                    self.knowledge_graph.add_entity(
                        project_id=context.project_id,
                        entity_type=entity.get("type", "unknown"),
                        content=entity.get("content", ""),
                        metadata=entity.get("metadata", {})
                    )
                
                return {
                    "status": "completed",
                    "entities_extracted": len(entities),
                    "knowledge_graph_initialized": True,
                    "confidence": response.confidence
                }
            else:
                return {
                    "status": "error",
                    "error": response.message
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _phase_3_stakeholder_analysis(self, onboarding_data: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """
        Phase 3: Analyze stakeholders and prepare interview strategy
        """
        try:
            # Prepare stakeholder analysis
            stakeholder_request = {
                "type": "stakeholder_analysis",
                "data": {
                    "stakeholders": onboarding_data.get("stakeholders", []),
                    "project_context": {
                        "name": onboarding_data.get("projectName", ""),
                        "type": onboarding_data.get("projectType", ""),
                        "scope": onboarding_data.get("scope", ""),
                        "critical_processes": onboarding_data.get("criticalProcesses", [])
                    }
                }
            }
            
            response = await self.gap_analysis_expert.process(stakeholder_request, context)
            
            if response.success:
                return {
                    "status": "completed",
                    "interview_strategy": response.data,
                    "stakeholder_mapping": response.data.get("stakeholder_mapping", {}),
                    "interview_questions": response.data.get("interview_questions", []),
                    "confidence": response.confidence
                }
            else:
                return {
                    "status": "error",
                    "error": response.message
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _phase_4_assessment_framework(self, onboarding_data: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """
        Phase 4: Set up ASPICE assessment framework and documentation structure
        """
        try:
            # Create assessment framework
            framework_request = {
                "type": "assessment_framework",
                "data": {
                    "project_type": onboarding_data.get("projectType", ""),
                    "target_level": onboarding_data.get("targetLevel", ""),
                    "critical_processes": onboarding_data.get("criticalProcesses", []),
                    "current_maturity": onboarding_data.get("currentMaturity", ""),
                    "industry": onboarding_data.get("industry", "")
                }
            }
            
            response = await self.documentation_strategy.process(framework_request, context)
            
            if response.success:
                return {
                    "status": "completed",
                    "framework": response.data,
                    "documentation_structure": response.data.get("documentation_structure", {}),
                    "assessment_templates": response.data.get("assessment_templates", []),
                    "confidence": response.confidence
                }
            else:
                return {
                    "status": "error",
                    "error": response.message
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _phase_5_monitoring_setup(self, onboarding_data: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """
        Phase 5: Set up monitoring, reporting, and dashboard configuration
        """
        try:
            # Configure monitoring and reporting
            monitoring_request = {
                "type": "monitoring_setup",
                "data": {
                    "autonomy_level": onboarding_data.get("autonomyLevel", "high"),
                    "reporting_frequency": onboarding_data.get("reportingFrequency", "daily"),
                    "communication_style": onboarding_data.get("communicationStyle", "detailed"),
                    "stakeholders": onboarding_data.get("stakeholders", [])
                }
            }
            
            response = await self.report_generation.process(monitoring_request, context)
            
            if response.success:
                return {
                    "status": "completed",
                    "monitoring_config": response.data,
                    "dashboard_setup": response.data.get("dashboard_setup", {}),
                    "reporting_schedule": response.data.get("reporting_schedule", {}),
                    "confidence": response.confidence
                }
            else:
                return {
                    "status": "error",
                    "error": response.message
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _generate_next_actions(self, onboarding_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate autonomous next actions based on onboarding data
        """
        next_actions = []
        
        # Stakeholder interview scheduling
        if onboarding_data.get("stakeholders"):
            next_actions.append({
                "action": "schedule_stakeholder_interviews",
                "description": "Automatically schedule interviews with key stakeholders",
                "priority": "high",
                "estimated_duration": "2-3 days",
                "responsible_agent": "GapAnalysisExpert"
            })
        
        # Document collection
        next_actions.append({
            "action": "collect_existing_documents",
            "description": "Gather and analyze existing project documentation",
            "priority": "medium",
            "estimated_duration": "1-2 days",
            "responsible_agent": "EntityExtraction"
        })
        
        # Initial gap analysis
        if onboarding_data.get("criticalProcesses"):
            next_actions.append({
                "action": "initial_gap_analysis",
                "description": "Conduct preliminary gap analysis for critical processes",
                "priority": "high",
                "estimated_duration": "3-5 days",
                "responsible_agent": "GapAnalysisExpert"
            })
        
        # Process documentation setup
        next_actions.append({
            "action": "setup_process_documentation",
            "description": "Create initial process documentation templates",
            "priority": "medium",
            "estimated_duration": "2-3 days",
            "responsible_agent": "DocumentationStrategy"
        })
        
        return next_actions
    
    def _generate_project_timeline(self, onboarding_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate estimated project timeline based on onboarding data
        """
        start_date = datetime.utcnow()
        
        # Base timeline estimates
        timeline_estimates = {
            "aspice_assessment": {"weeks": 12, "phases": 6},
            "process_improvement": {"weeks": 16, "phases": 7},
            "certification_prep": {"weeks": 20, "phases": 8},
            "gap_analysis": {"weeks": 6, "phases": 4},
            "full_consulting": {"weeks": 24, "phases": 9}
        }
        
        project_type = onboarding_data.get("projectType", "aspice_assessment")
        estimate = timeline_estimates.get(project_type, timeline_estimates["aspice_assessment"])
        
        end_date = start_date + timedelta(weeks=estimate["weeks"])
        
        return {
            "start_date": start_date.isoformat(),
            "estimated_end_date": end_date.isoformat(),
            "total_weeks": estimate["weeks"],
            "total_phases": estimate["phases"],
            "project_type": project_type,
            "milestones": self._generate_milestones(start_date, estimate["weeks"], project_type)
        }
    
    def _generate_milestones(self, start_date: datetime, total_weeks: int, project_type: str) -> List[Dict[str, Any]]:
        """
        Generate project milestones based on project type
        """
        milestones = []
        
        # Common milestones for all project types
        common_milestones = [
            {"name": "Project Kickoff", "week": 1, "description": "Project initialization and team setup"},
            {"name": "Stakeholder Interviews", "week": 2, "description": "Conduct stakeholder interviews and requirements gathering"},
            {"name": "Gap Analysis", "week": 4, "description": "Complete ASPICE gap analysis"},
            {"name": "Improvement Planning", "week": 6, "description": "Develop improvement roadmap and strategies"},
            {"name": "Mid-Project Review", "week": int(total_weeks * 0.6), "description": "Review progress and adjust plans"},
            {"name": "Final Assessment", "week": total_weeks - 2, "description": "Conduct final ASPICE assessment"},
            {"name": "Project Closure", "week": total_weeks, "description": "Project completion and handover"}
        ]
        
        for milestone in common_milestones:
            milestone_date = start_date + timedelta(weeks=milestone["week"])
            milestones.append({
                "name": milestone["name"],
                "date": milestone_date.isoformat(),
                "week": milestone["week"],
                "description": milestone["description"],
                "status": "planned"
            })
        
        return milestones
    
    def _define_success_metrics(self, onboarding_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Define success metrics based on project goals
        """
        return {
            "primary_metrics": [
                {
                    "name": "ASPICE Capability Level Achievement",
                    "target": onboarding_data.get("targetLevel", "level_2"),
                    "measurement": "Capability level ratings for critical processes"
                },
                {
                    "name": "Process Coverage",
                    "target": "100%",
                    "measurement": "Percentage of critical processes assessed and improved"
                },
                {
                    "name": "Stakeholder Satisfaction",
                    "target": ">= 4.0/5.0",
                    "measurement": "Average stakeholder satisfaction rating"
                }
            ],
            "secondary_metrics": [
                {
                    "name": "Documentation Completeness",
                    "target": ">= 95%",
                    "measurement": "Percentage of required documentation completed"
                },
                {
                    "name": "Timeline Adherence",
                    "target": "+/- 10%",
                    "measurement": "Variance from planned timeline"
                },
                {
                    "name": "Budget Adherence",
                    "target": "+/- 5%",
                    "measurement": "Variance from planned budget"
                }
            ],
            "success_criteria": onboarding_data.get("successCriteria", ""),
            "business_drivers": onboarding_data.get("businessDrivers", "")
        }
    
    async def get_onboarding_status(self, project_id: str) -> Dict[str, Any]:
        """
        Get the current status of the onboarding process
        """
        # This would typically query the database for actual status
        # For now, return a mock status
        return {
            "project_id": project_id,
            "status": "in_progress",
            "current_phase": "stakeholder_analysis",
            "progress_percentage": 65,
            "last_updated": datetime.utcnow().isoformat(),
            "active_agents": ["ProjectOrchestrator", "EntityExtraction", "GapAnalysisExpert"],
            "completed_phases": ["project_analysis", "knowledge_graph"],
            "pending_phases": ["assessment_framework", "monitoring_setup"]
        }