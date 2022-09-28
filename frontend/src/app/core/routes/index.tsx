import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Authentication } from '../auth'
import Factory from '../pages/factory'
import Home from '../pages/home'
import Login from '../pages/login'
import Management from '../pages/management'

export interface IProps {
  children: JSX.Element
}

const ProtectedRoute = ({ children }: IProps): JSX.Element => {
  if (!Authentication.isAuthenticated()) {
    return <Navigate to={'/login'} replace />
  }

  return children
}

const CoreRouter = (): JSX.Element => (
  <BrowserRouter>
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        }
      />
      <Route
        path="/factory"
        element={
          <ProtectedRoute>
            <Factory />
          </ProtectedRoute>
        }
      />
      <Route
        path="/management"
        element={
          <ProtectedRoute>
            <Management />
          </ProtectedRoute>
        }
      />
    </Routes>
  </BrowserRouter>
)

export { CoreRouter }
