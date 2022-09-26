export interface IAssetProps {
    code: string
    issuer: string
    supply: number
    name: string
  }
  
  export interface INewAssetResponse {
    envelope_xdr: string
    required_signatures: ['']
  }
  
  export interface ISubmitResponse {
    transaction_hash: string
    transaction_link: string
  }
  
  export interface IAssetDistributorProps {
    public_key: string
  }
  
  export interface IMintResponse {
    envelope_xdr: string
    required_signatures: ['']
  }