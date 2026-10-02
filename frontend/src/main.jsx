import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import './index.css'
import { FocusProvider } from './lib/focus'
import { AppProvider } from './lib/store'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <AppProvider>
        <FocusProvider>
          <App />
        </FocusProvider>
      </AppProvider>
    </BrowserRouter>
  </StrictMode>,
)
