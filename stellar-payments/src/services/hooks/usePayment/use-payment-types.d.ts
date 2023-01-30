declare namespace Hooks {
  namespace UsePaymentTypes {
    interface IPaymentParams {
      destination_public_key: string
      receive_amount: number
      user_id: string
    }

    interface IPayment {
      envelope_xdr: string
      final_cost: number
      required_signatures: string[]
      usd_price: number
    }

    interface ISubmitParams {
      envelope_xdr: string
      sign: number
      user_id: string
    }

    interface ISubmit {
      transaction_hash: string
      transaction_link: string
    }

    interface IPendingSigner {
      envelope_xdr: string
      final_cost: number
      usd_price: number
      amount: number
      sign: number
      user_id: string
      date: number
      payee: string
    }

    interface IPaymentData {
      payee: string
      amount: number
      createdAt: number
      expirationAt: number
    }

    interface IPaymentContext {
      createPayment(params: IPaymentParams): Promise<IPayment | undefined>
      loading: boolean
      payment: IPayment | undefined
      submit: ISubmit | undefined
      makeSubmit(params: ISubmitParams): Promise<ISubmit | undefined>
      addUserToPendingSigners(params: IPendingSigner): boolean
      getPendingSigners(user: string, payee: string): IPendingSigner[]
      pendingSigners: IPendingSigner[] | undefined
      removePendingSigners(params: IPendingSigner): boolean
      setSubmit: Dispatch<SetStateAction<ISubmit | undefined>>
      setPendingSigners: Dispatch<SetStateAction<IPendingSigner[] | undefined>>
    }
  }
}
