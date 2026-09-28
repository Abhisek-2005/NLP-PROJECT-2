import React, { useState } from 'react';
import { CheckCircle2, XCircle, Search, Filter, Copy, Check } from 'lucide-react';

export default function SkillsComparison({ matchedSkills = [], missingSkills = [] }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [copied, setCopied] = useState(false);

  // Extract unique categories
  const categories = [
    'ALL',
    ...Array.from(
      new Set([
        ...matchedSkills.map((s) => s.category),
        ...missingSkills.map((s) => s.category),
      ])
    ).filter(Boolean),
  ];

  // Filtering helper
  const filterList = (list) => {
    return list.filter((item) => {
      const matchesSearch = item.name.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesCat = selectedCategory === 'ALL' || item.category === selectedCategory;
      return matchesSearch && matchesCat;
    });
  };

  const filteredMatched = filterList(matchedSkills);
  const filteredMissing = filterList(missingSkills);

  const copyMissingList = () => {
    const text = missingSkills.map((s) => s.name).join(', ');
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800 bg-slate-900/60 shadow-xl">
      {/* Title & Toolbar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-slate-800">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            Skill Taxonomy Analysis
            <span className="text-xs font-normal text-slate-400">
              ({matchedSkills.length} matched / {missingSkills.length} missing)
            </span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Classified across programming languages, AI/ML libraries, cloud platforms, and architecture
          </p>
        </div>

        {/* Search & Copy */}
        <div className="flex items-center space-x-2">
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search skills..."
              className="pl-8 pr-3 py-1.5 rounded-lg bg-slate-950/70 border border-slate-800 text-xs text-slate-200 placeholder-slate-500 focus:border-indigo-500 w-44 transition-all"
            />
          </div>

          {missingSkills.length > 0 && (
            <button
              onClick={copyMissingList}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 text-xs font-medium text-slate-300 transition-all"
              title="Copy missing skills list"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied' : 'Copy Missing'}</span>
            </button>
          )}
        </div>
      </div>

      {/* Category Pills */}
      {categories.length > 2 && (
        <div className="flex items-center gap-1.5 py-3.5 overflow-x-auto text-xs no-scrollbar">
          <span className="text-slate-500 text-[11px] font-medium mr-1 flex items-center gap-1">
            <Filter className="w-3 h-3" /> Filter:
          </span>
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-2.5 py-1 rounded-md text-xs font-medium whitespace-nowrap transition-all ${
                selectedCategory === cat
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'bg-slate-950/50 text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      )}

      {/* Two Column Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mt-3">
        {/* Matched Skills */}
        <div className="rounded-xl bg-slate-950/50 border border-emerald-950/40 p-4.5">
          <div className="flex items-center justify-between mb-3.5 pb-2 border-b border-emerald-900/30">
            <div className="flex items-center space-x-2 text-emerald-400 text-sm font-semibold">
              <CheckCircle2 className="w-4 h-4" />
              <span>Matched Skills ({filteredMatched.length})</span>
            </div>
            <span className="text-[11px] text-emerald-400/80 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
              Found on Resume
            </span>
          </div>

          {filteredMatched.length === 0 ? (
            <p className="text-xs text-slate-500 italic py-4 text-center">
              No matched skills in this category
            </p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {filteredMatched.map((skill, idx) => (
                <div
                  key={idx}
                  className="group flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-medium hover:bg-emerald-500/20 transition-all"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                  <span>{skill.name}</span>
                  <span className="text-[10px] text-emerald-400/60 ml-0.5 group-hover:text-emerald-300">
                    • {skill.category}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Missing Skills */}
        <div className="rounded-xl bg-slate-950/50 border border-rose-950/40 p-4.5">
          <div className="flex items-center justify-between mb-3.5 pb-2 border-b border-rose-900/30">
            <div className="flex items-center space-x-2 text-rose-400 text-sm font-semibold">
              <XCircle className="w-4 h-4" />
              <span>Missing Required Skills ({filteredMissing.length})</span>
            </div>
            <span className="text-[11px] text-rose-400/80 bg-rose-500/10 px-2 py-0.5 rounded-full border border-rose-500/20">
              Gaps Identified
            </span>
          </div>

          {filteredMissing.length === 0 ? (
            <div className="text-center py-5">
              <p className="text-xs text-emerald-400 font-medium">
                Outstanding! No missing skill gaps detected for this selection.
              </p>
            </div>
          ) : (
            <div className="flex flex-wrap gap-2">
              {filteredMissing.map((skill, idx) => (
                <div
                  key={idx}
                  className={`group flex items-center space-x-1.5 px-2.5 py-1 rounded-lg text-xs font-medium transition-all ${
                    skill.importance === 'Critical'
                      ? 'bg-rose-500/15 border border-rose-500/40 text-rose-300 hover:bg-rose-500/25'
                      : 'bg-amber-500/10 border border-amber-500/30 text-amber-300 hover:bg-amber-500/20'
                  }`}
                >
                  <span
                    className={`w-1.5 h-1.5 rounded-full ${
                      skill.importance === 'Critical' ? 'bg-rose-400 animate-pulse' : 'bg-amber-400'
                    }`}
                  />
                  <span>{skill.name}</span>
                  {skill.importance === 'Critical' && (
                    <span className="text-[9px] uppercase px-1 py-0.2 rounded bg-rose-500/30 text-rose-200 font-bold ml-1">
                      Critical
                    </span>
                  )}
                  <span className="text-[10px] opacity-60 ml-0.5">
                    • {skill.category}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
