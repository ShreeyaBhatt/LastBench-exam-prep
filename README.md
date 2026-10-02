# LastBench

Exam preparation for Computer Networks (Sem V), built from the T1 notes and the LJIET practice book, plus tools for any other subject.

## Start it

```powershell
cd "cn-exam-prep"
.\run.ps1
```

Open http://localhost:8000. The first run installs packages and builds the frontend. After changing frontend code, run `.\run.ps1 -rebuild`.

For development with hot reload use `.\dev.ps1` (FastAPI on :8000, Vite on http://localhost:5173).

If PowerShell blocks the script, run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## What's inside

Built around the official LJU Sem V syllabus (batch 2024) and the T1/T2 marks distribution: **T1 = Units 1-4, T2 = Units 5-10, each 50 marks = 20 MCQ + 5 descriptive + 25 numerical.**

| Section | What it does |
|---|---|
| Home | Greeting, test countdown, today's plan, streak, question of the day, weak-spot alert, subjects, tools |
| Study plan | Set T1/T2 dates; get a day-by-day plan of the questions you haven't got right, numericals first, last days for mock papers |
| Daily review | Spaced repetition (SM-2): flashcards and missed questions return just before you'd forget them |
| CN overview | Units grouped by test with syllabus weightage and the marks pattern |
| Units | One-minute notes, formulas, exam traps, syllabus topics, and every question with a worked solution (420 practice book + 28 syllabus extras) |
| Syllabus tracker | Every topic 1.1-10.2 with weightage, linked questions, and a revised checkbox; evaluation scheme, course outcomes, books |
| Mock T1 / T2 | Fresh 50-mark paper in the exact pattern, weighted by unit; timed exam mode with focus mode; MCQs auto-marked, self-marking for the rest |
| Quick quiz | Smart mode adapts to your weak units and missed questions, or pick units yourself |
| Formula sheet | Every formula and trap on one page |
| Labs & projects | Step guides for the 10 practicals and 5 projects: Packet Tracer, Cisco IOS (static/RIP/OSPF/DHCP), cable pinouts, Wireshark |
| Notes Studio | Upload notes (PDF/TXT/MD) for any subject; get detailed notes, flashcards, exam questions and a printable PDF |
| Ask AI | Ask a doubt; answers cite your notes, solved questions and uploads |
| Focus timer | Pomodoro (25/5/15) with generated rain or brown noise; Focus mode hides navigation |
| Progress | Streaks, 12-week activity heatmap, accuracy per unit (chart or table), mock scores |
| Settings | Easy-read fonts (Lexend, Atkinson Hyperlegible), text size, test dates, daily goal, subjects, reset |
| Subjects | CN is built in. EEF is an empty space ready for its material. Add more in Settings. |

The app's name lives in `frontend/src/lib/brand.js` if you want to change it.

Every unit also has a **Download PDF** button: notes, formulas, traps and all solutions as a revision booklet.

## Adding the Claude API key

Ask AI and Notes Studio work without a key, in a simpler offline mode. For written AI answers and full study packs:

1. Create a key at https://console.anthropic.com → API Keys → Create Key.
2. Copy `backend/.env.example` to `backend/.env`.
3. Set `ANTHROPIC_API_KEY=sk-ant-...` in that file.
4. Restart `run.ps1`. The sidebar badge changes to "Claude connected".

The key never leaves your computer except in requests to Anthropic. `backend/.env` is git-ignored.

Model: `claude-opus-5` by default (set `STUDYHUB_MODEL` in `.env` to change it). Requests enable server-side refusal fallbacks.

## Project layout

```
backend/
  app/main.py          FastAPI routes
  app/content/u01-u10  One-minute notes + a solution for every practice-book question
  app/solver.py        Generates CRC divisions, Dijkstra and Bellman-Ford step tables
  app/ai.py            Claude calls (Ask AI, study-pack generation)
  app/studio.py        Upload processing and the offline generator
  app/pdf_export.py    ReportLab PDFs
  app/data/            Extracted practice book + routing diagrams
  storage/             SQLite database and uploaded files (created on first run)
frontend/              React + Tailwind (Vite)
```

## Notes on the answers

- Hamming code: the T1 notes number bit positions from the right (position 1 = rightmost). The practice book's Q124 key uses left-to-right order; that solution explains both.
- Q236's forwarding table is missing from the practice book, so its solution explains the method and gives the key's answer.
- Where a question leaves something unstated (e.g. signal speed in Q32), the solution states the assumption.
