import { useEffect, useState } from 'react'
import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom'
import { APP_NAME } from '../lib/brand'
import { MODES, formatTime, useFocus } from '../lib/focus'
import { useApp } from '../lib/store'
import { cx } from './ui'

const HOME_NAV = [
  { to: '/', label: 'Dashboard', end: true },
  { to: '/plan', label: 'Study plan' },
  { to: '/review', label: 'Daily review' },
  { to: '/progress', label: 'Progress' },
]

// Learn and Practice follow the subject picked in the sidebar.
const CN_NAV = [
  {
    group: 'Learn',
    items: [
      { to: '/cn', label: 'Overview', end: true },
      { to: '/cn/units/1', label: 'Units', match: '/cn/units' },
      { to: '/cn/syllabus', label: 'Syllabus' },
      { to: '/cn/labs', label: 'Labs & projects' },
    ],
  },
  {
    group: 'Practice',
    items: [
      { to: '/cn/quiz', label: 'Quick quiz' },
      { to: '/cn/mock', label: 'Mock exams' },
      { to: '/cn/formulas', label: 'Formula sheet' },
    ],
  },
]

const TOOLS_NAV = [
  { to: '/studio', label: 'Notes' },
  { to: '/ask', label: 'Ask AI' },
  { to: '/focus', label: 'Focus timer' },
]

const darkQuery = window.matchMedia('(prefers-color-scheme: dark)')
const currentTheme = () => document.documentElement.dataset.theme || (darkQuery.matches ? 'dark' : 'light')

/** Light/dark switch. Follows the system setting until the student picks one; the choice is remembered. */
function ThemeToggle({ className }) {
  const [theme, setTheme] = useState(currentTheme)

  useEffect(() => {
    const follow = () => setTheme(currentTheme())
    darkQuery.addEventListener('change', follow)
    return () => darkQuery.removeEventListener('change', follow)
  }, [])

  const toggle = () => {
    const next = theme === 'dark' ? 'light' : 'dark'
    document.documentElement.dataset.theme = next
    try {
      localStorage.setItem('theme', next)
    } catch {
      /* storage blocked: the switch still works for this visit */
    }
    setTheme(next)
  }

  const dark = theme === 'dark'
  return (
    <button
      type="button"
      role="switch"
      aria-checked={dark}
      aria-label="Dark mode"
      title={dark ? 'Switch to light mode' : 'Switch to dark mode'}
      onClick={toggle}
      className={cx('relative inline-flex h-8 w-[3.75rem] shrink-0 cursor-pointer items-center rounded-full border border-line bg-sunken p-0.5', className)}
    >
      <span
        aria-hidden="true"
        className={cx(
          'flex h-6 w-6 items-center justify-center rounded-full bg-surface text-ink shadow-sm transition-transform duration-200',
          dark ? 'translate-x-7' : 'translate-x-0',
        )}
      >
        {dark ? (
          <svg viewBox="0 0 24 24" className="h-3.5 w-3.5" fill="currentColor">
            <path d="M20.5 14.6A8.5 8.5 0 0 1 9.4 3.5a8.5 8.5 0 1 0 11.1 11.1Z" />
          </svg>
        ) : (
          <svg viewBox="0 0 24 24" className="h-3.5 w-3.5" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round">
            <circle cx="12" cy="12" r="4" fill="currentColor" stroke="none" />
            <path d="M12 2.5v2M12 19.5v2M4.6 4.6 6 6M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4 6 18M18 6l1.4-1.4" />
          </svg>
        )}
      </span>
    </button>
  )
}

function AiStatus() {
  const { health } = useApp()
  if (!health) return null
  const on = health.ai.available
  return (
    <NavLink
      to="/ask?setup=1"
      className={cx('flex items-center gap-2 rounded-md px-2 py-1 text-xs', on ? 'text-good' : 'text-warn', 'hover:bg-sunken')}
      title={on ? `Using ${health.ai.model}` : 'Add an API key to enable Claude'}
    >
      <span className={cx('h-2 w-2 rounded-full', on ? 'bg-good' : 'bg-warn')} />
      {on ? 'Claude connected' : 'AI offline: add key'}
    </NavLink>
  )
}

