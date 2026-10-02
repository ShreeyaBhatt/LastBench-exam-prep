import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import QuestionCard from '../components/QuestionCard'
import { Button, FibreDot, Pill, ProgressBar, btn, cx } from '../components/ui'
import { api } from '../lib/api'
import { APP_NAME, TAGLINE } from '../lib/brand'
import { taskLink } from '../lib/tasks'
import { daysUntil, todayISO, unitStats, useApp } from '../lib/store'

const greeting = () => {
  const h = new Date().getHours()
  if (h < 5) return 'Still up? Let’s make it count.'
  if (h < 12) return 'Good morning.'
  if (h < 17) return 'Good afternoon.'
  if (h < 21) return 'Good evening.'
  return 'Late-night revision mode.'
}

const card = 'rounded-xl border border-line bg-surface p-4 sm:p-5'
const primaryLink = cx(btn.base, btn.primary, 'px-4 py-2.5')
const secondaryLink = 'text-sm font-medium text-accent hover:underline underline-offset-2'

function Countdown() {
  const { settings } = useApp()
  const tests = ['T1', 'T2']
    .map((t) => ({ t, date: settings[`exam:cn-${t.toLowerCase()}`] }))
    .map((x) => ({ ...x, left: daysUntil(x.date) }))
    .filter((x) => x.date && x.left >= 0)
    .sort((a, b) => a.left - b.left)
  if (!tests.length) return null
  const n = tests[0]
  return (
    <p className="text-sm text-muted">
      {n.left === 0 ? (
        <>Your CN <b className="text-ink">{n.t}</b> is <b className="text-ink">today</b>. You've got this.</>
      ) : (
        <>
          CN <b className="text-ink">{n.t}</b> is in <b className="tabular text-ink">{n.left} day{n.left > 1 ? 's' : ''}</b>.
          {tests[1] && <> {tests[1].t} follows in {tests[1].left} days.</>}
        </>
      )}
    </p>
  )
}

/** The unit to continue: the last one opened, else the first with questions left. */
function pickUnit(units, progress) {
  let last = null
  try {
    last = Number(localStorage.getItem('lastUnit')) || null
  } catch {
    /* ignore */
  }
  const stats = units.map((u) => ({ u, s: unitStats(progress, u.qids) }))
  const pick = stats.find((x) => x.u.id === last) || stats.find((x) => x.s.done < x.s.total) || stats[0]
  return pick ? { ...pick, resumed: last === pick.u.id } : null
}

function Stats({ stats, goal }) {
  const today = stats?.today?.items || 0
  const due = stats ? stats.due.questions + stats.due.cards : 0
  const left = Math.max(goal - today, 0)
  return (
    <dl className="grid grid-cols-3 gap-px overflow-hidden rounded-lg border border-line bg-line text-sm">
      <div className="bg-surface px-3 py-2">
        <dt className="label">Streak</dt>
        <dd className="tabular mt-0.5 font-semibold">
          {stats?.streak ?? 0} day{stats?.streak === 1 ? '' : 's'}
        </dd>
      </div>
      <div className="bg-surface px-3 py-2">
        <dt className="label">Today</dt>
        <dd className="tabular mt-0.5 font-semibold">
          {today} / {goal}
        </dd>
        <dd className="tabular text-xs text-muted">{left ? `${left} to go` : 'Goal met'}</dd>
      </div>
      <Link to="/review" className="bg-surface px-3 py-2 hover:bg-sunken">
        <dt className="label">Due for review</dt>
        <dd className={cx('tabular mt-0.5 font-semibold', due && 'text-warn')}>{due}</dd>
      </Link>
    </dl>
  )
}

function ContinueCard({ pick }) {
  const { u, s, resumed } = pick
  const pct = s.total ? Math.round((s.done / s.total) * 1000) / 10 : 0
  return (
    <section className={cx(card, 'flex flex-col gap-4 md:col-span-8')}>
      <span className="label">{resumed ? 'Continue studying' : 'Up next'}</span>
      <div>
        <div className="flex items-center gap-2">
          <FibreDot colour={u.colour} size={12} />
          <h2 className="text-xl font-bold">Unit {u.id} · {u.title}</h2>
        </div>
        <p className="tabular mt-1 text-sm text-muted">
          {pct}% complete · {s.done} / {s.total} questions attempted · {u.test} · {u.weight}% of syllabus
        </p>
      </div>
      <ProgressBar value={s.done} total={s.total} colour={u.accent} />
      <div className="mt-auto flex flex-wrap items-center gap-4">
        <Link to={`/cn/units/${u.id}`} className={primaryLink}>
          Continue Unit {u.id} →
        </Link>
        <Link to={`/cn/units/${u.id}?tab=questions`} className={secondaryLink}>
          Jump to questions
        </Link>
      </div>
    </section>
  )
}

