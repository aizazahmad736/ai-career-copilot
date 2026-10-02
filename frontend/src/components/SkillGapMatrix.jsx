import React, { useState } from 'react';
import { CheckCircle2, AlertTriangle, XCircle, Star } from 'lucide-react';

export default function SkillGapMatrix({
  matched = [],
  partial = [],
  missing = [],
  bonus = [],
  targetRole
}) {
  const [activeFilter, setActiveFilter] = useState('all');

  const allItems = [
    ...matched.map(item => ({ ...item, displayStatus: 'matched' })),
    ...partial.map(item => ({ ...item, displayStatus: 'partial' })),
    ...missing.map(item => ({ ...item, displayStatus: 'missing' })),
    ...bonus.map(item => ({ ...item, displayStatus: 'bonus' })),
  ];

  const filteredItems = activeFilter === 'all'
    ? allItems
    : allItems.filter(item => item.displayStatus === activeFilter);

  const getStatusBadge = (status) => {
    switch (status) {
      case 'matched':
        return {
          icon: CheckCircle2,
          text: 'Matched',
          className: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
        };
      case 'partial':
        return {
          icon: AlertTriangle,
          text: 'Partial / Adjacent',
          className: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
        };
      case 'missing':
        return {
          icon: XCircle,
          text: 'Missing Critical',
          className: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
        };
      case 'bonus':
        return {
          icon: Star,
          text: 'Bonus / Differentiator',
          className: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
        };
      default:
        return {
          icon: CheckCircle2,
          text: status,
          className: 'bg-slate-800 text-slate-300 border-slate-700',
        };
    }
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800/90 rounded-2xl p-6 shadow-xl space-y-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800/80">
        <div>
          <h3 className="text-base font-semibold text-white tracking-tight flex items-center space-x-2">
            <span>Skill Gap Analysis Matrix</span>
            <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-indigo-400 font-mono">
              {filteredItems.length} Skills
            </span>
          </h3>
          <p className="text-xs text-slate-400">
            Comparing your CV skills against benchmarks for {targetRole}.
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex flex-wrap items-center gap-1.5 p-1 bg-slate-950 border border-slate-800 rounded-xl text-xs">
          <button
            onClick={() => setActiveFilter('all')}
            className={`px-3 py-1 rounded-lg font-medium transition-all ${
              activeFilter === 'all' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            All ({allItems.length})
          </button>
          <button
            onClick={() => setActiveFilter('matched')}
            className={`px-2.5 py-1 rounded-lg font-medium transition-all flex items-center space-x-1 ${
              activeFilter === 'matched' ? 'bg-emerald-600 text-white' : 'text-emerald-400 hover:bg-emerald-500/10'
            }`}
          >
            <span>Matched ({matched.length})</span>
          </button>
          <button
            onClick={() => setActiveFilter('partial')}
            className={`px-2.5 py-1 rounded-lg font-medium transition-all flex items-center space-x-1 ${
              activeFilter === 'partial' ? 'bg-amber-600 text-white' : 'text-amber-400 hover:bg-amber-500/10'
            }`}
          >
            <span>Partial ({partial.length})</span>
          </button>
          <button
            onClick={() => setActiveFilter('missing')}
            className={`px-2.5 py-1 rounded-lg font-medium transition-all flex items-center space-x-1 ${
              activeFilter === 'missing' ? 'bg-rose-600 text-white' : 'text-rose-400 hover:bg-rose-500/10'
            }`}
          >
            <span>Missing ({missing.length})</span>
          </button>
          <button
            onClick={() => setActiveFilter('bonus')}
            className={`px-2.5 py-1 rounded-lg font-medium transition-all flex items-center space-x-1 ${
              activeFilter === 'bonus' ? 'bg-purple-600 text-white' : 'text-purple-400 hover:bg-purple-500/10'
            }`}
          >
            <span>Bonus ({bonus.length})</span>
          </button>
        </div>
      </div>

      {/* Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
        {filteredItems.map((item, index) => {
          const badge = getStatusBadge(item.displayStatus);
          const Icon = badge.icon;

          return (
            <div
              key={index}
              className="p-4 rounded-xl bg-slate-950 border border-slate-800/90 hover:border-slate-700 transition-all flex flex-col justify-between space-y-2.5"
            >
              <div className="flex items-start justify-between gap-2">
                <div>
                  <span className="text-xs uppercase tracking-wider font-mono text-slate-500 block mb-0.5">
                    {item.category || 'Competency'}
                  </span>
                  <h4 className="text-sm font-semibold text-white">{item.skill}</h4>
                </div>

                <div className={`flex items-center space-x-1 px-2.5 py-1 rounded-full text-xs font-medium border ${badge.className} flex-shrink-0`}>
                  <Icon className="w-3.5 h-3.5" />
                  <span>{badge.text}</span>
                </div>
              </div>

              {item.evidence_or_tip && (
                <p className="text-xs text-slate-400 bg-slate-900/60 p-2.5 rounded-lg border border-slate-800/60 leading-relaxed">
                  {item.evidence_or_tip}
                </p>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
