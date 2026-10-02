/** Where each kind of study-plan task takes the student. */
export function taskLink(task) {
  switch (task.type) {
    case 'notes':
      return `/cn/units/${task.unit}`
    case 'questions':
      return `/cn/units/${task.unit}?tab=questions`
    case 'topic':
      return `/cn/units/${task.unit}?tab=questions&topic=${task.topic}`
    case 'syllabus':
      return '/cn/syllabus'
    case 'review':
      return '/review'
    case 'quiz':
      return '/cn/quiz?smart=1'
    case 'mock':
      return `/cn/mock?test=${task.test || 'T1'}`
    case 'formulas':
      return '/cn/formulas'
    case 'deck':
      return `/studio/${task.deck}`
    case 'upload':
      return '/studio'
    default:
      return '/'
  }
}
