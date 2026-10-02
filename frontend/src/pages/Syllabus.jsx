import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { FibreDot, PageHeader, ProgressBar, Spinner, cx } from '../components/ui'
import { api } from '../lib/api'
import { unitStats, useApp } from '../lib/store'

export default function Syllabus() {
  const { progress, setProgress } = useApp()
  const [syl, setSyl] = useState(null)
  useEffect(() => {
    api.syllabus().then(setSyl)
  }, [])
  if (!syl) return <Spinner />

  const allTopics = syl.units.flatMap((u) => u.topics)
  const ticked = allTopics.filter((t) => progress[`syl:${t.code}`]?.status === 'done').length

  return (
    <div className="space-y-8">
      <PageHeader eyebrow="LJU · Sem V · Batch 2024" title="Syllabus tracker">
        Every topic in the official syllabus, with its weightage, the questions that cover it, and a box to tick once you have revised it.
      </PageHeader>

      <div className="max-w-md space-y-1">
        <ProgressBar value={ticked} total={allTopics.length} colour="var(--good)" />
        <p className="tabular text-sm text-muted">{ticked} of {allTopics.length} topics revised</p>
      </div>

      {['T1', 'T2'].map((t) => (
        <section key={t} className="space-y-4">
          <div className="flex flex-wrap items-baseline gap-x-3">
            <h2 className="text-2xl font-bold">{t}</h2>
            <span className="tabular text-sm text-muted">
              Units {syl.tests[t].units.join(', ')} · {syl.tests[t].share}% of syllabus · 20 MCQ + 5 descriptive + 25 numerical
            </span>
          </div>
          {syl.units
            .filter((u) => u.test === t)
            .map((u) => {
              const s = unitStats(progress, u.qids)
              return (
                <div key={u.id} className="overflow-hidden rounded-xl border border-line bg-surface">
                  <Link to={`/cn/units/${u.id}`} className="flex flex-wrap items-center gap-x-3 gap-y-1 border-b border-line px-4 py-3 hover:bg-sunken">
                    <FibreDot colour={u.colour} />
                    <span className="font-semibold">Unit {u.id}: {u.title}</span>
                    <span className="tabular ml-auto text-xs text-muted">
                      {u.weight}% · {u.hours} teaching hours · {s.done}/{s.total} attempted
                    </span>
                  </Link>
                  <ul className="divide-y divide-line">
                    {u.topics.map((tp) => {
                      const key = `syl:${tp.code}`
                      const done = progress[key]?.status === 'done'
                      const tried = tp.questions.filter((id) => progress[`cn:${id}`]?.status).length
                      return (
                        <li key={tp.code} className="flex flex-wrap items-center gap-x-3 gap-y-1 px-4 py-2.5">
                          <input
                            id={`syl-${tp.code}`}
                            type="checkbox"
                            checked={done}
                            onChange={() => setProgress(key, { status: done ? null : 'done' })}
                            className="h-4 w-4 accent-[var(--good)]"
                            aria-label={`Mark ${tp.code} revised`}
                          />
                          <label htmlFor={`syl-${tp.code}`} className={cx('min-w-0 flex-1 cursor-pointer text-sm', done && 'text-muted line-through')}>
                            <span className="mr-2 font-mono text-xs text-muted">{tp.code}</span>
                            {tp.title}
                          </label>
                          <Link to={`/cn/units/${u.id}?tab=questions&topic=${tp.code}`} className="tabular text-xs text-accent hover:underline">
                            {tp.questions.length} questions · {tried} tried
                          </Link>
                        </li>
                      )
                    })}
                  </ul>
                </div>
              )
            })}
        </section>
      ))}

      <section className="grid gap-4 md:grid-cols-2">
        <div className="rounded-xl border border-line bg-surface p-4">
          <h2 className="font-bold">Evaluation scheme</h2>
          <table className="mt-2 w-full text-sm">
            <tbody>
              {syl.evaluation.map(([k, pct, marks]) => (
                <tr key={k} className="border-b border-line last:border-0">
                  <td className="py-1.5">{k}</td>
                  <td className="tabular py-1.5 text-right text-muted">{pct}</td>
                  <td className="tabular py-1.5 text-right font-medium">{marks}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className="mt-2 text-xs text-muted">Theory 100 marks (T1 + T2, 50 each) and practical 100 marks (projects): 200 in total.</p>
        </div>
        <div className="rounded-xl border border-line bg-surface p-4">
          <h2 className="font-bold">Course outcomes</h2>
          <ul className="mt-2 space-y-1.5 text-sm">
            {syl.outcomes.map(([k, v]) => (
              <li key={k}>
                <span className="font-mono text-xs font-semibold text-muted">{k}</span> {v}
              </li>
            ))}
          </ul>
          <h2 className="mt-4 font-bold">Reference books</h2>
          <ol className="mt-1 list-decimal pl-5 text-sm text-muted">
            {syl.books.map((b) => (
              <li key={b}>{b}</li>
            ))}
          </ol>
        </div>
      </section>
    </div>
  )
}
