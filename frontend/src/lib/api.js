async function request(path, options = {}) {
  const res = await fetch(`/api${path}`, options)
  if (!res.ok) {
    let message = `Request failed (${res.status})`
    try {
      const body = await res.json()
      if (body.detail) message = typeof body.detail === 'string' ? body.detail : body.detail[0]?.msg || message
    } catch {
      /* not JSON */
    }
    throw new Error(message)
  }
  return res.json()
}

const json = (method, body) => ({
  method,
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
})

export const api = {
  health: () => request('/health'),
  subjects: () => request('/subjects'),
  subject: (id) => request(`/subjects/${id}`),
  createSubject: (body) => request('/subjects', json('POST', body)),
  updateSubject: (id, body) => request(`/subjects/${id}`, json('PUT', body)),
  unit: (id) => request(`/cn/units/${id}`),
  questions: (params) => request(`/cn/questions?${new URLSearchParams(params)}`),
  formulas: () => request('/cn/formulas'),
  quiz: (units, n) => request(`/cn/quiz?units=${units.join(',')}&n=${n}`),
  progress: () => request('/progress'),
  setProgress: (key, body) => request(`/progress/${encodeURIComponent(key)}`, json('PUT', body)),
  clearProgress: (prefix) => request(`/progress?prefix=${encodeURIComponent(prefix)}`, { method: 'DELETE' }),
  daily: (day) => request(`/cn/daily?day=${day}`),
  syllabus: () => request('/cn/syllabus'),
  labs: () => request('/cn/labs'),
  mock: (test) => request(`/cn/mock?test=${test}`),
  smartQuiz: (n) => request(`/cn/smart-quiz?n=${n}`),
  stats: () => request('/stats'),
  plan: (subjectId = 'cn', test = '', mode = 'questions') =>
    request(`/plan?${new URLSearchParams({ subject_id: subjectId, mode, ...(test && { test }) })}`),
  settings: () => request('/settings'),
  setSetting: (key, value) => request(`/settings/${encodeURIComponent(key)}`, json('PUT', { value })),
  reviewDue: () => request('/review/due'),
  reviewStates: (prefix) => request(`/review/states?prefix=${encodeURIComponent(prefix)}`),
  review: (key, grade) => request('/review', json('POST', { key, grade })),
  logFocus: (minutes) => request('/focus', json('POST', { minutes })),
  decks: (subjectId) => request(`/studio/decks${subjectId ? `?subject_id=${subjectId}` : ''}`),
  deck: (id) => request(`/studio/decks/${id}`),
  deleteDeck: (id) => request(`/studio/decks/${id}`, { method: 'DELETE' }),
  regenerate: (id) => request(`/studio/decks/${id}/regenerate`, { method: 'POST' }),
  upload: (file, subjectId, title) => {
    const fd = new FormData()
    fd.append('file', file)
    fd.append('subject_id', subjectId)
    fd.append('title', title || '')
    return request('/studio/upload', { method: 'POST', body: fd })
  },
}

export const unitPdfUrl = (id) => `/api/cn/units/${id}/pdf`
export const formulasPdfUrl = '/api/cn/formulas/pdf'
export const deckPdfUrl = (id) => `/api/studio/decks/${id}/pdf`

/** Stream an Ask AI answer. Calls onEvent for each server-sent event. */
export async function askStream(body, onEvent, signal) {
  const res = await fetch('/api/ask', { ...json('POST', body), signal })
  if (!res.ok) {
    let message = `Request failed (${res.status})`
    try {
      message = (await res.json()).detail || message
    } catch {
      /* ignore */
    }
    throw new Error(message)
  }
  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  for (;;) {
    const { value, done } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    let idx
    while ((idx = buffer.indexOf('\n\n')) >= 0) {
      const chunk = buffer.slice(0, idx)
      buffer = buffer.slice(idx + 2)
      if (chunk.startsWith('data: ')) onEvent(JSON.parse(chunk.slice(6)))
    }
  }
}