function TodayPlan({ plan }) {
  const today = plan?.days?.[0]
  return (
    <section className={cx(card, 'flex flex-col md:col-span-4')}>
      <span className="label">Today’s plan</span>
      {!plan ? null : today ? (
        <>
          <p className="tabular mt-1 text-xs text-muted">
            {plan.mode === 'syllabus'
              ? `${plan.test} · ${plan.remaining_topics} of ${plan.total_topics} topics left`
              : `${plan.test} · ${plan.remaining_questions} questions left · ~${plan.per_day}/day`}
          </p>
          <ul className="mt-3 space-y-1">
            {today.tasks.slice(0, 4).map((t, i) => (
              <li key={i}>
                <Link to={taskLink(t)} className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm hover:bg-sunken">
                  <span className={cx('h-1.5 w-1.5 shrink-0 rounded-full', t.type === 'questions' || t.type === 'topic' ? 'bg-accent' : 'bg-faint')} />
                  <span className="flex-1">{t.label}</span>
                </Link>
              </li>
            ))}
          </ul>
          <Link to="/plan" className={cx(secondaryLink, 'mt-auto pt-3')}>View full plan →</Link>
        </>
      ) : (
        <>
          <p className="mt-2 text-sm text-muted">
            Add your T1 / T2 dates and {APP_NAME} builds a day-by-day plan, numericals first.
          </p>
          <Link to="/plan" className={cx(btn.base, btn.ghost, 'mt-auto self-start')}>Set exam dates</Link>
        </>
      )}
    </section>
  )
}

const TOOLS = [
  ['/cn/mock', 'Mock T1 / T2', 'Timed 50-mark papers in the real pattern: 20 MCQ, 5 descriptive, 25 numerical.'],
  ['/cn/quiz?smart=1', 'Smart quiz', 'Adapts to you: missed questions and weak units come up more often.'],
  ['/review', 'Daily review', 'Spaced-repetition flashcards and questions you missed, right before you forget them.'],
  ['/cn/syllabus', 'Syllabus tracker', 'Every topic from 1.1 to 10.2 with its weightage, notes and questions.'],
  ['/focus', 'Focus timer', '25-minute Pomodoro sessions with rain or brown noise and a distraction-free mode.'],
  ['/studio', 'Notes Studio', 'Upload notes for any subject and get detailed notes, flashcards and a PDF.'],
  ['/ask', 'Ask AI', 'Ask a doubt; answers cite your notes and solved questions.'],
  ['/cn/labs', 'Labs & projects', 'Step-by-step Packet Tracer, Cisco and Wireshark guides for all 10 practicals.'],
]

