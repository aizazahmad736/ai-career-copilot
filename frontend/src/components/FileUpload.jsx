import React, { useState, useRef } from 'react';
import { UploadCloud, File, X, Sparkles, CheckCircle2, ArrowRight, Loader2 } from 'lucide-react';

export default function FileUpload({
  file,
  onFileChange,
  onAnalyze,
  onTrySample,
  loading,
  loadingStep
}) {
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0];
      validateAndSetFile(droppedFile);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (selectedFile) => {
    const validExtensions = ['pdf', 'docx', 'doc', 'txt'];
    const ext = selectedFile.name.split('.').pop().toLowerCase();
    if (!validExtensions.includes(ext)) {
      alert('Please upload a PDF, DOCX, or TXT file.');
      return;
    }
    if (selectedFile.size > 10 * 1024 * 1024) {
      alert('File size exceeds 10MB limit.');
      return;
    }
    onFileChange(selectedFile);
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800/90 rounded-2xl p-6 shadow-xl space-y-5">
      <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
        <div className="flex items-center space-x-2.5">
          <UploadCloud className="w-5 h-5 text-indigo-400" />
          <h2 className="text-base font-semibold text-white tracking-tight">
            Step 2: Upload Resume / CV
          </h2>
        </div>

        <button
          type="button"
          onClick={onTrySample}
          disabled={loading}
          className="text-xs text-indigo-400 hover:text-indigo-300 font-medium flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-indigo-500/10 border border-indigo-500/20 hover:bg-indigo-500/20 transition-colors disabled:opacity-50"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>Try with Sample Resume</span>
        </button>
      </div>

      {/* Drop Zone */}
      {!file ? (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all ${
            dragOver
              ? 'border-indigo-500 bg-indigo-500/10 scale-[0.99]'
              : 'border-slate-800 hover:border-slate-700 bg-slate-950/50 hover:bg-slate-950'
          }`}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.docx,.doc,.txt"
            onChange={handleFileInput}
            className="hidden"
          />
          <div className="w-14 h-14 mx-auto rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-4 shadow-inner">
            <UploadCloud className="w-7 h-7" />
          </div>
          <h3 className="text-sm font-semibold text-white mb-1">
            Click to browse or drag & drop your CV
          </h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto mb-3">
            Supports PDF, DOCX, and TXT (Max 10MB). Text is extracted securely and evaluated directly.
          </p>
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-800/80 border border-slate-700/60 text-[11px] text-slate-300">
            <span>📄 ATS-Compliant PDF / Word supported</span>
          </div>
        </div>
      ) : (
        /* Selected File Card */
        <div className="p-4 rounded-xl bg-slate-950 border border-indigo-500/30 flex items-center justify-between">
          <div className="flex items-center space-x-3.5 min-w-0">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 flex-shrink-0">
              <File className="w-5 h-5" />
            </div>
            <div className="min-w-0">
              <p className="text-sm font-medium text-white truncate">{file.name}</p>
              <p className="text-xs text-slate-400">{formatFileSize(file.size)}</p>
            </div>
          </div>

          <button
            type="button"
            onClick={() => onFileChange(null)}
            disabled={loading}
            className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Action / Analyze Button */}
      <div>
        <button
          type="button"
          onClick={onAnalyze}
          disabled={loading || !file}
          className={`w-full py-3.5 px-6 rounded-xl font-semibold text-sm flex items-center justify-center space-x-2 transition-all shadow-xl ${
            loading || !file
              ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700/50'
              : 'bg-gradient-to-r from-indigo-600 via-indigo-500 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white shadow-indigo-600/30 hover:shadow-indigo-600/50 scale-[1.0]'
          }`}
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin text-indigo-300" />
              <span>{loadingStep || 'AI is analyzing your resume...'}</span>
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4 text-indigo-200" />
              <span>Analyze CV & Generate Skill Gap</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>

        {loading && (
          <div className="mt-3 text-center">
            <p className="text-xs text-slate-400 animate-pulse">
              Parsing sections, evaluating competencies, and calculating match readiness...
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
