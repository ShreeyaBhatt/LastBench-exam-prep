import { Link, Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import { Empty } from './components/ui'
import Ask from './pages/Ask'
import Course from './pages/Course'
import Deck from './pages/Deck'
import Focus from './pages/Focus'
import Formulas from './pages/Formulas'
import Home from './pages/Home'
import Labs from './pages/Labs'
import Mock from './pages/Mock'
import Plan from './pages/Plan'
import Progress from './pages/Progress'
import Quiz from './pages/Quiz'
import Review from './pages/Review'
import Settings from './pages/Settings'
import Studio from './pages/Studio'
import Subject from './pages/Subject'
import Syllabus from './pages/Syllabus'
import Unit from './pages/Unit'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="plan" element={<Plan />} />
        <Route path="review" element={<Review />} />
        <Route path="cn" element={<Course />} />
        <Route path="cn/units/:id" element={<Unit />} />
        <Route path="cn/syllabus" element={<Syllabus />} />
        <Route path="cn/mock" element={<Mock />} />
        <Route path="cn/formulas" element={<Formulas />} />
        <Route path="cn/quiz" element={<Quiz />} />
        <Route path="cn/labs" element={<Labs />} />
        <Route path="studio" element={<Studio />} />
        <Route path="studio/:id" element={<Deck />} />
        <Route path="ask" element={<Ask />} />
        <Route path="focus" element={<Focus />} />
        <Route path="progress" element={<Progress />} />
        <Route path="settings" element={<Settings />} />
        <Route path="subjects/:sid" element={<Subject />} />
        <Route
          path="*"
          element={<Empty title="Page not found" action={<Link to="/" className="text-accent underline">Back to home</Link>} />}
        />
      </Route>
    </Routes>
  )
}
