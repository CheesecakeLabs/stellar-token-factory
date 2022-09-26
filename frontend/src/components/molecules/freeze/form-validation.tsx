import { Dispatch, SetStateAction } from 'react'
import { messageError } from 'services/factory/constants'
import { defaultFreeze, freezeErrors } from './constants'

export const validateInputError = (
  inputs: typeof defaultFreeze,
  setInputsErrors: Dispatch<SetStateAction<typeof freezeErrors>>,
  setError: Dispatch<SetStateAction<string>>
): boolean => {
  let hasError = false
  try {
    if (!inputs.target) {
      hasError = true
      setInputsErrors(values => ({
        ...values,
        ['target']: 'The target must be informed',
      }))
    }
  } catch (e) {
    hasError = true
    setError((e as string) || 'There are invalid fields')
  }
  return hasError
}

export const handleSubmitErrors = (
  responseError: typeof freezeErrors,
  code: number,
  error: string,
  setInputsErrors: Dispatch<SetStateAction<typeof freezeErrors>>,
  setError: Dispatch<SetStateAction<string>>
): void => {
  const defaultMessageError =
    'An error has occurred, please check the information provided.'
  if (code) {
    const error = messageError.get(code)
    setError(error ?? defaultMessageError)
    return
  }
  if (responseError?.target) {
    setInputsErrors(values => ({ ...values, ['amount']: responseError.target }))
  }
  if (responseError?.memo_text) {
    setInputsErrors(values => ({
      ...values,
      ['distributor']: responseError.memo_text,
    }))
  }
  if (!error) {
    setError(defaultMessageError)
  }
}
