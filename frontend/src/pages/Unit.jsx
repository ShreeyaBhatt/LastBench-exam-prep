import { useEffect, useMemo, useState } from 'react'
import { Link, useParams, useSearchParams } from 'react-router-dom'
import QuestionCard from '../components/QuestionCard'
import { Button, Empty, FibreDot, LinkButton, Markdown, ProgressBar, Segmented, Spinner, cx } from '../components/ui'
import { api, unitPdfUrl } from '../lib/api'
import { unitStats, useApp } from '../lib/store'

function UnitSwitcher({ current }) {
  const [units, setUnits] = useState([])
  useEffect(() => {
    api.subject('cn').then((s) => setUnits(s.units))
  }, [])
  return (
    <nav aria-label="Units" className="-mx-1 flex gap-1 overflow-x-auto pb-1">
      {units.map((u) => (
        <Link
          key={u.id}
          to={`/cn/units/${u.id}`}
          className={cx(
            'flex shrink-0 items-center gap-1.5 rounded-full border px-3 py-1 text-xs',
            u.id === current ? 'border-ink bg-ink text-bg' : 'border-line bg-surface text-muted hover:text-ink',
          )}
          title={u.title}
        >
          <FibreDot colour={u.colour} size={8} />
          Unit {u.id}
        </Link>
      ))}
    </nav>
  )
}

