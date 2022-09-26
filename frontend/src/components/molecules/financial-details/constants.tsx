export const financialDetailsErrors = {
  name: '',
  value: '',
}

export const defaultFinancialDetails = {
  name: '',
  value: '',
  public_key: '',
}

export const getInitialFinancialDetails = (
  key: string
): typeof defaultFinancialDetails => {
  defaultFinancialDetails.public_key = key
  return defaultFinancialDetails
}
