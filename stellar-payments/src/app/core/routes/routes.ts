import { Home } from '../pages/home';
import { Login } from '../pages/login';
import { IAppRoute } from './types';


export const coreRoutes: IAppRoute[] = [
  { path: '/', exact: true, component: Login },
  { path: '/home', exact: true, component: Home },
  { path: '/private', exact: true, component: Home, isPrivate: true },
]