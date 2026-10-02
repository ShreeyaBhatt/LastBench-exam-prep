import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export const btn = {
  base: 'inline-flex items-center justify-center gap-2 rounded-lg px-3.5 py-2 text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer',
  primary: 'bg-accent text-accent-ink hover:brightness-110',
  ghost: 'border border-line bg-surface text-ink hover:bg-sunken',
  quiet: 'text-muted hover:text-ink hover:bg-sunken',
  danger: 'border border-line bg-surface text-bad hover:bg-bad-soft',
}

export const cx = (...c) => c.filter(Boolean).join(' ')

export function Button({ variant = 'ghost', className, ...props }) {
  return <button type="button" className={cx(btn.base, btn[variant], className)} {...props} />
}

export function LinkButton({ variant = 'ghost', className, ...props }) {
  return <a className={cx(btn.base, btn[variant], className)} {...props} />
}

export function Markdown({ children, className }) {
  return (
    <div className={cx('prose-x', className)}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          table: ({ node, ...props }) => (
            <div className="table-wrap">
              <table {...props} />
            </div>
          ),
          a: ({ node, ...props }) => <a target="_blank" rel="noreferrer" {...props} />,
        }}
      >
        {children || ''}
      </ReactMarkdown>
    </div>
  )
}

/** Unit colour chip, named after the TIA-598 fibre strand colour code. */
export function FibreDot({ colour, size = 10 }) {
  return (
    <span
      aria-hidden="true"
      className="inline-block shrink-0 rounded-full ring-1 ring-black/15 dark:ring-white/20"
      style={{ width: size, height: size, background: colour }}
    />
  )
}

// Blue (accent) is kept for things you can click; progress reads as green.
export function ProgressBar({ value, total, colour = 'var(--good)' }) {
  const pct = total ? Math.round((value / total) * 100) : 0
  return (
    <div className="h-1.5 w-full overflow-hidden rounded-full bg-sunken" role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}>
      <div className="h-full rounded-full transition-[width] duration-500" style={{ width: `${pct}%`, background: colour }} />
    </div>
  )
}

export function Pill({ tone = 'neutral', children, className }) {
  const tones = {
    neutral: 'bg-sunken text-muted',
    accent: 'bg-accent-soft text-accent',
    good: 'bg-good-soft text-good',
    bad: 'bg-bad-soft text-bad',
    warn: 'bg-warn-soft text-warn',
  }
  return <span className={cx('inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium', tones[tone], className)}>{children}</span>
}

export function PageHeader({ eyebrow, title, children, actions }) {
  return (
    <header className="flex flex-col gap-4 border-b border-line pb-6 md:flex-row md:items-end md:justify-between">
      <div className="min-w-0">
        {eyebrow && <div className="label mb-2">{eyebrow}</div>}
        <h1 className="display text-3xl font-bold md:text-4xl">{title}</h1>
        {children && <div className="mt-2 max-w-2xl text-muted">{children}</div>}
      </div>
      {actions && <div className="flex flex-wrap gap-2">{actions}</div>}
    </header>
  )
}

export function Empty({ title, children, action }) {
  return (
    <div className="rounded-xl border border-dashed border-line bg-surface px-6 py-10 text-center">
      <p className="font-display text-lg font-semibold">{title}</p>
      {children && <p className="mx-auto mt-1 max-w-md text-sm text-muted">{children}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  )
}

export function Segmented({ options, value, onChange, label }) {
  return (
    <div role="radiogroup" aria-label={label} className="inline-flex flex-wrap gap-1 rounded-lg border border-line bg-surface p-1">
      {options.map((o) => (
        <button
          key={o.value}
          type="button"
          role="radio"
          aria-checked={value === o.value}
          onClick={() => onChange(o.value)}
          className={cx(
            'cursor-pointer rounded-md px-2.5 py-1 text-sm transition-colors',
            value === o.value ? 'bg-ink text-bg' : 'text-muted hover:bg-sunken hover:text-ink',
          )}
        >
          {o.label}
          {o.count !== undefined && <span className="tabular ml-1.5 opacity-70">{o.count}</span>}
        </button>
      ))}
    </div>
  )
}

export function Spinner({ label = 'Loading' }) {
  return (
    <div className="flex items-center gap-3 py-10 text-muted" role="status">
      <span className="h-4 w-4 animate-spin rounded-full border-2 border-line border-t-accent" />
      {label}
    </div>
  )
}
