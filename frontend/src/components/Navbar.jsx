import React from 'react';
import { Sparkles, Key } from 'lucide-react';

export default function Navbar({ onOpenApiKeyModal, onOpenDashboard, onLogout, dashboardActive, userEmail, hasCustomKey, backendOnline }) {
  const phases = [
    { num: 1, name: 'CV & Skill Gap', active: true },
    { num: 2, name: 'Job Matching', active: true },
    { num: 3, name: 'Roadmap', active: true },
    { num: 4, name: 'AI Interview', active: true },
    { num: 5, name: 'Dashboard', active: true },
  ];

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-blue-500 to-cyan-400 p-0.5 shadow-lg shadow-indigo-500/20 flex items-center justify-center">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-indigo-400 animate-pulse" />
            </div>
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg text-white tracking-tight">CareerCopilot</span>
              <span className="px-2 py-0.5 text-[11px] font-semibold tracking-wide uppercase rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                Phases 1-6
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">CV → Skills → Gap Analysis → Jobs</p>
          </div>
        </div>

        {/* Phase Pills */}
        <nav className="hidden md:flex items-center space-x-1.5 p-1 bg-slate-900/60 border border-slate-800 rounded-full text-xs">
          {phases.map((p) => p.num === 5 ? (
            <button key={p.num} onClick={onOpenDashboard} className={`px-3 py-1 rounded-full font-medium transition-all ${dashboardActive ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'}`}>
              P{p.num}: {p.name}
            </button>
          ) : (
            <div key={p.num} className={`px-3 py-1 rounded-full font-medium ${p.active ? 'bg-indigo-600 text-white shadow-sm shadow-indigo-600/50' : 'text-slate-400 opacity-60'}`}>
              P{p.num}: {p.name}
            </div>
          ))}
        </nav>

        {/* Right Actions */}
        <div className="flex items-center space-x-3">
          {userEmail && <span className="hidden xl:block max-w-40 truncate text-xs text-slate-400">{userEmail}</span>}
          {onLogout && <button onClick={onLogout} className="text-xs text-slate-400 hover:text-white">Sign out</button>}
          <div className="hidden sm:flex items-center space-x-1.5 text-xs text-slate-400">
            <div className={`w-2 h-2 rounded-full ${backendOnline ? 'bg-emerald-400 shadow-sm shadow-emerald-400/50' : 'bg-amber-400 animate-ping'}`} />
            <span>{backendOnline ? 'Backend Connected' : 'Connecting...'}</span>
          </div>

          <button
            onClick={onOpenApiKeyModal}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
              hasCustomKey
                ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300 hover:bg-emerald-500/20'
                : 'border-slate-700 bg-slate-800/80 text-slate-300 hover:bg-slate-700 hover:text-white'
            }`}
          >
            <Key className="w-3.5 h-3.5" />
            <span>{hasCustomKey ? 'API Keys Configured' : 'API Keys'}</span>
          </button>
        </div>
      </div>
    </header>
  );
}
