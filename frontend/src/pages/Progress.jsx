import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { FibreDot, PageHeader, Pill, Segmented, Spinner } from '../components/ui'
import { api } from '../lib/api'

// Sequential blue ramp (one hue, light to dark); tokens flip for dark mode in index.css.
const level = (n) => (n === 0 ? 0 : n < 5 ? 1 : n < 15 ? 2 : n < 30 ? 3 : 4)

function Tooltip({ tip }) {
  if (!tip) return null
  return (
    <div
      role="tooltip"
      className="pointer-events-none absolute z-10 -translate-x-1/2 -translate-y-full rounded-md border border-line bg-surface px-2.5 py-1.5 text-xs whitespace-nowrap shadow-lg"
      style={{ left: tip.x, top: tip.y - 8 }}
    >
      {tip.lines.map((l, i) => (
        <div key={i} className={i === 0 ? 'font-semibold text-ink' : 'tabular text-muted'}>{l}</div>
      ))}
    </div>
  )
}

function Heatmap({ days }) {
  const [tip, setTip] = useState(null)
  // Columns are weeks (Mon-Sun), oldest on the left.
  const first = new Date(`${days[0].day}T00:00`)
  const pad = (first.getDay() + 6) % 7
  const cells = [...Array(pad).fill(null), ...days]
  const weeks = []
  for (let i = 0; i < cells.length; i += 7) weeks.push(cells.slice(i, i + 7))
  const fmt = (iso) => new Date(`${iso}T00:00`).toLocaleDateString(undefined, { weekday: 'short', day: 'numeric', month: 'short' })

  return (
    <div className="relative overflow-x-auto" onMouseLeave={() => setTip(null)}>
      <div className="inline-flex gap-1 pt-1">
        <div className="mr-1 grid grid-rows-7 gap-1 text-[0.65rem] text-muted">
          {['Mon', '', 'Wed', '', 'Fri', '', 'Sun'].map((d, i) => (
            <span key={i} className="h-3.5 leading-[0.875rem]">{d}</span>
          ))}
        </div>
        {weeks.map((w, wi) => (
          <div key={wi} className="grid grid-rows-7 gap-1">
            {Array.from({ length: 7 }, (_, di) => {
              const d = w[di]
              if (!d) return <span key={di} className="h-3.5 w-3.5" />
              const lv = level(d.items)
              const lines = [fmt(d.day), `${d.items} question${d.items === 1 ? '' : 's'} / cards`, d.questions ? `${d.correct} of ${d.questions} questions right` : null, d.focus_minutes ? `${Math.round(d.focus_minutes)} min focused` : null].filter(Boolean)
              return (
                <span
                  key={di}
                  role="img"
                  aria-label={lines.join(', ')}
                  onMouseEnter={(e) => {
                    const r = e.currentTarget.getBoundingClientRect()
                    const p = e.currentTarget.closest('.relative').getBoundingClientRect()
                    setTip({ x: r.left - p.left + r.width / 2, y: r.top - p.top, lines })
                  }}
                  className="h-3.5 w-3.5 rounded-[3px] ring-offset-1 hover:ring-2 hover:ring-ink"
                  style={{ background: `var(--heat-${lv})` }}
                />
              )
            })}
          </div>
        ))}
      </div>
      <div className="mt-2 flex items-center gap-1.5 text-xs text-muted">
        Less
        {[0, 1, 2, 3, 4].map((l) => (
          <span key={l} className="h-3 w-3 rounded-[3px]" style={{ background: `var(--heat-${l})` }} />
        ))}
        More
      </div>
      <Tooltip tip={tip} />
    </div>
  )
}

function UnitBars({ units }) {
  const [tip, setTip] = useState(null)
  return (
    <div className="relative" onMouseLeave={() => setTip(null)}>
      <ul className="space-y-2.5">
        {units.map((u) => {
          const pct = u.accuracy === null ? null : Math.round(u.accuracy * 100)
          const weak = pct !== null && u.attempted >= 5 && pct < 60
          return (
            <li key={u.id} className="grid grid-cols-[minmax(0,11rem)_1fr_auto] items-center gap-3 text-sm">
              <Link to={`/cn/units/${u.id}?tab=questions`} className="flex min-w-0 items-center gap-2 hover:text-accent">
                <FibreDot colour={u.colour} size={8} />
                <span className="truncate">Unit {u.id} · {u.title}</span>
              </Link>
              <div
                className="h-5 rounded-[4px] bg-sunken"
                onMouseEnter={(e) => {
                  const r = e.currentTarget.getBoundingClientRect()
                  const p = e.currentTarget.closest('.relative').getBoundingClientRect()
                  setTip({
                    x: r.left - p.left + (r.width * (pct ?? 0)) / 100,
                    y: r.top - p.top,
                    lines: [`Unit ${u.id}`, pct === null ? 'Not started' : `${u.correct} right of ${u.attempted} attempted`, `${u.attempted}/${u.total} attempted`],
                  })
                }}
              >
                {pct !== null && <div className="h-full rounded-[4px] bg-accent" style={{ width: `${Math.max(pct, 2)}%` }} />}
              </div>
              <span className="tabular flex w-24 items-center justify-end gap-1.5 text-right">
                {weak && <Pill tone="warn">Weak</Pill>}
                <span className={pct === null ? 'text-muted' : 'font-medium'}>{pct === null ? 'not started' : `${pct}%`}</span>
              </span>
            </li>
          )
        })}
      </ul>
      <Tooltip tip={tip} />
    </div>
  )
}

