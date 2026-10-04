import React, { useState } from 'react';
import { Key, ExternalLink, X, Check } from 'lucide-react';

export default function ApiKeyModal({ isOpen, onClose, currentKey, onSaveKey, currentSearchKeys, onSaveSearchKeys }) {
  const [apiKey, setApiKey] = useState(currentKey || '');
  const [tavilyKey, setTavilyKey] = useState(currentSearchKeys?.tavily || '');
  const [serperKey, setSerperKey] = useState(currentSearchKeys?.serper || '');
  const [saved, setSaved] = useState(false);

  if (!isOpen) return null;

  const handleSave = () => {
    onSaveKey(apiKey.trim());
    onSaveSearchKeys({ tavily: tavilyKey.trim(), serper: serperKey.trim() });
    setSaved(true);
    setTimeout(() => {
      setSaved(false);
      onClose();
    }, 800);
  };

  const handleClear = () => {
    setApiKey('');
    setTavilyKey('');
    setSerperKey('');
    onSaveKey('');
    onSaveSearchKeys({ tavily: '', serper: '' });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-md p-6 shadow-2xl relative text-slate-100 max-h-[90vh] overflow-y-auto">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center space-x-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
            <Key className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-semibold text-white">API Keys</h3>
            <p className="text-xs text-slate-400">Optional: Use your own keys for live AI analysis and wider job search</p>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">
              Gemini API Key
            </label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="AIzaSy..."
              className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all font-mono"
            />
          </div>

          <div className="p-3 rounded-xl bg-indigo-950/40 border border-indigo-800/40 text-xs text-slate-300 space-y-1.5">
            <p className="font-medium text-indigo-300">💡 No key? No problem!</p>
            <p className="text-slate-400">
              The platform automatically provides high-fidelity analysis even without an API key for demo & evaluation.
            </p>
            <a
              href="https://aistudio.google.com/app/apikey"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-1 text-indigo-400 hover:text-indigo-300 underline font-medium pt-1"
            >
              <span>Get a free Gemini API key from Google AI Studio</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>

          <div className="pt-3 border-t border-slate-800 space-y-3">
            <div>
              <p className="text-xs font-medium text-slate-300">Job Search Sources</p>
              <p className="text-xs text-slate-400 mt-0.5">
                Remotive and Arbeitnow work without a key. Add either key below to search the web for roles matching your CV skills too.
              </p>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">
                Tavily API Key
              </label>
              <input
                type="password"
                value={tavilyKey}
                onChange={(e) => setTavilyKey(e.target.value)}
                placeholder="tvly-..."
                className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all font-mono"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">
                Serper API Key
              </label>
              <input
                type="password"
                value={serperKey}
                onChange={(e) => setSerperKey(e.target.value)}
                placeholder="Serper key"
                className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all font-mono"
              />
            </div>
          </div>

          <div className="flex items-center justify-between pt-2">
            {apiKey || tavilyKey || serperKey ? (
              <button
                onClick={handleClear}
                className="text-xs text-red-400 hover:text-red-300 hover:underline"
              >
                Clear Keys
              </button>
            ) : <div />}

            <div className="flex space-x-2">
              <button
                onClick={onClose}
                className="px-4 py-2 text-xs font-medium text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-xl transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                className="flex items-center space-x-1.5 px-4 py-2 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 rounded-xl transition-all shadow-lg shadow-indigo-600/30"
              >
                {saved ? (
                  <>
                    <Check className="w-4 h-4 text-emerald-300" />
                    <span>Saved!</span>
                  </>
                ) : (
                  <span>Save Keys</span>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
