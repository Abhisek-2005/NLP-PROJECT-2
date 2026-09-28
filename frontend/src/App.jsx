import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import {
  Sparkles,
  Zap,
  ArrowRight,
  AlertCircle,
  FileSearch,
  CheckCircle2,
  RefreshCw,
} from 'lucide-react';
import Header from './components/Header';
import ResumeUploader from './components/ResumeUploader';
import JobDescriptionInput from './components/JobDescriptionInput';
import AnalysisDashboard from './components/AnalysisDashboard';
import HistoryModal from './components/HistoryModal';
import SampleSelector from './components/SampleSelector';
import { apiClient } from './services/api';

export default function App() {
  // Input states
  const [activeTab, setActiveTab] = useState('upload'); // 'upload' | 'paste'
  const [file, setFile] = useState(null);
  const [pastedText, setPastedText] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');

  // Execution & Data states
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisStep, setAnalysisStep] = useState(0);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);

  // App Meta states
  const [health, setHealth] = useState(null);
  const [samples, setSamples] = useState([]);
  const [history, setHistory] = useState([]);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const [isSamplesOpen, setIsSamplesOpen] = useState(false);

  // Initial load
  useEffect(() => {
    loadAppMeta();
  }, []);

  const loadAppMeta = async () => {
    try {
      const [hData, sData, histData] = await Promise.all([
        apiClient.getHealth().catch(() => null),
        apiClient.getSamples().catch(() => []),
        apiClient.getHistory().catch(() => []),
      ]);
      if (hData) setHealth(hData);
      if (sData) setSamples(sData);
      if (histData) setHistory(histData);
    } catch (err) {
      console.error('Failed to load application metadata:', err);
    }
  };

  const handleSelectSample = (sample) => {
    setActiveTab('paste');
    setPastedText(sample.resume_text);
    setJobTitle(sample.job_title);
    setJobDescription(sample.job_description);
    setFile(null);
    setError(null);
  };

  const handleStartAnalysis = async (e) => {
    e.preventDefault();
    setError(null);

    // Validation
    if (activeTab === 'upload' && !file) {
      setError('Please choose a PDF, DOCX, or TXT resume file to upload.');
      return;
    }
    if (activeTab === 'paste' && (!pastedText || pastedText.trim().length < 20)) {
      setError('Please paste your resume text (minimum 20 characters).');
      return;
    }
    if (!jobDescription || jobDescription.trim().length < 20) {
      setError('Please enter or paste the target job description (minimum 20 characters).');
      return;
    }

    setIsAnalyzing(true);
    setAnalysisStep(1);

    // Step cycle simulator for rich UX
    const stepInterval = setInterval(() => {
      setAnalysisStep((prev) => (prev < 4 ? prev + 1 : prev));
    }, 700);

    try {
      let result;
      if (activeTab === 'upload') {
        result = await apiClient.analyzeFile(file, jobDescription, jobTitle || 'Target Role');
      } else {
        result = await apiClient.analyzeText(
          pastedText,
          jobDescription,
          jobTitle || 'Target Role',
          'Pasted_Resume.txt'
        );
      }

      clearInterval(stepInterval);
      setAnalysisResult(result);

      // Trigger confetti if high match
      if (result.scores && result.scores.overall_score >= 75) {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 },
          colors: ['#6366f1', '#a855f7', '#10b981', '#38bdf8'],
        });
      }

      // Refresh history
      apiClient.getHistory().then(setHistory).catch(() => {});
    } catch (err) {
      clearInterval(stepInterval);
      setError(err.message || 'Analysis encountered an error. Please verify input documents.');
    } finally {
      setIsAnalyzing(false);
      setAnalysisStep(0);
    }
  };

  const handleSelectHistoryItem = async (id) => {
    try {
      const fullDetail = await apiClient.getHistoryItem(id);
      setAnalysisResult(fullDetail);
      setIsHistoryOpen(false);
    } catch (err) {
      setError('Failed to load past analysis details.');
    }
  };

  const handleDeleteHistoryItem = async (id) => {
    try {
      await apiClient.deleteHistoryItem(id);
      setHistory((prev) => prev.filter((item) => item.id !== id));
      if (analysisResult && analysisResult.id === id) {
        setAnalysisResult(null);
      }
    } catch (err) {
      setError('Failed to delete history item.');
    }
  };

  const handleClearAllHistory = async () => {
    try {
      await apiClient.clearAllHistory();
      setHistory([]);
    } catch (err) {
      setError('Failed to clear history.');
    }
  };

  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white relative bg-radial-glow">
      {/* Top Navbar Header */}
      <Header
        health={health}
        onOpenHistory={() => setIsHistoryOpen(true)}
        historyCount={history.length}
        onOpenSamples={() => setIsSamplesOpen(true)}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error Banner */}
        {error && (
          <div className="mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-between text-xs text-rose-300 animate-fadeIn">
            <div className="flex items-center space-x-2">
              <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
              <span>{error}</span>
            </div>
            <button
              onClick={() => setError(null)}
              className="text-slate-400 hover:text-white underline ml-4"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Dashboard or Input Workspace */}
        {analysisResult ? (
          <AnalysisDashboard
            result={analysisResult}
            onReset={() => {
              setAnalysisResult(null);
              setError(null);
            }}
          />
        ) : (
          <div className="space-y-8 animate-fadeIn">
            {/* Hero Section */}
            <div className="text-center max-w-3xl mx-auto pt-4 pb-2">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-xs font-semibold mb-4">
                <Sparkles className="w-3.5 h-3.5" />
                <span>Next-Gen Semantic Resume Screening</span>
              </div>
              <h2 className="text-3xl sm:text-5xl font-black text-white tracking-tight leading-tight">
                AI Resume–Job Description <br className="hidden sm:block" />
                <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                  Matching Engine
                </span>
              </h2>
              <p className="mt-3 text-sm sm:text-base text-slate-400 max-w-2xl mx-auto leading-relaxed">
                Extract technical skills, compute semantic sentence embeddings using Sentence
                Transformers, analyze keyword coverage, and receive prescriptive ATS optimization feedback.
              </p>
            </div>

            {/* Input Form Grid */}
            <form onSubmit={handleStartAnalysis} className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 min-h-[420px]">
                {/* 1. Resume Uploader Card */}
                <ResumeUploader
                  file={file}
                  setFile={setFile}
                  pastedText={pastedText}
                  setPastedText={setPastedText}
                  activeTab={activeTab}
                  setActiveTab={setActiveTab}
                />

                {/* 2. Job Description Input Card */}
                <JobDescriptionInput
                  jobTitle={jobTitle}
                  setJobTitle={setJobTitle}
                  jobDescription={jobDescription}
                  setJobDescription={setJobDescription}
                />
              </div>

              {/* Submit Action & Loading Progress */}
              <div className="flex flex-col items-center justify-center pt-2">
                {!isAnalyzing ? (
                  <button
                    type="submit"
                    className="group relative flex items-center space-x-3 px-8 py-4 rounded-2xl bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-base shadow-xl shadow-indigo-600/30 hover:shadow-indigo-600/50 hover:scale-[1.02] active:scale-[0.98] transition-all cursor-pointer ring-1 ring-white/20"
                  >
                    <Zap className="w-5 h-5 text-amber-300 animate-pulse" />
                    <span>Run NLP Match Analysis</span>
                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  </button>
                ) : (
                  <div className="glass-card rounded-2xl p-6 border border-indigo-500/40 bg-indigo-950/40 w-full max-w-md shadow-2xl flex flex-col items-center text-center">
                    <RefreshCw className="w-8 h-8 text-indigo-400 animate-spin mb-3" />
                    <h4 className="text-sm font-bold text-white mb-1">
                      Executing NLP Pipeline...
                    </h4>
                    <p className="text-xs text-indigo-200/80 mb-4">
                      {analysisStep === 1 && '1. Extracting text from document via PyMuPDF/DOCX...'}
                      {analysisStep === 2 && '2. Scanning against 100+ skill taxonomy terms...'}
                      {analysisStep === 3 && '3. Generating Sentence Transformer embeddings...'}
                      {analysisStep >= 4 && '4. Synthesizing weighted match score & feedback...'}
                    </p>
                    <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-indigo-500 to-purple-500 h-full rounded-full transition-all duration-500"
                        style={{ width: `${analysisStep * 25}%` }}
                      />
                    </div>
                  </div>
                )}

                <div className="mt-4 flex items-center gap-4 text-xs text-slate-500">
                  <span className="flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                    Real Transformer Embeddings
                  </span>
                  <span>•</span>
                  <span className="flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                    Automated SQLite Persistence
                  </span>
                  <span>•</span>
                  <span className="flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                    ATS Optimization
                  </span>
                </div>
              </div>
            </form>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="w-full border-t border-slate-800/80 bg-slate-950/60 py-6 mt-12 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p>Resume–Job Description Matching Using NLP • Production Full-Stack Pipeline</p>
          <div className="flex items-center space-x-3 text-slate-400 text-[11px]">
            <span>FastAPI</span>
            <span>•</span>
            <span>Sentence-Transformers</span>
            <span>•</span>
            <span>PyMuPDF</span>
            <span>•</span>
            <span>React</span>
            <span>•</span>
            <span>Tailwind CSS</span>
            <span>•</span>
            <span>SQLite</span>
          </div>
        </div>
      </footer>

      {/* History Slide-over Modal */}
      <HistoryModal
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        history={history}
        onSelectAnalysis={handleSelectHistoryItem}
        onDeleteAnalysis={handleDeleteHistoryItem}
        onClearAll={handleClearAllHistory}
      />

      {/* Samples Selector Modal */}
      <SampleSelector
        isOpen={isSamplesOpen}
        onClose={() => setIsSamplesOpen(false)}
        samples={samples}
        onSelectSample={handleSelectSample}
      />
    </div>
  );
}
