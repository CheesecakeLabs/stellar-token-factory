export const labelsFromMonth = (): string[] => {
  return [
    '10 Mar',
    '11 Mar',
    '12 Mar',
    '13 Mar',
    '14 Mar',
    '15 Mar',
    '16 Mar',
    '17 Mar',
  ]
}

export const labelsFromYear = (): string[] => {
  return ['SEP', 'OCT', 'NOV', 'DEC', 'JAN', 'FEB', 'MAR']
}

export const labelsChart = (mode: 'MONTH' | 'YEAR' | 'ALL'): string[] => {
  if (mode == 'MONTH') {
    return labelsFromMonth()
  }
  if (mode == 'YEAR') {
    return labelsFromYear()
  }
  return labelsFromYear()
}
