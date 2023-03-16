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

export interface ITopHolders {
  account: string
  symbol: string
  balance: number
  percentage: number
}

export interface IGeneralInfo {
  total_supply: number | undefined
  total_in_circulation: number | undefined
  total_trustlines: number | undefined
  total_reserves: number | undefined
  last_updated: number
  top_holders: ITopHolders[]
}

export interface IInfoTransaction {
  date: number
  amount: number
  symbol: string
  hash: string
}

export interface IMintInfo {
  total_supply: number | undefined
  total_in_circulation: number | undefined
  total_mint_transactions: number | undefined
  total_reserves: number | undefined
  last_updated: number
  last_transactions: IInfoTransaction[]
}

export interface IBurnInfo {
  total_supply: number | undefined
  total_in_circulation: number | undefined
  total_burn_transactions: number | undefined
  total_reserves: number | undefined
  last_updated: number
  last_transactions: IInfoTransaction[]
}

export interface ITransferInfo {
  total_amount_transfered: number | undefined
  total_transfer_transactions: number | undefined
  last_updated: number
  last_transactions: IInfoTransaction[]
}

export interface IFrozenAccount {
  date_freeze: number
  account: string
}

export interface IFreezeInfo {
  total_frozen_accounts: number | undefined
  last_updated: number
  frozen_accounts: IFrozenAccount[]
}
