import { initReactI18next } from 'react-i18next'

import i18next from 'i18next'
import I18nextBrowserLanguageDetector from 'i18next-browser-languagedetector'
import Backend from 'i18next-http-backend'

import translationEN from './en/translationEN.json'
import translationES from './es/translationES.json'

const resources = {
  en: {
    translation: translationEN,
  },
  es: {
    translation: translationES,
  },
}

i18next
  .use(initReactI18next)
  .use(Backend)
  .use(I18nextBrowserLanguageDetector)
  .init({
    debug: true,
    resources: resources,
  })
