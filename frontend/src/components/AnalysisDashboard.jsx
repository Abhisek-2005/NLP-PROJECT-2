import React, { useState } from 'react';
import {
  Printer,
  RotateCcw,
  FileText,
  Briefcase,
  Layers,
  Sparkles,
  ChevronDown,
  ChevronUp,
  Cpu,
  Info,
} from 'lucide-react';
import ScoreGauge from './ScoreGauge';
import SkillsComparison from './SkillsComparison';
import RecommendationsView from './RecommendationsView';

export default function AnalysisDashboard({ result, onReset }) {
  const [showPreviews, setShowPreviews] = useState(false);

  if (!result) return null;

  const {
    resume_filename,
    job_title,
    scores,
    matched_skills,
    missing_skills,
    recommendations,
    model_used,
    is_fallback,
    fallback_reason,
    text_stats,
    resume_preview,
    job_preview,
  } = result;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Top Banner & Control Bar */}
      <div className="glass-card rounded-2xl p-6 border border-slate-800 bg-slate-900/80 shadow-2xl flex flex-col md:flex-row md:items-center justify-between gap-5">
        <div>
          <div className="flex items-center space-x-2 text-indigo-400 text-xs font-semibold mb-1">
            <Sparkles className="w-4 h-4" />
            <span>ANALYSIS REPORT GENERATED</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-white tracking-tight">
            {job_title || 'Target Role Analysis'}
          </h2>
          <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400 mt-2">
            <span className="flex items-center gap-1">
              <FileText className="w-3.5 h-3.5 text-slate-500" />
              {resume_filename}
            </span>
            <span>•</span>
            <span className="flex items-center gap-1 text-slate-300">
              <Cpu className="w-3.5 h-3.5 text-indigo-400" />
              {model_used}
            </span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center space-x-3">
          <button
            onClick={handlePrint}
            className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 text-xs font-semibold text-slate-200 transition-all shadow-sm"
          >
            <Printer className="w-4 h-4 text-slate-400" />
            <span>Export / Print</span>
          </button>

          <button
            onClick={onReset}
            className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-xs font-semibold text-white transition-all shadow-md shadow-indigo-600/25"
          >
            <RotateCcw className="w-4 h-4" />
            <span>New Analysis</span>
          </button>
        </div>
      </div>

      {/* Fallback Notice if triggered */}
      {is_fallback && (
        <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-start space-x-3 text-xs text-amber-200">
          <Info className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold text-amber-300">NLP Fallback Active: </span>
            {fallback_reason ||
              'Sentence Transformers could not be initialized. The system seamlessly used TF-IDF N-gram Cosine Similarity.'}
          </div>
        </div>
      )}

      {/* Quick Statistics Strip */}
      {text_stats && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
            <span className="text-xs text-slate-400 block mb-0.5">Resume Length</span>
            <span className="text-base font-bold text-white">{text_stats.resume_word_count}</span>
            <span className="text-[10px] text-slate-500 block">words</span>
          </div>
          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
            <span className="text-xs text-slate-400 block mb-0.5">Job Description</span>
            <span className="text-base font-bold text-white">{text_stats.job_word_count}</span>
            <span className="text-[10px] text-slate-500 block">words</span>
          </div>
          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
            <span className="text-xs text-slate-400 block mb-0.5">Vocabulary Overlap</span>
            <span className="text-base font-bold text-cyan-400">
              {text_stats.common_keywords_count}
            </span>
            <span className="text-[10px] text-slate-500 block">shared unique terms</span>
          </div>
          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
            <span className="text-xs text-slate-400 block mb-0.5">Skills Extracted</span>
            <span className="text-base font-bold text-purple-400">
              {text_stats.total_skills_detected_resume} / {text_stats.total_skills_detected_job}
            </span>
            <span className="text-[10px] text-slate-500 block">candidate vs target</span>
          </div>
        </div>
      )}

      {/* 1. Score Gauge Component */}
      <ScoreGauge scores={scores} modelUsed={model_used} isFallback={is_fallback} />

      {/* 2. Skills Comparison Component */}
      <SkillsComparison matchedSkills={matched_skills} missingSkills={missing_skills} />

      {/* 3. Targeted Recommendations Component */}
      <RecommendationsView recommendations={recommendations} />

      {/* Collapsible Source Previews */}
      <div className="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/50">
        <button
          type="button"
          onClick={() => setShowPreviews(!showPreviews)}
          className="w-full flex items-center justify-between text-xs font-semibold text-slate-300 hover:text-white transition-colors"
        >
          <span className="flex items-center gap-2">
            <FileText className="w-4 h-4 text-indigo-400" />
            <span>Extracted Document Text Previews</span>
          </span>
          {showPreviews ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>

        {showPreviews && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 pt-4 border-t border-slate-800 text-xs">
            <div>
              <h5 className="font-semibold text-slate-300 mb-1.5 flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5 text-slate-500" /> Extracted Resume Snippet
              </h5>
              <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-850 font-mono text-[11px] text-slate-400 max-h-48 overflow-y-auto leading-relaxed">
                {resume_preview || 'No preview available.'}
              </div>
            </div>

            <div>
              <h5 className="font-semibold text-slate-300 mb-1.5 flex items-center gap-1.5">
                <Briefcase className="w-3.5 h-3.5 text-slate-500" /> Job Description Snippet
              </h5>
              <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-850 font-mono text-[11px] text-slate-400 max-h-48 overflow-y-auto leading-relaxed">
                {job_preview || 'No preview available.'}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
