import { BrowserRouter as Router, Switch } from 'react-router-dom'

import { Authentication } from '../auth'
import ModuleRoutes from './module-routes'
import { coreRoutes } from './routes'

const CoreRouter = (): JSX.Element => (
  <Router>
    <Switch>
      <ModuleRoutes
        routes={coreRoutes}
        isAuthenticated={Authentication.isAuthenticated}
      />
    </Switch>
  </Router>
)

export { CoreRouter }
