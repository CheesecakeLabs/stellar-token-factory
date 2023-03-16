export const transferErrors = {
  distributor: '',
  amount: '',
  target: '',
}

export const defaultTransfer = {
  issuer: '',
  distributor: '',
  asset_code: '',
  amount: '',
  recipient: '',
}

export const getInitialTransfer = (key: string): typeof defaultTransfer => {
  defaultTransfer.distributor = key
  return defaultTransfer
}
