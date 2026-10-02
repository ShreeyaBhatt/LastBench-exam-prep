import { useEffect, useState } from 'react'
import { Markdown, PageHeader, Pill, Spinner, cx } from '../components/ui'
import { api } from '../lib/api'
import { useApp } from '../lib/store'

function Item({ item, prefix }) {
  const { progress, setProgress } = useApp()
  const key = `lab:${prefix}${item.no}`
  const done = progress[key]?.status === 'done'
  return (
    <details className="group rounded-xl border border-line bg-surface open:border-ink/30">
      <summary className="flex cursor-pointer list-none items-center gap-3 px-4 py-3">
        <span className="tabular w-6 font-mono text-sm font-semibold text-muted">{item.no}</span>
        <span className={cx('flex-1 font-medium', done && 'text-muted line-through')}>{item.title}</span>
        <span className="hidden gap-1 sm:flex">
          {item.units.map((u) => (
            <Pill key={u}>Unit {u}</Pill>
          ))}
        </span>
        <span className="text-muted transition-transform group-open:rotate-90" aria-hidden="true">›</span>
      </summary>
      <div className="space-y-3 border-t border-line px-4 py-4">
        <Markdown>{item.guide}</Markdown>
        <label className="flex items-center gap-2 text-sm">
          <input
            id={key}
            type="checkbox"
            checked={done}
            onChange={() => setProgress(key, { status: done ? null : 'done' })}
            className="h-4 w-4 accent-[var(--good)]"
          />
          Done in the lab
        </label>
      </div>
    </details>
  )
}

export default function Labs() {
  const [labs, setLabs] = useState(null)
  const { progress } = useApp()
  useEffect(() => {
    api.labs().then(setLabs)
  }, [])
  if (!labs) return <Spinner />
  const done = Object.entries(progress).filter(([k, v]) => k.startsWith('lab:') && v.status === 'done').length
  return (
    <div className="space-y-8">
      <PageHeader eyebrow="Practical = 20% of the course" title="Labs & projects">
        Step-by-step guides for the 10 syllabus practicals and the 5 hands-on projects: Packet Tracer builds, Cisco IOS commands, cable pinouts and Wireshark filters. Each ends with likely viva points.
      </PageHeader>
      <p className="tabular text-sm text-muted">{done} of {labs.practicals.length + labs.projects.length} done</p>
      <section className="space-y-3">
        <h2 className="text-xl font-bold">Practicals</h2>
        {labs.practicals.map((p) => (
          <Item key={p.no} item={p} prefix="p" />
        ))}
      </section>
      <section className="space-y-3">
        <h2 className="text-xl font-bold">Hands-on projects</h2>
        <p className="text-sm text-muted">Individual project (50 marks) and group project (50 marks) make up the practical evaluation.</p>
        {labs.projects.map((p) => (
          <Item key={p.no} item={p} prefix="j" />
        ))}
      </section>
    </div>
  )
}
