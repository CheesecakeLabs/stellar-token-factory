export interface IAssetProps {
  code: string
  issuer: string
  supply: number
  name: string
}

export interface IIssuerInfo {
  freeze: boolean
  clawback: boolean
  assets: IAssetProps[]
}

export interface ITransactionResponse {
  envelope_xdr: string
  required_signatures: ['']
}

export interface IEnvelopeResponse {
  transaction_hash: string
  transaction_link: string
}

export interface IAssetDistributor {
  public_key: string
}

export interface ITomlResponse {
  toml: string
}
