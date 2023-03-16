import { AxiosResponse } from 'axios'
import { IToml } from 'components/organisms/generate-toml/constants'
import { ISettings } from 'components/molecules/settings-modal/constants'
import { http } from 'interfaces/http'
import {
  IAssetDistributor,
  ITransactionResponse,
  IEnvelopeResponse,
  IIssuerInfo,
} from './interfaces'

const getIssuerInfo = async (
  publicKey: string
): Promise<AxiosResponse<IIssuerInfo>> => {
  return http.get(`/api/v1/wallets/${publicKey}/issuer-info`)
}

const addAsset = async (
  issuer: string,
  distribution: string,
  asset_code: string,
  limit: string
): Promise<AxiosResponse<ITransactionResponse>> => {
  return http.post(`/api/v1/assets`, {
    issuer: issuer,
    distributor: distribution,
    asset_code: asset_code,
    limit: limit.length > 0 ? limit : null,
  })
}

const postEnvelope = async (
  envelope_xdr: string
): Promise<AxiosResponse<IEnvelopeResponse>> => {
  return http.post(`/api/v1/transactions/submit`, {
    envelope_xdr: envelope_xdr,
  })
}

const getAssetDistributor = async (
  asset_code: string,
  asset_issuer: string
): Promise<AxiosResponse<IAssetDistributor>> => {
  return http.get(`/api/v1/assets/${asset_code}/${asset_issuer}/distributor`)
}

const postMint = async (
  issuer: string,
  distribution: string,
  asset_code: string,
  amount: string
): Promise<AxiosResponse<ITransactionResponse>> => {
  return http.post(`/api/v1/assets/mint`, {
    issuer: issuer,
    distributor: distribution,
    asset_code: asset_code,
    amount: amount,
  })
}

const postBurn = async (
  issuer: string,
  distribution: string,
  asset_code: string,
  amount: string
): Promise<AxiosResponse<ITransactionResponse>> => {
  return http.post(`/api/v1/assets/burn`, {
    issuer: issuer,
    distributor: distribution,
    asset_code: asset_code,
    amount: amount,
  })
}

const postTransfer = async (
  issuer: string,
  distribution: string,
  asset_code: string,
  amount: string,
  recipient: string
): Promise<AxiosResponse<ITransactionResponse>> => {
  return http.post(`/api/v1/transactions/payment`, {
    issuer: issuer,
    distributor: distribution,
    asset_code: asset_code,
    amount: amount,
    target: recipient,
  })
}

const postFinancialDetails = async (
  name: string,
  value: string,
  public_key: string
): Promise<AxiosResponse<ITransactionResponse>> => {
  return http.post(`/api/v1/transactions/manage-data`, {
    name: name,
    value: value.length > 0 ? value : null,
    public_key: public_key,
  })
}

const postClawback = async (
  issuer: string,
  target: string,
  asset_code: string,
  amount: string,
  claimableId: string,
  isClaimable: boolean
): Promise<AxiosResponse<ITransactionResponse>> => {
  const request = isClaimable
    ? {
        issuer: issuer,
        claimable_id: claimableId,
      }
    : {
        issuer: issuer,
        target: target,
        asset_code: asset_code,
        amount: amount,
      }

  return http.post(`/api/v1/transactions/clawback`, request)
}

const postFreeze = async (
  issuer: string,
  assetCode: string,
  target: string,
  memoText: string,
  isFreeze: boolean
): Promise<AxiosResponse<ITransactionResponse>> => {
  const operation = isFreeze ? 'clear-auth-flag' : 'set-auth-flag'
  return http.post(`/api/v1/wallets/${operation}`, {
    issuer: issuer,
    asset_code: assetCode,
    target: target,
    memo_text: memoText ? memoText : null,
  })
}

const postToml = async (toml: IToml): Promise<AxiosResponse> => {
  return http.post(`/api/v1/assets/generate-toml`, toml)
}

const postHomeDomain = async (
  home_domain: string,
  issuer: string
): Promise<AxiosResponse<ITransactionResponse>> => {
  return http.post(`/api/v1/wallets/set-home-domain`, {
    home_domain: home_domain,
    public_key: issuer,
  })
}

const getToml = async (public_key: string): Promise<AxiosResponse<IToml>> => {
  return http.get(`/api/v1/assets/retrieve-toml/${public_key}`)
}

const postSetOptions = async (
  settings: ISettings,
  isReadOnly: boolean
): Promise<AxiosResponse<ITransactionResponse>> => {
  return http.post(`/api/v1/wallets/set-options`, {
    public_key: settings.public_key,
    clawback: settings.clawback,
    freeze: settings.freeze,
    signers: isReadOnly ? null : settings.signers,
  })
}

const getSetOptions = async (
  public_key: string
): Promise<AxiosResponse<ISettings>> => {
  return http.get(`/api/v1/wallets/${public_key}/account-options`)
}

const FactoryService = {
  getIssuerInfo,
  addAsset,
  postEnvelope,
  getAssetDistributor,
  postMint,
  postBurn,
  postTransfer,
  postFinancialDetails,
  postClawback,
  postFreeze,
  postToml,
  postHomeDomain,
  getToml,
  postSetOptions,
  getSetOptions,
}

export { FactoryService }
