import { useCallback, useEffect, useRef, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { Button, Empty, PageHeader, Pill, cx } from '../components/ui'
import { api } from '../lib/api'
import { useApp } from '../lib/store'

const STATUS = {
  processing: <Pill tone="warn">Generating…</Pill>,
  ready: <Pill tone="good">Ready</Pill>,
  failed: <Pill tone="bad">Failed</Pill>,
}

export function DeckList({ decks, subjects }) {
  const nameOf = (id) => subjects.find((s) => s.id === id)?.name || id
  return (
    <ul className="grid gap-3 sm:grid-cols-2">
      {decks.map((d) => (
        <li key={d.id}>
          <Link to={`/studio/${d.id}`} className="flex h-full flex-col gap-2 rounded-xl border border-line bg-surface p-4 hover:border-ink/40">
            <div className="flex items-center gap-2">
              <span className="label truncate">{nameOf(d.subject_id)}</span>
              <span className="ml-auto">{STATUS[d.status]}</span>
            </div>
            <h3 className="leading-snug font-semibold">{d.title}</h3>
            {d.status === 'ready' && <p className="line-clamp-2 text-sm text-muted">{d.summary}</p>}
            {d.status === 'failed' && <p className="text-sm text-bad">{d.error}</p>}
            {d.status === 'processing' && <p className="text-sm text-muted">Reading the file and writing notes. Large PDFs can take a few minutes.</p>}
            <div className="tabular mt-auto flex flex-wrap gap-x-3 pt-1 text-xs text-muted">
              {d.stats && (
                <>
                  <span>{d.stats.sections} sections</span>
                  <span>{d.stats.flashcards} flashcards</span>
                  <span>{d.stats.key_terms} terms</span>
                </>
              )}
              {d.engine && <span>{d.engine === 'claude' ? 'By Claude' : 'Offline draft'}</span>}
            </div>
          </Link>
        </li>
      ))}
    </ul>
  )
}

export function useDecks(subjectId) {
  const [decks, setDecks] = useState(null)
  const load = useCallback(() => api.decks(subjectId).then(setDecks).catch(() => setDecks([])), [subjectId])
  useEffect(() => {
    load()
  }, [load])
  const processing = decks?.some((d) => d.status === 'processing')
  useEffect(() => {
    if (!processing) return
    const t = setInterval(load, 3000)
    return () => clearInterval(t)
  }, [processing, load])
  return [decks, load]
}

function Uploader({ subjects, subjectId, setSubjectId, onUploaded }) {
  const { health } = useApp()
  const [file, setFile] = useState(null)
  const [title, setTitle] = useState('')
  const [drag, setDrag] = useState(false)
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  const input = useRef(null)

  const pick = (f) => {
    setErr('')
    if (!f) return
    if (!/\.(pdf|txt|md|markdown)$/i.test(f.name)) return setErr('Upload a PDF, TXT or Markdown file.')
    setFile(f)
  }

  const submit = async (e) => {
    e.preventDefault()
    if (!file) return setErr('Choose a file first.')
    setBusy(true)
    setErr('')
    try {
      await api.upload(file, subjectId, title)
      setFile(null)
      setTitle('')
      onUploaded()
    } catch (ex) {
      setErr(ex.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <form onSubmit={submit} className="space-y-4 rounded-xl border border-line bg-surface p-4 sm:p-5">
      <div className="grid gap-3 sm:grid-cols-2">
        <label className="space-y-1 text-sm">
          <span className="label">Subject</span>
          <select id="studio-subject" value={subjectId} onChange={(e) => setSubjectId(e.target.value)} className="w-full rounded-lg border border-line bg-bg px-3 py-2">
            {subjects.map((s) => (
              <option key={s.id} value={s.id}>
                {s.code === s.name ? s.name : `${s.code} · ${s.name}`}
              </option>
            ))}
          </select>
        </label>
        <label className="space-y-1 text-sm">
          <span className="label">Chapter title (optional)</span>
          <input id="studio-title" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="e.g. Unit 3: Cost concepts" className="w-full rounded-lg border border-line bg-bg px-3 py-2" />
        </label>
      </div>
      <div
        onDragOver={(e) => {
          e.preventDefault()
          setDrag(true)
        }}
        onDragLeave={() => setDrag(false)}
        onDrop={(e) => {
          e.preventDefault()
          setDrag(false)
          pick(e.dataTransfer.files[0])
        }}
        onClick={() => input.current?.click()}
        onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && input.current?.click()}
        role="button"
        tabIndex={0}
        className={cx(
          'flex cursor-pointer flex-col items-center justify-center gap-1 rounded-lg border-2 border-dashed px-4 py-8 text-center',
          drag ? 'border-accent bg-accent-soft' : 'border-line hover:border-accent',
        )}
      >
        <input ref={input} id="studio-file" type="file" accept=".pdf,.txt,.md,.markdown" className="hidden" onChange={(e) => pick(e.target.files[0])} />
        {file ? (
          <>
            <span className="font-medium">{file.name}</span>
            <span className="tabular text-xs text-muted">{(file.size / 1024 / 1024).toFixed(2)} MB · click to change</span>
          </>
        ) : (
          <>
            <span className="font-medium">Drop your notes here, or click to choose a file</span>
            <span className="text-xs text-muted">PDF, TXT or Markdown, up to 30 MB. Handwritten or scanned PDFs need Claude.</span>
          </>
        )}
      </div>
      {err && <p className="text-sm text-bad">{err}</p>}
      <div className="flex flex-wrap items-center gap-3">
        <Button type="submit" variant="primary" disabled={busy || !file}>
          {busy ? 'Uploading…' : 'Make notes and flashcards'}
        </Button>
        <span className="text-xs text-muted">
          {health?.ai.available
            ? 'Claude will write detailed notes, flashcards and likely exam questions.'
            : 'Claude is not connected, so you will get an offline draft. '}
          {!health?.ai.available && (
            <Link to="/ask?setup=1" className="text-accent underline">
              Add an API key
            </Link>
          )}
        </span>
      </div>
    </form>
  )
}

export default function Studio() {
  const { subjects, refreshSubjects } = useApp()
  const [params] = useSearchParams()
  const [subjectId, setSubjectId] = useState(params.get('subject') || 'eef')
  const [filter, setFilter] = useState('all')
  const [decks, reload] = useDecks(filter === 'all' ? undefined : filter)

  useEffect(() => {
    if (subjects.length && !subjects.some((s) => s.id === subjectId)) setSubjectId(subjects[0].id)
  }, [subjects, subjectId])

  return (
    <div className="space-y-8">
      <PageHeader eyebrow="Notes Studio" title="Turn any chapter into a study pack">
        Upload notes for a chapter that is not covered here, or for another subject. You get detailed notes, flip-through flashcards, likely exam questions, and a printable PDF.
      </PageHeader>
      <Uploader
        subjects={subjects}
        subjectId={subjectId}
        setSubjectId={setSubjectId}
        onUploaded={() => {
          reload()
          refreshSubjects()
        }}
      />
      <section className="space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 className="text-xl font-bold">Your study packs</h2>
          <select id="studio-filter" aria-label="Filter by subject" value={filter} onChange={(e) => setFilter(e.target.value)} className="rounded-lg border border-line bg-surface px-3 py-1.5 text-sm">
            <option value="all">All subjects</option>
            {subjects.map((s) => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
        </div>
        {decks === null ? null : decks.length === 0 ? (
          <Empty title="No study packs yet">Upload a PDF or text file above to create your first one.</Empty>
        ) : (
          <DeckList decks={decks} subjects={subjects} />
        )}
      </section>
    </div>
  )
}
