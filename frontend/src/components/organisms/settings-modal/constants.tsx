export const inputsAccounts = {
  account: '',
}

export interface IAccounts {
  accounts: ['']
}

export interface ISettings {
  signers: string[],
  freeze: boolean,
  clawback: boolean,
  public_key?: string
}

export const defaultSettings = {
  signers: [],
  freeze: false,
  clawback: false
}
