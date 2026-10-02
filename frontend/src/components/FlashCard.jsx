import { useEffect } from 'react'
import { Button, Markdown, cx } from './ui'

export const GRADES = [
  { grade: 'again', label: 'Again', hint: 'today', tone: 'danger' },
  { grade: 'hard', label: 'Hard', hint: 'soon', tone: 'ghost' },
  { grade: 'good', label: 'Good', hint: 'later', tone: 'ghost' },
  { grade: 'easy', label: 'Easy', hint: 'much later', tone: 'primary' },
]

/** A flip card with spaced-repetition grading. Keys: Space flips, 1-4 grade. */
export default function FlashCard({ card, flipped, setFlipped, onGrade, eyebrow }) {
  useEffect(() => {
    const onKey = (e) => {
      if (e.target.closest('input, textarea, select')) return
      if (e.key === ' ' || e.key === 'Enter') {
        e.preventDefault()
        setFlipped((f) => !f)
      } else if (flipped && ['1', '2', '3', '4'].includes(e.key)) {
        onGrade(GRADES[Number(e.key) - 1].grade)
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [flipped, setFlipped, onGrade])

  return (
    <div className="space-y-4">
      <button
        type="button"
        onClick={() => setFlipped(!flipped)}
        className={cx('flip block w-full cursor-pointer text-left', flipped && 'is-flipped')}
        aria-label={flipped ? 'Show question' : 'Show answer'}
      >
        <div className="flip-inner min-h-64">
          <div className="flex flex-col rounded-2xl border border-line bg-surface p-6 sm:p-8">
            <span className="label">{eyebrow || card.topic || 'Question'}</span>
            <p className="display my-auto py-6 text-2xl leading-snug font-semibold sm:text-3xl">{card.front}</p>
            <span className="text-xs text-muted">Tap or press Space to flip</span>
          </div>
          <div className="flip-back flex flex-col rounded-2xl border border-accent/40 bg-accent-soft p-6 sm:p-8">
            <span className="label">Answer</span>
            <Markdown className="my-auto py-6 text-lg">{card.back}</Markdown>
            <span className="text-xs text-muted">{card.front}</span>
          </div>
        </div>
      </button>
      {flipped ? (
        <div className="grid grid-cols-4 gap-2">
          {GRADES.map((g, i) => (
            <Button key={g.grade} variant={g.tone} onClick={() => onGrade(g.grade)} className="flex-col gap-0 py-2">
              <span>{g.label}</span>
              <span className="text-[0.7rem] font-normal opacity-75">
                {i + 1} · {g.hint}
              </span>
            </Button>
          ))}
        </div>
      ) : (
        <Button variant="primary" className="w-full" onClick={() => setFlipped(true)}>
          Show answer
        </Button>
      )}
    </div>
  )
}
