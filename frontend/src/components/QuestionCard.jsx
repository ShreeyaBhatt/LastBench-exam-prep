import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useApp } from '../lib/store'
import { Button, Markdown, Pill, cx } from './ui'

const KIND = { mcq: 'MCQ', numerical: 'Numerical', theory: 'Theory' }
const LETTERS = ['A', 'B', 'C', 'D']

export default function QuestionCard({ q, colour, onAnswer, quizMode = false }) {
  const { progress, setProgress } = useApp()
  const key = `cn:${q.id}`
  const p = progress[key] || {}
  const [picked, setPicked] = useState(null)
  const [open, setOpen] = useState(false)

  const choose = (letter) => {
    if (picked) return
    setPicked(letter)
    const ok = letter === q.answer
    setProgress(key, { status: ok ? 'correct' : 'wrong' })
    onAnswer?.(ok)
  }

  const revealed = q.kind === 'mcq' ? picked !== null : open
  const status =
    p.status === 'correct' ? <Pill tone="good">Got it</Pill> : p.status === 'wrong' ? <Pill tone="bad">Revise</Pill> : null

  return (
    <article id={`q${q.id}`} className="scroll-mt-24 rounded-xl border border-line bg-surface">
      <div className="flex flex-wrap items-center gap-2 border-b border-line px-4 py-2.5 sm:px-5">
        <span className="font-mono text-sm font-semibold" style={{ color: colour }}>
          Q{q.id}
        </span>
        <Pill>{KIND[q.kind]}</Pill>
        {q.source === 'syllabus' && <Pill tone="accent" className="hidden sm:inline-flex">Syllabus extra</Pill>}
        <span className="tabular text-xs text-muted">
          {q.marks} mark{q.marks > 1 ? 's' : ''}
        </span>
        {!quizMode && status}
        <div className="ml-auto flex items-center gap-1">
          <Link
            to={`/ask?qid=${q.id}&unit=${q.unit}`}
            className="rounded-md px-2 py-1 text-xs text-muted hover:bg-sunken hover:text-accent"
          >
            Ask AI
          </Link>
          {!quizMode && (
            <button
              type="button"
              onClick={() => setProgress(key, { bookmarked: !p.bookmarked })}
              aria-pressed={!!p.bookmarked}
              className={cx(
                'cursor-pointer rounded-md px-2 py-1 text-xs hover:bg-sunken',
                p.bookmarked ? 'font-semibold text-warn' : 'text-muted hover:text-ink',
              )}
            >
              {p.bookmarked ? '★ Saved' : '☆ Save'}
            </button>
          )}
        </div>
      </div>

      <div className="space-y-4 px-4 py-4 sm:px-5">
        <p className="max-w-[72ch] font-medium">{q.text}</p>
        {q.diagram && (
          <div className="overflow-x-auto">
            <img src={q.diagram} alt={`Network diagram for question ${q.id}`} className="max-h-64 rounded-lg border border-line bg-white p-2" />
          </div>
        )}

        {q.kind === 'mcq' && (
          <ol className="grid gap-2 sm:grid-cols-2">
            {q.options.map((opt, i) => {
              const L = LETTERS[i]
              const isAns = L === q.answer
              const isPicked = L === picked
              return (
                <li key={L}>
                  <button
                    type="button"
                    disabled={picked !== null}
                    onClick={() => choose(L)}
                    className={cx(
                      'flex h-full w-full items-start gap-3 rounded-lg border px-3 py-2.5 text-left text-sm transition-colors',
                      picked === null && 'cursor-pointer border-line hover:border-accent hover:bg-accent-soft',
                      picked !== null && isAns && 'border-good bg-good-soft',
                      picked !== null && isPicked && !isAns && 'border-bad bg-bad-soft',
                      picked !== null && !isAns && !isPicked && 'border-line opacity-60',
                    )}
                  >
                    <span className="font-mono text-xs font-semibold text-muted">{L}</span>
                    <span className="flex-1">{opt}</span>
                    {picked !== null && isAns && <span className="text-xs font-semibold text-good">Correct</span>}
                    {picked !== null && isPicked && !isAns && <span className="text-xs font-semibold text-bad">Your pick</span>}
                  </button>
                </li>
              )
            })}
          </ol>
        )}

        {q.kind !== 'mcq' && !open && (
          <Button variant="ghost" onClick={() => setOpen(true)}>
            Show solution
          </Button>
        )}

        {revealed && (
          <div className="space-y-3 rounded-lg bg-sunken px-4 py-3">
            <div className="flex flex-wrap items-baseline gap-x-2">
              <span className="label">Answer</span>
              <span className="font-semibold text-good">
                {q.answer ? `${q.answer}. ${q.answer_text}` : q.answer_text}
              </span>
            </div>
            <Markdown>{q.explanation}</Markdown>
            {q.kind === 'mcq' && picked !== null && !quizMode && (
              <Button variant="quiet" className="-ml-2" onClick={() => setPicked(null)}>
                Try again
              </Button>
            )}
            {q.kind !== 'mcq' && (
              <div className="flex flex-wrap items-center gap-2 pt-1">
                <span className="text-sm text-muted">Could you write this in the exam?</span>
                <Button variant={p.status === 'correct' ? 'primary' : 'ghost'} onClick={() => setProgress(key, { status: 'correct' })}>
                  Yes, got it
                </Button>
                <Button variant={p.status === 'wrong' ? 'primary' : 'ghost'} onClick={() => setProgress(key, { status: 'wrong' })}>
                  Revise again
                </Button>
                <Button variant="quiet" onClick={() => setOpen(false)}>
                  Hide
                </Button>
              </div>
            )}
          </div>
        )}
      </div>
    </article>
  )
}
