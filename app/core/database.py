"""
Database configuration and models for the ASPICE Agent platform
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.sql import func
from typing import Generator
import asyncio
from app.core.config import get_settings

settings = get_settings()

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


class Project(Base):
    """Project model"""
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    client_company = Column(String)
    industry = Column(String)
    project_type = Column(String)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    project_metadata = Column(JSON)
    
    # Relationships
    stakeholders = relationship("Stakeholder", back_populates="project")
    assessments = relationship("Assessment", back_populates="project")
    documents = relationship("Document", back_populates="project")
    entities = relationship("Entity", back_populates="project")


class Stakeholder(Base):
    """Stakeholder model"""
    __tablename__ = "stakeholders"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))
    name = Column(String, nullable=False)
    role = Column(String)
    email = Column(String)
    department = Column(String)
    responsibilities = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="stakeholders")
    interviews = relationship("Interview", back_populates="stakeholder")


class Assessment(Base):
    """ASPICE Assessment model"""
    __tablename__ = "assessments"
    
    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))
    assessment_type = Column(String)  # gap_analysis, formal_assessment, etc.
    status = Column(String, default="in_progress")
    scope = Column(JSON)  # Process areas and levels
    findings = Column(JSON)
    recommendations = Column(JSON)
    capability_ratings = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    project = relationship("Project", back_populates="assessments")
    gaps = relationship("Gap", back_populates="assessment")


class Gap(Base):
    """Gap model for tracking identified gaps"""
    __tablename__ = "gaps"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(String, ForeignKey("assessments.id"))
    process_area = Column(String, nullable=False)
    gap_type = Column(String)  # process, documentation, evidence, etc.
    description = Column(Text, nullable=False)
    severity = Column(String)  # critical, high, medium, low
    status = Column(String, default="identified")  # identified, in_progress, resolved
    recommendations = Column(Text)
    evidence = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    assessment = relationship("Assessment", back_populates="gaps")


class Interview(Base):
    """Interview model"""
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True, index=True)
    stakeholder_id = Column(Integer, ForeignKey("stakeholders.id"))
    interviewer = Column(String)
    interview_date = Column(DateTime(timezone=True))
    focus_areas = Column(JSON)  # Process areas discussed
    transcript = Column(Text)
    summary = Column(Text)
    extracted_entities = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    stakeholder = relationship("Stakeholder", back_populates="interviews")


class Document(Base):
    """Document model"""
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))
    name = Column(String, nullable=False)
    document_type = Column(String)  # strategy, process_description, work_instruction, etc.
    content = Column(Text)
    format = Column(String)  # html, pdf, markdown, etc.
    version = Column(String, default="1.0")
    status = Column(String, default="draft")  # draft, review, approved, published
    created_by = Column(String)  # Agent or user
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    document_metadata = Column(JSON)
    
    # Relationships
    project = relationship("Project", back_populates="documents")


class Entity(Base):
    """Entity model for knowledge graph"""
    __tablename__ = "entities"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))
    name = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)  # stakeholder, process_area, artifact, etc.
    properties = Column(JSON)
    confidence_score = Column(String)  # Confidence in extraction
    source = Column(String)  # Where the entity was extracted from
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="entities")


class EntityRelationship(Base):
    """Entity relationship model for knowledge graph"""
    __tablename__ = "entity_relationships"
    
    id = Column(Integer, primary_key=True, index=True)
    source_entity_id = Column(Integer, ForeignKey("entities.id"))
    target_entity_id = Column(Integer, ForeignKey("entities.id"))
    relationship_type = Column(String, nullable=False)
    properties = Column(JSON)
    confidence_score = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AgentSession(Base):
    """Agent session model for tracking agent interactions"""
    __tablename__ = "agent_sessions"
    
    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))
    agent_name = Column(String, nullable=False)
    session_data = Column(JSON)
    conversation_history = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


async def init_db():
    """Initialize database tables"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")


def get_db() -> Generator[Session, None, None]:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()