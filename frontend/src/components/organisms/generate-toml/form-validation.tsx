import { Dispatch, SetStateAction } from 'react'
import { messageError } from 'services/factory/constants'
import { IToml } from './constants'

export const handleSubmitErrors = (
  responseError: IToml,
  code: number,
  setError: Dispatch<SetStateAction<string>>
): void => {
  const defaultMessageError =
    'An error has occurred, please check the information provided.'
  if (code) {
    const error = messageError.get(code)
    setError(error ?? defaultMessageError)
    return
  }
  if (responseError?.org_doc?.url) {
    setError(`ORG URL: Only URLs with HTTPS are allowed.`)
    return
  }
  if (responseError?.org_doc?.logo) {
    setError(`ORG Logo: Enter a valid URL`)
    return
  }
  setError(defaultMessageError)
}
