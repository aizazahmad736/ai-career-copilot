import React from 'react';
import { CheckCircle, AlertTriangle, XCircle, Star } from 'lucide-react';

export default function MatchScoreGauge({
  score = 0,
  matchedCount = 0,
  partialCount = 0,
  missingCount = 0,
  bonusCount = 0,
  targetRole = 'Target Role'
}) {
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  let colorClass = 'text-emerald-400';
  let badgeText = 'Strong Match';
  let badgeBg = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';

  if (score < 60) {
    colorClass = 'text-amber-400';
    badgeText = 'Needs Preparation';
    badgeBg = 'bg-amber-500/10 text-amber-400 border-amber-500/20';
  } else if (score < 78) {
    colorClass = 'text-blue-400';
    badgeText = 'Good Foundation';
    badgeBg = 'bg-blue-500/10 text-blue-400 border-blue-500/20';
  }

  return (
    <div className="bg-slate-900/90 border border-slate-800/90 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row items-center justify-between gap-6">
      {/* Radial Gauge */}
      <div className="flex items-center space-x-6">
        <div className="relative w-32 h-32 flex-shrink-0 flex items-center justify-center">
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 128 128">
            {/* Background circle */}
            <circle
              cx="64"
              cy="64"
              r={radius}
              stroke="currentColor"
              strokeWidth="10"
              className="text-slate-800"
              fill="transparent"
            />
            {/* Progress circle */}
            <circle
              cx="64"
              cy="64"
              r={radius}
              stroke="currentColor"
              strokeWidth="10"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              className={`${colorClass} transition-all duration-1000 ease-out`}
              fill="transparent"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
            <span className="text-3xl font-bold tracking-tight text-white">{Math.round(score)}%</span>
            <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">Match</span>
          </div>
        </div>

        <div>
          <div className="flex items-center space-x-2 mb-1">
            <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold border ${badgeBg}`}>
              {badgeText}
            </span>
          </div>
          <h3 className="text-lg font-bold text-white tracking-tight">{targetRole}</h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Role readiness evaluated against core prerequisites & industry hiring benchmarks.
          </p>
        </div>
      </div>

      {/* Breakdown Pills */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 w-full md:w-auto">
        <div className="p-3 bg-slate-950 border border-emerald-500/20 rounded-xl text-center">
          <div className="flex items-center justify-center space-x-1 text-emerald-400 mb-1">
            <CheckCircle className="w-3.5 h-3.5" />
            <span className="text-xs font-semibold">Matched</span>
          </div>
          <span className="text-xl font-bold text-white">{matchedCount}</span>
        </div>

        <div className="p-3 bg-slate-950 border border-amber-500/20 rounded-xl text-center">
          <div className="flex items-center justify-center space-x-1 text-amber-400 mb-1">
            <AlertTriangle className="w-3.5 h-3.5" />
            <span className="text-xs font-semibold">Partial</span>
          </div>
          <span className="text-xl font-bold text-white">{partialCount}</span>
        </div>

        <div className="p-3 bg-slate-950 border border-rose-500/20 rounded-xl text-center">
          <div className="flex items-center justify-center space-x-1 text-rose-400 mb-1">
            <XCircle className="w-3.5 h-3.5" />
            <span className="text-xs font-semibold">Missing</span>
          </div>
          <span className="text-xl font-bold text-white">{missingCount}</span>
        </div>

        <div className="p-3 bg-slate-950 border border-purple-500/20 rounded-xl text-center">
          <div className="flex items-center justify-center space-x-1 text-purple-400 mb-1">
            <Star className="w-3.5 h-3.5" />
            <span className="text-xs font-semibold">Bonus</span>
          </div>
          <span className="text-xl font-bold text-white">{bonusCount}</span>
        </div>
      </div>
    </div>
  );
}
