import React, { useState } from 'react';
import { Loader2, LockKeyhole, Sparkles } from 'lucide-react';
import { authenticate } from '../services/api';

export default function AuthScreen({ onAuthenticated }) {
  const [mode, setMode] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setLoading(true);
    try {
      const user = await authenticate(mode, email, password);
      onAuthenticated(user);
    } catch (err) {
      setError(err.message || 'Authentication failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center px-4 py-10">
      <section className="w-full max-w-md border border-slate-800 bg-slate-900 p-7 rounded-xl shadow-2xl">
        <div className="flex items-center gap-3 mb-7">
          <div className="w-10 h-10 rounded-lg bg-cyan-400/10 flex items-center justify-center text-cyan-300"><Sparkles className="w-5 h-5" /></div>
          <div><p className="text-lg font-bold text-white">CareerCopilot</p><p className="text-xs text-slate-400">Your private career workspace</p></div>
        </div>
        <div className="flex border-b border-slate-800 mb-6" role="tablist" aria-label="Account access">
          {[['login', 'Sign in'], ['register', 'Create account']].map(([value, label]) => <button key={value} role="tab" aria-selected={mode === value} onClick={() => { setMode(value); setError(''); }} className={`px-4 py-2.5 text-sm border-b-2 ${mode === value ? 'border-cyan-400 text-white' : 'border-transparent text-slate-400 hover:text-white'}`}>{label}</button>)}
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="block text-xs text-slate-300">Email address<input type="email" autoComplete="email" required value={email} onChange={(event) => setEmail(event.target.value)} className="mt-1.5 w-full rounded-lg bg-slate-950 border border-slate-700 px-3 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-400" /></label>
          <label className="block text-xs text-slate-300">Password<input type="password" autoComplete={mode === 'login' ? 'current-password' : 'new-password'} required minLength={12} maxLength={128} value={password} onChange={(event) => setPassword(event.target.value)} className="mt-1.5 w-full rounded-lg bg-slate-950 border border-slate-700 px-3 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-400" /><span className="block mt-1 text-[11px] text-slate-500">Use at least 12 characters.</span></label>
          {error && <p role="alert" className="text-xs text-rose-300">{error}</p>}
          <button type="submit" disabled={loading} className="w-full inline-flex justify-center items-center gap-2 rounded-lg bg-cyan-500 hover:bg-cyan-400 disabled:opacity-50 py-2.5 text-sm font-semibold text-slate-950"><LockKeyhole className="w-4 h-4" />{loading ? <Loader2 className="w-4 h-4 animate-spin" /> : mode === 'login' ? 'Sign in' : 'Create account'}</button>
        </form>
      </section>
    </main>
  );
}