import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

export default function Onboarding() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [agentStatus, setAgentStatus] = useState({});
  const [onboardingData, setOnboardingData] = useState({
    // Basic Info
    projectName: '',
    clientCompany: '',
    industry: '',
    projectType: 'aspice_assessment',
    
    // Context
    description: '',
    scope: '',
    timeline: '',
    budget: '',
    
    // Technical Details
    developmentProcess: '',
    toolchain: '',
    teamSize: '',
    currentMaturity: '',
    
    // Goals & Objectives
    targetLevel: '',
    criticalProcesses: [],
    businessDrivers: '',
    successCriteria: '',
    
    // Stakeholders
    stakeholders: [
      { name: '', role: '', email: '', involvement: 'high' }
    ],
    
    // Documents
    existingDocuments: [],
    
    // AI Preferences
    autonomyLevel: 'high',
    reportingFrequency: 'daily',
    communicationStyle: 'detailed'
  });

  const steps = [
    { id: 1, title: 'Project Basics', icon: '🎯', description: 'Essential project information' },
    { id: 2, title: 'Context & Scope', icon: '🔍', description: 'Project context and boundaries' },
    { id: 3, title: 'Technical Details', icon: '⚙️', description: 'Development environment and processes' },
    { id: 4, title: 'Goals & Objectives', icon: '🎪', description: 'What you want to achieve' },
    { id: 5, title: 'Stakeholders', icon: '👥', description: 'Key people and their roles' },
    { id: 6, title: 'AI Configuration', icon: '🧠', description: 'How our agents should work' },
    { id: 7, title: 'Launch', icon: '🚀', description: 'Activate autonomous agents' }
  ];

  const industries = [
    'Automotive', 'Aerospace', 'Medical Devices', 'Industrial Automation',
    'Telecommunications', 'Defense', 'Energy', 'Transportation', 'Other'
  ];

  const projectTypes = [
    { value: 'aspice_assessment', label: 'ASPICE Assessment' },
    { value: 'process_improvement', label: 'Process Improvement' },
    { value: 'certification_prep', label: 'Certification Preparation' },
    { value: 'gap_analysis', label: 'Gap Analysis Only' },
    { value: 'full_consulting', label: 'Full Consulting Engagement' }
  ];

  const maturityLevels = [
    { value: 'unknown', label: 'Unknown / Not Assessed' },
    { value: 'level_0', label: 'Level 0 - Incomplete' },
    { value: 'level_1', label: 'Level 1 - Performed' },
    { value: 'level_2', label: 'Level 2 - Managed' },
    { value: 'level_3', label: 'Level 3 - Established' }
  ];

  const aspiceProcesses = [
    'SYS.1 - Requirements Elicitation',
    'SYS.2 - System Requirements Analysis',
    'SYS.3 - System Architectural Design',
    'SYS.4 - System Integration and Integration Test',
    'SYS.5 - System Qualification Test',
    'SWE.1 - Software Requirements Analysis',
    'SWE.2 - Software Architectural Design',
    'SWE.3 - Software Detailed Design and Unit Construction',
    'SWE.4 - Software Unit Verification',
    'SWE.5 - Software Integration and Integration Test',
    'SWE.6 - Software Qualification Test',
    'SUP.1 - Quality Assurance',
    'SUP.8 - Configuration Management',
    'SUP.9 - Problem Resolution Management',
    'SUP.10 - Change Request Management',
    'MAN.3 - Project Management'
  ];

  useEffect(() => {
    fetchAgentStatus();
  }, []);

  const fetchAgentStatus = async () => {
    try {
      const response = await fetch('http://localhost:12000/api/agents/status');
      const data = await response.json();
      setAgentStatus(data);
    } catch (error) {
      console.error('Error fetching agent status:', error);
    }
  };

  const updateData = (field, value) => {
    setOnboardingData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const addStakeholder = () => {
    setOnboardingData(prev => ({
      ...prev,
      stakeholders: [...prev.stakeholders, { name: '', role: '', email: '', involvement: 'medium' }]
    }));
  };

  const updateStakeholder = (index, field, value) => {
    setOnboardingData(prev => ({
      ...prev,
      stakeholders: prev.stakeholders.map((stakeholder, i) => 
        i === index ? { ...stakeholder, [field]: value } : stakeholder
      )
    }));
  };

  const removeStakeholder = (index) => {
    setOnboardingData(prev => ({
      ...prev,
      stakeholders: prev.stakeholders.filter((_, i) => i !== index)
    }));
  };

  const toggleProcess = (process) => {
    setOnboardingData(prev => ({
      ...prev,
      criticalProcesses: prev.criticalProcesses.includes(process)
        ? prev.criticalProcesses.filter(p => p !== process)
        : [...prev.criticalProcesses, process]
    }));
  };

  const nextStep = () => {
    if (currentStep < steps.length) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const launchProject = async () => {
    setIsLoading(true);
    try {
      // Create project
      const projectResponse = await fetch('http://localhost:12000/api/projects/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: onboardingData.projectName,
          description: onboardingData.description,
          client_company: onboardingData.clientCompany,
          industry: onboardingData.industry,
          project_type: onboardingData.projectType,
          metadata: onboardingData
        }),
      });

      if (!projectResponse.ok) {
        throw new Error('Failed to create project');
      }

      const project = await projectResponse.json();

      // Trigger autonomous onboarding
      const onboardingResponse = await fetch(`http://localhost:12000/api/projects/${project.id}/onboard`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(onboardingData),
      });

      if (!onboardingResponse.ok) {
        throw new Error('Failed to start onboarding');
      }

      // Redirect to project dashboard
      router.push(`/project/${project.id}`);
    } catch (error) {
      console.error('Error launching project:', error);
      alert('Failed to launch project. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <div className="text-6xl mb-4">🎯</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Project Basics</h2>
              <p className="text-gray-600">Let's start with the essential information about your project</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Project Name *
                </label>
                <input
                  type="text"
                  value={onboardingData.projectName}
                  onChange={(e) => updateData('projectName', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., ECU Software ASPICE Assessment"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Client Company *
                </label>
                <input
                  type="text"
                  value={onboardingData.clientCompany}
                  onChange={(e) => updateData('clientCompany', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., Automotive Corp"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Industry *
                </label>
                <select
                  value={onboardingData.industry}
                  onChange={(e) => updateData('industry', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Select Industry</option>
                  {industries.map(industry => (
                    <option key={industry} value={industry}>{industry}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Project Type *
                </label>
                <select
                  value={onboardingData.projectType}
                  onChange={(e) => updateData('projectType', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {projectTypes.map(type => (
                    <option key={type.value} value={type.value}>{type.label}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <div className="text-6xl mb-4">🔍</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Context & Scope</h2>
              <p className="text-gray-600">Help our AI agents understand your project context</p>
            </div>

            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Project Description *
                </label>
                <textarea
                  value={onboardingData.description}
                  onChange={(e) => updateData('description', e.target.value)}
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Describe your project, its objectives, and what you're trying to achieve..."
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Project Scope
                  </label>
                  <textarea
                    value={onboardingData.scope}
                    onChange={(e) => updateData('scope', e.target.value)}
                    rows={3}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="What's included and excluded from this project..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Timeline
                  </label>
                  <input
                    type="text"
                    value={onboardingData.timeline}
                    onChange={(e) => updateData('timeline', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g., 3 months, Q2 2024"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Budget Range (Optional)
                </label>
                <input
                  type="text"
                  value={onboardingData.budget}
                  onChange={(e) => updateData('budget', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., $50k-100k, €75k"
                />
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <div className="text-6xl mb-4">⚙️</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Technical Details</h2>
              <p className="text-gray-600">Tell us about your development environment and current processes</p>
            </div>

            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Development Process
                  </label>
                  <textarea
                    value={onboardingData.developmentProcess}
                    onChange={(e) => updateData('developmentProcess', e.target.value)}
                    rows={3}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Describe your current development process, methodologies used..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Toolchain & Technologies
                  </label>
                  <textarea
                    value={onboardingData.toolchain}
                    onChange={(e) => updateData('toolchain', e.target.value)}
                    rows={3}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Tools, technologies, platforms you're using..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Team Size
                  </label>
                  <input
                    type="text"
                    value={onboardingData.teamSize}
                    onChange={(e) => updateData('teamSize', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g., 15 developers, 3 teams"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Current ASPICE Maturity
                  </label>
                  <select
                    value={onboardingData.currentMaturity}
                    onChange={(e) => updateData('currentMaturity', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select Current Level</option>
                    {maturityLevels.map(level => (
                      <option key={level.value} value={level.value}>{level.label}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          </div>
        );

      case 4:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <div className="text-6xl mb-4">🎪</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Goals & Objectives</h2>
              <p className="text-gray-600">What do you want to achieve with this project?</p>
            </div>

            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Target ASPICE Level
                  </label>
                  <select
                    value={onboardingData.targetLevel}
                    onChange={(e) => updateData('targetLevel', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select Target Level</option>
                    {maturityLevels.slice(1).map(level => (
                      <option key={level.value} value={level.value}>{level.label}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Business Drivers
                  </label>
                  <textarea
                    value={onboardingData.businessDrivers}
                    onChange={(e) => updateData('businessDrivers', e.target.value)}
                    rows={3}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Why is this project important? What business needs does it address?"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-4">
                  Critical ASPICE Processes (Select all that apply)
                </label>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {aspiceProcesses.map(process => (
                    <label key={process} className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-gray-50 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={onboardingData.criticalProcesses.includes(process)}
                        onChange={() => toggleProcess(process)}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <span className="text-sm text-gray-700">{process}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Success Criteria
                </label>
                <textarea
                  value={onboardingData.successCriteria}
                  onChange={(e) => updateData('successCriteria', e.target.value)}
                  rows={3}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="How will you measure success? What are the key outcomes you expect?"
                />
              </div>
            </div>
          </div>
        );

      case 5:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <div className="text-6xl mb-4">👥</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Stakeholders</h2>
              <p className="text-gray-600">Who are the key people involved in this project?</p>
            </div>

            <div className="space-y-4">
              {onboardingData.stakeholders.map((stakeholder, index) => (
                <div key={index} className="p-4 border border-gray-200 rounded-lg bg-gray-50">
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Name
                      </label>
                      <input
                        type="text"
                        value={stakeholder.name}
                        onChange={(e) => updateStakeholder(index, 'name', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Full name"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Role
                      </label>
                      <input
                        type="text"
                        value={stakeholder.role}
                        onChange={(e) => updateStakeholder(index, 'role', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="e.g., Project Manager"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Email
                      </label>
                      <input
                        type="email"
                        value={stakeholder.email}
                        onChange={(e) => updateStakeholder(index, 'email', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="email@company.com"
                      />
                    </div>

                    <div className="flex items-end space-x-2">
                      <div className="flex-1">
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Involvement
                        </label>
                        <select
                          value={stakeholder.involvement}
                          onChange={(e) => updateStakeholder(index, 'involvement', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="high">High</option>
                          <option value="medium">Medium</option>
                          <option value="low">Low</option>
                        </select>
                      </div>
                      {onboardingData.stakeholders.length > 1 && (
                        <button
                          onClick={() => removeStakeholder(index)}
                          className="px-3 py-2 text-red-600 hover:text-red-800 hover:bg-red-50 rounded-md"
                        >
                          🗑️
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))}

              <button
                onClick={addStakeholder}
                className="w-full py-3 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-blue-400 hover:text-blue-600 transition-colors"
              >
                ➕ Add Another Stakeholder
              </button>
            </div>
          </div>
        );

      case 6:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <div className="text-6xl mb-4">🧠</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">AI Configuration</h2>
              <p className="text-gray-600">Configure how our autonomous agents should work for you</p>
            </div>

            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Autonomy Level
                  </label>
                  <select
                    value={onboardingData.autonomyLevel}
                    onChange={(e) => updateData('autonomyLevel', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="high">High - Agents work independently</option>
                    <option value="medium">Medium - Agents ask for approval</option>
                    <option value="low">Low - Agents provide recommendations only</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Reporting Frequency
                  </label>
                  <select
                    value={onboardingData.reportingFrequency}
                    onChange={(e) => updateData('reportingFrequency', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="realtime">Real-time updates</option>
                    <option value="daily">Daily summaries</option>
                    <option value="weekly">Weekly reports</option>
                    <option value="milestone">Milestone-based</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Communication Style
                  </label>
                  <select
                    value={onboardingData.communicationStyle}
                    onChange={(e) => updateData('communicationStyle', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="detailed">Detailed explanations</option>
                    <option value="concise">Concise summaries</option>
                    <option value="executive">Executive-level overview</option>
                  </select>
                </div>
              </div>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-blue-900 mb-4">🤖 Your AI Agent Team</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {[
                    { name: 'Project Orchestrator', role: 'Manages overall project coordination', status: 'Ready' },
                    { name: 'Gap Analysis Expert', role: 'Analyzes ASPICE gaps and provides recommendations', status: 'Ready' },
                    { name: 'Documentation Strategy', role: 'Creates and manages project documentation', status: 'Ready' },
                    { name: 'Entity Extraction', role: 'Processes documents and extracts key information', status: 'Ready' },
                    { name: 'Report Generation', role: 'Generates comprehensive reports and dashboards', status: 'Ready' }
                  ].map((agent, index) => (
                    <div key={index} className="bg-white p-4 rounded-lg border border-blue-200">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium text-gray-900">{agent.name}</h4>
                        <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">
                          ✅ {agent.status}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600">{agent.role}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        );

      case 7:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <div className="text-6xl mb-4">🚀</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Ready to Launch!</h2>
              <p className="text-gray-600">Review your configuration and activate your autonomous ASPICE consulting project</p>
            </div>

            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">📋 Project Summary</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium text-gray-700">Project:</span>
                  <span className="ml-2 text-gray-900">{onboardingData.projectName}</span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">Client:</span>
                  <span className="ml-2 text-gray-900">{onboardingData.clientCompany}</span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">Industry:</span>
                  <span className="ml-2 text-gray-900">{onboardingData.industry}</span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">Type:</span>
                  <span className="ml-2 text-gray-900">
                    {projectTypes.find(t => t.value === onboardingData.projectType)?.label}
                  </span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">Target Level:</span>
                  <span className="ml-2 text-gray-900">
                    {maturityLevels.find(l => l.value === onboardingData.targetLevel)?.label || 'Not specified'}
                  </span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">Stakeholders:</span>
                  <span className="ml-2 text-gray-900">{onboardingData.stakeholders.length} people</span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">Critical Processes:</span>
                  <span className="ml-2 text-gray-900">{onboardingData.criticalProcesses.length} selected</span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">AI Autonomy:</span>
                  <span className="ml-2 text-gray-900 capitalize">{onboardingData.autonomyLevel}</span>
                </div>
              </div>
            </div>

            <div className="bg-green-50 border border-green-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-green-900 mb-4">🎯 What Happens Next</h3>
              <div className="space-y-3">
                <div className="flex items-start space-x-3">
                  <div className="bg-green-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">1</div>
                  <div>
                    <p className="font-medium text-green-900">Project Initialization</p>
                    <p className="text-sm text-green-700">Our Project Orchestrator will analyze your requirements and create a detailed project plan</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="bg-green-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">2</div>
                  <div>
                    <p className="font-medium text-green-900">Stakeholder Outreach</p>
                    <p className="text-sm text-green-700">Automated scheduling and preparation for stakeholder interviews</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="bg-green-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">3</div>
                  <div>
                    <p className="font-medium text-green-900">Knowledge Graph Creation</p>
                    <p className="text-sm text-green-700">Building a comprehensive knowledge base from your project context</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="bg-green-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">4</div>
                  <div>
                    <p className="font-medium text-green-900">Continuous Monitoring</p>
                    <p className="text-sm text-green-700">Real-time project tracking and autonomous progress updates</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="text-center">
              <button
                onClick={launchProject}
                disabled={isLoading}
                className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                {isLoading ? (
                  <span className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    <span>Launching Project...</span>
                  </span>
                ) : (
                  <span className="flex items-center space-x-2">
                    <span>🚀</span>
                    <span>Launch Autonomous Project</span>
                  </span>
                )}
              </button>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => router.push('/')}
                className="text-gray-600 hover:text-gray-900"
              >
                ← Back to Dashboard
              </button>
              <h1 className="text-2xl font-bold text-gray-900">
                🧠 Autonomous Project Onboarding
              </h1>
            </div>
            <div className="text-sm text-gray-500">
              Step {currentStep} of {steps.length}
            </div>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between mb-4">
            {steps.map((step, index) => (
              <div key={step.id} className="flex items-center">
                <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 ${
                  currentStep >= step.id 
                    ? 'bg-blue-600 border-blue-600 text-white' 
                    : 'border-gray-300 text-gray-400'
                }`}>
                  {currentStep > step.id ? '✓' : step.icon}
                </div>
                {index < steps.length - 1 && (
                  <div className={`w-16 h-1 mx-2 ${
                    currentStep > step.id ? 'bg-blue-600' : 'bg-gray-300'
                  }`} />
                )}
              </div>
            ))}
          </div>
          <div className="text-center">
            <h2 className="text-lg font-semibold text-gray-900">
              {steps[currentStep - 1]?.title}
            </h2>
            <p className="text-sm text-gray-600">
              {steps[currentStep - 1]?.description}
            </p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-lg border p-8">
          {renderStep()}
        </div>

        {/* Navigation */}
        <div className="flex justify-between mt-8">
          <button
            onClick={prevStep}
            disabled={currentStep === 1}
            className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            ← Previous
          </button>
          
          {currentStep < steps.length ? (
            <button
              onClick={nextStep}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Next →
            </button>
          ) : null}
        </div>
      </div>
    </div>
  );
}