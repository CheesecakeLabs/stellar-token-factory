declare namespace Hooks {
  namespace UseAccountTypes {
    interface IBalance {
      balance: number
      asset_code: string
      asset_issuer: string
    }

    interface ISignIn {
      email: string
      password: string
    }

    interface IUser {
      email: string
      name: string
    }

    interface IAccountContext {
      getBalance(): Promise<IBalance | undefined>
      loading: boolean
      balance: IBalance | undefined
      signIn: (params: ISignIn) => Promise<boolean>
    }
  }
}
