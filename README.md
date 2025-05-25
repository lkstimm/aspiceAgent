# 🤖 Autonomous ASPICE Consulting Platform

An AI-powered platform using **autonomous Claude agents** for ASPICE consulting workflows. This platform transforms traditional ASPICE consulting by deploying specialized AI agents that can independently analyze, document, and improve automotive software processes.

## 🌟 Key Features

### **Autonomous Agent Architecture**
- **5 Specialized Claude Agents** working independently and collaboratively
- **Self-directed workflows** that adapt to project needs
- **Knowledge graph integration** for contextual understanding
- **Real-time agent orchestration** and coordination

### **Core Capabilities**
- 📊 **Autonomous Gap Analysis**: AI agents conduct interviews, analyze evidence, and map findings to ASPICE process areas
- 📝 **Intelligent Document Generation**: Automated creation of professional ASPICE documentation, strategies, and reports
- 🔍 **Entity Extraction & Tagging**: Smart parsing of project documents and meeting transcripts
- 📈 **Dynamic Report Generation**: Real-time dashboards and formatted assessment reports
- 🧠 **Knowledge Graph**: ChromaDB-powered semantic search and relationship mapping

## 🏗️ Architecture

### **Autonomous Agents**

#### 1. **ProjectOrchestrator Agent**
- Manages overall project lifecycle and coordination
- Orchestrates multi-agent workflows
- Handles project onboarding and setup
- Coordinates between different agents

#### 2. **GapAnalysisExpert Agent**
- Analyzes stakeholder interviews and meeting transcripts
- Maps evidence to ASPICE process areas
- Generates provisional capability ratings (L0-L3)
- Creates gap analysis dashboards

#### 3. **DocumentationStrategy Agent**
- Creates professional ASPICE documentation
- Generates process descriptions and work instructions
- Produces training materials and strategy documents
- Ensures compliance with ASPICE standards

#### 4. **EntityExtraction Agent**
- Extracts entities from various input sources
- Tags and categorizes project artifacts
- Builds knowledge graph relationships
- Processes uploaded documents and transcripts

#### 5. **ReportGeneration Agent**
- Creates formatted assessment reports (PDF/HTML)
- Generates interactive dashboards
- Produces client-facing summaries
- Handles report customization and branding

### **Technology Stack**

#### **Backend (FastAPI)**
```
├── Core Agent Framework
│   ├── AutonomousAgent base class
│   ├── AgentOrchestrator coordination
│   └── AgentContext management
├── Specialized Agents (5 Claude-powered agents)
├── Knowledge Graph (ChromaDB)
├── Database (SQLAlchemy + SQLite/PostgreSQL)
└── API Routes (REST + WebSocket)
```

#### **Frontend (Next.js/React)**
```
├── Project Management Interface
├── Agent Interaction Dashboard
├── Real-time Status Monitoring
├── Document Viewer & Editor
└── Knowledge Graph Visualization
```

#### **AI & Knowledge**
```
├── Anthropic Claude API integration
├── ChromaDB vector database
├── Semantic search capabilities
└── Entity relationship mapping
```

## 🚀 Quick Start

### **Prerequisites**
- Python 3.9+
- Node.js 16+
- Anthropic API key

### **Installation**

1. **Clone and setup**:
```bash
git clone <repository-url>
cd aspiceAgent
chmod +x setup.sh
./setup.sh
```

2. **Configure environment**:
```bash
# Edit .env file
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DATABASE_URL=sqlite:///./aspice_agent.db
```

3. **Start the platform**:
```bash
# Terminal 1: Backend
./start_backend.sh

# Terminal 2: Frontend  
./start_frontend.sh
```

4. **Access the platform**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📋 Usage Workflow

### **1. Project Creation & Onboarding**
- Create new ASPICE consulting project
- Input client context, technical details, and scope
- Upload existing documents and artifacts
- **Autonomous agents automatically**:
  - Extract and tag key entities
  - Build project knowledge graph
  - Initialize assessment framework

### **2. Gap Analysis Execution**
- Schedule stakeholder interviews
- Upload meeting transcripts or notes
- **GapAnalysisExpert agent autonomously**:
  - Analyzes interview content
  - Maps evidence to ASPICE process areas
  - Generates provisional capability ratings
  - Creates interactive gap analysis dashboard

