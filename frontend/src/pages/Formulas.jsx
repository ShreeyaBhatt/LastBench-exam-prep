import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { FibreDot, LinkButton, PageHeader, Spinner } from '../components/ui'
import { api, formulasPdfUrl } from '../lib/api'

export default function Formulas() {
  const [units, setUnits] = useState(null)
  useEffect(() => {
    api.formulas().then(setUnits)
  }, [])
  if (!units) return <Spinner />
  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Revise in 5 minutes"
        title="Formula sheet"
        actions={
          <LinkButton href={formulasPdfUrl} download>
            Download PDF
          </LinkButton>
        }
      >
        Every formula, rule and common trap from the ten units. Read it the night before the exam.
      </PageHeader>
      <div className="columns-1 gap-6 md:columns-2">
        {units.map((u) => (
          <section key={u.unit} className="mb-6 break-inside-avoid rounded-xl border border-line bg-surface">
            <Link to={`/cn/units/${u.unit}`} className="flex items-center gap-2 border-b border-line px-4 py-2.5 hover:text-accent">
              <FibreDot colour={u.colour} />
              <span className="label">Unit {u.unit}</span>
              <span className="font-semibold">{u.title}</span>
            </Link>
            <dl className="divide-y divide-line">
              {u.formulas.map(([name, expr]) => (
                <div key={name} className="px-4 py-2">
                  <dt className="text-xs text-muted">{name}</dt>
                  <dd className="font-mono text-[0.85rem]">{expr}</dd>
                </div>
              ))}
            </dl>
            <ul className="space-y-1 border-t border-line bg-warn-soft/60 px-4 py-2.5 text-sm">
              {u.traps.map((t) => (
                <li key={t} className="flex gap-2">
                  <span className="font-bold text-warn">!</span>
                  {t}
                </li>
              ))}
            </ul>
          </section>
        ))}
      </div>
    </div>
  )
}
