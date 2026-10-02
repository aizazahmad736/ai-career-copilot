import React, { useEffect, useState } from 'react';
import { BookOpen, CheckCircle2, Circle, Clock3, Loader2, Sparkles } from 'lucide-react';
import { createLearningPlan, getLearningPlan, updateLearningMilestone } from '../services/api';

export default function LearningPlanView({ analysisId }) {
  const [durationWeeks, setDurationWeeks] = useState(6);
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [savingWeek, setSavingWeek] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    if (analysisId) {
      getLearningPlan(analysisId)
        .then((savedPlan) => active && setPlan(savedPlan))
        .catch(() => {});
    }
    return () => { active = false; };
  }, [analysisId]);

  const handleGenerate = async () => {
    setLoading(true);
    setError('');
    try {
      setPlan(await createLearningPlan(analysisId, durationWeeks));
    } catch (err) {
      setError(err.message || 'Could not generate a learning plan.');
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (milestone) => {
    setSavingWeek(milestone.week);
    setError('');
    try {
      const updated = await updateLearningMilestone(plan.id, milestone.week, !milestone.completed);
      setPlan(updated);
    } catch (err) {
      setError(err.message || 'Could not save milestone progress.');
    } finally {
      setSavingWeek(null);
    }
  };

  const completedCount = plan?.milestones.filter((milestone) => milestone.completed).length || 0;

  return (
    <section className="bg-slate-900/90 border border-slate-800/90 rounded-2xl p-6 shadow-xl space-y-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
        <div>
          <h3 className="text-base font-semibold text-white flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-cyan-400" /> Weekly Learning Plan
          </h3>
          <p className="text-xs text-slate-400 mt-1">Milestones are based on this resume’s identified skill gaps.</p>
        </div>
        {!plan && (
          <div className="flex items-center gap-2">
            <select
              value={durationWeeks}
              onChange={(event) => setDurationWeeks(Number(event.target.value))}
              className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
              aria-label="Plan duration in weeks"
            >
              {[4, 6, 8, 12].map((weeks) => <option key={weeks} value={weeks}>{weeks} weeks</option>)}
            </select>
            <button
              onClick={handleGenerate}
              disabled={loading || !analysisId}
              className="inline-flex items-center gap-2 bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 rounded-lg px-3 py-2 text-xs font-semibold text-white"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
              Build plan
            </button>
          </div>
        )}
      </div>

      {!analysisId && <p className="text-xs text-amber-300">Upload a resume to save a plan and track weekly progress.</p>}
      {error && <p role="alert" className="text-xs text-rose-300">{error}</p>}

      {plan && (
        <>
          <div className="flex items-center justify-between text-xs text-slate-300">
            <span>{completedCount} of {plan.milestones.length} weeks complete</span>
            <span className="text-slate-500">{plan.duration_weeks}-week plan</span>
          </div>
          <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-cyan-400 transition-all" style={{ width: `${completedCount / plan.milestones.length * 100}%` }} />
          </div>
          <div className="grid gap-3 md:grid-cols-2">
            {plan.milestones.map((milestone) => (
              <article key={milestone.week} className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-3">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-[11px] text-cyan-300 font-semibold uppercase">Week {milestone.week}</p>
                    <h4 className="text-sm font-semibold text-white mt-1">{milestone.focus}</h4>
                  </div>
                  <button
                    onClick={() => handleToggle(milestone)}
                    disabled={savingWeek === milestone.week}
                    aria-label={`${milestone.completed ? 'Mark incomplete' : 'Mark complete'} week ${milestone.week}`}
                    className="text-cyan-300 disabled:opacity-50"
                  >
                    {savingWeek === milestone.week ? <Loader2 className="w-5 h-5 animate-spin" /> : milestone.completed ? <CheckCircle2 className="w-5 h-5" /> : <Circle className="w-5 h-5" />}
                  </button>
                </div>
                <p className="text-xs text-slate-300">{milestone.goal}</p>
                <ul className="space-y-1.5">
                  {milestone.tasks.map((task) => <li key={task} className="text-xs text-slate-400">- {task}</li>)}
                </ul>
                <p className="text-xs text-slate-300"><strong>Build:</strong> {milestone.project_checkpoint}</p>
                <div className="flex items-center justify-between border-t border-slate-800 pt-2">
                  <div className="flex flex-wrap gap-x-3 gap-y-1">
                    {milestone.resources.map((resource) => (
                      <a key={resource.url} href={resource.url} target="_blank" rel="noreferrer" className="text-xs text-cyan-300 hover:text-cyan-200 underline underline-offset-2">{resource.label}</a>
                    ))}
                  </div>
                  <span className="inline-flex items-center gap-1 text-[11px] text-slate-500 shrink-0"><Clock3 className="w-3.5 h-3.5" /> {milestone.estimated_hours}h</span>
                </div>
              </article>
            ))}
          </div>
        </>
      )}
    </section>
  );
}