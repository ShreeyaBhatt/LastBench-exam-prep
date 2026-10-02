import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import FlashCard from '../components/FlashCard'
import { Empty, PageHeader, ProgressBar, Spinner } from '../components/ui'
import { api } from '../lib/api'

export default function Review() {
  const [due, setDue] = useState(null)
  const [queue, setQueue] = useState([])
  const [doneCount, setDoneCount] = useState(0)
  const [flipped, setFlipped] = useState(false)
  const [units, setUnits] = useState([])

  useEffect(() => {
    api.reviewDue().then((d) => {
      setDue(d)
      setQueue([...d.cards, ...d.new_cards])
    })
    api.subject('cn').then((s) => setUnits(s.units))
  }, [])

  const card = queue[0]
  const grade = useCallback(
    (g) => {
      if (!card) return
      api.review(card.key, g).catch(() => {})
      setFlipped(false)
      // "Again" sends the card to the back of today's queue; anything else is done for today.
      setQueue((q) => (g === 'again' ? [...q.slice(1), q[0]] : q.slice(1)))
      if (g !== 'again') setDoneCount((n) => n + 1)
    },
    [card],
  )

  if (!due) return <Spinner />
  const unitOf = (id) => units.find((u) => u.qids.includes(id))
  const total = doneCount + queue.length

  return (
    <div className="space-y-8">
      <PageHeader eyebrow="Spaced repetition" title="Daily review">
        Cards come back just before you would forget them: rate each one and {''}
        <b>Again</b> shows it later today, <b>Good</b> in a few days, <b>Easy</b> even later. Questions you got wrong in practice wait here too.
      </PageHeader>

      <section className="space-y-4">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <h2 className="text-xl font-bold">Flashcards</h2>
          {total > 0 && (
            <span className="tabular text-sm text-muted">
              {doneCount} of {total} done · {due.cards.length} due, {due.new_cards.length} new
            </span>
          )}
        </div>
        {total > 0 && <ProgressBar value={doneCount} total={total} colour="var(--good)" />}
        {card ? (
          <FlashCard
            card={card}
            flipped={flipped}
            setFlipped={setFlipped}
            onGrade={grade}
            eyebrow={`${card.new ? 'New · ' : ''}${card.deck_title}${card.topic ? ` · ${card.topic}` : ''}`}
          />
        ) : total > 0 ? (
          <Empty title="All cards done for today">Come back tomorrow. The schedule spaces cards out so each review sticks.</Empty>
        ) : (
          <Empty title="No flashcards yet" action={<Link to="/studio" className="text-accent underline">Open Notes Studio</Link>}>
            Flashcards come from study packs. Upload notes in Notes Studio and their cards show up here every day.
          </Empty>
        )}
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Questions to revise</h2>
        {due.questions.length === 0 ? (
          <p className="text-sm text-muted">Nothing due. Questions you answer wrong appear here, then come back on a spaced schedule once you get them right.</p>
        ) : (
          <ul className="grid gap-2 sm:grid-cols-2">
            {due.questions.map((id) => {
              const u = unitOf(id)
              return (
                <li key={id}>
                  <Link
                    to={u ? `/cn/units/${u.id}?tab=questions#q${id}` : '/cn'}
                    className="flex items-center gap-3 rounded-lg border border-line bg-surface px-3 py-2.5 text-sm hover:border-ink/40"
                  >
                    <span className="font-mono font-semibold" style={{ color: u?.accent }}>Q{id}</span>
                    <span className="text-muted">Unit {u?.id}: {u?.title}</span>
                    <span className="ml-auto text-accent">→</span>
                  </Link>
                </li>
              )
            })}
          </ul>
        )}
      </section>
    </div>
  )
}
