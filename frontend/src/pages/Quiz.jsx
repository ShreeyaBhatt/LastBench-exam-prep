import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import QuestionCard from '../components/QuestionCard'
import { Button, FibreDot, PageHeader, Segmented, Spinner, cx } from '../components/ui'
import { api } from '../lib/api'

export default function Quiz() {
  const [params] = useSearchParams()
  const [mode, setMode] = useState(params.get('smart') === '0' ? 'units' : 'smart')
  const [units, setUnits] = useState([])
  const [picked, setPicked] = useState([])
  const [n, setN] = useState(10)
  const [qs, setQs] = useState(null)
  const [idx, setIdx] = useState(0)
  const [answers, setAnswers] = useState({})
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    api.subject('cn').then((s) => setUnits(s.units))
  }, [])

  const start = async () => {
    setLoading(true)
    const list = mode === 'smart' ? await api.smartQuiz(n) : await api.quiz(picked, n)
    setQs(list)
    setIdx(0)
    setAnswers({})
    setLoading(false)
  }

  const colourOf = (u) => units.find((x) => x.id === u)?.accent

  if (loading) return <Spinner label="Picking questions" />

  if (qs && idx < qs.length) {
    const q = qs[idx]
    const answered = q.id in answers
    return (
      <div className="space-y-5">
        <div className="flex items-center justify-between gap-3">
          <span className="label tabular">
            Question {idx + 1} of {qs.length} · Unit {q.unit}
          </span>
          <Button variant="quiet" onClick={() => setQs(null)}>Quit quiz</Button>
        </div>
        <div className="flex gap-1" aria-hidden="true">
          {qs.map((x, i) => (
            <span
              key={x.id}
              className={cx(
                'h-1.5 flex-1 rounded-full',
                x.id in answers ? (answers[x.id] ? 'bg-good' : 'bg-bad') : i === idx ? 'bg-ink' : 'bg-sunken',
              )}
            />
          ))}
        </div>
        <QuestionCard key={q.id} q={q} colour={colourOf(q.unit)} quizMode onAnswer={(ok) => setAnswers((a) => ({ ...a, [q.id]: ok }))} />
        <div className="flex justify-end">
          <Button variant="primary" disabled={!answered} onClick={() => setIdx(idx + 1)}>
            {idx + 1 === qs.length ? 'See score' : 'Next question'}
          </Button>
        </div>
      </div>
    )
  }

  if (qs) {
    const score = Object.values(answers).filter(Boolean).length
    const missed = qs.filter((q) => answers[q.id] === false)
    return (
      <div className="space-y-6">
        <PageHeader eyebrow="Quiz finished" title={`You scored ${score} / ${qs.length}`}>
          {score === qs.length ? 'Perfect run.' : `${missed.length} to revise. They are marked "Revise" in their units.`}
        </PageHeader>
        {missed.length > 0 && (
          <ul className="space-y-2">
            {missed.map((q) => (
              <li key={q.id}>
                <a href={`/cn/units/${q.unit}?tab=questions#q${q.id}`} className="flex gap-3 rounded-lg border border-line bg-surface px-4 py-3 hover:border-ink/40">
                  <span className="font-mono text-sm font-semibold" style={{ color: colourOf(q.unit) }}>Q{q.id}</span>
                  <span className="text-sm">{q.text}</span>
                </a>
              </li>
            ))}
          </ul>
        )}
        <div className="flex gap-2">
          <Button variant="primary" onClick={start}>New quiz</Button>
          <Button onClick={() => setQs(null)}>Change units</Button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <PageHeader eyebrow="Practice" title="Quick quiz">
        Answer MCQs one at a time and see your score at the end. Smart mode adapts to you: questions you missed and units where your accuracy is low come up more often.
      </PageHeader>
      <Segmented
        label="Quiz mode"
        value={mode}
        onChange={setMode}
        options={[
          { value: 'smart', label: 'Smart (adapts to you)' },
          { value: 'units', label: 'Choose units' },
        ]}
      />
      {mode === 'units' && (
        <>
      <div className="space-y-2">
            <div className="flex items-baseline justify-between">
              <h2 className="font-semibold">Units</h2>
              <button type="button" className="cursor-pointer text-sm text-accent" onClick={() => setPicked(picked.length ? [] : units.map((u) => u.id))}>
                {picked.length ? 'Clear' : 'Select all'}
              </button>
            </div>
            <div className="grid gap-2 sm:grid-cols-2">
              {units.map((u) => {
                const on = picked.includes(u.id)
                return (
                  <label key={u.id} className={cx('flex cursor-pointer items-center gap-3 rounded-lg border px-3 py-2.5 text-sm', on ? 'border-ink bg-surface' : 'border-line bg-surface/60')}>
                    <input
                      id={`quiz-unit-${u.id}`}
                      type="checkbox"
                      checked={on}
                      onChange={() => setPicked(on ? picked.filter((x) => x !== u.id) : [...picked, u.id])}
                      className="accent-[var(--accent)]"
                    />
                    <FibreDot colour={u.colour} />
                    <span>Unit {u.id}: {u.title}</span>
                    <span className="tabular ml-auto text-xs text-muted">{u.counts.mcq} MCQ</span>
                  </label>
                )
              })}
            </div>
            <p className="text-xs text-muted">No units selected means all units.</p>
          </div>
        </>
      )}
      <div className="flex flex-wrap items-center gap-3">
        <span className="font-semibold">Questions</span>
        <Segmented label="Number of questions" value={n} onChange={setN} options={[5, 10, 20, 30].map((v) => ({ value: v, label: String(v) }))} />
      </div>
      <Button variant="primary" onClick={start}>Start quiz</Button>
    </div>
  )
}
