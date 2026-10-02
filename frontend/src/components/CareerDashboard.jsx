import React, { useEffect, useState } from 'react';
import { ArrowLeft, BarChart3, BriefcaseBusiness, FileText, Loader2, Mic2, TrendingUp } from 'lucide-react';
import { getDashboardSummary } from '../services/api';

function formatDate(value) {
  if (!value) return 'Date unavailable';
  return new Date(value).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
}

export default function CareerDashboard({ onReturn, onSelectVersion }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    getDashboardSummary()
      .then((summary) => active && setData(summary))
      .catch((err) => active && setError(err.message || 'Could not load career history.'))
      .finally(() => active && setLoading(false));
    return () => { active = false; };
  }, []);

  if (loading) return <div className="py-24 flex justify-center text-cyan-300"><Loader2 className="w-6 h-6 animate-spin" /></div>;
  if (error) return <div role="alert" className="mx-auto max-w-5xl py-16 text-sm text-rose-300">{error}</div>;

  const { metrics, resume_versions: versions, match_trend: trend, skill_gaps: gaps, interview_history: interviews, job_search_history: searches } = data;
  const metricItems = [
    { label: 'Resume versions', value: metrics.resume_versions, icon: FileText, color: 'text-cyan-300' },
    { label: 'Average role match', value: `${metrics.average_match_score}%`, icon: TrendingUp, color: 'text-emerald-300' },
    { label: 'Learning weeks complete', value: `${metrics.completed_learning_weeks}/${metrics.total_learning_weeks}`, icon: BarChart3, color: 'text-amber-300' },
    { label: 'Interview average', value: metrics.completed_interviews ? `${metrics.average_interview_score}%` : 'Not scored', icon: Mic2, color: 'text-rose-300' },
    { label: 'Job searches', value: metrics.job_searches, icon: BriefcaseBusiness, color: 'text-sky-300' },
    { label: 'Tracked applications', value: metrics.tracked_applications, icon: BriefcaseBusiness, color: 'text-cyan-300' },
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 border-b border-slate-800 pb-5">
        <div><p className="text-xs uppercase text-cyan-300 font-semibold">Career progress</p><h1 className="text-2xl font-bold text-white mt-1">Dashboard</h1><p className="text-sm text-slate-400 mt-1">Resume versions, skill progress, practice results, and job-search activity.</p></div>
        <button onClick={onReturn} className="inline-flex items-center gap-2 text-xs text-slate-300 hover:text-white"><ArrowLeft className="w-4 h-4" /> Return to workspace</button>
      </div>

      <section className="grid grid-cols-2 lg:grid-cols-6 divide-x divide-y lg:divide-y-0 divide-slate-800 border-y border-slate-800">
        {metricItems.map(({ label, value, icon: Icon, color }) => (
          <div key={label} className="p-4 min-w-0">
            <Icon className={`w-4 h-4 ${color}`} />
            <p className="text-xl font-bold text-white mt-3">{value}</p>
            <p className="text-xs text-slate-500 mt-1">{label}</p>
          </div>
        ))}
      </section>

      <div className="grid gap-8 lg:grid-cols-2">
        <section className="space-y-4">
          <div><h2 className="text-sm font-semibold text-white">Resume versions</h2><p className="text-xs text-slate-500 mt-1">Select a snapshot to reopen its analysis.</p></div>
          {versions.length === 0 ? <p className="text-xs text-slate-500">No resume analyses yet.</p> : (
            <div className="divide-y divide-slate-800 border-y border-slate-800">
              {versions.map((version) => (
                <button key={version.analysis_id} onClick={() => version.parsed_resume && onSelectVersion(version)} disabled={!version.parsed_resume} className="w-full text-left py-3 flex items-center justify-between gap-4 disabled:opacity-50 hover:bg-slate-900/50 px-2">
                  <span className="min-w-0"><span className="block text-sm text-white truncate">{version.filename} · v{version.version_number}</span><span className="block text-xs text-slate-500 mt-1">{version.target_role} · {formatDate(version.created_at)}</span></span>
                  <span className="shrink-0 text-right"><span className="block text-sm font-semibold text-cyan-300">{Math.round(version.match_score)}%</span><span className="text-[10px] text-slate-500">role match</span></span>
                </button>
              ))}
            </div>
          )}
        </section>

        <section className="space-y-4">
          <div><h2 className="text-sm font-semibold text-white">Role match trend</h2><p className="text-xs text-slate-500 mt-1">Scores from saved resume analyses.</p></div>
          {trend.length === 0 ? <p className="text-xs text-slate-500">No score history yet.</p> : (
            <div className="space-y-3">
              {trend.map((item, index) => <div key={`${item.date}-${index}`} className="grid grid-cols-[1fr_auto] gap-x-4 gap-y-1 items-center"><span className="text-xs text-slate-300 truncate">{item.target_role}</span><span className="text-xs text-slate-400">{Math.round(item.score)}%</span><div className="col-span-2 h-1.5 bg-slate-800 rounded-full overflow-hidden"><div className="h-full bg-emerald-400" style={{ width: `${item.score}%` }} /></div></div>)}
            </div>
          )}
        </section>

        <section className="space-y-4">
          <div><h2 className="text-sm font-semibold text-white">Recurring skill gaps</h2><p className="text-xs text-slate-500 mt-1">Most frequently missing across your analyses.</p></div>
          {gaps.length === 0 ? <p className="text-xs text-slate-500">No skill gaps recorded yet.</p> : <div className="space-y-2">{gaps.map((item) => <div key={item.skill} className="flex items-center justify-between border-b border-slate-800 py-2"><span className="text-xs text-slate-300">{item.skill}</span><span className="text-xs text-rose-300">{item.count}×</span></div>)}</div>}
        </section>

        <section className="space-y-4">
          <div><h2 className="text-sm font-semibold text-white">Interview practice</h2><p className="text-xs text-slate-500 mt-1">Recent completed and active sessions.</p></div>
          {interviews.length === 0 ? <p className="text-xs text-slate-500">No interview sessions yet.</p> : <div className="divide-y divide-slate-800 border-y border-slate-800">{interviews.map((interview) => <div key={interview.id} className="py-3 flex items-center justify-between gap-3"><span><span className="block text-xs text-white">{interview.target_role} · {interview.mode}</span><span className="text-[11px] text-slate-500">{formatDate(interview.created_at)} · {interview.status}</span></span><span className="text-sm text-amber-300">{interview.score == null ? 'In progress' : `${Math.round(interview.score)}%`}</span></div>)}</div>}
        </section>

        <section className="space-y-4 lg:col-span-2">
          <div><h2 className="text-sm font-semibold text-white">Job-search activity</h2><p className="text-xs text-slate-500 mt-1">Recent searches and results.</p></div>
          {searches.length === 0 ? <p className="text-xs text-slate-500">No searches recorded yet.</p> : <div className="divide-y divide-slate-800 border-y border-slate-800">{searches.map((search) => <div key={search.id} className="py-3 flex items-center justify-between gap-4"><span><span className="block text-xs text-white">{search.query} · {search.target_role}</span><span className="text-[11px] text-slate-500">{formatDate(search.created_at)}</span></span><span className="text-xs text-slate-300">{search.results} results · top {Math.round(search.top_match_score)}%</span></div>)}</div>}
        </section>

        <section className="space-y-4 lg:col-span-2">
          <div><h2 className="text-sm font-semibold text-white">Application tracker</h2><p className="text-xs text-slate-500 mt-1">Status for jobs you have saved from matching results.</p></div>
          {data.applications.length === 0 ? <p className="text-xs text-slate-500">No tracked applications yet.</p> : <div className="divide-y divide-slate-800 border-y border-slate-800">{data.applications.map((application) => <div key={application.id} className="py-3 flex items-center justify-between gap-4"><span><span className="block text-xs text-white">{application.title} · {application.company}</span><span className="text-[11px] text-slate-500">{application.target_role} · {formatDate(application.updated_at)}</span></span><span className="text-xs capitalize text-cyan-300">{application.status}</span></div>)}</div>}
        </section>
      </div>
    </div>
  );
}