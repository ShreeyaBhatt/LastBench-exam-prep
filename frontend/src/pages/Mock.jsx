import { useEffect, useRef, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { Button, Markdown, PageHeader, Pill, Segmented, Spinner, cx } from '../components/ui'
import { api } from '../lib/api'
import { formatTime, useFocus } from '../lib/focus'
import { useApp } from '../lib/store'

const LETTERS = ['A', 'B', 'C', 'D']

const loadHistory = () => {
  try {
    return JSON.parse(localStorage.getItem('mocks') || '[]')
  } catch {
    return []
  }
}

function Setup({ onStart }) {
  const [params] = useSearchParams()
  const [test, setTest] = useState(params.get('test') === 'T2' ? 'T2' : 'T1')
  const [timed, setTimed] = useState(true)
  const history = loadHistory()
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="Exam practice" title="Mock T1 / T2 paper">
        A fresh 50-mark paper in the LJU pattern every time: 20 marks MCQ, 5 marks descriptive, 25 marks numerical, spread across units by their syllabus weight. Write the descriptive and numerical answers on paper, then mark yourself against the model answers.
      </PageHeader>
      <div className="grid gap-3 sm:grid-cols-2">
        {[
          ['T1', 'Units 1–4', '2 h 15 min', 'Intro, physical layer, DLL (LLC and MAC)'],
          ['T2', 'Units 5–10', '2 h 30 min', 'Network, routing, transport, application, design & monitoring'],
        ].map(([t, units, time, desc]) => (
          <button
            key={t}
            type="button"
            onClick={() => setTest(t)}
            className={cx('cursor-pointer rounded-xl border bg-surface p-4 text-left', test === t ? 'border-ink ring-1 ring-ink' : 'border-line hover:border-ink/40')}
          >
            <div className="flex items-baseline justify-between">
              <span className="display text-2xl font-bold">{t}</span>
              <span className="tabular text-sm text-muted">{time}</span>
            </div>
            <div className="mt-1 font-medium">{units}</div>
            <div className="text-sm text-muted">{desc}</div>
          </button>
        ))}
      </div>
      <div className="flex flex-wrap items-center gap-3">
        <Segmented label="Timing" value={timed} onChange={setTimed} options={[{ value: true, label: 'Timed (exam mode)' }, { value: false, label: 'Untimed' }]} />
        <Button variant="primary" onClick={() => onStart(test, timed)}>Start {test} paper</Button>
      </div>
      <p className="text-sm text-muted">Timed mode hides the navigation (focus mode) and submits automatically when time runs out.</p>
      {history.length > 0 && (
        <section>
          <h2 className="mb-2 font-bold">Past attempts</h2>
          <ul className="divide-y divide-line rounded-xl border border-line bg-surface">
            {history.slice(0, 8).map((h, i) => (
              <li key={i} className="tabular flex items-center gap-3 px-4 py-2 text-sm">
                <span className="font-semibold">{h.test}</span>
                <span className="text-muted">{new Date(h.at).toLocaleDateString()}</span>
                <span className="ml-auto font-semibold">{h.score} / {h.total}</span>
                <Pill tone={h.score >= 0.7 * h.total ? 'good' : h.score >= 0.4 * h.total ? 'warn' : 'bad'}>{Math.round((h.score / h.total) * 100)}%</Pill>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  )
}

export default function Mock() {
  const { setProgress } = useApp()
  const { setFocusMode } = useFocus()
  const [paper, setPaper] = useState(null)
  const [loading, setLoading] = useState(false)
  const [answers, setAnswers] = useState({})
  const [selfMarks, setSelfMarks] = useState({})
  const [submitted, setSubmitted] = useState(false)
  const [deadline, setDeadline] = useState(null)
  const [left, setLeft] = useState(0)
  const submitRef = useRef(null)

  const start = async (test, timed) => {
    setLoading(true)
    const p = await api.mock(test)
    setPaper(p)
    setAnswers({})
    setSelfMarks({})
    setSubmitted(false)
    setDeadline(timed ? Date.now() + p.duration_min * 60000 : null)
    setLoading(false)
    if (timed) setFocusMode(true)
    window.scrollTo(0, 0)
  }

  const submit = () => {
    if (!paper || submitted) return
    setSubmitted(true)
    setDeadline(null)
    setFocusMode(false)
    for (const q of paper.sections[0].questions) {
      if (answers[q.id]) setProgress(`cn:${q.id}`, { status: answers[q.id] === q.answer ? 'correct' : 'wrong' })
    }
    window.scrollTo(0, 0)
  }
  submitRef.current = submit

  useEffect(() => {
    if (!deadline) return
    const tick = () => {
      const s = Math.max(0, Math.round((deadline - Date.now()) / 1000))
      setLeft(s)
      if (s === 0) submitRef.current()
    }
    tick()
    const t = setInterval(tick, 1000)
    return () => clearInterval(t)
  }, [deadline])

  useEffect(() => () => setFocusMode(false), [setFocusMode])

  if (loading) return <Spinner label="Setting your paper" />
  if (!paper) return <Setup onStart={start} />

  const [mcq, theory, numerical] = paper.sections
  const mcqScore = mcq.questions.reduce((a, q) => a + (answers[q.id] === q.answer ? q.marks : 0), 0)
  const selfScore = [...theory.questions, ...numerical.questions].reduce((a, q) => a + (Number(selfMarks[q.id]) || 0), 0)
  const score = mcqScore + selfScore
  const answered = mcq.questions.filter((q) => answers[q.id]).length

  const saveResult = () => {
    const h = [{ test: paper.test, at: Date.now(), score, total: paper.total, mcq: mcqScore }, ...loadHistory()].slice(0, 30)
    try {
      localStorage.setItem('mocks', JSON.stringify(h))
    } catch {
      /* ignore */
    }
    setPaper(null)
  }

  let n = 0
  return (
    <div className="space-y-8">
      <header className="sticky top-14 z-10 -mx-4 flex flex-wrap items-center gap-3 border-b border-line bg-bg/95 px-4 py-3 backdrop-blur sm:-mx-6 sm:px-6 lg:top-0">
        <span className="display text-xl font-bold">Mock {paper.test}</span>
        <span className="tabular text-sm text-muted">{paper.total} marks · Units {paper.units.join(', ')}</span>
        {!submitted && deadline && (
          <span className={cx('tabular rounded-full px-3 py-1 font-mono text-sm font-semibold', left < 600 ? 'bg-bad-soft text-bad' : 'bg-accent-soft text-accent')}>
            {Math.floor(left / 3600)}:{formatTime(left % 3600)}
          </span>
        )}
        <div className="ml-auto flex gap-2">
          {!submitted ? (
            <Button variant="primary" onClick={submit}>Submit paper ({answered}/{mcq.questions.length} MCQ answered)</Button>
          ) : (
            <Button variant="primary" onClick={saveResult}>Save score and finish</Button>
          )}
        </div>
      </header>

      {submitted && (
        <section className="rounded-xl border border-line bg-surface p-5">
          <div className="label">Your score</div>
          <div className="tabular display mt-1 text-5xl font-bold">
            {score}
            <span className="text-2xl text-muted"> / {paper.total}</span>
          </div>
          <p className="mt-2 text-sm text-muted">
            MCQ {mcqScore}/{mcq.marks} (auto-marked) · Descriptive and numerical {selfScore}/{theory.marks + numerical.marks} (enter your own marks below by comparing with the model answers).
          </p>
        </section>
      )}

      {paper.sections.map((sec) => (
        <section key={sec.kind} className="space-y-4">
          <div className="flex items-baseline justify-between border-b border-line pb-2">
            <h2 className="text-xl font-bold">{sec.title}</h2>
            <span className="tabular text-sm text-muted">{sec.marks} marks</span>
          </div>
          {sec.kind !== 'mcq' && !submitted && <p className="text-sm text-muted">Solve these on paper with full working. Model answers appear after you submit.</p>}
          {sec.questions.map((q) => {
            n += 1
            const picked = answers[q.id]
            return (
              <article key={q.id} className="rounded-xl border border-line bg-surface p-4 sm:p-5">
                <div className="flex items-start gap-3">
                  <span className="tabular font-mono text-sm font-semibold text-muted">{n}.</span>
                  <div className="min-w-0 flex-1 space-y-3">
                    <div className="flex flex-wrap items-start justify-between gap-2">
                      <p className="max-w-[72ch] font-medium">{q.text}</p>
                      <span className="tabular shrink-0 text-xs text-muted">[{q.marks}] · Unit {q.unit} · Q{q.id}</span>
                    </div>
                    {q.diagram && <img src={q.diagram} alt="" className="max-h-56 rounded-lg border border-line bg-white p-2" />}
                    {sec.kind === 'mcq' && (
                      <div className="grid gap-2 sm:grid-cols-2">
                        {q.options.map((o, i) => {
                          const L = LETTERS[i]
                          const right = submitted && L === q.answer
                          const wrong = submitted && L === picked && L !== q.answer
                          return (
                            <label
                              key={L}
                              className={cx(
                                'flex cursor-pointer items-start gap-2 rounded-lg border px-3 py-2 text-sm',
                                right ? 'border-good bg-good-soft' : wrong ? 'border-bad bg-bad-soft' : picked === L ? 'border-accent bg-accent-soft' : 'border-line',
                              )}
                            >
                              <input
                                type="radio"
                                name={`m-${q.id}`}
                                id={`m-${q.id}-${L}`}
                                disabled={submitted}
                                checked={picked === L}
                                onChange={() => setAnswers({ ...answers, [q.id]: L })}
                                className="mt-1 accent-[var(--accent)]"
                              />
                              <span>
                                <span className="font-mono text-xs text-muted">{L}</span> {o}
                              </span>
                            </label>
                          )
                        })}
                      </div>
                    )}
                    {submitted && (
                      <div className="space-y-2 rounded-lg bg-sunken px-4 py-3">
                        <div className="flex flex-wrap items-center gap-3">
                          <span className="label">Model answer</span>
                          <span className="font-semibold text-good">{q.answer ? `${q.answer}. ${q.answer_text}` : q.answer_text}</span>
                          {sec.kind !== 'mcq' && (
                            <label className="ml-auto flex items-center gap-2 text-sm">
                              Your marks
                              <input
                                id={`self-${q.id}`}
                                type="number"
                                min={0}
                                max={q.marks}
                                step={0.5}
                                value={selfMarks[q.id] ?? ''}
                                onChange={(e) => setSelfMarks({ ...selfMarks, [q.id]: Math.min(q.marks, Math.max(0, Number(e.target.value))) })}
                                className="tabular w-16 rounded-md border border-line bg-surface px-2 py-1"
                              />
                              / {q.marks}
                            </label>
                          )}
                        </div>
                        <Markdown>{q.explanation}</Markdown>
                      </div>
                    )}
                  </div>
                </div>
              </article>
            )
          })}
        </section>
      ))}
      {!submitted ? (
        <Button variant="primary" onClick={submit}>Submit paper</Button>
      ) : (
        <div className="flex gap-2">
          <Button variant="primary" onClick={saveResult}>Save score and finish</Button>
          <Link to="/review" className="rounded-lg border border-line px-3.5 py-2 text-sm hover:bg-sunken">Review missed MCQs</Link>
        </div>
      )}
    </div>
  )
}
