export const mintErrors = {
  distributor: '',
  amount: '',
}

export const defaultMint = {
  issuer: '',
  distributor: '',
  asset_code: '',
  amount: '',
}

export const getInitialMint = (key: string): typeof defaultMint => {
  defaultMint.distributor = key
  return defaultMint
}