function TimerChip() {
  const { running, remaining, mode } = useFocus()
  if (!running) return null
  return (
    <NavLink to="/focus" className="tabular flex items-center gap-1.5 rounded-full bg-accent-soft px-2.5 py-1 font-mono text-xs font-semibold text-accent">
      <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-accent" />
      {formatTime(remaining)} {MODES[mode].label.split(' ')[0].toLowerCase()}
    </NavLink>
  )
}

const linkClass = (active) =>
  cx(
    'relative shrink-0 rounded-md px-2.5 py-1.5 text-sm whitespace-nowrap transition-colors',
    active
      ? 'bg-accent-soft font-medium text-ink lg:before:absolute lg:before:inset-y-1.5 lg:before:left-0 lg:before:w-0.5 lg:before:rounded-full lg:before:bg-accent'
      : 'text-muted hover:bg-sunken hover:text-ink',
  )

function NavItems({ items, pathname, className }) {
  return items.map((item) => (
    <NavLink
      key={item.to}
      to={item.to}
      end={item.end}
      className={({ isActive }) => cx(linkClass(isActive || (item.match && pathname.startsWith(item.match))), className)}
    >
      {item.label}
    </NavLink>
  ))
}

const groupLabel = 'label hidden px-2.5 pt-4 pb-1 lg:block'

/** Picks the subject that Learn and Practice point at. */
function SubjectPicker({ custom, current }) {
  const navigate = useNavigate()
  const change = (e) => {
    const v = e.target.value
    navigate(v === 'cn' ? '/cn' : v === '+' ? '/settings#subjects' : `/subjects/${v}`)
  }
  return (
    <div className="hidden pt-4 lg:block">
      <label htmlFor="subject-picker" className="label block px-2.5 pb-1">Subject</label>
      <select
        id="subject-picker"
        value={current}
        onChange={change}
        className="w-full cursor-pointer rounded-md border border-line bg-sunken px-2 py-1.5 text-sm font-semibold text-ink"
      >
        <option value="cn">Computer Networks</option>
        {custom.map((s) => (
          <option key={s.id} value={s.id}>{s.code === s.name ? s.name : `${s.code} · ${s.name}`}</option>
        ))}
        <option value="+">+ Add a subject…</option>
      </select>
    </div>
  )
}

