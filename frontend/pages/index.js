import { useState, useEffect } from 'react';

export default function Home() {
  const [projects, setProjects] = useState([]);
  const [agentStatus, setAgentStatus] = useState({});

  useEffect(() => {
    fetchProjects();
    fetchAgentStatus();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await fetch('http://localhost:12000/api/projects/');
      const data = await response.json();
      setProjects(data);
    } catch (error) {
      console.error('Error fetching projects:', error);
    }
  };

  const fetchAgentStatus = async () => {
    try {
      const response = await fetch('http://localhost:12000/agents/status');
      const data = await response.json();
      setAgentStatus(data);
    } catch (error) {
      console.error('Error fetching agent status:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-7xl mx-auto">
        <header className="bg-white rounded-lg shadow-sm border p-6 mb-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                🧠 Autonomous ASPICE Platform
              </h1>
              <p className="text-gray-600">
                AI-powered consulting with Claude agents
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                ⚡ {agentStatus.total_agents || 0} Agents Active
              </div>
              <button 
                onClick={() => window.location.href = '/onboarding'}
                className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-2 rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                🚀 Start Autonomous Onboarding
              </button>
            </div>
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Active Projects</p>
                <p className="text-2xl font-bold text-gray-900">{projects.length}</p>
              </div>
              <div className="text-blue-600 text-2xl">🎯</div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">AI Agents</p>
                <p className="text-2xl font-bold text-gray-900">{agentStatus.total_agents || 0}</p>
              </div>
              <div className="text-green-600 text-2xl">🧠</div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Assessments</p>
                <p className="text-2xl font-bold text-gray-900">12</p>
              </div>
              <div className="text-purple-600 text-2xl">📊</div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Reports Generated</p>
                <p className="text-2xl font-bold text-gray-900">34</p>
              </div>
              <div className="text-orange-600 text-2xl">📄</div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">🎯 Recent Projects</h2>
          {projects.length === 0 ? (
            <div className="text-center py-8">
              <div className="text-6xl mb-4">🎯</div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No projects yet</h3>
              <p className="text-gray-500 mb-4">Create your first ASPICE consulting project</p>
              <button 
                onClick={() => window.location.href = '/onboarding'}
                className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                🚀 Start Autonomous Onboarding
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {projects.map((project) => (
                <div key={project.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                  <div>
                    <h4 className="font-medium text-gray-900">{project.name}</h4>
                    <p className="text-sm text-gray-500">{project.client_company}</p>
                    <p className="text-xs text-gray-400">{project.description}</p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="bg-gray-100 text-gray-800 px-2 py-1 rounded text-sm">{project.status}</span>
                    <button className="border border-gray-300 px-3 py-1 rounded text-sm hover:bg-gray-50">
                      View
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">🧠 Autonomous Agents</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { name: 'Project Orchestrator', status: 'active', description: 'Manages project workflows and coordination' },
              { name: 'Gap Analysis Expert', status: 'active', description: 'Analyzes ASPICE gaps and provides recommendations' },
              { name: 'Documentation Strategy', status: 'active', description: 'Creates and manages project documentation' },
              { name: 'Entity Extraction', status: 'active', description: 'Extracts entities from documents and conversations' },
              { name: 'Report Generation', status: 'active', description: 'Generates comprehensive ASPICE reports' }
            ].map((agent) => (
              <div key={agent.name} className="border-l-4 border-l-green-500 bg-gray-50 p-4 rounded">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-900">{agent.name}</h4>
                  <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">
                    ✅ {agent.status}
                  </span>
                </div>
                <p className="text-sm text-gray-600">{agent.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
