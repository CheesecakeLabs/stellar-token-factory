import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Factory from '../pages/factory'
import Home from '../pages/home'
import Management from '../pages/management'
import Quickstart from '../pages/quickstart'

export interface IProps {
  children: JSX.Element
}

const CoreRouter = (): JSX.Element => (
  <BrowserRouter basename='/sandbox/v1'>
    <Routes>
      <Route path="/" element={<Quickstart />} />
      <Route path="/home" element={<Home />} />
      <Route path="/factory" element={<Factory />} />
      <Route path="/management" element={<Management />} />
    </Routes>
  </BrowserRouter>
)

export { CoreRouter }
