import { createI18n } from 'vue-i18n'

const messages = {
  en: {
    message: {
      hello: 'Hello world',
    },
  },
  fr: {
    message: {
      hello: 'Bonjour le monde',
    },
  },
  es: {
    message: {
      hello: 'Hola mundo',
    },
  },
}

const i18n = createI18n({
  locale: 'en', // 默认显示的语言 
  messages,
})

export default i18n
