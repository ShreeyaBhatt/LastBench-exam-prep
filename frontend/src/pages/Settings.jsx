import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import ExamDates from '../components/ExamDates'
import { Button, PageHeader, Segmented, cx } from '../components/ui'
import { api } from '../lib/api'
import { useApp } from '../lib/store'

const FONTS = [
  { value: 'default', label: 'Default', family: '"IBM Plex Sans", system-ui', note: 'IBM Plex Sans' },
  { value: 'lexend', label: 'Lexend', family: 'Lexend, system-ui', note: 'Easy-read: wider letters, designed to reduce visual stress' },
  { value: 'atkinson', label: 'Atkinson Hyperlegible', family: '"Atkinson Hyperlegible", system-ui', note: 'High legibility: distinct shapes for look-alike letters (I l 1, O 0)' },
]

function Section({ id, title, children, note }) {
  return (
    <section id={id} className="scroll-mt-20 space-y-3 rounded-xl border border-line bg-surface p-4 sm:p-5">
      <div>
        <h2 className="font-bold">{title}</h2>
        {note && <p className="text-sm text-muted">{note}</p>}
      </div>
      {children}
    </section>
  )
}

function AddSubject() {
  const { refreshSubjects } = useApp()
  const navigate = useNavigate()
  const [form, setForm] = useState({ code: '', name: '', description: '' })
  const [err, setErr] = useState('')
  const submit = async (e) => {
    e.preventDefault()
    setErr('')
    try {
      const s = await api.createSubject(form)
      await refreshSubjects()
      navigate(`/subjects/${s.id}`)
    } catch (ex) {
      setErr(ex.message)
    }
  }
  return (
    <form onSubmit={submit} className="grid gap-2 sm:grid-cols-[7rem_1fr_auto]">
      <input id="new-code" required maxLength={12} placeholder="Code (e.g. OS)" aria-label="Subject code" value={form.code}
        onChange={(e) => setForm({ ...form, code: e.target.value })} className="rounded-lg border border-line bg-bg px-3 py-2 text-sm" />
      <input id="new-name" required maxLength={80} placeholder="Subject name" aria-label="Subject name" value={form.name}
        onChange={(e) => setForm({ ...form, name: e.target.value })} className="rounded-lg border border-line bg-bg px-3 py-2 text-sm" />
      <Button type="submit" variant="primary">Add subject</Button>
      {err && <p className="text-sm text-bad sm:col-span-3">{err}</p>}
    </form>
  )
}

export default function Settings() {
  const { settings, saveSetting, clearProgress } = useApp()
  const [confirm, setConfirm] = useState(false)
  const font = settings.reading_font || 'default'
  const size = settings.text_size || 'm'
  const goal = settings.daily_goal || 20

  useEffect(() => {
    if (window.location.hash) document.querySelector(window.location.hash)?.scrollIntoView()
  }, [])

  return (
    <div className="space-y-6">
      <PageHeader eyebrow="Settings" title="Make it yours" />

      <Section title="Reading font" note="Changes the font across the whole app. Easy-read fonts can help with dyslexia and late-night eye strain.">
        <div className="grid gap-2 sm:grid-cols-3">
          {FONTS.map((f) => (
            <button
              key={f.value}
              type="button"
              onClick={() => saveSetting('reading_font', f.value)}
              aria-pressed={font === f.value}
              className={cx('cursor-pointer rounded-lg border p-3 text-left', font === f.value ? 'border-ink ring-1 ring-ink' : 'border-line hover:border-ink/40')}
            >
              <span className="block text-lg" style={{ fontFamily: f.family }}>
                {f.label}
              </span>
              <span className="mt-1 block text-sm" style={{ fontFamily: f.family }}>
                TCP uses a 3-way handshake: SYN, SYN-ACK, ACK.
              </span>
              <span className="mt-1 block text-xs text-muted">{f.note}</span>
            </button>
          ))}
        </div>
      </Section>

      <Section title="Text size">
        <Segmented
          label="Text size"
          value={size}
          onChange={(v) => saveSetting('text_size', v)}
          options={[
            { value: 's', label: 'Small' },
            { value: 'm', label: 'Medium' },
            { value: 'l', label: 'Large' },
            { value: 'xl', label: 'Extra large' },
          ]}
        />
      </Section>

      <Section title="Test dates" note="Used for the countdown and the day-by-day study plan.">
        <ExamDates />
      </Section>

      <Section title="Daily goal" note="Questions or flashcards per day. Shown on the home page.">
        <Segmented label="Daily goal" value={goal} onChange={(v) => saveSetting('daily_goal', v)} options={[10, 20, 30, 50].map((v) => ({ value: v, label: String(v) }))} />
      </Section>

      <Section id="subjects" title="Subjects" note="Add a subject, then upload its notes in Notes Studio to get notes, flashcards and a study plan.">
        <AddSubject />
      </Section>

      <Section title="Reset progress" note="Clears your CN answers, saved questions and review schedule. Study packs are kept.">
        {confirm ? (
          <div className="flex flex-wrap items-center gap-2 text-sm">
            This cannot be undone.
            <Button
              variant="danger"
              onClick={() => {
                clearProgress('cn:')
                clearProgress('syl:')
                setConfirm(false)
              }}
            >
              Yes, reset CN progress
            </Button>
            <Button variant="quiet" onClick={() => setConfirm(false)}>Cancel</Button>
          </div>
        ) : (
          <Button variant="danger" onClick={() => setConfirm(true)}>Reset CN progress</Button>
        )}
      </Section>
    </div>
  )
}
