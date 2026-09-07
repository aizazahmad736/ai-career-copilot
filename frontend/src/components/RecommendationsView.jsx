import React from 'react';
import { Compass, Clock, CheckSquare, ArrowRight, Sparkles } from 'lucide-react';

export default function RecommendationsView({ recommendations = [], onNextPhase }) {
  if (recommendations.length === 0) return null;

  return (
    <div className="bg-slate-900/90 border border-slate-800/90 rounded-2xl p-6 shadow-xl space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800/80">
        <div>
          <h3 className="text-base font-semibold text-white tracking-tight flex items-center space-x-2">
            <Compass className="w-5 h-5 text-indigo-400" />
            <span>Actionable Roadmap to Close Skill Gaps</span>
          </h3>
          <p className="text-xs text-slate-400">
            Tailored step-by-step actions prioritized by industry hiring impact.
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {recommendations.map((rec, index) => {
          const isHigh = rec.priority === 'High';

          return (
            <div
              key={index}
              className="p-5 rounded-xl bg-slate-950 border border-slate-800/90 hover:border-slate-700 transition-all space-y-3"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center space-x-2.5">
                  <span
                    className={`px-2.5 py-0.5 rounded-full text-xs font-semibold border ${
                      isHigh
                        ? 'bg-rose-500/10 text-rose-400 border-rose-500/20'
                        : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                    }`}
                  >
                    {rec.priority} Priority
                  </span>
                  <h4 className="text-sm font-bold text-white">{rec.title}</h4>
                </div>

                <div className="flex items-center space-x-1 text-xs text-slate-400 bg-slate-900 px-3 py-1 rounded-lg border border-slate-800">
                  <Clock className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Est. Time: {rec.estimated_time}</span>
                </div>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed">{rec.description}</p>

              {rec.learning_path && rec.learning_path.length > 0 && (
                <div className="p-3 bg-slate-900/60 rounded-xl border border-slate-800/60 space-y-1.5">
                  <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block mb-1">
                    Recommended Action Steps:
                  </span>
                  {rec.learning_path.map((step, sIdx) => (
                    <div key={sIdx} className="flex items-start space-x-2 text-xs text-slate-300">
                      <CheckSquare className="w-3.5 h-3.5 text-indigo-400 flex-shrink-0 mt-0.5" />
                      <span>{step}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Teaser for Next Stage */}
      <div className="mt-6 p-5 rounded-xl bg-gradient-to-r from-indigo-950/40 via-purple-950/30 to-slate-950 border border-indigo-500/30 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-indigo-300 flex-shrink-0">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h5 className="text-sm font-semibold text-white">Ready for the Next Stage?</h5>
            <p className="text-xs text-slate-400">
              In Phase 2, CareerCopilot will use your matched skills to search & recommend targeted job and internship opportunities!
            </p>
          </div>
        </div>

        <button
          onClick={onNextPhase}
          className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs flex items-center space-x-2 transition-all shadow-lg shadow-indigo-600/30 flex-shrink-0"
        >
          <span>Preview Phase 2 Roadmap</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}
