import React from 'react';
import { Code, Layers, Database, Cloud, Brain, HeartHandshake } from 'lucide-react';

export default function ExtractedSkillsView({ skills }) {
  if (!skills) return null;

  const categories = [
    { key: 'languages', label: 'Programming Languages', icon: Code, color: 'indigo' },
    { key: 'frameworks', label: 'Frameworks & Libraries', icon: Layers, color: 'blue' },
    { key: 'databases', label: 'Databases & Storage', icon: Database, color: 'cyan' },
    { key: 'tools_and_cloud', label: 'DevOps & Tools', icon: Cloud, color: 'sky' },
    { key: 'core_concepts', label: 'Core CS & Concepts', icon: Brain, color: 'violet' },
    { key: 'soft_skills', label: 'Soft Skills & Leadership', icon: HeartHandshake, color: 'emerald' },
  ];

  return (
    <div className="bg-slate-900/90 border border-slate-800/90 rounded-2xl p-6 shadow-xl space-y-5">
      <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
        <div>
          <h3 className="text-base font-semibold text-white tracking-tight">
            Extracted Candidate Skills Inventory
          </h3>
          <p className="text-xs text-slate-400">
            Skills identified and normalized by AI from your uploaded resume.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {categories.map((cat) => {
          const items = skills[cat.key] || [];
          if (items.length === 0) return null;
          const Icon = cat.icon;

          return (
            <div key={cat.key} className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 flex flex-col">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <Icon className="w-4 h-4 text-indigo-400" />
                  <span className="text-xs font-semibold text-white">{cat.label}</span>
                </div>
                <span className="text-[11px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 font-mono">
                  {items.length}
                </span>
              </div>

              <div className="flex flex-wrap gap-1.5 mt-auto">
                {items.map((skill, i) => (
                  <span
                    key={i}
                    className="px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-800/80 hover:bg-slate-800 text-slate-200 border border-slate-700/50 transition-colors"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
