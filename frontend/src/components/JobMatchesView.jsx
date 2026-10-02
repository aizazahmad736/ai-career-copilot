import React, { useState } from 'react';
import { Briefcase, MapPin, Search, ExternalLink, Building2, Clock, Wifi, AlertCircle, CheckCircle2, XCircle, Loader2 } from 'lucide-react';
import { searchJobs } from '../services/api';

const FIT_STYLES = {
  'Strong Match': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
  'Good Match': 'bg-indigo-500/10 text-indigo-300 border-indigo-500/20',
  'Stretch': 'bg-amber-500/10 text-amber-400 border-amber-500/20',
  'Low Match': 'bg-slate-800 text-slate-400 border-slate-700',
};

function formatPostedDate(value) {
  if (!value) return null;
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return null;
  const days = Math.floor((Date.now() - date.getTime()) / (1000 * 60 * 60 * 24));
  if (days <= 0) return 'Posted today';
  if (days === 1) return 'Posted yesterday';
  if (days < 30) return `Posted ${days} days ago`;
  return `Posted ${date.toLocaleDateString()}`;
}

export default function JobMatchesView({ skills, targetRole, experienceLevel, analysisId, tavilyApiKey, serperApiKey }) {
  const [location, setLocation] = useState('');
  const [remoteOnly, setRemoteOnly] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleSearch = async () => {
    setError(null);
    setLoading(true);
    try {
      const res = await searchJobs({
        skills,
        targetRole,
        experienceLevel,
        location: location.trim() || undefined,
        remoteOnly,
        analysisId,
        tavilyApiKey: tavilyApiKey || undefined,
        serperApiKey: serperApiKey || undefined,
      });
      setResult(res);
    } catch (err) {
      console.error(err);
      setError(err.message || 'Failed to search for jobs.');
    } finally {
      setLoading(false);
    }
  };

  const jobs = result?.jobs || [];
  const failedSources = Object.keys(result?.source_errors || {});

  return (
    <div className="bg-slate-900/90 border border-slate-800/90 rounded-2xl p-6 shadow-xl space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800/80">
        <div>
          <h3 className="text-base font-semibold text-white tracking-tight flex items-center space-x-2">
            <Briefcase className="w-5 h-5 text-indigo-400" />
            <span>Job Search & Matching Engine</span>
            <span className="px-2 py-0.5 text-[10px] font-semibold tracking-wide uppercase rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              Phase 2
            </span>
          </h3>
          <p className="text-xs text-slate-400">
            Live listings ranked against the skills extracted from your CV for <strong className="text-indigo-300">{targetRole}</strong>.
          </p>
        </div>
      </div>

      {/* Search Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center gap-3">
        <div className="relative flex-1">
          <MapPin className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && !loading && handleSearch()}
            placeholder="Location (optional) e.g. Berlin, USA, Europe"
            className="w-full pl-9 pr-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
          />
        </div>

        <label className="flex items-center space-x-2 text-xs text-slate-300 cursor-pointer select-none px-1">
          <input
            type="checkbox"
            checked={remoteOnly}
            onChange={(e) => setRemoteOnly(e.target.checked)}
            className="w-4 h-4 rounded accent-indigo-500"
          />
          <span>Remote only</span>
        </label>

        <button
          onClick={handleSearch}
          disabled={loading}
          className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-60 disabled:cursor-not-allowed text-white font-medium text-xs flex items-center justify-center space-x-2 transition-all shadow-lg shadow-indigo-600/30 flex-shrink-0"
        >
          {loading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Search className="w-3.5 h-3.5" />}
          <span>{loading ? 'Searching job boards...' : result ? 'Search Again' : 'Find Matching Jobs'}</span>
        </button>
      </div>

      {error && (
        <div className="p-3 rounded-xl bg-rose-950/40 border border-rose-800/60 text-rose-300 text-xs flex items-center space-x-2.5">
          <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-400" />
          <span>{error}</span>
        </div>
      )}

      {result && (
        <div className="space-y-4">
          {/* Result Summary */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs text-slate-400">
            <span>
              Showing <strong className="text-white">{jobs.length}</strong> of {result.total_found} relevant listings for
              “{result.query}”
            </span>
            <span>Sources: {result.sources_used.join(', ') || 'None'}</span>
          </div>

          {result.is_demo_mode && (
            <div className="p-3 rounded-xl bg-amber-950/30 border border-amber-800/40 text-amber-300 text-xs flex items-start space-x-2.5">
              <AlertCircle className="w-4 h-4 flex-shrink-0 text-amber-400 mt-0.5" />
              <span>
                Live job boards could not be reached, so these are sample listings with fictional companies. Each link opens a real search for that job title.
              </span>
            </div>
          )}

          {!result.is_demo_mode && failedSources.length > 0 && (
            <p className="text-[11px] text-slate-500">
              Could not reach: {failedSources.join(', ')}. Results below come from the remaining sources.
            </p>
          )}

          {jobs.length === 0 && (
            <div className="p-6 rounded-xl bg-slate-950 border border-slate-800/90 text-center text-xs text-slate-400">
              No listings matched these filters. Try clearing the location or turning off “Remote only”.
            </div>
          )}

          {jobs.map((job) => {
            const posted = formatPostedDate(job.posted_at);
            return (
              <div
                key={job.id}
                className="p-5 rounded-xl bg-slate-950 border border-slate-800/90 hover:border-slate-700 transition-all space-y-3"
              >
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                  <div className="space-y-1.5 min-w-0">
                    <h4 className="text-sm font-bold text-white">{job.title}</h4>
                    <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-slate-400">
                      <span className="flex items-center space-x-1">
                        <Building2 className="w-3.5 h-3.5 text-slate-500" />
                        <span>{job.company}</span>
                      </span>
                      {job.location && (
                        <span className="flex items-center space-x-1">
                          <MapPin className="w-3.5 h-3.5 text-slate-500" />
                          <span>{job.location}</span>
                        </span>
                      )}
                      {job.remote && (
                        <span className="flex items-center space-x-1 text-cyan-400">
                          <Wifi className="w-3.5 h-3.5" />
                          <span>Remote</span>
                        </span>
                      )}
                      {job.job_type && <span>{job.job_type}</span>}
                      {job.salary && <span className="text-emerald-400">{job.salary}</span>}
                      {posted && (
                        <span className="flex items-center space-x-1">
                          <Clock className="w-3.5 h-3.5 text-slate-500" />
                          <span>{posted}</span>
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center space-x-2 flex-shrink-0">
                    <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold border ${FIT_STYLES[job.fit_label] || FIT_STYLES['Low Match']}`}>
                      {job.fit_label}
                    </span>
                    <span className="text-lg font-extrabold text-white tabular-nums">{Math.round(job.match_score)}%</span>
                  </div>
                </div>

                <p className="text-xs text-slate-300 leading-relaxed">{job.fit_summary}</p>

                {(job.matched_skills.length > 0 || job.missing_skills.length > 0) && (
                  <div className="p-3 bg-slate-900/60 rounded-xl border border-slate-800/60 space-y-2">
                    {job.matched_skills.length > 0 && (
                      <div className="flex flex-wrap items-center gap-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
                        <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mr-1">You have:</span>
                        {job.matched_skills.map((skill) => (
                          <span key={skill} className="px-2 py-0.5 rounded-md text-[11px] bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                            {skill}
                          </span>
                        ))}
                      </div>
                    )}
                    {job.missing_skills.length > 0 && (
                      <div className="flex flex-wrap items-center gap-1.5">
                        <XCircle className="w-3.5 h-3.5 text-rose-400 flex-shrink-0" />
                        <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mr-1">To learn:</span>
                        {job.missing_skills.map((skill) => (
                          <span key={skill} className="px-2 py-0.5 rounded-md text-[11px] bg-rose-500/10 text-rose-300 border border-rose-500/20">
                            {skill}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {job.description_snippet && (
                  <p className="text-xs text-slate-500 leading-relaxed">{job.description_snippet}</p>
                )}

                <div className="flex items-center justify-between pt-1">
                  <span className="text-[11px] text-slate-500">via {job.source}</span>
                  <a
                    href={job.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-200 transition-colors"
                  >
                    <span>{job.source === 'Sample' ? 'Search this title' : 'View & Apply'}</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
