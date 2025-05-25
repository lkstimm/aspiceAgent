"""
API routes for the ASPICE Agent platform
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, UploadFile, File
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import uuid
from datetime import datetime

from app.core.agent_base import AgentOrchestrator, AgentContext, AgentResponse
from app.core.database import get_db, Project, Stakeholder, Assessment, Document
from sqlalchemy.orm import Session

# Create routers
router = APIRouter()
projects = APIRouter()
agents = APIRouter()
reports = APIRouter()
documents = APIRouter()


# Pydantic models for API
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    client_company: Optional[str] = None
    industry: Optional[str] = None
    project_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    client_company: Optional[str]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class AgentRequest(BaseModel):
    agent_name: str
    input_data: Any
    project_id: Optional[str] = None
    user_id: Optional[str] = "anonymous"
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}


class WorkflowRequest(BaseModel):
    workflow_name: str
    input_data: Any
    project_id: Optional[str] = None
    user_id: Optional[str] = "anonymous"
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}


# Project routes
@projects.post("/", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new ASPICE consulting project"""
    try:
        # Generate unique project ID
        project_id = str(uuid.uuid4())
        
        # Create project in database
        db_project = Project(
            id=project_id,
            name=project.name,
            description=project.description,
            client_company=project.client_company,
            industry=project.industry,
            project_type=project.project_type,
            metadata=project.metadata
        )
        
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        
        # Trigger autonomous project onboarding workflow
        background_tasks.add_task(
            trigger_project_onboarding,
            project_id,
            project.dict()
        )
        
        return db_project
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")


