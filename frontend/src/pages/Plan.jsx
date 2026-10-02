import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import ExamDates from '../components/ExamDates'
import { Empty, PageHeader, Segmented, Spinner, cx } from '../components/ui'
import { api } from '../lib/api'
import { taskLink } from '../lib/tasks'
import { daysUntil, useApp } from '../lib/store'

const MODES = [
  { value: 'questions', label: 'By questions' },
  { value: 'syllabus', label: 'By syllabus topic' },
]

function Summary({ plan, test }) {
  const days = `${plan.days_left} day${plan.days_left > 1 ? 's' : ''} left`
  if (plan.mode === 'syllabus') {
    return (
      <p className="tabular text-sm text-muted">
        {test}: {days} · {plan.remaining_topics} of {plan.total_topics} topics to revise · {plan.remaining_questions} open questions in them
      </p>
    )
  }
  return (
    <p className="tabular text-sm text-muted">
      {test}: {days} · {plan.remaining_questions} questions to go · about {plan.per_day} a day
    </p>
  )
}

export default function Plan() {
  const { settings, saveSetting } = useApp()
  const dates = { T1: settings['exam:cn-t1'], T2: settings['exam:cn-t2'] }
  const mode = settings.plan_mode || 'questions'
  const upcoming = ['T1', 'T2'].filter((t) => dates[t] && daysUntil(dates[t]) > 0)
  const [test, setTest] = useState('')
  const active = test && upcoming.includes(test) ? test : upcoming[0] || ''
  const [plan, setPlan] = useState(null)

  useEffect(() => {
    if (!active) {
      setPlan({ days: [] })
      return
    }
    setPlan(null)
    api.plan('cn', active, mode).then(setPlan).catch(() => setPlan({ days: [] }))
  }, [active, mode, dates.T1, dates.T2])

  const fmt = (iso) => new Date(`${iso}T00:00`).toLocaleDateString(undefined, { weekday: 'short', day: 'numeric', month: 'short' })

  return (
    <div className="space-y-6">
      <PageHeader eyebrow="Study plan" title="Your road to the test">
        {mode === 'syllabus'
          ? 'Set your test dates. The plan walks the official syllabus topic by topic, in order, skipping topics you have ticked as revised, and keeps the last days for mock papers and revision.'
          : 'Set your test dates. The plan spreads every question you haven’t got right yet across the days left, numericals first, and keeps the last days for mock papers and revision. It updates as you practise.'}
      </PageHeader>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <ExamDates />
        <div className="flex flex-wrap gap-2">
          <Segmented label="Plan type" value={mode} onChange={(v) => saveSetting('plan_mode', v)} options={MODES} />
          {upcoming.length > 1 && (
            <Segmented label="Test" value={active} onChange={setTest} options={upcoming.map((t) => ({ value: t, label: `${t} plan` }))} />
          )}
        </div>
      </div>
      {!active ? (
        <Empty title="No upcoming test date">Pick your T1 (Units 1–4) or T2 (Units 5–10) date above to get a day-by-day plan.</Empty>
      ) : !plan ? (
        <Spinner />
      ) : (
        <>
          <Summary plan={plan} test={active} />
          <ol className="space-y-3">
            {plan.days.map((d, i) => (
              <li key={d.date} className={cx('grid gap-3 rounded-xl border bg-surface p-4 sm:grid-cols-[9rem_1fr]', i === 0 ? 'border-accent' : 'border-line')}>
                <div>
                  <div className="font-semibold">{i === 0 ? 'Today' : i === 1 ? 'Tomorrow' : fmt(d.date)}</div>
                  <div className="tabular text-xs text-muted">{i <= 1 ? fmt(d.date) : `Day ${i + 1}`}</div>
                </div>
                <ul className="space-y-1.5">
                  {d.tasks.map((t, j) => (
                    <li key={j}>
                      <Link to={taskLink(t)} className="flex items-center gap-2 rounded-md px-2 py-1 text-sm hover:bg-sunken">
                        <span
                          className={cx(
                            'h-1.5 w-1.5 shrink-0 rounded-full',
                            t.type === 'mock' ? 'bg-bad' : t.type === 'questions' || t.type === 'topic' ? 'bg-accent' : 'bg-faint',
                          )}
                        />
                        {t.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </li>
            ))}
          </ol>
        </>
      )}
    </div>
  )
}