### **3. Documentation & Strategy**
- Select target process areas for improvement
- **DocumentationStrategy agent autonomously**:
  - Creates professional strategy documents
  - Generates process descriptions and workflows
  - Produces training materials
  - Ensures ASPICE compliance and traceability

### **4. Report Generation**
- Trigger comprehensive assessment reports
- **ReportGeneration agent autonomously**:
  - Compiles findings and recommendations
  - Creates formatted PDF and HTML reports
  - Generates client-facing summaries
  - Produces interactive dashboards

### **5. Continuous Improvement**
- Collaborate on process improvements
- Track implementation progress
- Monitor capability maturity evolution

## 🔧 Development

### **Project Structure**
```
aspiceAgent/
├── app/                          # Backend FastAPI application
│   ├── agents/                   # Autonomous agent implementations
│   ├── api/                      # REST API routes
│   ├── core/                     # Core framework and database
│   └── services/                 # External service integrations
├── frontend/                     # Next.js React frontend
│   ├── pages/                    # Page components
│   ├── components/               # Reusable UI components
│   └── styles/                   # CSS and styling
├── static/                       # Static files and uploads
└── chroma_db/                    # ChromaDB persistence
```

### **Key Components**

#### **Agent Framework** (`app/core/agent_base.py`)
```python
class AutonomousAgent:
    """Base class for all autonomous agents"""
    async def process(self, input_data, context) -> AgentResponse
    async def analyze(self, data, context) -> Dict[str, Any]
    async def generate_response(self, analysis, context) -> AgentResponse
```

#### **Agent Orchestrator** (`app/core/agent_base.py`)
```python
class AgentOrchestrator:
    """Coordinates multiple autonomous agents"""
    async def execute_workflow(self, workflow_name, input_data, context)
    async def coordinate_agents(self, agents, input_data, context)
```

#### **Knowledge Graph** (`app/services/knowledge_graph.py`)
```python
class KnowledgeGraph:
    """ChromaDB-based knowledge management"""
    def add_entity(self, project_id, entity_type, content, metadata)
    def search_entities(self, project_id, query, entity_type)
    def get_related_entities(self, project_id, entity_id)
```

### **API Endpoints**

#### **Projects**
- `POST /api/projects/` - Create new project
- `GET /api/projects/{id}` - Get project details
- `POST /api/projects/{id}/onboard` - Trigger autonomous onboarding

#### **Agents**
- `POST /api/agents/process` - Process with specific agent
- `POST /api/agents/workflow` - Execute multi-agent workflow
- `GET /api/agents/status` - Get agent status

#### **Reports & Documents**
- `GET /api/reports/{project_id}/gap-analysis` - Get gap analysis report
- `POST /api/documents/{project_id}/upload` - Upload and process documents

## 🧪 Testing

```bash
# Run backend tests
pytest app/tests/

# Run frontend tests  
cd frontend && npm test

# Integration tests
pytest app/tests/integration/
```

## 🚀 Deployment

### **Production Setup**
1. Configure production environment variables
2. Set up PostgreSQL database
3. Configure Redis for background tasks
4. Deploy with Docker or cloud services

### **Environment Variables**
```bash
# Production settings
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@host:port/db
ANTHROPIC_API_KEY=your_production_key
REDIS_URL=redis://host:port/0
SECRET_KEY=your_secure_secret_key
```

## 📚 Documentation

- **Agent Development Guide**: `docs/agent_development.md`
- **API Reference**: `docs/api_reference.md`
- **Deployment Guide**: `docs/deployment.md`
- **ASPICE Process Mapping**: `docs/aspice_mapping.md`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/autonomous-agent-enhancement`
3. Commit changes: `git commit -am 'Add new agent capability'`
4. Push to branch: `git push origin feature/autonomous-agent-enhancement`
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: GitHub Issues
- **Documentation**: `/docs` directory
- **API Docs**: http://localhost:8000/docs (when running)

---

**Built with ❤️ using Autonomous Claude AI Agents for the future of ASPICE consulting**