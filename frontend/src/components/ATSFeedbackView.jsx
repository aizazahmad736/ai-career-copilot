import React from 'react';
import { CheckCircle2, AlertCircle, Sparkles, ArrowRight, Gauge } from 'lucide-react';

export default function ATSFeedbackView({ atsFeedback }) {
  if (!atsFeedback) return null;

  const {
    overall_ats_score = 75,
    readability_score = 80,
    impact_metrics_score = 65,
    strengths = [],
    weaknesses = [],
    actionable_bullet_fixes = []
  } = atsFeedback;

  return (
    <div className="bg-slate-900/90 border border-slate-800/90 rounded-2xl p-6 shadow-xl space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800/80">
        <div>
          <h3 className="text-base font-semibold text-white tracking-tight flex items-center space-x-2">
            <Gauge className="w-5 h-5 text-indigo-400" />
            <span>ATS Resume Optimization & Critique</span>
          </h3>
          <p className="text-xs text-slate-400">
            How applicant tracking systems and recruiters evaluate your CV phrasing and format.
          </p>
        </div>

        <div className="flex items-center space-x-3 bg-slate-950 px-3.5 py-1.5 rounded-xl border border-slate-800">
          <span className="text-xs text-slate-400 font-medium">ATS Score:</span>
          <span className="text-base font-bold text-indigo-400">{overall_ats_score}/100</span>
        </div>
      </div>

      {/* Score Bars */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-3.5 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
          <div className="flex justify-between text-xs">
            <span className="text-slate-400 font-medium">Overall ATS Readability</span>
            <span className="text-indigo-400 font-bold">{overall_ats_score}%</span>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
            <div
              className="bg-indigo-500 h-full rounded-full transition-all duration-500"
              style={{ width: `${overall_ats_score}%` }}
            />
          </div>
        </div>

        <div className="p-3.5 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
          <div className="flex justify-between text-xs">
            <span className="text-slate-400 font-medium">Format & Section Hierarchy</span>
            <span className="text-blue-400 font-bold">{readability_score}%</span>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
            <div
              className="bg-blue-500 h-full rounded-full transition-all duration-500"
              style={{ width: `${readability_score}%` }}
            />
          </div>
        </div>

        <div className="p-3.5 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
          <div className="flex justify-between text-xs">
            <span className="text-slate-400 font-medium">Quantified Impact & Metrics</span>
            <span className="text-purple-400 font-bold">{impact_metrics_score}%</span>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
            <div
              className="bg-purple-500 h-full rounded-full transition-all duration-500"
              style={{ width: `${impact_metrics_score}%` }}
            />
          </div>
        </div>
      </div>

      {/* Strengths and Weaknesses Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Strengths */}
        {strengths.length > 0 && (
          <div className="p-4 bg-slate-950 border border-emerald-500/20 rounded-xl space-y-2.5">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-emerald-400 flex items-center space-x-1.5">
              <CheckCircle2 className="w-4 h-4" />
              <span>Key Strengths</span>
            </h4>
            <ul className="space-y-1.5 text-xs text-slate-300">
              {strengths.map((str, i) => (
                <li key={i} className="flex items-start space-x-2">
                  <span className="text-emerald-400 font-bold">•</span>
                  <span>{str}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Weaknesses */}
        {weaknesses.length > 0 && (
          <div className="p-4 bg-slate-950 border border-amber-500/20 rounded-xl space-y-2.5">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-amber-400 flex items-center space-x-1.5">
              <AlertCircle className="w-4 h-4" />
              <span>Areas to Improve</span>
            </h4>
            <ul className="space-y-1.5 text-xs text-slate-300">
              {weaknesses.map((weak, i) => (
                <li key={i} className="flex items-start space-x-2">
                  <span className="text-amber-400 font-bold">•</span>
                  <span>{weak}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Actionable Bullet Point Transformations */}
      {actionable_bullet_fixes.length > 0 && (
        <div className="space-y-3 pt-2">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-indigo-400 flex items-center space-x-1.5">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Bullet Point Rewrites (High-Impact Metrics)</span>
          </h4>

          <div className="space-y-3">
            {actionable_bullet_fixes.map((fix, i) => (
              <div key={i} className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
                <div className="flex items-start space-x-2">
                  <span className="px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20 text-[10px] font-mono uppercase flex-shrink-0">
                    Original
                  </span>
                  <p className="text-xs text-slate-400 line-through">{fix.original}</p>
                </div>

                <div className="flex items-start space-x-2 pt-1">
                  <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-mono uppercase flex-shrink-0">
                    Optimized
                  </span>
                  <p className="text-xs text-emerald-300 font-medium leading-relaxed">{fix.improved}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
