const API_BASE = '/api/v1';

export async function checkBackendHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error('Health check failed');
    return await res.json();
  } catch (err) {
    console.warn('Backend health check error:', err);
    return null;
  }
}

export async function getSupportedRoles() {
  try {
    const res = await fetch(`${API_BASE}/cv/roles`);
    if (!res.ok) throw new Error('Failed to fetch roles');
    const data = await res.json();
    return data.roles || [];
  } catch (err) {
    console.error('Error fetching roles:', err);
    return [];
  }
}

export async function analyzeCV({ file, targetRole, experienceLevel, jobDescription, customApiKey }) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('target_role', targetRole);
  formData.append('target_experience_level', experienceLevel);
  if (jobDescription) formData.append('job_description', jobDescription);
  if (customApiKey) formData.append('custom_gemini_api_key', customApiKey);

  const res = await fetch(`${API_BASE}/cv/analyze`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to analyze CV. Please try again.');
  }

  return await res.json();
}

export async function searchJobs({ skills, targetRole, experienceLevel, location, remoteOnly, analysisId, tavilyApiKey, serperApiKey, limit = 20 }) {
  const res = await fetch(`${API_BASE}/jobs/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      skills: skills || {},
      target_role: targetRole,
      experience_level: experienceLevel,
      location: location || null,
      remote_only: Boolean(remoteOnly),
      analysis_id: analysisId ?? null,
      tavily_api_key: tavilyApiKey || null,
      serper_api_key: serperApiKey || null,
      limit,
    }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(typeof errorData.detail === 'string' ? errorData.detail : 'Failed to search for jobs. Please try again.');
  }

  return await res.json();
}

export async function analyzeSampleCV({ targetRole, experienceLevel, customApiKey }) {
  const formData = new FormData();
  formData.append('target_role', targetRole);
  formData.append('target_experience_level', experienceLevel);
  if (customApiKey) formData.append('custom_gemini_api_key', customApiKey);

  const res = await fetch(`${API_BASE}/cv/analyze-sample`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to analyze sample CV.');
  }

  return await res.json();
}
