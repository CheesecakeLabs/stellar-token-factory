export const defaultOrgDoc = {
  name: undefined,
  url: undefined,
  logo: undefined,
  description: undefined,
  physical_address: undefined,
  twitter: undefined,
  github: undefined,
  official_email: undefined,
  support_email: undefined,
}

export const defaultGenerateToml = {
  general_info: {
    accounts: [],
  },
  org_doc: defaultOrgDoc,
  point_of_contact_doc: [],
  currency_doc: [],
}

export const inputsGeneralInfo = {
  account: '',
}

export const inputsContact = {
  name: '',
  email: '',
}

export const inputsCurrencyDoc = {
  code: '',
  issuer: '',
  status: '',
  name: '',
  desc: '',
  image: '',
  is_asset_anchored: false,
  anchor_asset_type: '',
  anchor_asset: '',
  attestation_of_reserve: '',
  redemption_instructions: '',
}

export interface IAccountValue {
  value: string
}

export interface IContact {
  name: string
  email: string
}

export interface ICurrency {
  code: string
  issuer: string
  status: string
  name: string
  desc: string
  image: string
  is_asset_anchored: boolean
  anchor_asset_type: string
  anchor_asset: string
  attestation_of_reserve: string
  redemption_instructions: string
}

export interface IToml {
  general_info: {
    accounts: string[]
  }
  org_doc: {
    name?: string
    url?: string
    logo?: string
    description?: string
    physical_address?: string
    twitter?: string
    github?: string
    official_email?: string
    support_email?: string
  }
  point_of_contact_doc: IContact[]
  currency_doc: ICurrency[]
}