@projects.get("/", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all projects"""
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects


@projects.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str, db: Session = Depends(get_db)):
    """Get project by ID"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@projects.post("/{project_id}/onboard")
async def onboard_project_data(
    project_id: str,
    onboarding_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Onboard project data using autonomous agents"""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Trigger autonomous onboarding workflow
    background_tasks.add_task(
        trigger_project_onboarding,
        project_id,
        onboarding_data
    )
    
    return {
        "message": "Autonomous project onboarding initiated",
        "project_id": project_id,
        "status": "processing",
        "description": "AI agents are now autonomously setting up your project"
    }


@projects.get("/{project_id}/onboarding-status")
async def get_onboarding_status(
    project_id: str,
    db: Session = Depends(get_db)
):
    """Get the current status of the autonomous onboarding process"""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        from app.services.autonomous_onboarding import AutonomousOnboardingService
        
        onboarding_service = AutonomousOnboardingService()
        status = await onboarding_service.get_onboarding_status(project_id)
        
        return status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get onboarding status: {str(e)}")


@projects.post("/{project_id}/gap-analysis")
async def initiate_gap_analysis(
    project_id: str,
    analysis_request: Dict[str, Any],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Initiate autonomous gap analysis"""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Create assessment record
    assessment_id = str(uuid.uuid4())
    assessment = Assessment(
        id=assessment_id,
        project_id=project_id,
        assessment_type="gap_analysis",
        scope=analysis_request.get("scope", {}),
        status="in_progress"
    )
    
    db.add(assessment)
    db.commit()
    
    # Trigger autonomous gap analysis workflow
    background_tasks.add_task(
        trigger_gap_analysis,
        project_id,
        assessment_id,
        analysis_request
    )
    
    return {
        "message": "Gap analysis initiated",
        "project_id": project_id,
        "assessment_id": assessment_id,
        "status": "processing"
    }


# Agent routes
@agents.post("/process")
async def process_with_agent(
    request: AgentRequest,
    background_tasks: BackgroundTasks
):
    """Process a request with a specific autonomous agent"""
    try:
        # This would be implemented with the actual orchestrator
        # For now, return a mock response
        
        context = AgentContext(
            project_id=request.project_id or "default",
            user_id=request.user_id,
            session_id=request.session_id or str(uuid.uuid4()),
            metadata=request.metadata
        )
        
        # Mock response - in production this would use the actual agent
        response = AgentResponse(
            success=True,
            data={"message": f"Processed by {request.agent_name}"},
            message=f"Request processed by {request.agent_name}",
            confidence=0.9,
            reasoning=f"Mock processing by {request.agent_name}",
            next_actions=[f"Review {request.agent_name} output"]
        )
        
        return {
            "agent": request.agent_name,
            "response": response.dict(),
            "context": context.dict()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent processing failed: {str(e)}")


@agents.post("/workflow")
async def execute_workflow(
    request: WorkflowRequest,
    background_tasks: BackgroundTasks
):
    """Execute a multi-agent workflow"""
    try:
        context = AgentContext(
            project_id=request.project_id or "default",
            user_id=request.user_id,
            session_id=request.session_id or str(uuid.uuid4()),
            metadata=request.metadata
        )
        
        # Mock workflow execution - in production this would use the actual orchestrator
        response = AgentResponse(
            success=True,
            data={"workflow_result": f"Executed {request.workflow_name}"},
            message=f"Workflow {request.workflow_name} completed",
            confidence=0.9,
            reasoning=f"Mock execution of {request.workflow_name}",
            next_actions=[f"Review {request.workflow_name} results"]
        )
        
        return {
            "workflow": request.workflow_name,
            "response": response.dict(),
            "context": context.dict()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")


# Report routes
@reports.post("/{project_id}/generate")
async def generate_report(
    project_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate a comprehensive report for a project using AI agents"""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Trigger report generation workflow
    background_tasks.add_task(
        trigger_report_generation,
        project_id
    )
    
    return {
        "message": "Report generation initiated",
        "project_id": project_id,
        "status": "processing"
    }


@reports.get("/{project_id}/gap-analysis")
async def get_gap_analysis_report(
    project_id: str,
    format: str = "json",
    db: Session = Depends(get_db)
):
    """Get gap analysis report for a project"""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get latest assessment
    assessment = db.query(Assessment).filter(
        Assessment.project_id == project_id,
        Assessment.assessment_type == "gap_analysis"
    ).order_by(Assessment.created_at.desc()).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="No gap analysis found for this project")
    
    return {
        "project_id": project_id,
        "assessment_id": assessment.id,
        "status": assessment.status,
        "findings": assessment.findings,
        "recommendations": assessment.recommendations,
        "capability_ratings": assessment.capability_ratings,
        "created_at": assessment.created_at,
        "completed_at": assessment.completed_at
    }


@reports.post("/{project_id}/generate")
async def generate_report(
    project_id: str,
    report_request: Dict[str, Any],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate a report using autonomous agents"""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    report_type = report_request.get("type", "general")
    
    # Trigger autonomous report generation
    background_tasks.add_task(
        trigger_report_generation,
        project_id,
        report_type,
        report_request
    )
    
    return {
        "message": "Report generation initiated",
        "project_id": project_id,
        "report_type": report_type,
        "status": "processing"
    }


# Document routes
@documents.post("/{project_id}/upload")
async def upload_document(
    project_id: str,
    file: UploadFile = File(...),
    document_type: Optional[str] = None,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Upload and process a document"""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        # Read file content
        content = await file.read()
        
        # Create document record
        document_id = str(uuid.uuid4())
        document = Document(
            id=document_id,
            project_id=project_id,
            name=file.filename,
            document_type=document_type or "uploaded",
            content=content.decode('utf-8', errors='ignore'),
            format=file.content_type,
            created_by="user_upload"
        )
        
        db.add(document)
        db.commit()
        
        # Trigger autonomous document analysis
        if background_tasks:
            background_tasks.add_task(
                trigger_document_analysis,
                project_id,
                document_id,
                content
            )
        
        return {
            "message": "Document uploaded successfully",
            "document_id": document_id,
            "filename": file.filename,
            "size": len(content)
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to upload document: {str(e)}")


@documents.get("/{project_id}")
async def list_documents(
    project_id: str,
    document_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List documents for a project"""
    query = db.query(Document).filter(Document.project_id == project_id)
    
    if document_type:
        query = query.filter(Document.document_type == document_type)
    
    documents = query.all()
    
    return [
        {
            "id": doc.id,
            "name": doc.name,
            "document_type": doc.document_type,
            "format": doc.format,
            "version": doc.version,
            "status": doc.status,
            "created_at": doc.created_at,
            "created_by": doc.created_by
        }
        for doc in documents
    ]


@documents.get("/{project_id}/{document_id}")
async def get_document(
    project_id: str,
    document_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific document"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.project_id == project_id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return {
        "id": document.id,
        "name": document.name,
        "document_type": document.document_type,
        "content": document.content,
        "format": document.format,
        "version": document.version,
        "status": document.status,
        "created_at": document.created_at,
        "metadata": document.metadata
    }


# Background task functions
async def trigger_project_onboarding(project_id: str, project_data: Dict[str, Any]):
    """Trigger autonomous project onboarding workflow"""
    try:
        from app.services.autonomous_onboarding import AutonomousOnboardingService
        
        print(f"🚀 Starting autonomous onboarding for project {project_id}")
        
        # Initialize the autonomous onboarding service
        onboarding_service = AutonomousOnboardingService()
        
        # Execute the complete onboarding workflow
        result = await onboarding_service.initiate_autonomous_onboarding(project_id, project_data)
        
        print(f"✅ Autonomous onboarding completed for project {project_id}")
        print(f"Result: {result.get('status', 'unknown')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error in autonomous onboarding for project {project_id}: {str(e)}")
        return {
            "project_id": project_id,
            "status": "error",
            "error": str(e)
        }


async def trigger_gap_analysis(project_id: str, assessment_id: str, analysis_request: Dict[str, Any]):
    """Trigger autonomous gap analysis workflow"""
    # This would use the actual agent orchestrator
    print(f"Triggering gap analysis for project {project_id}, assessment {assessment_id}")
    # Implementation would call the GapAnalysisExpert agent


async def trigger_report_generation(project_id: str):
    """Trigger autonomous report generation"""
    # This would use the actual agent orchestrator
    print(f"Triggering comprehensive report generation for project {project_id}")
    # Implementation would call the ReportGeneration agent


async def trigger_document_analysis(project_id: str, document_id: str, content: bytes):
    """Trigger autonomous document analysis"""
    # This would use the actual agent orchestrator
    print(f"Triggering document analysis for project {project_id}, document {document_id}")
    # Implementation would call the EntityExtraction and DocumentationStrategy agents