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

    interface IPaymentData {
      amount: number
      payee: string
      createdAt: number
      envelope_xdr: string
      final_cost: number
      usd_price: number
      sign: number
      user_id?: string
      createdBy: string
      status: StatusPayment
      transactionLink?: string
      typePayment: TypePayment
    }

    interface IPaymentContext {
      createPayment(params: IPaymentParams): Promise<IPayment | undefined>
      loading: boolean
      payment: IPayment | undefined
      submit: ISubmit | undefined
      makeSubmit(params: ISubmitParams): Promise<ISubmit | undefined>
      updatePayment(params: IPaymentData): boolean
      setSubmit: Dispatch<SetStateAction<ISubmit | undefined>>
      addLocalPayment(params: IPaymentData): boolean
      getLocalPayments(user: string): IPaymentData[]
      localPayments: IPaymentData[] | undefined
    }
  }
}
