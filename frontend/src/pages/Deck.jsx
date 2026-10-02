import { useCallback, useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import FlashCard from '../components/FlashCard'
import { Button, Empty, LinkButton, Markdown, Pill, ProgressBar, Segmented, Spinner, cx } from '../components/ui'
import { api, deckPdfUrl } from '../lib/api'
import { todayISO, useApp } from '../lib/store'

function Flashcards({ deck }) {
  const cards = deck.data.flashcards
  const prefix = `deck:${deck.id}:card:`
  const [states, setStates] = useState(null)
  const [mode, setMode] = useState('due')
  const [queue, setQueue] = useState([])
  const [flipped, setFlipped] = useState(false)
  const today = todayISO()

  useEffect(() => {
    api.reviewStates(prefix).then(setStates).catch(() => setStates({}))
  }, [prefix])

  const isDue = useCallback((i) => {
    const st = states?.[`${prefix}${i}`]
    return !st || st.due <= today
  }, [states, prefix, today])

  useEffect(() => {
    if (!states) return
    const all = cards.map((_, i) => i)
    setQueue(mode === 'due' ? all.filter(isDue) : all)
    setFlipped(false)
    // Rebuild only when the mode changes or the states first arrive.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mode, states === null])

  const current = queue[0]
  const grade = useCallback(
    (g) => {
      if (current === undefined) return
      api.review(`${prefix}${current}`, g).then((st) => setStates((s) => ({ ...s, [st.key]: st }))).catch(() => {})
      setFlipped(false)
      setQueue((q) => (g === 'again' ? [...q.slice(1), q[0]] : q.slice(1)))
    },
    [current, prefix],
  )

  if (!cards.length) return <Empty title="No flashcards in this pack" />
  if (!states) return <Spinner />
  const learned = cards.filter((_, i) => (states[`${prefix}${i}`]?.interval || 0) >= 1).length
  const dueCount = cards.filter((_, i) => isDue(i)).length

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <Segmented
          label="Cards to study"
          value={mode}
          onChange={setMode}
          options={[
            { value: 'due', label: 'Due today', count: dueCount },
            { value: 'all', label: 'All cards', count: cards.length },
          ]}
        />
        <Button variant="quiet" onClick={() => setQueue((q) => [...q].sort(() => Math.random() - 0.5))}>Shuffle</Button>
      </div>
      <div className="max-w-md space-y-1">
        <ProgressBar value={learned} total={cards.length} colour="var(--good)" />
        <p className="tabular text-xs text-muted">{learned} of {cards.length} cards learned · rate each card and it returns just before you would forget it</p>
      </div>
      {current === undefined ? (
        <Empty title={mode === 'due' ? 'Nothing due in this pack today' : 'You went through every card'}>
          {mode === 'due' ? 'Come back tomorrow, or switch to "All cards" to keep going.' : 'Shuffle or switch to "Due today".'}
        </Empty>
      ) : (
        <FlashCard card={cards[current]} flipped={flipped} setFlipped={setFlipped} onGrade={grade} />
      )}
    </div>
  )
}

function NotesTab({ data }) {
  return (
    <div className="space-y-8">
      <nav aria-label="Sections" className="flex flex-wrap gap-1.5">
        {data.sections.map((s, i) => (
          <a key={i} href={`#sec-${i}`} className="rounded-full border border-line bg-surface px-2.5 py-1 text-xs text-muted hover:text-ink">
            {s.heading}
          </a>
        ))}
      </nav>
      {data.sections.map((s, i) => (
        <section key={i} id={`sec-${i}`} className="scroll-mt-24 space-y-3">
          <h2 className="text-xl font-bold">{s.heading}</h2>
          <Markdown>{s.content_md}</Markdown>
          {s.key_points?.length > 0 && (
            <div className="max-w-[72ch] rounded-lg bg-sunken px-4 py-3">
              <div className="label mb-1.5">Key points</div>
              <ul className="space-y-1 text-sm">
                {s.key_points.map((p, j) => (
                  <li key={j} className="flex gap-2">
                    <span className="text-accent">•</span>
                    <span>{p}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      ))}
    </div>
  )
}

function ExamTab({ data }) {
  const [open, setOpen] = useState({})
  if (!data.exam_questions?.length) return <Empty title="No exam questions in this pack" />
  return (
    <ol className="space-y-3">
      {data.exam_questions.map((q, i) => (
        <li key={i} className="rounded-xl border border-line bg-surface">
          <div className="flex items-start gap-3 px-4 py-3">
            <span className="font-mono text-sm font-semibold text-accent">{i + 1}</span>
            <p className="flex-1 font-medium">{q.question}</p>
            <Pill>{q.marks} marks</Pill>
          </div>
          <div className="border-t border-line px-4 py-3">
            {open[i] ? (
              <Markdown>{q.answer_md}</Markdown>
            ) : (
              <Button variant="quiet" className="-ml-2" onClick={() => setOpen({ ...open, [i]: true })}>
                Show model answer
              </Button>
            )}
          </div>
        </li>
      ))}
    </ol>
  )
}

function TermsTab({ data }) {
  return (
    <div className="space-y-8">
      {data.key_terms?.length > 0 && (
        <section>
          <h2 className="mb-2 text-lg font-bold">Key terms</h2>
          <dl className="divide-y divide-line rounded-xl border border-line bg-surface">
            {data.key_terms.map((t) => (
              <div key={t.term} className="grid gap-1 px-4 py-2.5 sm:grid-cols-[14rem_1fr] sm:gap-4">
                <dt className="font-semibold">{t.term}</dt>
                <dd className="text-sm text-muted">{t.definition}</dd>
              </div>
            ))}
          </dl>
        </section>
      )}
      {data.formulas?.length > 0 && (
        <section>
          <h2 className="mb-2 text-lg font-bold">Formulas and rules</h2>
          <dl className="divide-y divide-line rounded-xl border border-line bg-surface">
            {data.formulas.map((f, i) => (
              <div key={i} className="px-4 py-2.5">
                <dt className="text-sm font-semibold">{f.name}</dt>
                <dd className="font-mono text-[0.85rem]">{f.expression}</dd>
                {f.note && <dd className="text-xs text-muted">{f.note}</dd>}
              </div>
            ))}
          </dl>
        </section>
      )}
      {!data.key_terms?.length && !data.formulas?.length && <Empty title="No key terms or formulas found" />}
    </div>
  )
}

export default function Deck() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { subjects, refreshSubjects } = useApp()
  const [deck, setDeck] = useState(null)
  const [err, setErr] = useState('')
  const [tab, setTab] = useState('notes')
  const [confirm, setConfirm] = useState(false)

  const load = useCallback(() => api.deck(id).then(setDeck).catch((e) => setErr(e.message)), [id])
  useEffect(() => {
    load()
  }, [load])
  useEffect(() => {
    if (deck?.status !== 'processing') return
    const t = setInterval(load, 3000)
    return () => clearInterval(t)
  }, [deck?.status, load])

  if (err) return <Empty title="Could not open this study pack">{err}</Empty>
  if (!deck) return <Spinner />

  const subject = subjects.find((s) => s.id === deck.subject_id)
  const data = deck.data

  const remove = async () => {
    await api.deleteDeck(deck.id)
    refreshSubjects()
    navigate(deck.subject_id === 'cn' ? '/studio' : `/subjects/${deck.subject_id}`)
  }

  return (
    <div className="space-y-6">
      <header className="space-y-3 border-b border-line pb-6">
        <div className="flex flex-wrap items-center gap-2">
          <Link to={deck.subject_id === 'cn' ? '/studio' : `/subjects/${deck.subject_id}`} className="label hover:text-ink">
            {subject?.name || deck.subject_id} · Notes Studio
          </Link>
          {deck.engine === 'claude' && <Pill tone="accent">By Claude</Pill>}
          {deck.engine === 'offline' && <Pill tone="warn">Offline draft</Pill>}
        </div>
        <h1 className="display text-3xl font-bold md:text-4xl">{data?.title || deck.title}</h1>
        {data?.summary && <p className="max-w-2xl text-muted">{data.summary}</p>}
        <p className="text-xs text-muted">From {deck.source_name}</p>
        <div className="flex flex-wrap gap-2 pt-1">
          {deck.status === 'ready' && (
            <>
              <LinkButton variant="primary" href={deckPdfUrl(deck.id)} download>
                Download PDF
              </LinkButton>
              <Link to={`/ask?subject=${deck.subject_id}`} className="rounded-lg border border-line bg-surface px-3.5 py-2 text-sm font-medium hover:bg-sunken">
                Ask AI about these notes
              </Link>
            </>
          )}
          {deck.status !== 'processing' && (
            <Button onClick={() => api.regenerate(deck.id).then(load)}>Regenerate</Button>
          )}
          {confirm ? (
            <span className="flex items-center gap-2 text-sm">
              Delete this pack?
              <Button variant="danger" onClick={remove}>Delete</Button>
              <Button variant="quiet" onClick={() => setConfirm(false)}>Keep</Button>
            </span>
          ) : (
            <Button variant="danger" onClick={() => setConfirm(true)}>Delete</Button>
          )}
        </div>
        {deck.engine === 'offline' && data?.notice && (
          <p className="max-w-2xl rounded-lg bg-bad-soft px-3 py-2 text-sm text-bad">Claude could not generate this pack: {data.notice}</p>
        )}
        {deck.engine === 'offline' && (
          <p className="max-w-2xl rounded-lg bg-warn-soft px-3 py-2 text-sm text-warn">
            This is an offline draft built by pattern-matching your file. <Link to="/ask?setup=1" className="underline">Add an API key</Link>, then press Regenerate for full notes written by Claude.
          </p>
        )}
      </header>

      {deck.status === 'processing' && <Spinner label="Generating notes and flashcards. This page updates on its own." />}
      {deck.status === 'failed' && <Empty title="Generation failed">{deck.error}</Empty>}

      {deck.status === 'ready' && data && (
        <>
          <div role="tablist" aria-label="Study pack sections" className="flex gap-5 overflow-x-auto border-b border-line">
            {[
              ['notes', `Notes (${data.sections.length})`],
              ['cards', `Flashcards (${data.flashcards.length})`],
              ['exam', `Exam questions (${data.exam_questions?.length || 0})`],
              ['terms', 'Key terms & formulas'],
            ].map(([k, label]) => (
              <button
                key={k}
                role="tab"
                type="button"
                aria-selected={tab === k}
                onClick={() => setTab(k)}
                className={cx('-mb-px shrink-0 cursor-pointer border-b-2 pb-2.5 text-sm font-medium', tab === k ? 'border-ink text-ink' : 'border-transparent text-muted hover:text-ink')}
              >
                {label}
              </button>
            ))}
          </div>
          {tab === 'notes' && <NotesTab data={data} />}
          {tab === 'cards' && <Flashcards deck={deck} />}
          {tab === 'exam' && <ExamTab data={data} />}
          {tab === 'terms' && <TermsTab data={data} />}
        </>
      )}
    </div>
  )
}