function Notes({ unit }) {
  const n = unit.notes
  return (
    <div className="space-y-8">
      <p className="max-w-[68ch] text-lg">{n.summary}</p>
      <div className="flex flex-wrap gap-1.5">
        <span className="label mr-1 self-center">Syllabus</span>
        {unit.topics.map((t) => (
          <Link key={t.code} to={`/cn/units/${unit.id}?tab=questions&topic=${t.code}`} className="rounded-full border border-line bg-surface px-2.5 py-1 text-xs text-muted hover:text-ink" title={t.title}>
            <span className="font-mono">{t.code}</span> {t.title.length > 42 ? `${t.title.slice(0, 40)}…` : t.title}
          </Link>
        ))}
      </div>
      <div className="grid gap-x-10 gap-y-7 md:grid-cols-2">
        {n.sections.map((s) => (
          <section key={s.h}>
            <h3 className="mb-2 flex items-center gap-2 text-base font-bold">
              <FibreDot colour={unit.colour} size={8} />
              {s.h}
            </h3>
            <ul className="space-y-1.5 text-[0.95rem]">
              {s.points.map((p, i) => (
                <li key={i} className="flex gap-2">
                  <span className="mt-[0.6em] h-1 w-1 shrink-0 rounded-full bg-faint" />
                  <Markdown className="min-w-0">{p}</Markdown>
                </li>
              ))}
            </ul>
          </section>
        ))}
      </div>

      {n.formulas.length > 0 && (
        <section>
          <h3 className="mb-2 text-base font-bold">Formulas and rules</h3>
          <div className="overflow-x-auto rounded-xl border border-line bg-surface">
            <table className="w-full text-sm">
              <tbody>
                {n.formulas.map(([name, expr]) => (
                  <tr key={name} className="border-b border-line last:border-0">
                    <th scope="row" className="w-2/5 px-4 py-2.5 text-left align-top font-medium">{name}</th>
                    <td className="px-4 py-2.5 font-mono text-[0.85rem]">{expr}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}

      <section className="rounded-xl border border-warn/40 bg-warn-soft p-4">
        <h3 className="mb-2 text-base font-bold text-warn">Exam traps</h3>
        <ul className="space-y-1.5 text-[0.95rem]">
          {n.traps.map((t) => (
            <li key={t} className="flex gap-2">
              <span className="font-bold text-warn">!</span>
              <span>{t}</span>
            </li>
          ))}
        </ul>
      </section>
      <p className="text-xs text-muted">Source: {unit.source}</p>
    </div>
  )
}

function Questions({ unit }) {
  const { progress } = useApp()
  const [params, setParams] = useSearchParams()
  const topic = unit.topics.find((t) => t.code === params.get('topic'))
  const [kind, setKind] = useState('all')
  const [state, setState] = useState('all')
  const [query, setQuery] = useState('')

  const list = useMemo(() => {
    const t = query.trim().toLowerCase()
    return unit.questions.filter((q) => {
      const p = progress[`cn:${q.id}`] || {}
      if (topic && !topic.questions.includes(q.id)) return false
      if (kind !== 'all' && q.kind !== kind) return false
      if (state === 'todo' && p.status) return false
      if (state === 'revise' && p.status !== 'wrong') return false
      if (state === 'saved' && !p.bookmarked) return false
      if (t && !(`q${q.id} ${q.text} ${q.options.join(' ')}`.toLowerCase().includes(t))) return false
      return true
    })
  }, [unit, progress, kind, state, query, topic])

  useEffect(() => {
    if (!window.location.hash) return
    const t = setTimeout(() => document.querySelector(window.location.hash)?.scrollIntoView({ block: 'start' }), 50)
    return () => clearTimeout(t)
  }, [unit])

  const count = (k) => unit.questions.filter((q) => k === 'all' || q.kind === k).length
  return (
    <div className="space-y-4">
      {topic && (
        <div className="flex flex-wrap items-center gap-2 rounded-lg bg-accent-soft px-3 py-2 text-sm text-accent">
          Showing syllabus topic <b>{topic.code}</b>: {topic.title}
          <button type="button" className="ml-auto cursor-pointer underline" onClick={() => setParams({ tab: 'questions' }, { replace: true })}>
            Show all
          </button>
        </div>
      )}
      <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <Segmented
          label="Question type"
          value={kind}
          onChange={setKind}
          options={[
            { value: 'all', label: 'All', count: count('all') },
            { value: 'mcq', label: 'MCQ', count: count('mcq') },
            { value: 'numerical', label: 'Numerical', count: count('numerical') },
            { value: 'theory', label: 'Theory', count: count('theory') },
          ].filter((o) => o.count > 0)}
        />
        <Segmented
          label="Progress filter"
          value={state}
          onChange={setState}
          options={[
            { value: 'all', label: 'Any' },
            { value: 'todo', label: 'Not tried' },
            { value: 'revise', label: 'To revise' },
            { value: 'saved', label: 'Saved' },
          ]}
        />
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <input
          id="unit-search"
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search this unit, e.g. CRC or Q146"
          className="min-w-0 flex-1 rounded-lg border border-line bg-surface px-3 py-2 text-sm"
        />
        <span className="tabular text-sm text-muted">{list.length} shown</span>
      </div>
      {list.length === 0 ? (
        <Empty title="No questions match">Change the filters or clear the search.</Empty>
      ) : (
        <div className="space-y-4">
          {list.map((q) => (
            <QuestionCard key={q.id} q={q} colour={unit.accent} />
          ))}
        </div>
      )}
    </div>
  )
}

export default function Unit() {
  const { id } = useParams()
  const [params, setParams] = useSearchParams()
  const tab = params.get('tab') === 'questions' ? 'questions' : 'notes'
  const [unit, setUnit] = useState(null)
  const [err, setErr] = useState('')
  const { progress } = useApp()

  useEffect(() => {
    setUnit(null)
    setErr('')
    api.unit(id).then(setUnit).catch((e) => setErr(e.message))
    try {
      localStorage.setItem('lastUnit', String(id))
    } catch {
      /* storage blocked */
    }
  }, [id])

  if (err) return <Empty title="Could not load this unit">{err}</Empty>
  if (!unit) return <Spinner label="Loading unit" />

  const s = unitStats(progress, unit.qids)
  const go = (t) => setParams(t === 'notes' ? {} : { tab: t }, { replace: true })

  return (
    <div className="space-y-6">
      <UnitSwitcher current={unit.id} />
      <header className="space-y-4 border-b border-line pb-6">
        <div className="flex items-center gap-2">
          <FibreDot colour={unit.colour} size={12} />
          <span className="label">
            Unit {unit.id} · {unit.test} · {unit.weight}% of syllabus · {unit.hours} teaching hours
          </span>
        </div>
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <h1 className="display text-3xl font-bold md:text-4xl">{unit.title}</h1>
          <div className="flex flex-wrap gap-2">
            <Link to={`/ask?unit=${unit.id}`} className="rounded-lg border border-line bg-surface px-3.5 py-2 text-sm font-medium hover:bg-sunken">
              Ask AI about this unit
            </Link>
            <LinkButton href={unitPdfUrl(unit.id)} download>
              Download PDF
            </LinkButton>
          </div>
        </div>
        <div className="max-w-md space-y-1">
          <ProgressBar value={s.done} total={s.total} colour={unit.accent} />
          <p className="tabular text-xs text-muted">
            {s.done} of {s.total} attempted · {s.correct} right · {s.wrong} to revise
          </p>
        </div>
      </header>

      <div role="tablist" aria-label="Unit sections" className="flex gap-6 border-b border-line">
        {[
          ['notes', 'One-minute notes'],
          ['questions', `Questions (${unit.questions.length})`],
        ].map(([k, label]) => (
          <button
            key={k}
            role="tab"
            type="button"
            aria-selected={tab === k}
            onClick={() => go(k)}
            className={cx(
              '-mb-px cursor-pointer border-b-2 pb-2.5 text-sm font-medium',
              tab === k ? 'border-ink text-ink' : 'border-transparent text-muted hover:text-ink',
            )}
          >
            {label}
          </button>
        ))}
      </div>

      {tab === 'notes' ? (
        <>
          <Notes unit={unit} />
          <div className="flex justify-end">
            <Button variant="primary" onClick={() => go('questions')}>
              Practise the {unit.questions.length} questions →
            </Button>
          </div>
        </>
      ) : (
        <Questions unit={unit} />
      )}
    </div>
  )
}
