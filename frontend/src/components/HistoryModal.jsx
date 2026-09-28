import React, { useState } from 'react';
import { X, Trash2, Calendar, FileText, ArrowRight, AlertCircle, Clock } from 'lucide-react';

export default function HistoryModal({
  isOpen,
  onClose,
  history = [],
  onSelectAnalysis,
  onDeleteAnalysis,
  onClearAll,
}) {
  const [confirmClear, setConfirmClear] = useState(false);

  if (!isOpen) return null;

  const formatDate = (isoString) => {
    try {
      const date = new Date(isoString);
      return date.toLocaleDateString(undefined, {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return isoString || 'Recently';
    }
  };

  const getScoreBadge = (score) => {
    if (score >= 80) return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30';
    if (score >= 60) return 'text-amber-400 bg-amber-500/10 border-amber-500/30';
    return 'text-rose-400 bg-rose-500/10 border-rose-500/30';
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md transition-all">
      <div className="relative w-full max-w-2xl max-h-[85vh] glass-card rounded-2xl border border-slate-800 bg-slate-900/95 shadow-2xl flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center">
              <Clock className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">Analysis History</h3>
              <p className="text-xs text-slate-400">
                {history.length} persistent analysis records stored in SQLite
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            {history.length > 0 && !confirmClear && (
              <button
                type="button"
                onClick={() => setConfirmClear(true)}
                className="text-xs text-rose-400 hover:text-rose-300 px-2.5 py-1 rounded-lg border border-rose-500/20 hover:border-rose-500/40 transition-colors"
              >
                Clear All
              </button>
            )}

            {confirmClear && (
              <div className="flex items-center space-x-2">
                <span className="text-xs text-rose-400">Confirm?</span>
                <button
                  type="button"
                  onClick={() => {
                    onClearAll();
                    setConfirmClear(false);
                  }}
                  className="px-2 py-0.5 rounded bg-rose-600 text-white text-xs font-bold"
                >
                  Yes, Clear
                </button>
                <button
                  type="button"
                  onClick={() => setConfirmClear(false)}
                  className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-xs"
                >
                  Cancel
                </button>
              </div>
            )}

            <button
              onClick={onClose}
              className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content list */}
        <div className="flex-1 overflow-y-auto p-5 space-y-3">
          {history.length === 0 ? (
            <div className="text-center py-12">
              <FileText className="w-12 h-12 text-slate-600 mx-auto mb-3" />
              <p className="text-sm text-slate-300 font-medium">No previous analyses saved</p>
              <p className="text-xs text-slate-500 mt-1">
                Upload a resume and job description to perform your first match analysis.
              </p>
            </div>
          ) : (
            history.map((item) => (
              <div
                key={item.id}
                className="group p-4 rounded-xl bg-slate-950/50 hover:bg-slate-950/80 border border-slate-800 hover:border-indigo-500/40 transition-all flex items-center justify-between"
              >
                {/* Details */}
                <div
                  onClick={() => onSelectAnalysis(item.id)}
                  className="flex-1 cursor-pointer pr-4"
                >
                  <div className="flex items-center space-x-2 mb-1">
                    <span
                      className={`text-xs font-bold px-2 py-0.5 rounded-full border ${getScoreBadge(
                        item.overall_score
                      )}`}
                    >
                      {Math.round(item.overall_score)}% Match
                    </span>
                    <h4 className="text-sm font-semibold text-white group-hover:text-indigo-400 transition-colors">
                      {item.job_title || 'Target Role'}
                    </h4>
                  </div>
                  <div className="flex items-center space-x-3 text-xs text-slate-400 mt-1">
                    <span className="flex items-center gap-1">
                      <FileText className="w-3 h-3 text-slate-500" />
                      {item.resume_filename}
                    </span>
                    <span>•</span>
                    <span className="flex items-center gap-1 text-slate-400">
                      <Calendar className="w-3 h-3 text-slate-500" />
                      {formatDate(item.created_at)}
                    </span>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex items-center space-x-2">
                  <button
                    type="button"
                    onClick={() => onSelectAnalysis(item.id)}
                    className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-indigo-600/20 hover:bg-indigo-600/40 border border-indigo-500/30 text-indigo-300 text-xs font-medium transition-all"
                  >
                    <span>View</span>
                    <ArrowRight className="w-3 h-3" />
                  </button>
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteAnalysis(item.id);
                    }}
                    className="p-1.5 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
                    title="Delete record"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
