export const burnErrors = {
  distributor: '',
  amount: '',
}

export const defaultBurn = {
  issuer: '',
  distributor: '',
  asset_code: '',
  amount: '',
}

export const getInitialBurn = (key: string): typeof defaultBurn => {
  defaultBurn.distributor = key
  return defaultBurn
}
