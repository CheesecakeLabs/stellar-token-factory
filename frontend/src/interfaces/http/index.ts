import { getNetwork } from '@stellar/freighter-api'
import axios from 'axios'

const http = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  withCredentials: false,
})

http.interceptors.request.use(async config => {
  const network = await getNetwork()
  if (network && config.headers) {
    config.headers.network = network
  }
  return Promise.resolve(config)
})

export { http }
