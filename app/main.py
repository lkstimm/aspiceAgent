"""
Main FastAPI application for the Autonomous ASPICE Consulting Platform
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from typing import Dict, Any
import logging

from app.core.agent_base import AgentOrchestrator, AgentContext
from app.agents.project_orchestrator import ProjectOrchestratorAgent
from app.agents.gap_analysis_expert import GapAnalysisExpertAgent
from app.agents.documentation_strategy import DocumentationStrategyAgent
from app.agents.entity_extraction import EntityExtractionAgent
from app.agents.report_generation import ReportGenerationAgent
from app.api.routes import projects, agents, reports, documents
from app.core.config import get_settings
from app.core.database import init_db
from app.services.anthropic_service import get_anthropic_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global agent orchestrator
orchestrator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    global orchestrator
    
    # Startup
    logger.info("Starting Autonomous ASPICE Consulting Platform...")
    
    # Initialize database
    await init_db()
    
    # Initialize agent orchestrator
    anthropic_client = get_anthropic_client()
    orchestrator = AgentOrchestrator(anthropic_client)
    
    # Register all autonomous agents
    orchestrator.register_agent(ProjectOrchestratorAgent(anthropic_client))
    orchestrator.register_agent(GapAnalysisExpertAgent(anthropic_client))
    orchestrator.register_agent(DocumentationStrategyAgent(anthropic_client))
    orchestrator.register_agent(EntityExtractionAgent(anthropic_client))
    orchestrator.register_agent(ReportGenerationAgent(anthropic_client))
    
    logger.info("All autonomous agents registered and ready")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Autonomous ASPICE Consulting Platform...")


# Create FastAPI application
app = FastAPI(
    title="Autonomous ASPICE Consulting Platform",
    description="AI-powered platform using autonomous Claude agents for ASPICE consulting workflows",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def get_orchestrator() -> AgentOrchestrator:
    """Dependency to get the agent orchestrator"""
    if orchestrator is None:
        raise HTTPException(status_code=500, detail="Agent orchestrator not initialized")
    return orchestrator


@app.get("/")
async def root():
    """Root endpoint with platform information"""
    return {
        "message": "Autonomous ASPICE Consulting Platform",
        "version": "1.0.0",
        "description": "AI-powered platform using autonomous Claude agents",
        "agents": [
            "ProjectOrchestrator",
            "GapAnalysisExpert", 
            "DocumentationStrategy",
            "EntityExtraction",
            "ReportGeneration"
        ],
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents_registered": len(orchestrator.agents) if orchestrator else 0,
        "timestamp": "2024-01-01T00:00:00Z"
    }


@app.get("/agents/status")
async def get_agents_status(orchestrator: AgentOrchestrator = Depends(get_orchestrator)):
    """Get status of all registered agents"""
    return {
        "agents": orchestrator.get_agent_status(),
        "total_agents": len(orchestrator.agents)
    }


@app.post("/agents/{agent_name}/process")
async def process_with_agent(
    agent_name: str,
    request_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Process a request with a specific agent"""
    if agent_name not in orchestrator.agents:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
    
    # Create agent context
    context = AgentContext(
        project_id=request_data.get("project_id", "default"),
        user_id=request_data.get("user_id", "anonymous"),
        session_id=request_data.get("session_id", "default"),
        metadata=request_data.get("metadata", {})
    )
    
    try:
        agent = orchestrator.agents[agent_name]
        response = await agent.process(request_data.get("input_data"), context)
        
        return {
            "agent": agent_name,
            "response": response.dict(),
            "context": context.dict()
        }
        
    except Exception as e:
        logger.error(f"Error processing with agent {agent_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Agent processing failed: {str(e)}")


@app.post("/workflows/{workflow_name}")
async def execute_workflow(
    workflow_name: str,
    request_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Execute a multi-agent workflow"""
    # Create agent context
    context = AgentContext(
        project_id=request_data.get("project_id", "default"),
        user_id=request_data.get("user_id", "anonymous"),
        session_id=request_data.get("session_id", "default"),
        metadata=request_data.get("metadata", {})
    )
    
    try:
        response = await orchestrator.execute_workflow(
            workflow_name,
            request_data.get("input_data"),
            context
        )
        
        return {
            "workflow": workflow_name,
            "response": response.dict(),
            "context": context.dict()
        }
        
    except Exception as e:
        logger.error(f"Error executing workflow {workflow_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")


# Include API routes
app.include_router(projects, prefix="/api/projects", tags=["projects"])
app.include_router(agents, prefix="/api/agents", tags=["agents"])
app.include_router(reports, prefix="/api/reports", tags=["reports"])
app.include_router(documents, prefix="/api/documents", tags=["documents"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )