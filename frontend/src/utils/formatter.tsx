export const formatNumber = (value: number): string => {
  const moneyFormatter = new Intl.NumberFormat('en-US')
  return moneyFormatter.format(value)
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

export const formatMonth = (date: number): string => {
  const formattedDate = new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  })

  return formattedDate
}
