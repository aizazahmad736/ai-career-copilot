import React from 'react';
import { X, CheckCircle2, Briefcase, Map, Mic, BarChart3, Globe } from 'lucide-react';

export default function PhaseRoadmapModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  const phases = [
    {
      phase: 'Phase 1 — MVP',
      status: 'Complete',
      title: 'CV Upload → Parsing → AI Analysis → Skill Gap',
      desc: 'Extract structured profile, categorize technical skills, benchmark against industry role expectations, and generate the match score and gap matrix.',
      icon: CheckCircle2,
      active: true,
      color: 'emerald'
    },
    {
      phase: 'Phase 2',
      status: 'Current / Complete',
      title: 'Job Search → Job Matching Engine',
      desc: 'Pull live job/internship listings (Remotive + Arbeitnow job APIs, optional Tavily/Serper web search), rank opportunities by match score, and pinpoint the skills you have and lack for each role.',
      icon: Briefcase,
      active: true,
      color: 'indigo'
    },
    {
      phase: 'Phase 3',
      status: 'Up Next',
      title: 'Personalized Learning Roadmap',
      desc: 'Generate interactive step-by-step learning schedules with curated resources, project benchmarks, and weekly milestones to close identified skill gaps.',
      icon: Map,
      active: false,
      color: 'blue'
    },
    {
      phase: 'Phase 4',
      status: 'Planned',
      title: 'AI Mock Interviewer',
      desc: 'Interactive audio/chat mock interviews with role-specific behavioral and technical coding questions, followed by instant real-time feedback & scoring.',
      icon: Mic,
      active: false,
      color: 'purple'
    },
    {
      phase: 'Phase 5',
      status: 'Planned',
      title: 'Dashboard + Analytics',
      desc: 'Track candidate progression over time, interview performance analytics, resume versioning, and application tracking history.',
      icon: BarChart3,
      active: false,
      color: 'cyan'
    },
    {
      phase: 'Phase 6',
      status: 'Planned',
      title: 'Public Cloud Deployment',
      desc: 'Production deployment architecture: Vercel frontend, Railway/Render backend, PostgreSQL database, and domain setup.',
      icon: Globe,
      active: false,
      color: 'sky'
    },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-2xl p-6 shadow-2xl relative text-slate-100 max-h-[90vh] overflow-y-auto">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="mb-5">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-indigo-400 font-mono">
            Full Development Plan
          </span>
          <h3 className="text-xl font-bold text-white tracking-tight mt-1">
            AI Career Copilot — 6-Stage Roadmap
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Built systematically in sequential stages as requested.
          </p>
        </div>

        <div className="space-y-3.5">
          {phases.map((p, idx) => {
            const Icon = p.icon;
            return (
              <div
                key={idx}
                className={`p-4 rounded-xl border transition-all ${
                  p.active
                    ? 'bg-emerald-950/20 border-emerald-500/40 shadow-sm'
                    : 'bg-slate-950 border-slate-800/80 opacity-80 hover:opacity-100'
                }`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-center space-x-2.5">
                    <div
                      className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                        p.active
                          ? 'bg-emerald-500/20 text-emerald-400'
                          : 'bg-slate-800 text-slate-400'
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs font-bold text-white">{p.phase}</span>
                        <span
                          className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${
                            p.active
                              ? 'bg-emerald-500/20 text-emerald-300'
                              : 'bg-slate-800 text-slate-400'
                          }`}
                        >
                          {p.status}
                        </span>
                      </div>
                      <h4 className="text-xs font-semibold text-slate-200 mt-0.5">{p.title}</h4>
                    </div>
                  </div>
                </div>
                <p className="text-xs text-slate-400 mt-2 pl-10.5">{p.desc}</p>
              </div>
            );
          })}
        </div>

        <div className="mt-6 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold transition-colors"
          >
            Got it, back to my results
          </button>
        </div>
      </div>
    </div>
  );
}
