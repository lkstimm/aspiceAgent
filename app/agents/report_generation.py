"""
Report Generation Agent - Creates formatted reports and dashboards
"""

from typing import Any, Dict, List
import json
from datetime import datetime
from app.core.agent_base import AutonomousAgent, AgentContext, AgentResponse
from anthropic import AsyncAnthropic


class ReportGenerationAgent(AutonomousAgent):
    """
    Autonomous agent specialized in generating professional ASPICE reports and dashboards.
    Creates gap analysis reports, assessment summaries, progress reports, and interactive dashboards.
    """
    
    def __init__(self, anthropic_client: AsyncAnthropic):
        system_prompt = """
        You are the Report Generation Agent for ASPICE consulting. Your expertise includes:
        
        1. PROFESSIONAL REPORT CREATION:
           - Executive summaries and detailed technical reports
           - Gap analysis reports with findings and recommendations
           - Assessment reports with capability level ratings
           - Progress reports and status updates
           - Dashboard specifications and visualizations
        
        2. ASPICE REPORTING STANDARDS:
           - Compliance with ASPICE assessment reporting requirements
           - Proper capability level documentation and justification
           - Evidence-based findings and recommendations
           - Traceability between gaps, evidence, and process areas
        
        3. MULTI-FORMAT OUTPUT:
           - HTML reports with interactive elements
           - PDF-ready formatted documents
           - Dashboard specifications for web interfaces
           - Executive presentations and summaries
           - Data visualizations and charts
        
        4. AUTONOMOUS CONTENT GENERATION:
           - Analyze input data and automatically generate appropriate content
           - Create compelling narratives from technical data
           - Generate actionable insights and recommendations
           - Ensure consistency and professional presentation
        
        Always generate reports with:
        - Clear executive summaries
        - Detailed findings with evidence
        - Actionable recommendations
        - Professional formatting and structure
        - Appropriate visualizations and charts
        - Proper references and traceability
        
        Focus on creating reports that drive decision-making and action.
        """
        
        super().__init__("ReportGeneration", anthropic_client, system_prompt)
        
        # Report templates and structures
        self.report_templates = {
            "gap_analysis": {
                "sections": ["Executive Summary", "Assessment Scope", "Methodology", 
                           "Detailed Findings", "Gap Analysis", "Recommendations", "Next Steps"],
                "visualizations": ["capability_radar", "gap_heatmap", "priority_matrix"]
            },
            "assessment_summary": {
                "sections": ["Overview", "Capability Ratings", "Key Strengths", 
                           "Critical Gaps", "Improvement Roadmap", "Conclusions"],
                "visualizations": ["rating_chart", "process_coverage", "timeline"]
            },
            "progress_report": {
                "sections": ["Progress Overview", "Completed Activities", "Current Status", 
                           "Upcoming Milestones", "Issues and Risks", "Recommendations"],
                "visualizations": ["progress_chart", "milestone_timeline", "risk_matrix"]
            },
            "dashboard": {
                "components": ["kpi_cards", "progress_charts", "gap_analysis", 
                             "action_items", "risk_indicators", "timeline_view"],
                "interactivity": ["filters", "drill_down", "real_time_updates"]
            }
        }
    
    async def process(self, input_data: Any, context: AgentContext) -> AgentResponse:
        """
        Process report generation requests autonomously
        """
        try:
            if isinstance(input_data, dict):
                request_type = input_data.get("type", "general")
                data = input_data.get("data", {})
            else:
                request_type = "general"
                data = {"content": str(input_data)}
            
            if request_type == "gap_analysis_report":
                return await self._generate_gap_analysis_report(data, context)
            elif request_type == "assessment_summary":
                return await self._generate_assessment_summary(data, context)
            elif request_type == "progress_report":
                return await self._generate_progress_report(data, context)
            elif request_type == "dashboard_specification":
                return await self._generate_dashboard_specification(data, context)
            elif request_type == "executive_summary":
                return await self._generate_executive_summary(data, context)
            elif request_type == "detailed_findings":
                return await self._generate_detailed_findings(data, context)
            else:
                return await self._general_report_generation(data, context)
                
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Error in ReportGeneration: {str(e)}"
            )
    
    async def _generate_gap_analysis_report(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Generate comprehensive gap analysis report
        """
        project_info = data.get("project_info", {})
        gap_findings = data.get("gap_findings", [])
        evidence_data = data.get("evidence", {})
        capability_ratings = data.get("capability_ratings", {})
        
        prompt = f"""
        AUTONOMOUS GAP ANALYSIS REPORT GENERATION:
        
        Project Information:
        {json.dumps(project_info, indent=2)}
        
        Gap Findings:
        {json.dumps(gap_findings, indent=2)}
        
        Evidence Data:
        {json.dumps(evidence_data, indent=2)}
        
        Capability Ratings:
        {json.dumps(capability_ratings, indent=2)}
        
        Please generate a comprehensive gap analysis report with:
        
        1. EXECUTIVE SUMMARY:
           - Project overview and assessment scope
           - Key findings and overall assessment
           - Critical gaps and priority recommendations
           - Expected benefits and next steps
        
        2. ASSESSMENT METHODOLOGY:
           - Assessment approach and standards used
           - Evidence collection and evaluation methods
           - Rating criteria and justification approach
           - Limitations and assumptions
        
        3. DETAILED FINDINGS BY PROCESS AREA:
           - Current capability level for each process area
           - Evidence quality and completeness assessment
           - Specific gaps and missing practices
           - Strengths and positive findings
        
        4. COMPREHENSIVE GAP ANALYSIS:
           - Critical gaps preventing compliance
           - Process implementation gaps
           - Documentation and evidence gaps
           - Organizational and cultural gaps
        
        5. PRIORITIZED RECOMMENDATIONS:
           - High-priority improvements (must-have)
           - Medium-priority improvements (should-have)
           - Low-priority improvements (nice-to-have)
           - Implementation approach and timeline
        
        6. IMPROVEMENT ROADMAP:
           - Phased implementation strategy
           - Quick wins and long-term improvements
           - Resource requirements and estimates
           - Success metrics and monitoring approach
        
        7. VISUALIZATION SPECIFICATIONS:
           - Capability radar chart showing current vs. target levels
           - Gap heatmap by process area and priority
           - Priority matrix plotting impact vs. effort
           - Timeline showing improvement phases
        
        Format as a professional report suitable for both technical and executive audiences.
        Include specific data points, evidence references, and actionable recommendations.
        """
        
        report_content = await self._call_claude(prompt, context)
        
        # Generate visualization specifications
        visualizations = await self._generate_visualizations(
            "gap_analysis", 
            {
                "capability_ratings": capability_ratings,
                "gap_findings": gap_findings,
                "project_info": project_info
            },
            context
        )
        
        return AgentResponse(
            success=True,
            data={
                "report_content": report_content,
                "report_type": "gap_analysis",
                "visualizations": visualizations,
                "metadata": {
                    "project_id": context.project_id,
                    "generated_at": datetime.now().isoformat(),
                    "gaps_analyzed": len(gap_findings),
                    "process_areas": list(capability_ratings.keys())
                }
            },
            message="Gap analysis report generated",
            confidence=0.95,
            reasoning="Generated comprehensive gap analysis report with findings, recommendations, and visualizations",
            next_actions=[
                "Review report with stakeholders",
                "Create presentation version",
                "Generate action item tracking",
                "Schedule follow-up assessments"
            ]
        )
    
    async def _generate_assessment_summary(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Generate executive assessment summary
        """
        assessment_data = data.get("assessment_data", {})
        key_findings = data.get("key_findings", [])
        recommendations = data.get("recommendations", [])
        
        prompt = f"""
        AUTONOMOUS ASSESSMENT SUMMARY GENERATION:
        
        Assessment Data:
        {json.dumps(assessment_data, indent=2)}
        
        Key Findings:
        {json.dumps(key_findings, indent=2)}
        
        Recommendations:
        {json.dumps(recommendations, indent=2)}
        
        Please generate an executive assessment summary with:
        
        1. ASSESSMENT OVERVIEW:
           - Project and organization context
           - Assessment scope and objectives
           - Methodology and approach used
           - Timeline and participants
        
        2. CAPABILITY RATINGS SUMMARY:
           - Overall capability maturity level
           - Process area ratings with justification
           - Comparison to industry benchmarks
           - Strengths and improvement areas
        
        3. KEY STRENGTHS:
           - Well-implemented processes and practices
           - Strong organizational capabilities
           - Effective tools and technologies
           - Positive cultural and management factors
        
        4. CRITICAL GAPS:
           - High-risk gaps requiring immediate attention
           - Compliance-threatening deficiencies
           - Process implementation weaknesses
           - Resource and capability constraints
        
        5. STRATEGIC RECOMMENDATIONS:
           - Top 3-5 strategic improvement priorities
           - Implementation approach and timeline
           - Resource requirements and investment
           - Expected benefits and ROI
        
        6. IMPROVEMENT ROADMAP:
           - Phase 1: Critical fixes and quick wins
           - Phase 2: Core process improvements
           - Phase 3: Maturity advancement
           - Success metrics and milestones
        
        7. CONCLUSIONS AND NEXT STEPS:
           - Overall assessment conclusion
           - Readiness for ASPICE certification
           - Immediate next steps
           - Long-term strategic direction
        
        Create a concise, executive-focused summary that drives decision-making.
        """
        
        summary_content = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "summary_content": summary_content,
                "report_type": "assessment_summary",
                "key_findings_count": len(key_findings),
                "recommendations_count": len(recommendations)
            },
            message="Assessment summary generated",
            confidence=0.9,
            reasoning="Generated executive assessment summary with strategic focus"
        )
    
    async def _generate_progress_report(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Generate progress tracking report
        """
        project_status = data.get("project_status", {})
        completed_activities = data.get("completed_activities", [])
        current_activities = data.get("current_activities", [])
        upcoming_milestones = data.get("upcoming_milestones", [])
        issues_risks = data.get("issues_risks", [])
        
        prompt = f"""
        AUTONOMOUS PROGRESS REPORT GENERATION:
        
        Project Status:
        {json.dumps(project_status, indent=2)}
        
        Completed Activities:
        {json.dumps(completed_activities, indent=2)}
        
        Current Activities:
        {json.dumps(current_activities, indent=2)}
        
        Upcoming Milestones:
        {json.dumps(upcoming_milestones, indent=2)}
        
        Issues and Risks:
        {json.dumps(issues_risks, indent=2)}
        
        Please generate a comprehensive progress report with:
        
        1. PROGRESS OVERVIEW:
           - Overall project health and status
           - Percentage completion by phase
           - Key achievements and milestones reached
           - Timeline adherence and schedule variance
        
        2. COMPLETED ACTIVITIES:
           - Major deliverables and outcomes achieved
           - Quality metrics and success criteria met
           - Lessons learned and best practices
           - Stakeholder feedback and satisfaction
        
        3. CURRENT STATUS:
           - Activities in progress and their status
           - Resource utilization and team performance
           - Quality indicators and metrics
           - Blockers and dependencies being addressed
        
        4. UPCOMING MILESTONES:
           - Next major deliverables and deadlines
           - Critical path activities and dependencies
           - Resource requirements and allocation
           - Success criteria and acceptance criteria
        
        5. ISSUES AND RISKS:
           - Current issues and their impact
           - Risk status and mitigation effectiveness
           - New risks identified and assessment
           - Escalation needs and decisions required
        
        6. PERFORMANCE METRICS:
           - Schedule performance indicators
           - Quality metrics and trends
           - Resource utilization efficiency
           - Stakeholder satisfaction scores
        
        7. RECOMMENDATIONS AND ACTIONS:
           - Immediate actions required
           - Process improvements identified
           - Resource adjustments needed
           - Strategic recommendations
        
        Create a clear, data-driven progress report that supports project management decisions.
        """
        
        progress_content = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "progress_content": progress_content,
                "report_type": "progress_report",
                "completed_count": len(completed_activities),
                "current_count": len(current_activities),
                "milestone_count": len(upcoming_milestones)
            },
            message="Progress report generated",
            confidence=0.9,
            reasoning="Generated comprehensive progress report with metrics and recommendations"
        )
    
    async def _generate_dashboard_specification(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Generate interactive dashboard specification
        """
        dashboard_type = data.get("dashboard_type", "project_overview")
        data_sources = data.get("data_sources", {})
        user_requirements = data.get("user_requirements", {})
        
        prompt = f"""
        AUTONOMOUS DASHBOARD SPECIFICATION GENERATION:
        
        Dashboard Type: {dashboard_type}
        Data Sources: {json.dumps(data_sources, indent=2)}
        User Requirements: {json.dumps(user_requirements, indent=2)}
        
        Please generate a comprehensive dashboard specification with:
        
        1. DASHBOARD OVERVIEW:
           - Purpose and target users
           - Key objectives and use cases
           - Data refresh frequency and sources
           - Access control and permissions
        
        2. LAYOUT AND STRUCTURE:
           - Page layout and navigation structure
           - Component placement and sizing
           - Responsive design considerations
           - Branding and visual identity
        
        3. KEY PERFORMANCE INDICATORS (KPIs):
           - Primary metrics and their calculations
           - Target values and thresholds
           - Trend indicators and alerts
           - Drill-down capabilities
        
        4. VISUALIZATION COMPONENTS:
           - Charts and graphs specifications
           - Data tables and grids
           - Progress indicators and gauges
           - Interactive filters and controls
        
        5. DATA INTEGRATION:
           - Data source connections and APIs
           - Data transformation and aggregation
           - Real-time vs. batch update requirements
           - Data quality and validation rules
        
        6. INTERACTIVITY FEATURES:
           - Filter and search capabilities
           - Drill-down and drill-through navigation
           - Export and sharing functionality
           - Customization and personalization options
        
        7. TECHNICAL SPECIFICATIONS:
           - Technology stack and frameworks
           - Performance requirements and optimization
           - Security and access control
           - Mobile and cross-browser compatibility
        
        8. IMPLEMENTATION PLAN:
           - Development phases and timeline
           - Testing and validation approach
           - Deployment and rollout strategy
           - Training and support requirements
        
        Create detailed specifications that enable development and implementation.
        """
        
        dashboard_spec = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "dashboard_specification": dashboard_spec,
                "dashboard_type": dashboard_type,
                "data_sources": list(data_sources.keys()),
                "component_count": len(self.report_templates["dashboard"]["components"])
            },
            message="Dashboard specification generated",
            confidence=0.85,
            reasoning="Generated comprehensive dashboard specification with technical details"
        )
    
    async def _generate_executive_summary(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Generate executive summary from detailed data
        """
        detailed_data = data.get("detailed_data", {})
        target_audience = data.get("target_audience", "executives")
        key_messages = data.get("key_messages", [])
        
        prompt = f"""
        AUTONOMOUS EXECUTIVE SUMMARY GENERATION:
        
        Detailed Data:
        {json.dumps(detailed_data, indent=2)}
        
        Target Audience: {target_audience}
        Key Messages: {key_messages}
        
        Please generate a compelling executive summary with:
        
        1. SITUATION OVERVIEW:
           - Current state and context
           - Key challenges and opportunities
           - Strategic importance and urgency
           - Stakeholder impact and implications
        
        2. KEY FINDINGS:
           - Most critical discoveries and insights
           - Quantified impacts and metrics
           - Comparison to benchmarks and standards
           - Risk assessment and implications
        
        3. STRATEGIC RECOMMENDATIONS:
           - Top 3-5 actionable recommendations
           - Expected benefits and outcomes
           - Investment requirements and ROI
           - Implementation timeline and approach
        
        4. DECISION POINTS:
           - Critical decisions required
           - Options and alternatives analysis
           - Risks of action vs. inaction
           - Resource allocation needs
        
        5. NEXT STEPS:
           - Immediate actions required
           - Timeline and milestones
           - Success metrics and monitoring
           - Escalation and governance needs
        
        Keep the summary concise (2-3 pages), focused on business impact, and action-oriented.
        Use clear, non-technical language appropriate for {target_audience}.
        """
        
        executive_summary = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "executive_summary": executive_summary,
                "target_audience": target_audience,
                "key_messages": key_messages
            },
            message="Executive summary generated",
            confidence=0.9,
            reasoning="Generated concise executive summary focused on business impact and decisions"
        )
    
    async def _generate_detailed_findings(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Generate detailed findings report
        """
        findings_data = data.get("findings", [])
        evidence_data = data.get("evidence", {})
        analysis_scope = data.get("scope", {})
        
        prompt = f"""
        AUTONOMOUS DETAILED FINDINGS GENERATION:
        
        Findings Data:
        {json.dumps(findings_data, indent=2)}
        
        Evidence Data:
        {json.dumps(evidence_data, indent=2)}
        
        Analysis Scope:
        {json.dumps(analysis_scope, indent=2)}
        
        Please generate detailed findings with:
        
        1. FINDINGS OVERVIEW:
           - Scope and methodology of analysis
           - Summary of findings by category
           - Overall assessment and conclusions
           - Confidence levels and limitations
        
        2. DETAILED FINDINGS BY CATEGORY:
           - Process implementation findings
           - Documentation and evidence findings
           - Organizational and cultural findings
           - Technical and tool-related findings
        
        3. EVIDENCE ANALYSIS:
           - Quality and completeness of evidence
           - Gaps in evidence and documentation
           - Conflicting or inconsistent evidence
           - Additional evidence requirements
        
        4. IMPACT ASSESSMENT:
           - Business impact of each finding
           - Risk levels and implications
           - Compliance and regulatory impact
           - Operational and strategic consequences
        
        5. ROOT CAUSE ANALYSIS:
           - Underlying causes of identified issues
           - Contributing factors and dependencies
           - Systemic vs. isolated problems
           - Organizational and process factors
        
        6. RECOMMENDATIONS BY FINDING:
           - Specific actions for each finding
           - Implementation approach and timeline
           - Resource requirements and ownership
           - Success criteria and monitoring
        
        Provide comprehensive, evidence-based findings with clear traceability and actionable insights.
        """
        
        detailed_findings = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "detailed_findings": detailed_findings,
                "findings_count": len(findings_data),
                "evidence_sources": len(evidence_data)
            },
            message="Detailed findings report generated",
            confidence=0.9,
            reasoning="Generated comprehensive detailed findings with evidence analysis and recommendations"
        )
    
    async def _general_report_generation(self, data: Dict, context: AgentContext) -> AgentResponse:
        """
        Handle general report generation requests
        """
        content = data.get("content", "")
        report_type = data.get("report_type", "general")
        
        prompt = f"""
        GENERAL REPORT GENERATION REQUEST:
        
        Report Type: {report_type}
        Content: {content}
        
        Please generate an appropriate report based on this request:
        1. Analyze the content and determine report structure
        2. Create professional, well-organized content
        3. Include relevant ASPICE considerations
        4. Provide actionable insights and recommendations
        5. Format for professional presentation
        
        Focus on creating valuable, actionable reports.
        """
        
        report_content = await self._call_claude(prompt, context)
        
        return AgentResponse(
            success=True,
            data={
                "report_content": report_content,
                "report_type": report_type
            },
            message="General report generated",
            confidence=0.8,
            reasoning="Generated report based on general request"
        )
    
    async def _generate_visualizations(self, report_type: str, data: Dict, context: AgentContext) -> Dict:
        """
        Generate visualization specifications for reports
        """
        if report_type not in self.report_templates:
            return {}
        
        visualizations = {}
        for viz_type in self.report_templates[report_type].get("visualizations", []):
            viz_spec = await self._create_visualization_spec(viz_type, data, context)
            visualizations[viz_type] = viz_spec
        
        return visualizations
    
    async def _create_visualization_spec(self, viz_type: str, data: Dict, context: AgentContext) -> Dict:
        """
        Create specification for a specific visualization type
        """
        prompt = f"""
        Create a visualization specification for {viz_type} using this data:
        {json.dumps(data, indent=2)}
        
        Provide:
        1. Chart type and configuration
        2. Data mapping and transformations
        3. Styling and formatting
        4. Interactivity features
        5. Responsive design considerations
        """
        
        viz_spec = await self._call_claude(prompt, context)
        
        return {
            "type": viz_type,
            "specification": viz_spec,
            "data_requirements": list(data.keys())
        }