import React from 'react';
import { Target, BrainCircuit, Layers, Percent } from 'lucide-react';

export default function ScoreGauge({ scores, modelUsed, isFallback }) {
  if (!scores) return null;

  const {
    overall_score,
    semantic_score,
    skill_score,
    keyword_score,
    semantic_weight,
    skill_weight,
    keyword_weight,
  } = scores;

  // Determine color theme based on overall score
  let scoreColor = 'text-emerald-400';
  let strokeColor = '#10b981';
  let badgeBg = 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400';
  let ratingLabel = 'Excellent Match';
  let ratingSummary = 'Candidate profile demonstrates exceptional technical and contextual alignment with job expectations.';

  if (overall_score < 50) {
    scoreColor = 'text-rose-400';
    strokeColor = '#f43f5e';
    badgeBg = 'bg-rose-500/10 border-rose-500/30 text-rose-400';
    ratingLabel = 'Low Alignment';
    ratingSummary = 'Significant gaps identified in core technologies and domain phrasing. Tailoring strongly recommended.';
  } else if (overall_score < 72) {
    scoreColor = 'text-amber-400';
    strokeColor = '#f59e0b';
    badgeBg = 'bg-amber-500/10 border-amber-500/30 text-amber-400';
    ratingLabel = 'Moderate Match';
    ratingSummary = 'Good foundational match with a few key skill gaps. Adding highlighted keywords will boost ATS ranking.';
  } else if (overall_score < 85) {
    scoreColor = 'text-blue-400';
    strokeColor = '#3b82f6';
    badgeBg = 'bg-blue-500/10 border-blue-500/30 text-blue-400';
    ratingLabel = 'Strong Match';
    ratingSummary = 'Strong candidate alignment across core technologies and technical experience.';
  }

  // Circular gauge calculations
  const radius = 68;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (overall_score / 100) * circumference;

  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800 bg-slate-900/70 shadow-2xl relative overflow-hidden">
      {/* Background radial glow */}
      <div
        className="absolute -top-24 -left-24 w-72 h-72 rounded-full blur-3xl opacity-20 pointer-events-none"
        style={{ backgroundColor: strokeColor }}
      />

      <div className="flex flex-col lg:flex-row items-center gap-8 relative z-10">
        {/* Circular SVG Gauge */}
        <div className="flex flex-col items-center">
          <div className="relative w-44 h-44 flex items-center justify-center">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 160 160">
              {/* Background circle track */}
              <circle
                cx="80"
                cy="80"
                r={radius}
                stroke="#1e293b"
                strokeWidth="12"
                fill="transparent"
              />
              {/* Progress stroke */}
              <circle
                cx="80"
                cy="80"
                r={radius}
                stroke={strokeColor}
                strokeWidth="12"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round"
                fill="transparent"
                style={{
                  transition: 'stroke-dashoffset 1.2s cubic-bezier(0.4, 0, 0.2, 1)',
                }}
              />
            </svg>

            {/* Inner score number */}
            <div className="absolute flex flex-col items-center justify-center text-center">
              <span className={`text-4xl font-extrabold tracking-tight ${scoreColor}`}>
                {Math.round(overall_score)}
              </span>
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-widest mt-0.5">
                Out of 100
              </span>
            </div>
          </div>

          {/* Tier Badge */}
          <div className="mt-3 text-center">
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold border ${badgeBg}`}>
              {ratingLabel}
            </span>
          </div>
        </div>

        {/* Narrative & Metric Breakdown */}
        <div className="flex-1 w-full">
          <div className="mb-5">
            <h3 className="text-lg font-bold text-white mb-1">Composite Match Evaluation</h3>
            <p className="text-xs text-slate-300 leading-relaxed">{ratingSummary}</p>
          </div>

          {/* 3 Component Score Bars */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
            {/* 1. Semantic Similarity */}
            <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800">
              <div className="flex items-center justify-between text-xs mb-1.5">
                <span className="flex items-center gap-1.5 text-slate-300 font-medium">
                  <BrainCircuit className="w-3.5 h-3.5 text-indigo-400" />
                  Semantic Match
                </span>
                <span className="font-bold text-indigo-300">{semantic_score}%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden mb-1.5">
                <div
                  className="h-full bg-gradient-to-r from-indigo-600 to-indigo-400 rounded-full transition-all duration-1000"
                  style={{ width: `${semantic_score}%` }}
                />
              </div>
              <p className="text-[10px] text-slate-400">
                Weight: {Math.round(semantic_weight * 100)}% • Dense Embeddings
              </p>
            </div>

            {/* 2. Skills Match */}
            <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800">
              <div className="flex items-center justify-between text-xs mb-1.5">
                <span className="flex items-center gap-1.5 text-slate-300 font-medium">
                  <Target className="w-3.5 h-3.5 text-purple-400" />
                  Skill Coverage
                </span>
                <span className="font-bold text-purple-300">{skill_score}%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden mb-1.5">
                <div
                  className="h-full bg-gradient-to-r from-purple-600 to-purple-400 rounded-full transition-all duration-1000"
                  style={{ width: `${skill_score}%` }}
                />
              </div>
              <p className="text-[10px] text-slate-400">
                Weight: {Math.round(skill_weight * 100)}% • Taxonomy Matches
              </p>
            </div>

            {/* 3. Keyword Overlap */}
            <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800">
              <div className="flex items-center justify-between text-xs mb-1.5">
                <span className="flex items-center gap-1.5 text-slate-300 font-medium">
                  <Layers className="w-3.5 h-3.5 text-cyan-400" />
                  Keyword Overlap
                </span>
                <span className="font-bold text-cyan-300">{keyword_score}%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden mb-1.5">
                <div
                  className="h-full bg-gradient-to-r from-cyan-600 to-cyan-400 rounded-full transition-all duration-1000"
                  style={{ width: `${keyword_score}%` }}
                />
              </div>
              <p className="text-[10px] text-slate-400">
                Weight: {Math.round(keyword_weight * 100)}% • Lexical & Jaccard
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
