import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { Button, Empty, PageHeader, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { useApp } from '../lib/store'
import { DeckList, useDecks } from './Studio'

function EditSubject({ subject, onSaved, onCancel }) {
  const [form, setForm] = useState({ code: subject.code, name: subject.name, description: subject.description })
  const [err, setErr] = useState('')
  const save = async (e) => {
    e.preventDefault()
    try {
      onSaved(await api.updateSubject(subject.id, form))
    } catch (ex) {
      setErr(ex.message)
    }
  }
  return (
    <form onSubmit={save} className="grid gap-3 rounded-xl border border-line bg-surface p-4 sm:grid-cols-[8rem_1fr]">
      <label className="space-y-1 text-sm">
        <span className="label">Code</span>
        <input id="edit-code" required maxLength={12} value={form.code} onChange={(e) => setForm({ ...form, code: e.target.value })} className="w-full rounded-lg border border-line bg-bg px-3 py-2" />
      </label>
      <label className="space-y-1 text-sm">
        <span className="label">Full name</span>
        <input id="edit-name" required maxLength={80} value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} className="w-full rounded-lg border border-line bg-bg px-3 py-2" />
      </label>
      <label className="space-y-1 text-sm sm:col-span-2">
        <span className="label">Description</span>
        <input id="edit-desc" maxLength={300} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} className="w-full rounded-lg border border-line bg-bg px-3 py-2" />
      </label>
      {err && <p className="text-sm text-bad sm:col-span-2">{err}</p>}
      <div className="flex gap-2 sm:col-span-2">
        <Button type="submit" variant="primary">Save</Button>
        <Button variant="quiet" onClick={onCancel}>Cancel</Button>
      </div>
    </form>
  )
}

export default function Subject() {
  const { sid } = useParams()
  const { subjects, refreshSubjects } = useApp()
  const [subject, setSubject] = useState(null)
  const [editing, setEditing] = useState(false)
  const [err, setErr] = useState('')
  const [decks] = useDecks(sid)

  useEffect(() => {
    setSubject(null)
    api.subject(sid).then(setSubject).catch((e) => setErr(e.message))
  }, [sid])

  if (err) return <Empty title="Subject not found">{err}</Empty>
  if (!subject) return <Spinner />

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow={`${subject.code} · Subject space`}
        title={subject.name}
        actions={
          <>
            <Link to={`/studio?subject=${sid}`} className="rounded-lg bg-accent px-3.5 py-2 text-sm font-medium text-accent-ink hover:brightness-110">
              Upload material
            </Link>
            <Link to={`/ask?subject=${sid}`} className="rounded-lg border border-line bg-surface px-3.5 py-2 text-sm font-medium hover:bg-sunken">
              Ask AI
            </Link>
            <Button variant="quiet" onClick={() => setEditing(!editing)}>Edit details</Button>
          </>
        }
      >
        {subject.description}
      </PageHeader>

      {editing && (
        <EditSubject
          subject={subject}
          onCancel={() => setEditing(false)}
          onSaved={(s) => {
            setSubject({ ...subject, ...s })
            setEditing(false)
            refreshSubjects()
          }}
        />
      )}

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Study packs</h2>
        {decks === null ? (
          <Spinner />
        ) : decks.length === 0 ? (
          <Empty
            title={`No ${subject.code} material yet`}
            action={
              <Link to={`/studio?subject=${sid}`} className="rounded-lg bg-accent px-4 py-2 text-sm font-medium text-accent-ink">
                Upload the first chapter
              </Link>
            }
          >
            This space is ready. Upload a chapter's notes as PDF or text, and Notes Studio will turn it into detailed notes, flashcards, likely exam questions and a PDF you can print.
          </Empty>
        ) : (
          <DeckList decks={decks} subjects={subjects} />
        )}
      </section>

      <section className="grid gap-3 sm:grid-cols-3">
        {[
          ['1', 'Upload', 'Add one chapter at a time. Smaller files give more detailed notes.'],
          ['2', 'Study', 'Read the notes, then flip through the flashcards until every card is known.'],
          ['3', 'Revise', 'Download the PDF for offline revision and practise the likely exam questions.'],
        ].map(([n, t, d]) => (
          <div key={n} className="rounded-xl border border-line bg-surface p-4">
            <span className="font-mono text-sm text-muted">Step {n}</span>
            <h3 className="mt-1 font-semibold">{t}</h3>
            <p className="mt-1 text-sm text-muted">{d}</p>
          </div>
        ))}
      </section>
    </div>
  )
}
