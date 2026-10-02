import React, { useEffect, useRef, useState } from 'react';
import { AudioLines, Brain, CheckCircle2, Loader2, Mic, MicOff, Send, Volume2 } from 'lucide-react';
import { answerInterviewQuestion, createInterviewSession } from '../services/api';

export default function MockInterviewView({ analysisId, targetRole, customApiKey }) {
  const [mode, setMode] = useState('mixed');
  const [session, setSession] = useState(null);
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false);
  const [error, setError] = useState('');
  const recognitionRef = useRef(null);

  useEffect(() => () => recognitionRef.current?.stop(), []);

  const handleStart = async () => {
    setLoading(true);
    setError('');
    try {
      const nextSession = await createInterviewSession({ analysisId, mode, customApiKey });
      setSession(nextSession);
      setAnswer('');
    } catch (err) {
      setError(err.message || 'Could not start interview.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    if (!answer.trim() || loading) return;
    setLoading(true);
    setError('');
    try {
      const updated = await answerInterviewQuestion(session.id, answer.trim(), customApiKey);
      setSession(updated);
      setAnswer('');
    } catch (err) {
      setError(err.message || 'Could not submit answer.');
    } finally {
      setLoading(false);
    }
  };

  const handleVoiceInput = () => {
    const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!Recognition) {
      setError('Speech recognition is not available in this browser. You can still type your answer.');
      return;
    }
    if (listening) {
      recognitionRef.current?.stop();
      return;
    }
    const recognition = new Recognition();
    recognition.lang = 'en-US';
    recognition.interimResults = true;
    recognition.continuous = true;
    recognition.onresult = (event) => {
      const transcript = Array.from(event.results).map((item) => item[0].transcript).join(' ');
      setAnswer(transcript);
    };
    recognition.onend = () => setListening(false);
    recognition.onerror = () => {
      setListening(false);
      setError('Microphone input stopped. You can continue by typing.');
    };
    recognitionRef.current = recognition;
    setError('');
    setListening(true);
    recognition.start();
  };

  const currentQuestion = session?.questions[session.responses.length];
  const speakQuestion = () => {
    if (!currentQuestion || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(new SpeechSynthesisUtterance(currentQuestion.question));
  };

  return (
    <section className="bg-slate-900/90 border border-slate-800/90 rounded-2xl p-6 shadow-xl space-y-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
        <div>
          <h3 className="text-base font-semibold text-white flex items-center gap-2"><Brain className="w-5 h-5 text-amber-300" /> AI Mock Interview</h3>
          <p className="text-xs text-slate-400 mt-1">Practice for {targetRole}; get feedback after each answer.</p>
        </div>
        {!session && (
          <div className="flex gap-2">
            <select value={mode} onChange={(event) => setMode(event.target.value)} aria-label="Interview style" className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white">
              <option value="mixed">Mixed</option>
              <option value="technical">Technical</option>
              <option value="behavioral">Behavioral</option>
            </select>
            <button onClick={handleStart} disabled={loading || !analysisId} className="inline-flex items-center gap-2 rounded-lg bg-amber-500 hover:bg-amber-400 disabled:opacity-50 px-3 py-2 text-xs font-semibold text-slate-950">
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <AudioLines className="w-4 h-4" />} Start practice
            </button>
          </div>
        )}
      </div>

      {!analysisId && <p className="text-xs text-amber-300">Upload a resume to save interview sessions and track results.</p>}
      {error && <p role="alert" className="text-xs text-rose-300">{error}</p>}

      {session && (
        <div className="space-y-4">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>{session.responses.length} of {session.questions.length} answered</span>
            <span className="capitalize">{session.mode} practice</span>
          </div>
          {session.responses.map((response, index) => (
            <article key={response.question_index} className="rounded-xl border border-slate-800 bg-slate-950 p-4 space-y-3">
              <p className="text-xs text-slate-500">Question {index + 1}: {session.questions[index].question}</p>
              <p className="text-sm text-slate-200">{response.answer}</p>
              <div className="flex flex-wrap items-center gap-3 border-t border-slate-800 pt-3">
                <span className="text-sm font-bold text-amber-300">{response.overall_score}/100</span>
                <span className="text-[10px] uppercase text-slate-500">{response.evaluation_source === 'gemini' ? 'Gemini feedback' : 'Local rubric feedback'}</span>
              </div>
              <div className="grid gap-3 sm:grid-cols-2 text-xs">
                <div><p className="font-semibold text-emerald-300 mb-1">What worked</p>{response.strengths.map((item) => <p key={item} className="text-slate-400">{item}</p>)}</div>
                <div><p className="font-semibold text-cyan-300 mb-1">Try next</p>{response.improvements.map((item) => <p key={item} className="text-slate-400">{item}</p>)}</div>
              </div>
            </article>
          ))}

          {session.status === 'completed' ? (
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 rounded-xl bg-emerald-950/30 border border-emerald-800/50 p-4">
              <p className="text-sm text-emerald-200 flex items-center gap-2"><CheckCircle2 className="w-5 h-5" /> Interview complete · average {session.total_score}/100</p>
              <button onClick={handleStart} disabled={loading} className="text-xs font-semibold text-amber-300 hover:text-amber-200">Start another</button>
            </div>
          ) : (
            <div className="rounded-xl bg-slate-950 border border-slate-800 p-4 space-y-3">
              <div className="flex items-start justify-between gap-3">
                <div><p className="text-[11px] uppercase text-amber-300 font-semibold">Question {session.responses.length + 1}</p><p className="text-sm text-white mt-1">{currentQuestion?.question}</p></div>
                <button onClick={speakQuestion} aria-label="Read question aloud" title="Read question aloud" className="text-slate-400 hover:text-white"><Volume2 className="w-4 h-4" /></button>
              </div>
              <textarea value={answer} onChange={(event) => setAnswer(event.target.value)} rows={4} maxLength={10000} placeholder="Structure your answer with a real example..." className="w-full resize-y rounded-lg border border-slate-700 bg-slate-900 p-3 text-sm text-white placeholder:text-slate-500 focus:outline-none focus:border-amber-400" />
              <div className="flex items-center justify-between gap-3">
                <button onClick={handleVoiceInput} className="inline-flex items-center gap-2 text-xs text-slate-300 hover:text-white" title="Dictate answer">
                  {listening ? <MicOff className="w-4 h-4 text-rose-300" /> : <Mic className="w-4 h-4" />}{listening ? 'Stop dictation' : 'Dictate'}
                </button>
                <button onClick={handleSubmit} disabled={loading || answer.trim().length < 10} className="inline-flex items-center gap-2 rounded-lg bg-amber-500 hover:bg-amber-400 disabled:opacity-50 px-3 py-2 text-xs font-semibold text-slate-950">
                  {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />} Submit answer
                </button>
              </div>
            </div>
          )}
          {session.status === 'completed' && session.total_score != null && (
            <div className="grid grid-cols-4 gap-2">
              {['relevance', 'specificity', 'clarity', 'role_alignment'].map((name) => {
                const scores = session.responses.flatMap((response) => response.scores[name] ?? []);
                const average = Math.round(scores.reduce((sum, score) => sum + score, 0) / scores.length);
                return <div key={name} className="bg-slate-950 border border-slate-800 rounded-lg p-3 text-center"><p className="text-lg font-bold text-white">{average}</p><p className="text-[10px] text-slate-500 capitalize">{name.replace('_', ' ')}</p></div>;
              })}
            </div>
          )}
        </div>
      )}
    </section>
  );
}