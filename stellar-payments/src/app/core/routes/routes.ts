import { Home } from '../pages/home'
import { Login } from '../pages/login'
import { IAppRoute } from './types'

export const coreRoutes: IAppRoute[] = [
  { path: '/', exact: true, component: Home, isPrivate: true },
  { path: '/login', exact: true, component: Login },
  { path: '/private', exact: true, component: Home, isPrivate: true },
]
