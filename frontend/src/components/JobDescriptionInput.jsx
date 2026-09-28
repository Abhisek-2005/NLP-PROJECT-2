import React from 'react';
import { Briefcase, FileCode, Trash2 } from 'lucide-react';

export default function JobDescriptionInput({
  jobTitle,
  setJobTitle,
  jobDescription,
  setJobDescription,
}) {
  const wordCount = jobDescription ? jobDescription.trim().split(/\s+/).filter(Boolean).length : 0;

  return (
    <div className="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/60 shadow-xl flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-800/80 mb-4">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-lg bg-purple-500/20 text-purple-400 flex items-center justify-center font-bold text-sm">
            2
          </div>
          <div>
            <h2 className="text-base font-semibold text-white">Target Job Description</h2>
            <p className="text-xs text-slate-400">Position requirements & desired skills</p>
          </div>
        </div>

        {jobDescription && (
          <button
            type="button"
            onClick={() => {
              setJobDescription('');
              setJobTitle('');
            }}
            className="flex items-center gap-1 text-xs text-slate-400 hover:text-rose-400 transition-colors"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Reset</span>
          </button>
        )}
      </div>

      {/* Role Title Input */}
      <div className="mb-3">
        <label className="block text-xs font-medium text-slate-300 mb-1.5 flex items-center gap-1.5">
          <Briefcase className="w-3.5 h-3.5 text-purple-400" />
          <span>Job Title / Role (Optional)</span>
        </label>
        <input
          type="text"
          value={jobTitle}
          onChange={(e) => setJobTitle(e.target.value)}
          placeholder="e.g. Senior Machine Learning Engineer, Full Stack Developer"
          className="w-full px-3.5 py-2 rounded-xl bg-slate-950/60 border border-slate-800 focus:border-purple-500 focus:ring-1 focus:ring-purple-500 text-xs text-slate-200 placeholder-slate-500 transition-all"
        />
      </div>

      {/* Job Description Textarea */}
      <div className="flex-1 flex flex-col">
        <label className="block text-xs font-medium text-slate-300 mb-1.5 flex items-center justify-between">
          <span className="flex items-center gap-1.5">
            <FileCode className="w-3.5 h-3.5 text-purple-400" />
            <span>Job Description Content *</span>
          </span>
          <span className="text-[11px] text-slate-400">
            {wordCount < 20 ? (
              <span className="text-amber-400">Min 20 words recommended</span>
            ) : (
              <span className="text-slate-300 font-medium">{wordCount} words</span>
            )}
          </span>
        </label>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste the job requirements, responsibilities, technical requirements, and nice-to-have qualifications..."
          className="w-full flex-1 min-h-[175px] p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 focus:border-purple-500 focus:ring-1 focus:ring-purple-500 text-slate-200 text-xs font-mono resize-none leading-relaxed transition-all"
        />
        <div className="flex items-center justify-between mt-2 text-[11px] text-slate-400">
          <span>
            Characters: <strong className="text-slate-200">{jobDescription.length}</strong>
          </span>
          <span>ATS Keyword matching enabled</span>
        </div>
      </div>
    </div>
  );
}
