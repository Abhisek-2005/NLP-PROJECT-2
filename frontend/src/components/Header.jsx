import React from 'react';
import { Sparkles, History, Cpu, FileText, CheckCircle2, AlertCircle } from 'lucide-react';

export default function Header({ health, onOpenHistory, historyCount, onOpenSamples }) {
  return (
    <header className="sticky top-0 z-40 w-full glass-panel border-b border-slate-800 bg-slate-950/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        {/* Brand & Title */}
        <div className="flex items-center space-x-3.5">
          <div className="w-11 h-11 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-indigo-500/25 ring-1 ring-white/20">
            <Sparkles className="w-6 h-6 text-white animate-pulse" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
                Resume–Job Matching <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">AI / NLP</span>
              </h1>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">
              Dense Semantic Embeddings • Skill Taxonomy Extraction • Actionable ATS Insights
            </p>
          </div>
        </div>

        {/* Right Actions */}
        <div className="flex items-center space-x-3">
          {/* NLP Model Status Pill */}
          {health && (
            <div className="hidden md:flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-900/90 border border-slate-800 text-xs">
              <Cpu className="w-3.5 h-3.5 text-indigo-400" />
              <span className="text-slate-300 font-medium">Model:</span>
              {health.is_fallback ? (
                <span className="flex items-center text-amber-400 font-medium gap-1">
                  <AlertCircle className="w-3 h-3" /> TF-IDF (Fallback)
                </span>
              ) : (
                <span className="flex items-center text-emerald-400 font-medium gap-1">
                  <CheckCircle2 className="w-3 h-3" /> Sentence-Transformers
                </span>
              )}
            </div>
          )}

          {/* Quick Samples Button */}
          <button
            onClick={onOpenSamples}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700/60 text-xs font-medium text-slate-200 transition-all shadow-sm hover:border-slate-600"
          >
            <FileText className="w-3.5 h-3.5 text-indigo-400" />
            <span>Load Samples</span>
          </button>

          {/* History Button */}
          <button
            onClick={onOpenHistory}
            className="relative flex items-center space-x-2 px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-indigo-600/90 to-purple-600/90 hover:from-indigo-500 hover:to-purple-500 text-xs font-semibold text-white shadow-md shadow-indigo-600/20 transition-all"
          >
            <History className="w-3.5 h-3.5" />
            <span>History</span>
            {historyCount > 0 && (
              <span className="ml-1 px-1.5 py-0.2 rounded-full bg-white/20 text-[10px] font-bold">
                {historyCount}
              </span>
            )}
          </button>
        </div>
      </div>
    </header>
  );
}
