import { useEffect, useRef, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { Button, Markdown, PageHeader, Pill, cx } from '../components/ui'
import { api, askStream } from '../lib/api'
import { useApp } from '../lib/store'

const STARTERS = {
  cn: [
    'Explain the difference between Go-Back-N and Selective Repeat with an example.',
    'How do I find the minimum frame size in CSMA/CD?',
    'Walk me through subnetting 192.168.10.0/24 into 6 subnets.',
    'When does a router fragment a packet, and how is the offset calculated?',
  ],
  other: [
    'Summarise my uploaded notes in 10 points.',
    'What are the most likely 7-mark questions from my notes?',
    'Explain the hardest topic in my notes in simple words.',
  ],
}

function KeySetup({ available }) {
  return (
    <section className={cx('rounded-xl border p-4 sm:p-5', available ? 'border-good/40 bg-good-soft' : 'border-warn/40 bg-warn-soft')}>
      <h2 className="font-semibold">{available ? 'Claude is connected' : 'Connect Claude to get written answers'}</h2>
      {available ? (
        <p className="mt-1 text-sm">Answers are written by Claude using your notes and the solved practice book as reference.</p>
      ) : (
        <>
          <p className="mt-1 text-sm">Without a key, Ask AI shows the closest matching notes and solved questions instead of writing an answer.</p>
          <ol className="mt-3 list-decimal space-y-1.5 pl-5 text-sm">
            <li>
              Create a key at <span className="font-mono">console.anthropic.com</span> → API Keys → Create Key. It starts with <span className="font-mono">sk-ant-</span>.
            </li>
            <li>
              In the <span className="font-mono">cn-exam-prep/backend</span> folder, copy <span className="font-mono">.env.example</span> to <span className="font-mono">.env</span>.
            </li>
            <li>
              Put your key on the line <span className="font-mono">ANTHROPIC_API_KEY=sk-ant-…</span> and save.
            </li>
            <li>Stop the server (Ctrl+C) and start it again with <span className="font-mono">run.ps1</span>. This badge turns green.</li>
          </ol>
          <p className="mt-3 text-xs">Keep the key private. The .env file stays on your computer and is not uploaded anywhere except to Anthropic with each request.</p>
        </>
      )}
    </section>
  )
}

function Sources({ items }) {
  if (!items?.length) return null
  return (
    <div className="flex flex-wrap items-center gap-1.5 pt-1">
      <span className="label mr-1">Based on</span>
      {items.map((s, i) => {
        const to = s.qid ? `/cn/units/${s.unit}?tab=questions#q${s.qid}` : s.deck ? `/studio/${s.deck}` : s.unit ? `/cn/units/${s.unit}` : null
        const chip = <span className="rounded-full border border-line bg-surface px-2 py-0.5 text-xs text-muted hover:text-ink">{s.ref}</span>
        return to ? (
          <a key={i} href={to}>
            {chip}
          </a>
        ) : (
          <span key={i}>{chip}</span>
        )
      })}
    </div>
  )
}

export default function Ask() {
  const { subjects, health } = useApp()
  const [params] = useSearchParams()
  const [subjectId, setSubjectId] = useState(params.get('subject') || 'cn')
  const [unit, setUnit] = useState(params.get('unit') || '')
  const [units, setUnits] = useState([])
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [busy, setBusy] = useState(false)
  const abortRef = useRef(null)
  const endRef = useRef(null)
  const askedQid = useRef(null)
  const showSetup = params.get('setup') === '1' || (health && !health.ai.available)

  useEffect(() => {
    api.subject('cn').then((s) => setUnits(s.units))
  }, [])

  const send = async (text, qid) => {
    const question = (text ?? input).trim()
    if (!question || busy) return
    setInput('')
    const history = messages.filter((m) => !m.error).map((m) => ({ role: m.role, content: m.content }))
    setMessages((m) => [...m, { role: 'user', content: question }, { role: 'assistant', content: '', sources: [], pending: true }])
    setBusy(true)
    const ctrl = new AbortController()
    abortRef.current = ctrl
    const patch = (fn) =>
      setMessages((m) => {
        const copy = [...m]
        copy[copy.length - 1] = fn(copy[copy.length - 1])
        return copy
      })
    try {
      await askStream(
        { question, subject_id: subjectId, unit: unit ? Number(unit) : null, question_id: qid || null, history },
        (ev) => {
          if (ev.type === 'sources') patch((a) => ({ ...a, sources: ev.items }))
          else if (ev.type === 'mode') patch((a) => ({ ...a, mode: ev.mode }))
          else if (ev.type === 'delta') patch((a) => ({ ...a, content: a.content + ev.text }))
          else if (ev.type === 'error') patch((a) => ({ ...a, error: ev.message }))
        },
        ctrl.signal,
      )
    } catch (e) {
      if (e.name !== 'AbortError') patch((a) => ({ ...a, error: e.message }))
    } finally {
      patch((a) => ({ ...a, pending: false }))
      setBusy(false)
    }
  }

  // "Ask AI" on a question card lands here with ?qid=; ask about it straight away.
  useEffect(() => {
    const qid = params.get('qid')
    if (qid && askedQid.current !== qid) {
      askedQid.current = qid
      send(`Explain Q${qid} step by step, the way I should write it in the exam.`, Number(qid))
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params])

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [messages])

  const subject = subjects.find((s) => s.id === subjectId)
  const starters = subjectId === 'cn' ? STARTERS.cn : STARTERS.other

  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Ask AI"
        title="Ask a doubt"
        actions={
          messages.length > 0 && (
            <Button variant="quiet" onClick={() => setMessages([])} disabled={busy}>
              New conversation
            </Button>
          )
        }
      >
        Answers are grounded in your notes, the solved practice book and anything you uploaded to Notes Studio, with links to the questions they used.
      </PageHeader>

      {showSetup && health && <KeySetup available={health.ai.available} />}

      <div className="flex flex-wrap gap-3">
        <label className="flex items-center gap-2 text-sm">
          <span className="label">Subject</span>
          <select id="ask-subject" value={subjectId} onChange={(e) => setSubjectId(e.target.value)} className="rounded-lg border border-line bg-surface px-2.5 py-1.5">
            {subjects.map((s) => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
        </label>
        {subjectId === 'cn' && (
          <label className="flex items-center gap-2 text-sm">
            <span className="label">Focus</span>
            <select id="ask-unit" value={unit} onChange={(e) => setUnit(e.target.value)} className="rounded-lg border border-line bg-surface px-2.5 py-1.5">
              <option value="">All units</option>
              {units.map((u) => (
                <option key={u.id} value={u.id}>Unit {u.id}: {u.title}</option>
              ))}
            </select>
          </label>
        )}
      </div>

      <div className="space-y-5">
        {messages.length === 0 && (
          <div className="space-y-2">
            <p className="text-sm text-muted">Try one of these{subject && subjectId !== 'cn' ? ` for ${subject.name}` : ''}:</p>
            <div className="grid gap-2 sm:grid-cols-2">
              {starters.map((s) => (
                <button key={s} type="button" onClick={() => send(s)} className="cursor-pointer rounded-lg border border-line bg-surface px-3 py-2.5 text-left text-sm hover:border-accent">
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map((m, i) =>
          m.role === 'user' ? (
            <div key={i} className="flex justify-end">
              <p className="max-w-[85%] rounded-2xl rounded-br-sm bg-ink px-4 py-2.5 whitespace-pre-wrap text-bg">{m.content}</p>
            </div>
          ) : (
            <div key={i} className="space-y-2 rounded-2xl rounded-bl-sm border border-line bg-surface px-4 py-3 sm:px-5">
              <div className="flex items-center gap-2">
                <span className="label">{m.mode === 'offline' ? 'From your material' : 'Claude'}</span>
                {m.mode === 'offline' && <Pill tone="warn">AI offline</Pill>}
              </div>
              {m.content ? <Markdown>{m.content}</Markdown> : m.pending && !m.error && <p className="animate-pulse text-sm text-muted">Reading your notes…</p>}
              {m.error && <p className="text-sm text-bad">{m.error}</p>}
              {!m.pending && <Sources items={m.sources} />}
            </div>
          ),
        )}
        <div ref={endRef} />
      </div>

      <form
        onSubmit={(e) => {
          e.preventDefault()
          send()
        }}
        className="sticky bottom-3 flex items-end gap-2 rounded-2xl border border-line bg-surface p-2 shadow-lg shadow-black/5"
      >
        <textarea
          id="ask-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              send()
            }
          }}
          rows={2}
          placeholder="Ask anything, e.g. Why does TCP need a 3-way handshake? or Solve Q245"
          className="min-h-11 flex-1 resize-none bg-transparent px-2 py-1.5 text-sm outline-none"
          aria-label="Your question"
        />
        {busy ? (
          <Button onClick={() => abortRef.current?.abort()}>Stop</Button>
        ) : (
          <Button type="submit" variant="primary" disabled={!input.trim()}>
            Ask
          </Button>
        )}
      </form>
      {subjectId !== 'cn' && subject && subject.deck_count === 0 && (
        <p className="text-sm text-muted">
          {subject.name} has no uploaded notes yet, so answers will come from general knowledge.{' '}
          <Link to={`/studio?subject=${subjectId}`} className="text-accent underline">Upload notes</Link>
        </p>
      )}
    </div>
  )
}