export default function Layout() {
  const { subjects, error } = useApp()
  const { focusMode, setFocusMode } = useFocus()
  const { pathname } = useLocation()
  const toolsActive = TOOLS_NAV.some((t) => pathname.startsWith(t.to))
  // Tools stays open while one of its pages is showing; otherwise it follows the toggle.
  const [toolsPicked, setToolsOpen] = useState(false)
  const toolsOpen = toolsPicked || toolsActive
  useEffect(() => {
    // Braces matter: newer browsers return a Promise from scrollTo, and React would try to
    // call a returned value as the effect's cleanup and crash on the next navigation.
    window.scrollTo(0, 0)
  }, [pathname])

  const custom = subjects.filter((s) => !s.builtin)
  const sid = pathname.match(/^\/subjects\/([^/]+)/)?.[1]
  const subject = sid && custom.some((s) => s.id === sid) ? sid : 'cn'
  const subjectNav = subject === 'cn' ? CN_NAV : [{ group: 'Learn', items: [{ to: `/subjects/${subject}`, label: 'Study packs' }] }]
  const brand = (
    <NavLink to="/" className="flex items-center gap-2.5">
      <img src="/favicon.svg" alt="" className="h-7 w-7" />
      <span className="display text-xl font-bold">{APP_NAME}</span>
    </NavLink>
  )

  if (focusMode) {
    return (
      <div className="min-h-screen">
        <header className="sticky top-0 z-20 flex items-center justify-between gap-3 border-b border-line bg-surface px-4 py-2.5 sm:px-6">
          <div className="flex items-center gap-3">
            {brand}
            <span className="label hidden sm:inline">Focus mode</span>
          </div>
          <div className="flex items-center gap-2">
            <TimerChip />
            <ThemeToggle />
            <button type="button" onClick={() => setFocusMode(false)} className="cursor-pointer rounded-lg border border-line px-3 py-1.5 text-sm hover:bg-sunken">
              Exit focus mode
            </button>
          </div>
        </header>
        <main className="px-4 pt-6 pb-16 sm:px-6 lg:pt-10">
          <div className="mx-auto max-w-4xl">
            <Outlet />
          </div>
        </main>
      </div>
    )
  }

  return (
    <div className="min-h-screen lg:grid lg:grid-cols-[248px_1fr]">
      <aside className="sticky top-0 z-20 border-b border-line bg-surface lg:h-screen lg:overflow-y-auto lg:border-r lg:border-b-0">
        <div className="flex h-full flex-col gap-3 px-4 py-3 lg:px-5 lg:py-6">
          <div className="flex items-center justify-between gap-3">
            {brand}
            <div className="flex items-center gap-2">
              <div className="lg:hidden">
                <TimerChip />
              </div>
              <ThemeToggle />
            </div>
          </div>
          <nav aria-label="Main" className="-mx-1 flex gap-1 overflow-x-auto pb-1 lg:mx-0 lg:flex-col lg:overflow-visible lg:pb-0">
            <div className="contents lg:flex lg:flex-col lg:gap-0.5">
              <NavItems items={HOME_NAV} pathname={pathname} />
            </div>
            <SubjectPicker custom={custom} current={subject} />
            {subjectNav.map((g) => (
              <div key={g.group} className="contents lg:flex lg:flex-col lg:gap-0.5">
                <div className={groupLabel}>{g.group}</div>
                <NavItems items={g.items} pathname={pathname} />
              </div>
            ))}
            {/* Mobile shows every link in one scrolling row; on desktop Tools folds away. */}
            {custom.map((s) => (
              <NavLink key={s.id} to={`/subjects/${s.id}`} className={({ isActive }) => cx(linkClass(isActive), 'lg:hidden')}>
                {s.code}
              </NavLink>
            ))}
            <div className="contents lg:flex lg:flex-col lg:gap-0.5">
              <button
                type="button"
                aria-expanded={toolsOpen}
                onClick={() => setToolsOpen(!toolsOpen)}
                className="label hidden cursor-pointer items-center justify-between px-2.5 pt-4 pb-1 text-left hover:text-ink lg:flex"
              >
                Tools
                <span aria-hidden="true" className={cx('transition-transform', toolsOpen && 'rotate-90')}>›</span>
              </button>
              <NavItems items={TOOLS_NAV} pathname={pathname} className={toolsOpen ? '' : 'lg:hidden'} />
            </div>
            <NavLink to="/settings" className={({ isActive }) => cx(linkClass(isActive), 'lg:hidden')}>
              Settings
            </NavLink>
          </nav>
          <div className="mt-auto hidden flex-col items-start gap-2 border-t border-line pt-3 lg:flex">
            <TimerChip />
            <AiStatus />
            <NavLink to="/settings" className={({ isActive }) => cx('rounded-md px-2 py-1 text-xs hover:bg-sunken', isActive ? 'text-ink' : 'text-muted')}>
              Settings
            </NavLink>
          </div>
        </div>
      </aside>
      <main className="min-w-0 px-4 pt-6 pb-16 sm:px-6 lg:px-10 lg:pt-10">
        <div className="mx-auto max-w-5xl">
          {error && <div className="mb-6 rounded-lg border border-bad/40 bg-bad-soft px-4 py-3 text-sm text-bad">{error}</div>}
          <Outlet />
        </div>
      </main>
    </div>
  )
}
