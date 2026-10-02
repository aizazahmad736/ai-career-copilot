const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1';

function apiFetch(url, options = {}) {
  const headers = new Headers(options.headers || {});
  const token = localStorage.getItem('career_copilot_access_token');
  if (token) headers.set('Authorization', `Bearer ${token}`);
  return fetch(url, { ...options, headers });
}

export async function getAuthConfig() {
  const res = await apiFetch(`${API_BASE}/auth/config`);
  if (!res.ok) throw new Error('Could not check account settings.');
  return await res.json();
}

export async function authenticate(mode, email, password) {
  const res = await apiFetch(`${API_BASE}/auth/${mode}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Authentication failed.');
  }
  const data = await res.json();
  localStorage.setItem('career_copilot_access_token', data.access_token);
  return data.user;
}

export async function getCurrentUser() {
  const res = await apiFetch(`${API_BASE}/auth/me`);
  if (!res.ok) throw new Error('Your session has expired. Sign in again.');
  return await res.json();
}

export function clearAuthSession() {
  localStorage.removeItem('career_copilot_access_token');
}

export async function checkBackendHealth() {
  try {
    const res = await apiFetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error('Health check failed');
    return await res.json();
  } catch (err) {
    console.warn('Backend health check error:', err);
    return null;
  }
}

export async function getSupportedRoles() {
  try {
    const res = await apiFetch(`${API_BASE}/cv/roles`);
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

  const res = await apiFetch(`${API_BASE}/cv/analyze`, {
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
  const res = await apiFetch(`${API_BASE}/jobs/search`, {
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

  const res = await apiFetch(`${API_BASE}/cv/analyze-sample`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to analyze sample CV.');
  }

  return await res.json();
}

export async function getLearningPlan(analysisId) {
  const res = await apiFetch(`${API_BASE}/learning/plans/${analysisId}`);
  if (!res.ok) throw new Error('No saved learning plan');
  return await res.json();
}

export async function createLearningPlan(analysisId, durationWeeks) {
  const res = await apiFetch(`${API_BASE}/learning/plans`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ analysis_id: analysisId, duration_weeks: durationWeeks }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to generate a learning plan.');
  }
  return await res.json();
}

export async function updateLearningMilestone(planId, week, completed) {
  const res = await apiFetch(`${API_BASE}/learning/plans/${planId}/milestones/${week}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ completed }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to update learning progress.');
  }
  return await res.json();
}

export async function createInterviewSession({ analysisId, mode, customApiKey }) {
  const res = await apiFetch(`${API_BASE}/interviews/sessions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      analysis_id: analysisId,
      mode,
      question_count: 5,
      custom_gemini_api_key: customApiKey || null,
    }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to start interview.');
  }
  return await res.json();
}

export async function answerInterviewQuestion(sessionId, answer, customApiKey) {
  const res = await apiFetch(`${API_BASE}/interviews/sessions/${sessionId}/answers`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ answer, custom_gemini_api_key: customApiKey || null }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to evaluate answer.');
  }
  return await res.json();
}

export async function getDashboardSummary() {
  const res = await apiFetch(`${API_BASE}/dashboard/summary`);
  if (!res.ok) throw new Error('Failed to load the career dashboard.');
  return await res.json();
}

export async function getApplications() {
  const res = await apiFetch(`${API_BASE}/applications`);
  if (!res.ok) throw new Error('Failed to load application tracking.');
  return await res.json();
}

export async function saveApplication({ jobKey, analysisId, targetRole, title, company, url }) {
  const res = await apiFetch(`${API_BASE}/applications`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      job_key: jobKey,
      analysis_id: analysisId,
      target_role: targetRole,
      title,
      company,
      url,
    }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to save this opportunity.');
  }
  return await res.json();
}

export async function updateApplicationStatus(applicationId, status) {
  const res = await apiFetch(`${API_BASE}/applications/${applicationId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to update application status.');
  }
  return await res.json();
}