export default function Progress() {
  const [stats, setStats] = useState(null)
  const [view, setView] = useState('chart')
  useEffect(() => {
    api.stats().then(setStats)
  }, [])
  if (!stats) return <Spinner />

  const attempted = stats.units.reduce((a, u) => a + u.attempted, 0)
  const correct = stats.units.reduce((a, u) => a + u.correct, 0)
  let mocks = []
  try {
    mocks = JSON.parse(localStorage.getItem('mocks') || '[]')
  } catch {
    /* ignore */
  }

  const tiles = [
    ['Current streak', `${stats.streak} day${stats.streak === 1 ? '' : 's'}`],
    ['Best streak', `${stats.best_streak} day${stats.best_streak === 1 ? '' : 's'}`],
    ['This week', `${stats.week.items} answered`],
    ['Focus this week', `${stats.week.focus_minutes} min`],
    ['Accuracy', attempted ? `${Math.round((correct / attempted) * 100)}%` : '–'],
    ['Due for review', `${stats.due.questions + stats.due.cards}`],
  ]

  return (
    <div className="space-y-8">
      <PageHeader eyebrow="Analytics" title="Your progress">
        Where you stand in each unit, how consistently you study, and which units need more work.
      </PageHeader>

      <dl className="grid grid-cols-2 gap-px overflow-hidden rounded-xl border border-line bg-line sm:grid-cols-3 lg:grid-cols-6">
        {tiles.map(([k, v]) => (
          <div key={k} className="bg-surface px-4 py-3">
            <dt className="label">{k}</dt>
            <dd className="tabular display mt-1 text-xl font-bold">{v}</dd>
          </div>
        ))}
      </dl>

      <section className="space-y-3 rounded-xl border border-line bg-surface p-4 sm:p-5">
        <h2 className="font-bold">Study activity, last 12 weeks</h2>
        <Heatmap days={stats.heatmap} />
      </section>

      <section className="space-y-3 rounded-xl border border-line bg-surface p-4 sm:p-5">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h2 className="font-bold">Accuracy by unit</h2>
            <p className="text-sm text-muted">Share of attempted questions you got right. Under 60% after 5+ tries is marked weak.</p>
          </div>
          <Segmented label="View" value={view} onChange={setView} options={[{ value: 'chart', label: 'Chart' }, { value: 'table', label: 'Table' }]} />
        </div>
        {view === 'chart' ? (
          <UnitBars units={stats.units} />
        ) : (
          <div className="overflow-x-auto">
            <table className="tabular w-full text-sm">
              <thead>
                <tr className="border-b border-line text-left text-muted">
                  <th className="py-2 font-medium">Unit</th>
                  <th className="py-2 font-medium">Test</th>
                  <th className="py-2 text-right font-medium">Weight</th>
                  <th className="py-2 text-right font-medium">Attempted</th>
                  <th className="py-2 text-right font-medium">Right</th>
                  <th className="py-2 text-right font-medium">Accuracy</th>
                </tr>
              </thead>
              <tbody>
                {stats.units.map((u) => (
                  <tr key={u.id} className="border-b border-line last:border-0">
                    <td className="py-2">{u.id}. {u.title}</td>
                    <td className="py-2">{u.test}</td>
                    <td className="py-2 text-right">{u.weight}%</td>
                    <td className="py-2 text-right">{u.attempted}/{u.total}</td>
                    <td className="py-2 text-right">{u.correct}</td>
                    <td className="py-2 text-right">{u.accuracy === null ? '–' : `${Math.round(u.accuracy * 100)}%`}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="space-y-3">
        <h2 className="font-bold">Mock paper scores</h2>
        {mocks.length === 0 ? (
          <p className="text-sm text-muted">
            No mock papers yet. <Link to="/cn/mock" className="text-accent underline">Take a timed T1 or T2 paper</Link> to track your score over time.
          </p>
        ) : (
          <ul className="divide-y divide-line rounded-xl border border-line bg-surface">
            {mocks.map((m, i) => (
              <li key={i} className="tabular flex items-center gap-3 px-4 py-2 text-sm">
                <span className="font-semibold">{m.test}</span>
                <span className="text-muted">{new Date(m.at).toLocaleString(undefined, { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })}</span>
                <span className="ml-auto">{m.score} / {m.total}</span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  )
}
