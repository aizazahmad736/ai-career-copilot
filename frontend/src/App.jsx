import React, { useState, useEffect, useRef } from 'react';
import Navbar from './components/Navbar';
import ApiKeyModal from './components/ApiKeyModal';
import TargetRoleSelector from './components/TargetRoleSelector';
import FileUpload from './components/FileUpload';
import MatchScoreGauge from './components/MatchScoreGauge';
import AnalysisOverview from './components/AnalysisOverview';
import ExtractedSkillsView from './components/ExtractedSkillsView';
import SkillGapMatrix from './components/SkillGapMatrix';
import ATSFeedbackView from './components/ATSFeedbackView';
import RecommendationsView from './components/RecommendationsView';
import JobMatchesView from './components/JobMatchesView';
import PhaseRoadmapModal from './components/PhaseRoadmapModal';
import { getSupportedRoles, checkBackendHealth, analyzeCV, analyzeSampleCV } from './services/api';
import { RefreshCw, Sparkles, FileText, ChevronRight, CheckCircle2, AlertCircle } from 'lucide-react';

export default function App() {
  const [backendOnline, setBackendOnline] = useState(false);
  const [roles, setRoles] = useState([
    { name: 'Junior Full Stack Developer' },
    { name: 'Frontend Developer' },
    { name: 'Backend Developer' },
    { name: 'AI / Machine Learning Engineer' },
    { name: 'Data Scientist / Data Analyst' },
    { name: 'DevOps / Cloud Engineer' },
  ]);

  const [selectedRole, setSelectedRole] = useState('Junior Full Stack Developer');
  const [experienceLevel, setExperienceLevel] = useState('Entry-Level / Junior');
  const [jobDescription, setJobDescription] = useState('');
  const [file, setFile] = useState(null);

  const [customApiKey, setCustomApiKey] = useState(() => {
    return localStorage.getItem('career_copilot_gemini_key') || '';
  });

  const [isApiKeyModalOpen, setIsApiKeyModalOpen] = useState(false);
  const [isRoadmapModalOpen, setIsRoadmapModalOpen] = useState(false);

  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState('');
  const [error, setError] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);

  const resultsRef = useRef(null);

  useEffect(() => {
    async function init() {
      const health = await checkBackendHealth();
      if (health) {
        setBackendOnline(true);
      }
      const fetchedRoles = await getSupportedRoles();
      if (fetchedRoles && fetchedRoles.length > 0) {
        setRoles(fetchedRoles);
      }
    }
    init();
  }, []);

  const handleSaveApiKey = (key) => {
    setCustomApiKey(key);
    if (key) {
      localStorage.setItem('career_copilot_gemini_key', key);
    } else {
      localStorage.removeItem('career_copilot_gemini_key');
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setError(null);
    setLoading(true);

    try {
      setLoadingStep('Step 1/4: Parsing document text & structure...');
      await new Promise((r) => setTimeout(r, 600));

      setLoadingStep('Step 2/4: Gemini AI extracting candidate competencies...');
      await new Promise((r) => setTimeout(r, 600));

      setLoadingStep('Step 3/4: Benchmarking against industry role criteria...');
      
      const res = await analyzeCV({
        file,
        targetRole: selectedRole,
        experienceLevel,
        jobDescription: jobDescription.trim() || undefined,
        customApiKey: customApiKey || undefined,
      });

      setLoadingStep('Step 4/4: Finalizing skill gap matrix & recommendations...');
      await new Promise((r) => setTimeout(r, 400));

      setAnalysisResult(res);
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 200);
    } catch (err) {
      console.error(err);
      setError(err.message || 'An error occurred while analyzing the CV.');
    } finally {
      setLoading(false);
      setLoadingStep('');
    }
  };

  const handleTrySample = async () => {
    setError(null);
    setLoading(true);
    setLoadingStep('Loading sample student resume & benchmarking...');

    try {
      const res = await analyzeSampleCV({
        targetRole: selectedRole,
        experienceLevel,
        customApiKey: customApiKey || undefined,
      });
      setAnalysisResult(res);
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 200);
    } catch (err) {
      console.error(err);
      setError(err.message || 'Failed to load sample resume analysis.');
    } finally {
      setLoading(false);
      setLoadingStep('');
    }
  };

  const handleReset = () => {
    setAnalysisResult(null);
    setFile(null);
    setError(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 selection:bg-indigo-500 selection:text-white pb-20">
      <Navbar
        onOpenApiKeyModal={() => setIsApiKeyModalOpen(true)}
        hasCustomKey={Boolean(customApiKey)}
        backendOnline={backendOnline}
      />

      <ApiKeyModal
        isOpen={isApiKeyModalOpen}
        onClose={() => setIsApiKeyModalOpen(false)}
        currentKey={customApiKey}
        onSaveKey={handleSaveApiKey}
      />

      <PhaseRoadmapModal
        isOpen={isRoadmapModalOpen}
        onClose={() => setIsRoadmapModalOpen(false)}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 space-y-8">
        {/* Hero Banner */}
        <section className="text-center max-w-3xl mx-auto space-y-3 pt-4">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-xs font-semibold text-indigo-400">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Career Copilot • Phase 2</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight">
            Go From <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-blue-400 to-cyan-400">CV to Skills</span> to Career Success
          </h1>
          <p className="text-sm sm:text-base text-slate-400 max-w-2xl mx-auto leading-relaxed">
            Upload your resume to extract competencies, benchmark against industry roles, discover exact skill gaps, and find live job listings ranked by how well they fit you.
          </p>
        </section>

        {/* Error Alert */}
        {error && (
          <div className="p-4 rounded-xl bg-rose-950/40 border border-rose-800/60 text-rose-300 text-xs flex items-center space-x-2.5 max-w-3xl mx-auto">
            <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-400" />
            <span className="flex-1">{error}</span>
            <button onClick={() => setError(null)} className="text-rose-400 hover:text-white font-bold ml-2">
              ✕
            </button>
          </div>
        )}

        {/* Input Configuration Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 max-w-6xl mx-auto">
          <TargetRoleSelector
            roles={roles}
            selectedRole={selectedRole}
            onSelectRole={setSelectedRole}
            experienceLevel={experienceLevel}
            onSelectExperienceLevel={setExperienceLevel}
            jobDescription={jobDescription}
            onChangeJobDescription={setJobDescription}
          />

          <FileUpload
            file={file}
            onFileChange={setFile}
            onAnalyze={handleAnalyze}
            onTrySample={handleTrySample}
            loading={loading}
            loadingStep={loadingStep}
          />
        </div>

        {/* Results Section */}
        {analysisResult && (
          <div ref={resultsRef} className="space-y-8 pt-8 animate-in fade-in slide-in-from-bottom-6 duration-500 max-w-6xl mx-auto">
            {/* Header / Reset Bar */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-xl bg-slate-900/60 border border-slate-800">
              <div className="flex items-center space-x-2.5">
                <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                <div>
                  <h3 className="text-sm font-semibold text-white">
                    Analysis Complete for {analysisResult.candidate_name || 'Candidate'}
                  </h3>
                  <p className="text-xs text-slate-400">
                    Target Role: <strong className="text-indigo-300">{analysisResult.target_role}</strong> ({analysisResult.experience_level})
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <button
                  onClick={handleReset}
                  className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-200 transition-colors"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                  <span>Analyze Another CV</span>
                </button>
              </div>
            </div>

            {/* Match Score Gauge */}
            <MatchScoreGauge
              score={analysisResult.match_score}
              matchedCount={analysisResult.matched_skills?.length || 0}
              partialCount={analysisResult.partial_skills?.length || 0}
              missingCount={analysisResult.missing_critical_skills?.length || 0}
              bonusCount={analysisResult.bonus_skills?.length || 0}
              targetRole={analysisResult.target_role}
            />

            {/* Candidate Overview */}
            <AnalysisOverview
              parsedResume={analysisResult.parsed_resume}
              headline={analysisResult.headline}
              summary={analysisResult.summary}
            />

            {/* Extracted Skills Inventory */}
            <ExtractedSkillsView
              skills={analysisResult.parsed_resume?.skills}
            />

            {/* Skill Gap Matrix */}
            <SkillGapMatrix
              matched={analysisResult.matched_skills || []}
              partial={analysisResult.partial_skills || []}
              missing={analysisResult.missing_critical_skills || []}
              bonus={analysisResult.bonus_skills || []}
              targetRole={analysisResult.target_role}
            />

            {/* ATS Feedback & Bullet Optimization */}
            <ATSFeedbackView
              atsFeedback={analysisResult.ats_feedback}
            />

            {/* Actionable Recommendations */}
            <RecommendationsView
              recommendations={analysisResult.recommendations || []}
              onNextPhase={() => setIsRoadmapModalOpen(true)}
            />

            {/* Phase 2: Job Search & Matching */}
            <JobMatchesView
              key={`${analysisResult.id}-${analysisResult.target_role}`}
              skills={analysisResult.parsed_resume?.skills}
              targetRole={analysisResult.target_role}
              experienceLevel={analysisResult.experience_level}
              analysisId={analysisResult.id === 999 ? undefined : analysisResult.id}
            />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 text-center text-xs text-slate-500">
        <p>AI Career Copilot • Phase 2 (CV Upload → Parsing → AI Analysis → Skill Gap → Job Search → Job Matching)</p>
      </footer>
    </div>
  );
}
