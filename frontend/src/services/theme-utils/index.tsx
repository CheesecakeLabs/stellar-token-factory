export const textColorByTheme = (isDarkMode: boolean | undefined): string => {
  if (isDarkMode == undefined) {
    return document.body.className == 'dark-mode' ? 'white' : 'black'
  }
  return isDarkMode ? 'white' : 'black'
}
