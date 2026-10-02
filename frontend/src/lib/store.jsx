import { createContext, useCallback, useContext, useEffect, useState } from 'react'
import { api } from './api'

const AppContext = createContext(null)

/** Reading preferences live on <html> so CSS can switch fonts and sizes everywhere. */
export function applyReading(settings) {
  const root = document.documentElement
  root.dataset.font = settings.reading_font || 'default'
  root.dataset.size = settings.text_size || 'm'
  try {
    // Cached so index.html can apply it before React loads (no flash of the default font).
    localStorage.setItem('reading', JSON.stringify({ font: root.dataset.font, size: root.dataset.size }))
  } catch {
    /* storage blocked */
  }
}

export function AppProvider({ children }) {
  const [health, setHealth] = useState(null)
  const [subjects, setSubjects] = useState([])
  const [progress, setProgressMap] = useState({})
  const [settings, setSettingsMap] = useState({})
  const [error, setError] = useState(null)

  const refreshSubjects = useCallback(() => api.subjects().then(setSubjects).catch((e) => setError(e.message)), [])

  useEffect(() => {
    api.health().then(setHealth).catch(() => setError('The server is not running. Start it with run.ps1 (see README).'))
    refreshSubjects()
    api.progress().then(setProgressMap).catch(() => {})
    api
      .settings()
      .then((s) => {
        setSettingsMap(s)
        applyReading(s)
      })
      .catch(() => {})
  }, [refreshSubjects])

  const setProgress = useCallback((key, patch) => {
    setProgressMap((p) => ({ ...p, [key]: { status: null, bookmarked: false, ...p[key], ...patch } }))
    api.setProgress(key, patch).catch(() => {})
  }, [])

  const clearProgress = useCallback((prefix) => {
    setProgressMap((p) => Object.fromEntries(Object.entries(p).filter(([k]) => !k.startsWith(prefix))))
    api.clearProgress(prefix).catch(() => {})
  }, [])

  const saveSetting = useCallback((key, value) => {
    setSettingsMap((s) => {
      const next = { ...s }
      if (value === null || value === undefined) delete next[key]
      else next[key] = value
      applyReading(next)
      return next
    })
    return api.setSetting(key, value).catch(() => {})
  }, [])

  return (
    <AppContext.Provider value={{ health, subjects, refreshSubjects, progress, setProgress, clearProgress, settings, saveSetting, error }}>
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => useContext(AppContext)

/** Attempt counts for a list of question ids. */
export function unitStats(progress, ids) {
  let done = 0
  let correct = 0
  let wrong = 0
  let bookmarked = 0
  for (const i of ids) {
    const p = progress[`cn:${i}`]
    if (!p) continue
    if (p.status) done++
    if (p.status === 'correct') correct++
    if (p.status === 'wrong') wrong++
    if (p.bookmarked) bookmarked++
  }
  return { done, correct, wrong, bookmarked, total: ids.length }
}

export const todayISO = () => {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

export const daysUntil = (iso) => {
  if (!iso) return null
  const [y, m, d] = iso.split('-').map(Number)
  const t = new Date()
  return Math.round((new Date(y, m - 1, d) - new Date(t.getFullYear(), t.getMonth(), t.getDate())) / 86400000)
}
