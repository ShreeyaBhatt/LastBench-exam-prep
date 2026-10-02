import { Button, PageHeader, Segmented, cx } from '../components/ui'
import { MODES, formatTime, useFocus } from '../lib/focus'

export default function Focus() {
  const f = useFocus()
  const total = MODES[f.mode].minutes * 60
  const pct = 1 - f.remaining / total
  const R = 120
  const C = 2 * Math.PI * R

  return (
    <div className="space-y-8">
      <PageHeader eyebrow="Pomodoro" title="Focus timer">
        25 minutes of focus, then a 5-minute break; every fourth break is 15 minutes. Finished sessions count toward your streak. The timer keeps running while you use the rest of the app.
      </PageHeader>

      <div className="flex flex-col items-center gap-6">
        <Segmented
          label="Timer mode"
          value={f.mode}
          onChange={(m) => f.reset(m)}
          options={Object.entries(MODES).map(([k, v]) => ({ value: k, label: `${v.label} ${v.minutes}` }))}
        />
        <div className="relative h-72 w-72 max-w-full">
          <svg viewBox="0 0 280 280" className="h-full w-full -rotate-90" aria-hidden="true">
            <circle cx="140" cy="140" r={R} fill="none" stroke="var(--sunken)" strokeWidth="10" />
            <circle
              cx="140"
              cy="140"
              r={R}
              fill="none"
              stroke={f.mode === 'focus' ? 'var(--accent)' : 'var(--good)'}
              strokeWidth="10"
              strokeLinecap="round"
              strokeDasharray={C}
              strokeDashoffset={C * (1 - pct)}
              className="transition-[stroke-dashoffset] duration-1000 ease-linear"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="label">{MODES[f.mode].label}</span>
            <span className="tabular display text-6xl font-bold" role="timer" aria-live="off">
              {formatTime(f.remaining)}
            </span>
            <span className="tabular text-sm text-muted">{f.sessions} session{f.sessions === 1 ? '' : 's'} today</span>
          </div>
        </div>
        <div className="flex gap-2">
          {f.running ? (
            <Button variant="primary" onClick={f.pause} className="min-w-28">Pause</Button>
          ) : (
            <Button variant="primary" onClick={f.start} className="min-w-28">{f.remaining < total ? 'Resume' : 'Start'}</Button>
          )}
          <Button onClick={() => f.reset()}>Reset</Button>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <section className="space-y-3 rounded-xl border border-line bg-surface p-4">
          <h2 className="font-bold">Background sound</h2>
          <p className="text-sm text-muted">Steady noise masks hostel and classroom chatter. Generated in your browser, no downloads.</p>
          <Segmented
            label="Background sound"
            value={f.sound}
            onChange={f.setSound}
            options={[
              { value: 'off', label: 'Off' },
              { value: 'pink', label: 'Rain' },
              { value: 'brown', label: 'Brown noise' },
            ]}
          />
          <label className={cx('flex items-center gap-3 text-sm', f.sound === 'off' && 'opacity-50')}>
            Volume
            <input
              id="focus-volume"
              type="range"
              min={0}
              max={1}
              step={0.05}
              value={f.volume}
              disabled={f.sound === 'off'}
              onChange={(e) => f.setVolume(Number(e.target.value))}
              className="flex-1 accent-[var(--accent)]"
            />
          </label>
        </section>
        <section className="space-y-3 rounded-xl border border-line bg-surface p-4">
          <h2 className="font-bold">Focus mode</h2>
          <p className="text-sm text-muted">Hides the navigation so only the page you are studying is on screen. Put your phone in another room too.</p>
          <Button variant={f.focusMode ? 'primary' : 'ghost'} onClick={() => f.setFocusMode(!f.focusMode)}>
            {f.focusMode ? 'Turn off focus mode' : 'Turn on focus mode'}
          </Button>
        </section>
      </div>
    </div>
  )
}
