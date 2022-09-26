import { Dispatch, SetStateAction } from 'react'
import { messageError } from 'services/factory/constants'
import { defaultFinancialDetails, financialDetailsErrors } from './constants'

export const validateInputError = (
  inputs: typeof defaultFinancialDetails,
  setInputsErrors: Dispatch<SetStateAction<typeof financialDetailsErrors>>,
  setError: Dispatch<SetStateAction<string>>
): boolean => {
  let hasError = false
  try {
    if (!inputs.name) {
      hasError = true
      setInputsErrors(values => ({
        ...values,
        ['name']: 'The Hash must be informed',
      }))
    }
  } catch (e) {
    hasError = true
    setError((e as string) || 'There are invalid fields')
  }
  return hasError
}

export const handleSubmitErrors = (
  responseError: typeof financialDetailsErrors,
  code: number,
  error: string,
  setInputsErrors: Dispatch<SetStateAction<typeof financialDetailsErrors>>,
  setError: Dispatch<SetStateAction<string>>
): void => {
  const defaultMessageError =
    'An error has occurred, please check the information provided.'
  if (code) {
    const error = messageError.get(code)
    setError(error ?? defaultMessageError)
    return
  }
  if (responseError?.value) {
    setInputsErrors(values => ({ ...values, ['value']: responseError.value }))
  }
  if (responseError?.name) {
    setInputsErrors(values => ({ ...values, ['name']: responseError.name }))
  }
  if (!error) {
    setError(defaultMessageError)
  }
}
