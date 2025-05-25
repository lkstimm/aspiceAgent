"""
Knowledge Graph service using ChromaDB for autonomous agents
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import uuid
import json
from datetime import datetime
import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class KnowledgeGraph:
    """Knowledge graph service for storing and retrieving project knowledge"""
    
    def __init__(self):
        self.client = None
        self.collections = {}
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize ChromaDB client"""
        try:
            self.client = chromadb.PersistentClient(
                path=settings.chroma_persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            logger.info("ChromaDB client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB client: {e}")
            # Fallback to in-memory client for development
            self.client = chromadb.Client()
            logger.warning("Using in-memory ChromaDB client")
    
    def get_or_create_collection(self, project_id: str, collection_type: str = "general"):
        """Get or create a collection for a project"""
        collection_name = f"project_{project_id}_{collection_type}"
        
        if collection_name not in self.collections:
            try:
                self.collections[collection_name] = self.client.get_or_create_collection(
                    name=collection_name,
                    metadata={"project_id": project_id, "type": collection_type}
                )
                logger.info(f"Collection {collection_name} ready")
            except Exception as e:
                logger.error(f"Failed to create collection {collection_name}: {e}")
                return None
        
        return self.collections[collection_name]
    
    def add_entity(
        self,
        project_id: str,
        entity_type: str,
        content: str,
        metadata: Dict[str, Any],
        collection_type: str = "entities"
    ) -> str:
        """Add an entity to the knowledge graph"""
        collection = self.get_or_create_collection(project_id, collection_type)
        if not collection:
            return None
        
        entity_id = str(uuid.uuid4())
        
        # Prepare metadata
        full_metadata = {
            "entity_type": entity_type,
            "project_id": project_id,
            "created_at": datetime.utcnow().isoformat(),
            **metadata
        }
        
        try:
            collection.add(
                documents=[content],
                metadatas=[full_metadata],
                ids=[entity_id]
            )
            logger.info(f"Added entity {entity_id} of type {entity_type} to project {project_id}")
            return entity_id
        except Exception as e:
            logger.error(f"Failed to add entity: {e}")
            return None
    
    def add_document(
        self,
        project_id: str,
        document_name: str,
        content: str,
        document_type: str,
        metadata: Dict[str, Any]
    ) -> str:
        """Add a document to the knowledge graph"""
        return self.add_entity(
            project_id=project_id,
            entity_type="document",
            content=content,
            metadata={
                "document_name": document_name,
                "document_type": document_type,
                **metadata
            },
            collection_type="documents"
        )
    
    def add_assessment_finding(
        self,
        project_id: str,
        process_area: str,
        finding: str,
        evidence: str,
        rating: str,
        metadata: Dict[str, Any]
    ) -> str:
        """Add an assessment finding to the knowledge graph"""
        return self.add_entity(
            project_id=project_id,
            entity_type="finding",
            content=f"Process Area: {process_area}\nFinding: {finding}\nEvidence: {evidence}",
            metadata={
                "process_area": process_area,
                "finding": finding,
                "evidence": evidence,
                "rating": rating,
                **metadata
            },
            collection_type="findings"
        )
    
    def add_stakeholder_interview(
        self,
        project_id: str,
        stakeholder_name: str,
        role: str,
        transcript: str,
        metadata: Dict[str, Any]
    ) -> str:
        """Add a stakeholder interview to the knowledge graph"""
        return self.add_entity(
            project_id=project_id,
            entity_type="interview",
            content=transcript,
            metadata={
                "stakeholder_name": stakeholder_name,
                "role": role,
                **metadata
            },
            collection_type="interviews"
        )
    
    def search_entities(
        self,
        project_id: str,
        query: str,
        entity_type: Optional[str] = None,
        collection_type: str = "entities",
        n_results: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for entities in the knowledge graph"""
        collection = self.get_or_create_collection(project_id, collection_type)
        if not collection:
            return []
        
        try:
            # Build where clause
            where_clause = {"project_id": project_id}
            if entity_type:
                where_clause["entity_type"] = entity_type
            
            results = collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_clause
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results["ids"][0])):
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results else None
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to search entities: {e}")
            return []
    
    def get_related_entities(
        self,
        project_id: str,
        entity_id: str,
        collection_type: str = "entities",
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """Get entities related to a specific entity"""
        collection = self.get_or_create_collection(project_id, collection_type)
        if not collection:
            return []
        
        try:
            # Get the entity content first
            entity = collection.get(ids=[entity_id])
            if not entity["documents"]:
                return []
            
            entity_content = entity["documents"][0]
            
            # Search for similar entities
            results = collection.query(
                query_texts=[entity_content],
                n_results=n_results + 1,  # +1 to exclude the original entity
                where={"project_id": project_id}
            )
            
            # Format results and exclude the original entity
            formatted_results = []
            for i in range(len(results["ids"][0])):
                if results["ids"][0][i] != entity_id:
                    formatted_results.append({
                        "id": results["ids"][0][i],
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "distance": results["distances"][0][i] if "distances" in results else None
                    })
            
            return formatted_results[:n_results]
            
        except Exception as e:
            logger.error(f"Failed to get related entities: {e}")
            return []
    
    def get_project_summary(self, project_id: str) -> Dict[str, Any]:
        """Get a summary of all knowledge for a project"""
        summary = {
            "project_id": project_id,
            "collections": {},
            "total_entities": 0
        }
        
        collection_types = ["entities", "documents", "findings", "interviews"]
        
        for collection_type in collection_types:
            collection = self.get_or_create_collection(project_id, collection_type)
            if collection:
                try:
                    count = collection.count()
                    summary["collections"][collection_type] = count
                    summary["total_entities"] += count
                except Exception as e:
                    logger.error(f"Failed to count collection {collection_type}: {e}")
                    summary["collections"][collection_type] = 0
        
        return summary
    
    def delete_project_data(self, project_id: str):
        """Delete all data for a project"""
        collection_types = ["entities", "documents", "findings", "interviews"]
        
        for collection_type in collection_types:
            collection_name = f"project_{project_id}_{collection_type}"
            try:
                self.client.delete_collection(collection_name)
                if collection_name in self.collections:
                    del self.collections[collection_name]
                logger.info(f"Deleted collection {collection_name}")
            except Exception as e:
                logger.warning(f"Failed to delete collection {collection_name}: {e}")


# Global knowledge graph instance
_knowledge_graph = None


def get_knowledge_graph() -> KnowledgeGraph:
    """Get the global knowledge graph instance"""
    global _knowledge_graph
    if _knowledge_graph is None:
        _knowledge_graph = KnowledgeGraph()
    return _knowledge_graph