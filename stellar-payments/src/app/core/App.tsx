import { AppProvider } from 'services/hooks'

import { CoreRouter } from 'app/core/routes'

import ErrorBoundary from './error-boundary'

const App = (): JSX.Element => (
  <ErrorBoundary displayMessage="Ooooppss... An unexpected error occured">
    <AppProvider>
      <CoreRouter />
    </AppProvider>
  </ErrorBoundary>
)

export default App
