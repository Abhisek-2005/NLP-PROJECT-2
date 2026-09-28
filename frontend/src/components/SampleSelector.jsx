import React from 'react';
import { X, Sparkles, Check, ArrowRight } from 'lucide-react';

export default function SampleSelector({ isOpen, onClose, samples = [], onSelectSample }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md transition-all">
      <div className="relative w-full max-w-3xl max-h-[85vh] glass-card rounded-2xl border border-slate-800 bg-slate-900/95 shadow-2xl flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">Pre-Loaded Role Presets</h3>
              <p className="text-xs text-slate-400">
                Instantly load real industry resumes and corresponding job descriptions for demo
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* List of sample roles */}
        <div className="flex-1 overflow-y-auto p-5 grid grid-cols-1 md:grid-cols-3 gap-4">
          {samples.map((sample) => (
            <div
              key={sample.id}
              className="rounded-xl bg-slate-950/60 border border-slate-800/90 hover:border-indigo-500/50 p-4 transition-all flex flex-col justify-between group hover:shadow-lg hover:shadow-indigo-500/10"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                    Sample
                  </span>
                </div>
                <h4 className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors mb-2">
                  {sample.role}
                </h4>
                <p className="text-xs text-slate-400 line-clamp-3 mb-3">
                  {sample.job_description.slice(0, 150)}...
                </p>
              </div>

              <button
                type="button"
                onClick={() => {
                  onSelectSample(sample);
                  onClose();
                }}
                className="w-full flex items-center justify-center gap-1.5 py-2 px-3 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md transition-all"
              >
                <span>Load This Role</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
