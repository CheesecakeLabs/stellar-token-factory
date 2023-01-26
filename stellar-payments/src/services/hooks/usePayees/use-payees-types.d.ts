declare namespace Hooks {
  namespace UsePayeesTypes {

    interface IPayee {
      name: string
      address: string
      phone: string
      bank_account: string
      stellar_wallet: string
    }

    interface IPayeesContext {
      getPayees(): Promise<IPayee[] | undefined>
      loading: boolean
      payees: IPayee[] | undefined
    }
  }
}
