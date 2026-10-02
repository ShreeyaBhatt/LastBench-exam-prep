import { createContext, useCallback, useContext, useEffect, useRef, useState } from 'react'
import { api } from './api'

const FocusContext = createContext(null)

export const MODES = {
  focus: { label: 'Focus', minutes: 25 },
  short: { label: 'Short break', minutes: 5 },
  long: { label: 'Long break', minutes: 15 },
}

const load = () => {
  try {
    return JSON.parse(localStorage.getItem('timer') || 'null')
  } catch {
    return null
  }
}

const save = (state) => {
  try {
    localStorage.setItem('timer', JSON.stringify(state))
  } catch {
    /* storage blocked */
  }
}

/* ---- background sound, generated with Web Audio (no files to download) ---- */

function makeNoise(ctx, kind) {
  const len = ctx.sampleRate * 4
  const buf = ctx.createBuffer(1, len, ctx.sampleRate)
  const out = buf.getChannelData(0)
  if (kind === 'brown') {
    let last = 0
    for (let i = 0; i < len; i++) {
      last = (last + 0.02 * (Math.random() * 2 - 1)) / 1.02
      out[i] = last * 3.5
    }
  } else {
    // Pink noise (Paul Kellet's filter): softer than white, sounds like steady rain.
    let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0
    for (let i = 0; i < len; i++) {
      const w = Math.random() * 2 - 1
      b0 = 0.99886 * b0 + w * 0.0555179
      b1 = 0.99332 * b1 + w * 0.0750759
      b2 = 0.969 * b2 + w * 0.153852
      b3 = 0.8665 * b3 + w * 0.3104856
      b4 = 0.55 * b4 + w * 0.5329522
      b5 = -0.7616 * b5 - w * 0.016898
      out[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + w * 0.5362) * 0.11
      b6 = w * 0.115926
    }
  }
  return buf
}

function chime() {
  try {
    const ctx = new AudioContext()
    ;[880, 1320].forEach((f, i) => {
      const o = ctx.createOscillator()
      const g = ctx.createGain()
      o.frequency.value = f
      g.gain.setValueAtTime(0.0001, ctx.currentTime + i * 0.25)
      g.gain.exponentialRampToValueAtTime(0.25, ctx.currentTime + i * 0.25 + 0.02)
      g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + i * 0.25 + 0.9)
      o.connect(g).connect(ctx.destination)
      o.start(ctx.currentTime + i * 0.25)
      o.stop(ctx.currentTime + i * 0.25 + 1)
    })
    setTimeout(() => ctx.close(), 2000)
  } catch {
    /* audio unavailable */
  }
}

export function FocusProvider({ children }) {
  const saved = load()
  const [mode, setMode] = useState(saved?.mode || 'focus')
  const [running, setRunning] = useState(Boolean(saved?.running && saved.endsAt > Date.now()))
  const [endsAt, setEndsAt] = useState(saved?.endsAt || null)
  const [remaining, setRemaining] = useState(saved?.remaining ?? MODES[saved?.mode || 'focus'].minutes * 60)
  const [sessions, setSessions] = useState(saved?.day === new Date().toDateString() ? saved.sessions : 0)
  const [focusMode, setFocusMode] = useState(false)
  const [sound, setSoundKind] = useState('off')
  const [volume, setVolume] = useState(0.35)
  const audio = useRef(null)

  useEffect(() => {
    save({ mode, running, endsAt, remaining, sessions, day: new Date().toDateString() })
  }, [mode, running, endsAt, remaining, sessions])

  const finish = useCallback(() => {
    setRunning(false)
    setEndsAt(null)
    chime()
    if (mode === 'focus') {
      api.logFocus(MODES.focus.minutes).catch(() => {})
      const n = sessions + 1
      setSessions(n)
      const next = n % 4 === 0 ? 'long' : 'short'
      setMode(next)
      setRemaining(MODES[next].minutes * 60)
    } else {
      setMode('focus')
      setRemaining(MODES.focus.minutes * 60)
    }
  }, [mode, sessions])

  useEffect(() => {
    if (!running) return
    const tick = () => {
      const left = Math.max(0, Math.round((endsAt - Date.now()) / 1000))
      setRemaining(left)
      if (left === 0) finish()
    }
    tick()
    const t = setInterval(tick, 1000)
    return () => clearInterval(t)
  }, [running, endsAt, finish])

  useEffect(() => {
    const base = document.title.replace(/^\d+:\d+ · .*? — /, '')
    if (running) {
      const m = String(Math.floor(remaining / 60)).padStart(2, '0')
      const s = String(remaining % 60).padStart(2, '0')
      document.title = `${m}:${s} · ${MODES[mode].label} — ${base}`
    } else document.title = base
  }, [running, remaining, mode])

  const start = () => {
    setEndsAt(Date.now() + remaining * 1000)
    setRunning(true)
  }
  const pause = () => setRunning(false)
  const reset = (m = mode) => {
    setRunning(false)
    setEndsAt(null)
    setMode(m)
    setRemaining(MODES[m].minutes * 60)
  }

  const setSound = (kind) => {
    const a = audio.current
    if (a?.src) {
      a.src.stop()
      a.src = null
    }
    setSoundKind(kind)
    if (kind === 'off') return
    try {
      if (!audio.current) {
        const ctx = new AudioContext()
        const gain = ctx.createGain()
        gain.connect(ctx.destination)
        audio.current = { ctx, gain, src: null }
      }
      const { ctx, gain } = audio.current
      ctx.resume()
      gain.gain.value = volume
      const src = ctx.createBufferSource()
      src.buffer = makeNoise(ctx, kind)
      src.loop = true
      src.connect(gain)
      src.start()
      audio.current.src = src
    } catch {
      setSoundKind('off')
    }
  }

  useEffect(() => {
    if (audio.current) audio.current.gain.gain.value = volume
  }, [volume])

  return (
    <FocusContext.Provider
      value={{ mode, running, remaining, sessions, start, pause, reset, focusMode, setFocusMode, sound, setSound, volume, setVolume }}
    >
      {children}
    </FocusContext.Provider>
  )
}

export const useFocus = () => useContext(FocusContext)

export const formatTime = (sec) => `${String(Math.floor(sec / 60)).padStart(2, '0')}:${String(sec % 60).padStart(2, '0')}`