export default function Home() {
  const { subjects, progress, settings } = useApp()
  const [cn, setCn] = useState(null)
  const [stats, setStats] = useState(null)
  const [daily, setDaily] = useState(null)
  const [plan, setPlan] = useState(null)
  const [showDaily, setShowDaily] = useState(false)
  const planMode = settings.plan_mode || 'questions'
  const planKey = `${settings['exam:cn-t1']}|${settings['exam:cn-t2']}|${planMode}`

  useEffect(() => {
    api.subject('cn').then(setCn).catch(() => {})
    api.stats().then(setStats).catch(() => {})
    api.daily(todayISO()).then(setDaily).catch(() => {})
  }, [])

  useEffect(() => {
    api.plan('cn', '', planMode).then(setPlan).catch(() => setPlan({ days: [] }))
  }, [planKey, planMode])

  const goal = settings.daily_goal || 20
  const dateLabel = new Date().toLocaleDateString(undefined, { weekday: 'long', day: 'numeric', month: 'long' })
  const weak = (stats?.units || []).filter((u) => u.accuracy !== null && u.attempted >= 5).sort((a, b) => a.accuracy - b.accuracy)[0]
  const due = stats ? stats.due.questions + stats.due.cards : 0
  const others = subjects.filter((s) => !s.builtin)
  const cnDone = cn ? cn.units.reduce((a, u) => a + unitStats(progress, u.qids).done, 0) : 0
  const cnTotal = cn ? cn.units.reduce((a, u) => a + u.qids.length, 0) : 0
  const pick = cn ? pickUnit(cn.units, progress) : null

  // The one thing to do now: today's first plan task, else the unit to continue.
  const todayTasks = plan?.days?.[0]?.tasks || []
  const planned = todayTasks.reduce((a, t) => a + (t.type === 'questions' || t.type === 'topic' ? t.count : 0), 0)
  const topicsToday = todayTasks.filter((t) => t.type === 'topic').length
  const startTo = todayTasks[0] ? taskLink(todayTasks[0]) : pick ? `/cn/units/${pick.u.id}?tab=questions` : '/cn'
  const dailyUnit = daily && cn?.units.find((u) => u.id === daily.unit)

  return (
    <div className="space-y-8">
      <section className="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
        <div className="space-y-3">
          <div className="label">{dateLabel}</div>
          <h1 className="display text-4xl leading-[1.05] font-bold md:text-5xl">{greeting()}</h1>
          <p className="text-lg text-muted">
            {topicsToday ? (
              <>
                <b className="tabular text-ink">{topicsToday} syllabus topic{topicsToday > 1 ? 's' : ''}</b>
                {planned > 0 && <> · {planned} questions</>} planned today
              </>
            ) : planned ? (
              <><b className="tabular text-ink">{planned} questions</b> planned today</>
            ) : (
              <>Daily goal: <b className="tabular text-ink">{goal} questions</b></>
            )}
            {due > 0 && <> · <b className="tabular text-ink">{due}</b> due for review</>}
          </p>
          <Countdown />
          <div className="flex flex-wrap items-center gap-4 pt-1">
            <Link to={startTo} className={primaryLink}>Start today’s study</Link>
            <Link to="/plan" className={secondaryLink}>View study plan →</Link>
          </div>
        </div>
        <div className="md:w-80 md:shrink-0">
          <Stats stats={stats} goal={goal} />
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-12">
        {pick && <ContinueCard pick={pick} />}
        <TodayPlan plan={plan} />
      </section>

      <section className="grid gap-4 md:grid-cols-12">
        {daily && (
          <div className="md:col-span-8">
            {showDaily ? (
              <QuestionCard q={daily} colour={dailyUnit?.accent} />
            ) : (
              <div className={cx(card, 'flex h-full flex-col gap-3')}>
                <div className="flex items-baseline justify-between gap-2">
                  <span className="label">Question of the day</span>
                  <span className="label">Unit {daily.unit} · Q{daily.id}</span>
                </div>
                <p className="text-lg font-medium">{daily.text}</p>
                <Button variant="primary" className="mt-auto self-start" onClick={() => setShowDaily(true)}>
                  Answer question →
                </Button>
              </div>
            )}
          </div>
        )}
        <div className="flex flex-col gap-4 md:col-span-4">
          {weak && (
            <Link to={`/cn/units/${weak.id}?tab=questions`} className="rounded-xl border border-warn/40 bg-warn-soft p-4 hover:brightness-[0.98]">
              <div className="flex items-center gap-2">
                <Pill tone="warn">Weak spot</Pill>
                <span className="tabular text-sm text-warn">{Math.round(weak.accuracy * 100)}% correct</span>
              </div>
              <p className="mt-2 font-semibold">Unit {weak.id}: {weak.title}</p>
              <p className="text-sm text-muted">Your lowest accuracy so far. A few more questions here will lift your score most.</p>
            </Link>
          )}
          <div className={cx(card, 'flex flex-1 flex-col gap-2')}>
            <span className="label">Quick review</span>
            <p className="text-sm text-muted">
              {due ? (
                <><b className="tabular text-ink">{due}</b> item{due > 1 ? 's' : ''} due for review. Clear them before they slip.</>
              ) : (
                'Nothing due right now. Questions you miss come back here at the right time.'
              )}
            </p>
            <Link to={due ? '/review' : '/cn/quiz?smart=1'} className={cx(btn.base, btn.ghost, 'mt-auto self-start')}>
              {due ? 'Start review' : 'Take a smart quiz'}
            </Link>
          </div>
        </div>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Your subjects</h2>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <Link to="/cn" className="flex min-h-36 flex-col rounded-xl border border-line bg-surface p-4 hover:border-ink/40">
            <span className="label">CN · Sem V</span>
            <span className="mt-1 text-lg font-semibold">Computer Networks</span>
            <span className="mt-1 text-sm text-muted">10 units · practice book + syllabus extras · mock T1/T2</span>
            <div className="mt-auto space-y-1 pt-3">
              <ProgressBar value={cnDone} total={cnTotal} />
              <span className="tabular text-xs text-muted">{cnDone} of {cnTotal} questions attempted</span>
            </div>
          </Link>
          {others.map((s) => (
            <Link key={s.id} to={`/subjects/${s.id}`} className="flex min-h-36 flex-col rounded-xl border border-line bg-surface p-4 hover:border-ink/40">
              <span className="label">{s.code}</span>
              <span className="mt-1 text-lg font-semibold">{s.name}</span>
              <span className="mt-1 line-clamp-2 text-sm text-muted">{s.description}</span>
              <span className={cx('mt-auto pt-3 text-xs', s.deck_count ? 'text-good' : 'text-muted')}>
                {s.deck_count ? `${s.deck_count} study pack${s.deck_count > 1 ? 's' : ''}` : 'Waiting for material: upload in Notes Studio'}
              </span>
            </Link>
          ))}
          <Link to="/settings#subjects" className="flex min-h-36 items-center justify-center rounded-xl border border-dashed border-line p-4 text-sm text-muted hover:border-accent hover:text-accent">
            + Add a subject
          </Link>
        </div>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Study tools</h2>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {TOOLS.map(([to, title, text]) => (
            <Link key={to} to={to} className="rounded-xl border border-line bg-surface p-4 hover:border-ink/40">
              <h3 className="font-semibold">{title}</h3>
              <p className="mt-1 text-sm text-muted">{text}</p>
            </Link>
          ))}
        </div>
      </section>

      <p className="text-center text-xs text-muted">{TAGLINE}</p>
    </div>
  )
}
