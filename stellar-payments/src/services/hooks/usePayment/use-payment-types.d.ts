declare namespace Hooks {
  namespace UsePaymentTypes {
    interface IPaymentParams {
      destination_public_key: string
      receive_amount: number
    }

    interface IPayment {
      envelope_xdr: string
      final_cost: number
    }

    interface IPaymentContext {
      createPayment(params: IPaymentParams): Promise<IPayment | undefined>
      loading: boolean
      payment: IPayment | undefined
    }
  }
}
