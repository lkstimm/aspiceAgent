import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

export default function ProjectDashboard() {
  const router = useRouter();
  const { id } = router.query;
  
  const [project, setProject] = useState(null);
  const [agentActivities, setAgentActivities] = useState([]);
  const [projectStatus, setProjectStatus] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [generatingReport, setGeneratingReport] = useState(false);

  useEffect(() => {
    if (id) {
      fetchProjectData();
      fetchAgentActivities();
      // Set up real-time updates
      const interval = setInterval(() => {
        fetchAgentActivities();
      }, 5000);
      return () => clearInterval(interval);
    }
  }, [id]);

  const fetchProjectData = async () => {
    try {
      const response = await fetch(`https://work-1-orvtlizcnwkmdpmi.prod-runtime.all-hands.dev/api/projects/${id}`);
      if (response.ok) {
        const data = await response.json();
        setProject(data);
      }
    } catch (error) {
      console.error('Error fetching project:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchAgentActivities = async () => {
    try {
      // Mock agent activities - in production this would come from the backend
      const mockActivities = [
        {
          id: 1,
          agent: 'ProjectOrchestrator',
          action: 'Project initialization completed',
          status: 'completed',
          timestamp: new Date(Date.now() - 5 * 60000),
          details: 'Analyzed project requirements and created comprehensive project structure',
          confidence: 0.95
        },
        {
          id: 2,
          agent: 'EntityExtraction',
          action: 'Knowledge graph creation in progress',
          status: 'in_progress',
          timestamp: new Date(Date.now() - 3 * 60000),
          details: 'Extracting entities from project documentation and stakeholder information',
          confidence: 0.88,
          progress: 65
        },
        {
          id: 3,
          agent: 'GapAnalysisExpert',
          action: 'Stakeholder interview preparation',
          status: 'pending',
          timestamp: new Date(Date.now() - 1 * 60000),
          details: 'Preparing interview questions and scheduling stakeholder meetings',
          confidence: 0.92
        },
        {
          id: 4,
          agent: 'DocumentationStrategy',
          action: 'Initial assessment framework setup',
          status: 'in_progress',
          timestamp: new Date(Date.now() - 2 * 60000),
          details: 'Creating ASPICE assessment templates and documentation structure',
          confidence: 0.90,
          progress: 40
        },
        {
          id: 5,
          agent: 'ReportGeneration',
          action: 'Dashboard configuration',
          status: 'completed',
          timestamp: new Date(Date.now() - 10 * 60000),
          details: 'Set up real-time monitoring and reporting dashboards',
          confidence: 0.93
        }
      ];
      
      setAgentActivities(mockActivities);
      
      // Mock project status
      setProjectStatus({
        overall_progress: 25,
        phase: 'Onboarding',
        next_milestone: 'Stakeholder Interviews',
        agents_active: 4,
        tasks_completed: 12,
        tasks_pending: 8,
        estimated_completion: '2024-08-15'
      });
    } catch (error) {
      console.error('Error fetching agent activities:', error);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'text-green-600 bg-green-100';
      case 'in_progress': return 'text-blue-600 bg-blue-100';
      case 'pending': return 'text-yellow-600 bg-yellow-100';
      case 'error': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getAgentIcon = (agent) => {
    const icons = {
      'ProjectOrchestrator': '🎯',
      'GapAnalysisExpert': '🔍',
      'DocumentationStrategy': '📝',
      'EntityExtraction': '🧠',
      'ReportGeneration': '📊'
    };
    return icons[agent] || '🤖';
  };

  const formatTimeAgo = (timestamp) => {
    const now = new Date();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    
    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return timestamp.toLocaleDateString();
  };

  const generateReport = async () => {
    setGeneratingReport(true);
    try {
      const response = await fetch(`https://work-1-orvtlizcnwkmdpmi.prod-runtime.all-hands.dev/api/reports/${id}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('Report generation initiated:', result);
        
        // Add a new activity to show report generation started
        const newActivity = {
          id: Date.now(),
          agent: 'ReportGeneration',
          action: 'Comprehensive report generation initiated',
          status: 'in_progress',
          timestamp: new Date(),
          details: 'AI agents are collaborating to generate a comprehensive ASPICE assessment report',
          confidence: 0.95,
          progress: 10
        };
        
        setAgentActivities(prev => [newActivity, ...prev]);
        
        // Show success message
        alert('Report generation initiated! Check the AI Agents tab to monitor progress.');
      } else {
        throw new Error('Failed to generate report');
      }
    } catch (error) {
      console.error('Error generating report:', error);
      alert('Failed to initiate report generation. Please try again.');
    } finally {
      setGeneratingReport(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading project dashboard...</p>
        </div>
      </div>
    );
  }

  if (!project) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">❌</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Project Not Found</h2>
          <p className="text-gray-600 mb-4">The project you're looking for doesn't exist.</p>
          <button
            onClick={() => router.push('/')}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => router.push('/')}
                className="text-gray-600 hover:text-gray-900"
              >
                ← Back to Dashboard
              </button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">{project.name}</h1>
                <p className="text-gray-600">{project.client_company} • {project.industry}</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <div className="text-sm text-gray-500">Project Status</div>
                <div className="text-lg font-semibold text-blue-600">{projectStatus.phase}</div>
              </div>
              <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                {projectStatus.overall_progress}% Complete
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Overall Progress</span>
            <span className="text-sm text-gray-500">{projectStatus.overall_progress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-blue-500 to-indigo-600 h-2 rounded-full transition-all duration-500"
              style={{ width: `${projectStatus.overall_progress}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', label: 'Overview', icon: '📊' },
              { id: 'agents', label: 'AI Agents', icon: '🤖' },
              { id: 'timeline', label: 'Timeline', icon: '📅' },
              { id: 'documents', label: 'Documents', icon: '📄' },
              { id: 'reports', label: 'Reports', icon: '📈' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Active Agents</p>
                    <p className="text-2xl font-bold text-gray-900">{projectStatus.agents_active}</p>
                  </div>
                  <div className="text-blue-600 text-2xl">🤖</div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Tasks Completed</p>
                    <p className="text-2xl font-bold text-gray-900">{projectStatus.tasks_completed}</p>
                  </div>
                  <div className="text-green-600 text-2xl">✅</div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Pending Tasks</p>
                    <p className="text-2xl font-bold text-gray-900">{projectStatus.tasks_pending}</p>
                  </div>
                  <div className="text-yellow-600 text-2xl">⏳</div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Next Milestone</p>
                    <p className="text-lg font-bold text-gray-900">{projectStatus.next_milestone}</p>
                  </div>
                  <div className="text-purple-600 text-2xl">🎯</div>
                </div>
              </div>
            </div>

            {/* Recent Agent Activity */}
            <div className="bg-white rounded-lg shadow-sm border">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900">🤖 Recent Agent Activity</h2>
                <p className="text-gray-600">Real-time updates from your autonomous AI agents</p>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {agentActivities.slice(0, 5).map(activity => (
                    <div key={activity.id} className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
                      <div className="text-2xl">{getAgentIcon(activity.agent)}</div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-1">
                          <h4 className="font-medium text-gray-900">{activity.agent}</h4>
                          <div className="flex items-center space-x-2">
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(activity.status)}`}>
                              {activity.status.replace('_', ' ')}
                            </span>
                            <span className="text-xs text-gray-500">{formatTimeAgo(activity.timestamp)}</span>
                          </div>
                        </div>
                        <p className="text-sm font-medium text-gray-800 mb-1">{activity.action}</p>
                        <p className="text-sm text-gray-600">{activity.details}</p>
                        {activity.progress && (
                          <div className="mt-2">
                            <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
                              <span>Progress</span>
                              <span>{activity.progress}%</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-1">
                              <div 
                                className="bg-blue-500 h-1 rounded-full transition-all duration-300"
                                style={{ width: `${activity.progress}%` }}
                              ></div>
                            </div>
                          </div>
                        )}
                        <div className="mt-2 flex items-center space-x-2">
                          <span className="text-xs text-gray-500">Confidence:</span>
                          <div className="flex items-center space-x-1">
                            {[...Array(5)].map((_, i) => (
                              <div
                                key={i}
                                className={`w-2 h-2 rounded-full ${
                                  i < Math.floor(activity.confidence * 5) ? 'bg-green-500' : 'bg-gray-300'
                                }`}
                              />
                            ))}
                          </div>
                          <span className="text-xs text-gray-500">{Math.round(activity.confidence * 100)}%</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'agents' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">🤖 Autonomous Agent Status</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {[
                  {
                    name: 'ProjectOrchestrator',
                    icon: '🎯',
                    status: 'active',
                    description: 'Managing project coordination and workflow',
                    lastAction: 'Project initialization completed',
                    confidence: 0.95,
                    tasksCompleted: 3,
                    currentTask: 'Monitoring project progress'
                  },
                  {
                    name: 'GapAnalysisExpert',
                    icon: '🔍',
                    status: 'preparing',
                    description: 'Preparing stakeholder interviews and gap analysis',
                    lastAction: 'Interview questions prepared',
                    confidence: 0.92,
                    tasksCompleted: 1,
                    currentTask: 'Scheduling stakeholder meetings'
                  },
                  {
                    name: 'DocumentationStrategy',
                    icon: '📝',
                    status: 'active',
                    description: 'Creating ASPICE documentation framework',
                    lastAction: 'Assessment templates created',
                    confidence: 0.90,
                    tasksCompleted: 2,
                    currentTask: 'Setting up process documentation'
                  },
                  {
                    name: 'EntityExtraction',
                    icon: '🧠',
                    status: 'active',
                    description: 'Building knowledge graph from project data',
                    lastAction: 'Extracting stakeholder entities',
                    confidence: 0.88,
                    tasksCompleted: 4,
                    currentTask: 'Processing project documents'
                  },
                  {
                    name: 'ReportGeneration',
                    icon: '📊',
                    status: 'ready',
                    description: 'Ready to generate reports and dashboards',
                    lastAction: 'Dashboard configuration completed',
                    confidence: 0.93,
                    tasksCompleted: 2,
                    currentTask: 'Monitoring for report triggers'
                  }
                ].map((agent, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl">{agent.icon}</span>
                        <h3 className="font-semibold text-gray-900">{agent.name}</h3>
                      </div>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        agent.status === 'active' ? 'bg-green-100 text-green-800' :
                        agent.status === 'preparing' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-blue-100 text-blue-800'
                      }`}>
                        {agent.status}
                      </span>
                    </div>
                    
                    <p className="text-sm text-gray-600 mb-3">{agent.description}</p>
                    
                    <div className="space-y-2 text-xs text-gray-500">
                      <div>
                        <span className="font-medium">Last Action:</span> {agent.lastAction}
                      </div>
                      <div>
                        <span className="font-medium">Current Task:</span> {agent.currentTask}
                      </div>
                      <div>
                        <span className="font-medium">Tasks Completed:</span> {agent.tasksCompleted}
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="font-medium">Confidence:</span>
                        <div className="flex items-center space-x-1">
                          {[...Array(5)].map((_, i) => (
                            <div
                              key={i}
                              className={`w-1.5 h-1.5 rounded-full ${
                                i < Math.floor(agent.confidence * 5) ? 'bg-green-500' : 'bg-gray-300'
                              }`}
                            />
                          ))}
                        </div>
                        <span>{Math.round(agent.confidence * 100)}%</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Agent Activity Log */}
            <div className="bg-white rounded-lg shadow-sm border">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900">📋 Complete Agent Activity Log</h2>
              </div>
              <div className="p-6">
                <div className="space-y-3">
                  {agentActivities.map(activity => (
                    <div key={activity.id} className="flex items-start space-x-3 p-3 border-l-4 border-l-blue-500 bg-blue-50 rounded-r-lg">
                      <div className="text-xl">{getAgentIcon(activity.agent)}</div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between">
                          <span className="font-medium text-gray-900">{activity.agent}</span>
                          <span className="text-xs text-gray-500">{formatTimeAgo(activity.timestamp)}</span>
                        </div>
                        <p className="text-sm text-gray-800">{activity.action}</p>
                        <p className="text-xs text-gray-600 mt-1">{activity.details}</p>
                      </div>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(activity.status)}`}>
                        {activity.status.replace('_', ' ')}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'timeline' && (
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">📅 Project Timeline</h2>
            <div className="space-y-6">
              {[
                { phase: 'Project Onboarding', status: 'completed', date: '2024-05-25', description: 'Initial project setup and agent configuration' },
                { phase: 'Stakeholder Interviews', status: 'in_progress', date: '2024-05-28', description: 'Conducting interviews with key stakeholders' },
                { phase: 'Gap Analysis', status: 'pending', date: '2024-06-05', description: 'Comprehensive ASPICE gap analysis' },
                { phase: 'Improvement Planning', status: 'pending', date: '2024-06-15', description: 'Creating improvement roadmap and strategies' },
                { phase: 'Implementation Support', status: 'pending', date: '2024-07-01', description: 'Supporting process improvements' },
                { phase: 'Final Assessment', status: 'pending', date: '2024-08-15', description: 'Final ASPICE assessment and certification prep' }
              ].map((milestone, index) => (
                <div key={index} className="flex items-start space-x-4">
                  <div className={`w-4 h-4 rounded-full mt-1 ${
                    milestone.status === 'completed' ? 'bg-green-500' :
                    milestone.status === 'in_progress' ? 'bg-blue-500' :
                    'bg-gray-300'
                  }`}></div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <h3 className="font-semibold text-gray-900">{milestone.phase}</h3>
                      <span className="text-sm text-gray-500">{milestone.date}</span>
                    </div>
                    <p className="text-sm text-gray-600">{milestone.description}</p>
                    <span className={`inline-block mt-1 px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(milestone.status)}`}>
                      {milestone.status.replace('_', ' ')}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'documents' && (
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">📄 Project Documents</h2>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                ➕ Upload Document
              </button>
            </div>
            <div className="text-center py-12">
              <div className="text-6xl mb-4">📄</div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No documents yet</h3>
              <p className="text-gray-500 mb-4">Upload project documents for AI analysis</p>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                Upload First Document
              </button>
            </div>
          </div>
        )}

        {activeTab === 'reports' && (
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">📈 Reports & Analytics</h2>
              <button 
                onClick={generateReport}
                disabled={generatingReport}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  generatingReport 
                    ? 'bg-gray-400 text-white cursor-not-allowed' 
                    : 'bg-blue-600 text-white hover:bg-blue-700'
                }`}
              >
                {generatingReport ? (
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Generating...</span>
                  </div>
                ) : (
                  'Generate Report'
                )}
              </button>
            </div>
            <div className="text-center py-12">
              <div className="text-6xl mb-4">📊</div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">Reports will be available soon</h3>
              <p className="text-gray-500 mb-4">Our AI agents are gathering data for comprehensive reports</p>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-md mx-auto">
                <p className="text-sm text-blue-800">
                  <strong>Next Report:</strong> Initial Gap Analysis<br/>
                  <strong>Expected:</strong> After stakeholder interviews complete
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}