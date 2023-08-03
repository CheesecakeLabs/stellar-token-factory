import { Suspense } from 'react'

import { AppProvider } from 'services/hooks'

import { Loading } from 'components/atoms'

import '../../i18n/config'
import { CoreRouter } from 'app/core/routes'

import ErrorBoundary from './error-boundary'

const App = (): JSX.Element => (
  <ErrorBoundary displayMessage="Ooooppss... An unexpected error occured">
    <Suspense fallback={<Loading />}>
      <AppProvider>
        <CoreRouter />
      </AppProvider>
    </Suspense>
  </ErrorBoundary>
)

export default App
