export const toEur = (num: number): string => {
  return '€ ' + num.toFixed(2).replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
}

export const toUsd = (num: number): string => {
  return '$ ' + num.toFixed(2).replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
}

export const formatValueToNumber = (value: string | undefined): number => {
  if (!value) return 0
  const valueWithoutDot = value.replaceAll(',', '')

  return Number(valueWithoutDot)
}
