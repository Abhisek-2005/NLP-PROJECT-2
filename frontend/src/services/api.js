const API_BASE = '/api';

export const apiClient = {
  // Check health and model status
  async getHealth() {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error('Failed to fetch API health');
    return res.json();
  },

  // Get sample data
  async getSamples() {
    const res = await fetch(`${API_BASE}/samples`);
    if (!res.ok) throw new Error('Failed to load sample data');
    return res.json();
  },

  // Analyze uploaded resume file (PDF, DOCX, TXT)
  async analyzeFile(file, jobDescription, jobTitle = 'Target Role') {
    const formData = new FormData();
    formData.append('resume_file', file);
    formData.append('job_description', jobDescription);
    formData.append('job_title', jobTitle);

    const res = await fetch(`${API_BASE}/analyze/file`, {
      method: 'POST',
      body: formData,
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Analysis failed' }));
      throw new Error(err.detail || 'File analysis failed');
    }
    return res.json();
  },

  // Analyze pasted text
  async analyzeText(resumeText, jobDescription, jobTitle = 'Target Role', resumeFilename = 'Pasted_Resume.txt') {
    const res = await fetch(`${API_BASE}/analyze/text`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        resume_text: resumeText,
        job_description: jobDescription,
        job_title: jobTitle,
        resume_filename: resumeFilename,
      }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Analysis failed' }));
      throw new Error(err.detail || 'Text analysis failed');
    }
    return res.json();
  },

  // History endpoints
  async getHistory() {
    const res = await fetch(`${API_BASE}/history`);
    if (!res.ok) throw new Error('Failed to fetch history');
    return res.json();
  },

  async getHistoryItem(id) {
    const res = await fetch(`${API_BASE}/history/${id}`);
    if (!res.ok) throw new Error('Failed to load analysis detail');
    return res.json();
  },

  async deleteHistoryItem(id) {
    const res = await fetch(`${API_BASE}/history/${id}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete history item');
    return res.json();
  },

  async clearAllHistory() {
    const res = await fetch(`${API_BASE}/history`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to clear history');
    return res.json();
  },
};
