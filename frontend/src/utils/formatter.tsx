export const toMoney = (value: number): string => {
  const moneyFormatter = new Intl.NumberFormat('pt-br', {
    style: 'currency',
    currency: 'BRL',
  })

  return moneyFormatter.format(value)
}

export const toCrypto = (value?: number): string => {
  if (!value) value = 0
  return value.toFixed(4).replace('.', ',')
}

export const formatDate = (date: number): string => {
  const formattedDate = new Date(date).toLocaleDateString('en-US', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
  })

  return formattedDate
}

export const formatSimpleDate = (date: number): string => {
  const formattedDate = new Date(date).toLocaleDateString('en-US', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })

  return formattedDate
}
