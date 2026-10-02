import { todayISO, useApp } from '../lib/store'

export default function ExamDates() {
  const { settings, saveSetting } = useApp()
  return (
    <div className="flex flex-wrap gap-3">
      {['t1', 't2'].map((t) => (
        <label key={t} className="flex items-center gap-2 text-sm">
          <span className="label">CN {t.toUpperCase()} date</span>
          <input
            id={`home-exam-${t}`}
            type="date"
            min={todayISO()}
            value={settings[`exam:cn-${t}`] || ''}
            onChange={(e) => saveSetting(`exam:cn-${t}`, e.target.value || null)}
            className="rounded-lg border border-line bg-surface px-2.5 py-1.5"
          />
        </label>
      ))}
    </div>
  )
}
