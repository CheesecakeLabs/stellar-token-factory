import React from 'react'
import ReactDOM from 'react-dom/client'

import reportWebVitals from './config/reportWebVitals'
import App from 'app/core/App'

import './index.css'

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement)
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)

reportWebVitals()
