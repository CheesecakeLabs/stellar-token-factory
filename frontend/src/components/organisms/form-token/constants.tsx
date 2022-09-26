export const defaultAsset = {
  issuer: '',
  distributor: '',
  asset_code: '',
  limit: '',
}

export const defaultResponseSubmit = {
  transaction_hash: '',
  transaction_link: '',
}

export const defaultErrors = {
  issuer: '',
  distributor: '',
  asset_code: '',
  limit: '',
}

export const getInitialAsset = (key: string): typeof defaultAsset => {
  defaultAsset.issuer = key
  return defaultAsset
}
