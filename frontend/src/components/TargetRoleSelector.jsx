import React, { useState } from 'react';
import { Target, ChevronDown, ChevronUp, Briefcase, Award, FileText } from 'lucide-react';

export default function TargetRoleSelector({
  roles,
  selectedRole,
  onSelectRole,
  experienceLevel,
  onSelectExperienceLevel,
  jobDescription,
  onChangeJobDescription
}) {
  const [showJdInput, setShowJdInput] = useState(false);
  const [customRoleInput, setCustomRoleInput] = useState('');
  const isCustom = selectedRole === 'Custom';

  const experienceLevels = [
    'Internship',
    'Entry-Level / Junior',
    'Associate / Mid-Level (1-3 yrs)'
  ];

  const handleRoleChange = (e) => {
    const val = e.target.value;
    if (val === 'Custom') {
      onSelectRole('Custom');
    } else {
      onSelectRole(val);
    }
  };

  const handleCustomSubmit = () => {
    if (customRoleInput.trim()) {
      onSelectRole(customRoleInput.trim());
    }
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800/90 rounded-2xl p-6 shadow-xl space-y-5">
      <div className="flex items-center space-x-2.5 pb-2 border-b border-slate-800/80">
        <Target className="w-5 h-5 text-indigo-400" />
        <h2 className="text-base font-semibold text-white tracking-tight">
          Step 1: Target Career Objective
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Target Role Dropdown */}
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5 flex items-center space-x-1.5">
            <Briefcase className="w-3.5 h-3.5 text-indigo-400" />
            <span>Target Role</span>
          </label>
          <div className="relative">
            <select
              value={isCustom ? 'Custom' : selectedRole}
              onChange={handleRoleChange}
              className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-slate-100 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 appearance-none transition-all cursor-pointer"
            >
              {roles.map((r) => (
                <option key={r.name} value={r.name} className="bg-slate-900 text-slate-100">
                  {r.name}
                </option>
              ))}
              <option value="Custom" className="bg-slate-900 text-indigo-300 font-medium">
                + Custom Target Role...
              </option>
            </select>
            <div className="absolute right-3.5 top-1/2 -translate-y-1/2 pointer-events-none text-slate-400">
              <ChevronDown className="w-4 h-4" />
            </div>
          </div>

          {isCustom && (
            <div className="mt-2.5 flex space-x-2">
              <input
                type="text"
                placeholder="e.g. Prompt Engineer / ML Researcher"
                value={customRoleInput}
                onChange={(e) => setCustomRoleInput(e.target.value)}
                className="flex-1 px-3 py-2 bg-slate-950 border border-indigo-500/50 rounded-xl text-xs text-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
              <button
                type="button"
                onClick={handleCustomSubmit}
                className="px-3 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-medium transition-colors"
              >
                Set
              </button>
            </div>
          )}
        </div>

        {/* Experience Level */}
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5 flex items-center space-x-1.5">
            <Award className="w-3.5 h-3.5 text-indigo-400" />
            <span>Target Seniority</span>
          </label>
          <div className="relative">
            <select
              value={experienceLevel}
              onChange={(e) => onSelectExperienceLevel(e.target.value)}
              className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-slate-100 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 appearance-none transition-all cursor-pointer"
            >
              {experienceLevels.map((lvl) => (
                <option key={lvl} value={lvl} className="bg-slate-900 text-slate-100">
                  {lvl}
                </option>
              ))}
            </select>
            <div className="absolute right-3.5 top-1/2 -translate-y-1/2 pointer-events-none text-slate-400">
              <ChevronDown className="w-4 h-4" />
            </div>
          </div>
        </div>
      </div>

      {/* Optional Job Description Accordion */}
      <div className="pt-1">
        <button
          type="button"
          onClick={() => setShowJdInput(!showJdInput)}
          className="flex items-center space-x-2 text-xs text-indigo-400 hover:text-indigo-300 font-medium transition-colors focus:outline-none"
        >
          <FileText className="w-3.5 h-3.5" />
          <span>{showJdInput ? 'Hide specific Job Description' : '+ Add specific Job Description (Optional)'}</span>
          {showJdInput ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
        </button>

        {showJdInput && (
          <div className="mt-3 animate-in fade-in duration-200">
            <textarea
              rows={4}
              value={jobDescription}
              onChange={(e) => onChangeJobDescription(e.target.value)}
              placeholder="Paste job posting description, requirements, and responsibilities here to benchmark directly against this specific listing..."
              className="w-full p-3 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all font-mono"
            />
          </div>
        )}
      </div>
    </div>
  );
}
