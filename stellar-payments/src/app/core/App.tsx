import { ConfigProvider } from 'antd'
import { AppProvider } from 'services/hooks'

import { CoreRouter } from 'app/core/routes'

import ErrorBoundary from './error-boundary'

const App = (): JSX.Element => (
  <ErrorBoundary displayMessage="Ooooppss... An unexpected error occured">
    <AppProvider>
      <ConfigProvider
        theme={{
          token: {
            colorPrimary: '#2c3e50',
          },
        }}
      >
        <CoreRouter />
      </ConfigProvider>
    </AppProvider>
  </ErrorBoundary>
)

export default App
