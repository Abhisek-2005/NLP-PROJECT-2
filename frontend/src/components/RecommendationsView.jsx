import React from 'react';
import { Lightbulb, AlertTriangle, ArrowUpRight, TrendingUp, CheckSquare, Layers } from 'lucide-react';

export default function RecommendationsView({ recommendations = [] }) {
  if (!recommendations || recommendations.length === 0) return null;

  const getPriorityStyle = (priority) => {
    switch (priority) {
      case 'high':
        return {
          badge: 'bg-rose-500/15 border-rose-500/30 text-rose-300',
          border: 'border-rose-900/30 hover:border-rose-500/50',
          icon: <AlertTriangle className="w-4 h-4 text-rose-400" />,
        };
      case 'medium':
        return {
          badge: 'bg-amber-500/15 border-amber-500/30 text-amber-300',
          border: 'border-amber-900/30 hover:border-amber-500/50',
          icon: <Lightbulb className="w-4 h-4 text-amber-400" />,
        };
      default:
        return {
          badge: 'bg-blue-500/15 border-blue-500/30 text-blue-300',
          border: 'border-blue-900/30 hover:border-blue-500/50',
          icon: <CheckSquare className="w-4 h-4 text-blue-400" />,
        };
    }
  };

  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800 bg-slate-900/60 shadow-xl">
      <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-5">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-amber-400" />
            <span>Targeted Optimization Recommendations</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Prescriptive changes to optimize your resume for recruiters and ATS screening algorithms
          </p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
          {recommendations.length} Action Items
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {recommendations.map((rec) => {
          const style = getPriorityStyle(rec.priority);

          return (
            <div
              key={rec.id}
              className={`rounded-xl bg-slate-950/60 p-4.5 border transition-all flex flex-col justify-between ${style.border}`}
            >
              <div>
                {/* Header with Category & Priority */}
                <div className="flex items-center justify-between gap-2 mb-2.5">
                  <div className="flex items-center space-x-1.5">
                    {style.icon}
                    <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider text-[11px]">
                      {rec.category}
                    </span>
                  </div>

                  <div className="flex items-center space-x-1.5">
                    <span
                      className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border ${style.badge}`}
                    >
                      {rec.priority} Priority
                    </span>
                    {rec.impact && (
                      <span className="flex items-center text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                        <TrendingUp className="w-2.5 h-2.5 mr-1" />
                        {rec.impact}
                      </span>
                    )}
                  </div>
                </div>

                {/* Title */}
                <h4 className="text-sm font-semibold text-white mb-2 leading-snug">{rec.title}</h4>

                {/* Message */}
                <p className="text-xs text-slate-300 leading-relaxed">{rec.message}</p>
              </div>

              {/* Action Hint Footer */}
              <div className="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
                <span>Resume enhancement strategy</span>
                <span className="text-indigo-400 flex items-center font-medium">
                  Review & Apply <ArrowUpRight className="w-3 h-3 ml-0.5" />
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
