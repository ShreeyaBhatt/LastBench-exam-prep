import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { FibreDot, Pill, ProgressBar, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { daysUntil, unitStats, useApp } from '../lib/store'

function UnitCard({ u, s }) {
  return (
    <Link to={`/cn/units/${u.id}`} className="group flex h-full flex-col gap-3 rounded-xl border border-line bg-surface p-4 transition-colors hover:border-ink/40">
      <div className="flex items-center gap-2">
        <FibreDot colour={u.colour} />
        <span className="label">Unit {u.id}</span>
        <span className="tabular ml-auto text-xs text-muted">{u.weight}% · {u.hours} h</span>
      </div>
      <div>
        <h3 className="text-lg leading-snug font-semibold group-hover:text-accent">{u.title}</h3>
        <p className="mt-1 line-clamp-2 text-sm text-muted">{u.summary}</p>
      </div>
      <div className="mt-auto space-y-1.5">
        <ProgressBar value={s.done} total={s.total} colour={u.accent} />
        <div className="tabular flex justify-between text-xs text-muted">
          <span>{u.counts.numerical} numerical · {u.counts.mcq} MCQ · {u.counts.theory} theory</span>
          <span>{s.done}/{s.total}</span>
        </div>
      </div>
    </Link>
  )
}

export default function Course() {
  const { progress, settings } = useApp()
  const [cn, setCn] = useState(null)
  const [syl, setSyl] = useState(null)
  useEffect(() => {
    api.subject('cn').then(setCn).catch(() => {})
    api.syllabus().then(setSyl).catch(() => {})
  }, [])

  if (!cn || !syl) return <Spinner label="Loading the course" />

  const stats = cn.units.map((u) => ({ u, s: unitStats(progress, u.qids) }))
  const done = stats.reduce((a, x) => a + x.s.done, 0)
  const total = stats.reduce((a, x) => a + x.s.total, 0)
  const next = stats.find((x) => x.s.done < x.s.total) || stats[0]

  return (
    <div className="space-y-10">
      <section className="space-y-4">
        <div className="label">{cn.term} · LJU syllabus, batch 2024</div>
        <h1 className="display text-4xl leading-[1.05] font-bold md:text-5xl">Computer Networks</h1>
        <p className="max-w-2xl text-muted">
          {total} questions with worked solutions: the full practice book plus extra questions for syllabus topics it skips. You have attempted {done}.
        </p>
        <div className="flex flex-wrap gap-2">
          <Link to={`/cn/units/${next.u.id}`} className="rounded-lg bg-accent px-4 py-2 text-sm font-medium text-accent-ink hover:brightness-110">
            {done ? 'Continue' : 'Start'} with Unit {next.u.id}
          </Link>
          <Link to="/cn/mock" className="rounded-lg border border-line bg-surface px-4 py-2 text-sm font-medium hover:bg-sunken">Take a mock paper</Link>
          <Link to="/cn/syllabus" className="rounded-lg border border-line bg-surface px-4 py-2 text-sm font-medium hover:bg-sunken">Syllabus tracker</Link>
        </div>
      </section>

      <section className="rounded-xl border border-line bg-surface p-4 sm:p-5">
        <h2 className="text-lg font-bold">How the tests are marked</h2>
        <p className="mt-1 text-sm text-muted">Each test is 50 marks. Numericals are half the paper, so practise them first.</p>
        <div className="mt-3 grid gap-3 sm:grid-cols-3">
          {[
            ['MCQ', 20, 'var(--accent)'],
            ['Descriptive', 5, 'var(--faint)'],
            ['Numerical', 25, 'var(--good)'],
          ].map(([k, v, c]) => (
            <div key={k} className="rounded-lg bg-sunken px-3 py-2.5">
              <div className="flex items-baseline justify-between">
                <span className="text-sm font-medium">{k}</span>
                <span className="tabular display text-2xl font-bold">{v}</span>
              </div>
              <div className="mt-1.5 h-1.5 rounded-full bg-bg">
                <div className="h-full rounded-full" style={{ width: `${(v / 50) * 100}%`, background: c }} />
              </div>
            </div>
          ))}
        </div>
      </section>

      {['T1', 'T2'].map((t) => {
        const spec = syl.tests[t]
        const date = settings[`exam:cn-${t.toLowerCase()}`]
        const left = daysUntil(date)
        return (
          <section key={t} className="space-y-3">
            <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
              <h2 className="text-xl font-bold">{t}: Units {spec.units[0]}–{spec.units[spec.units.length - 1]}</h2>
              <span className="tabular text-sm text-muted">{spec.share}% of the syllabus · 50 marks · {spec.duration_min / 60} h</span>
              {date && left >= 0 ? (
                <Pill tone={left <= 7 ? 'warn' : 'accent'}>{left === 0 ? 'Today' : `In ${left} day${left > 1 ? 's' : ''}`}</Pill>
              ) : (
                <Link to="/plan" className="text-sm text-accent underline">Set {t} date</Link>
              )}
            </div>
            <ol className="grid gap-3 sm:grid-cols-2">
              {stats
                .filter(({ u }) => spec.units.includes(u.id))
                .map(({ u, s }) => (
                  <li key={u.id}>
                    <UnitCard u={u} s={s} />
                  </li>
                ))}
            </ol>
          </section>
        )
      })}
      <p className="text-xs text-muted">Unit colours follow the fibre-optic strand code: 1 blue, 2 orange, 3 green, 4 brown, 5 slate, 6 white, 7 red, 8 black, 9 yellow, 10 violet.</p>
    </div>
  )
}
