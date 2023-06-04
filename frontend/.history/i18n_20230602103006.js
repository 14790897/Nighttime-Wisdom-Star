import { createI18n } from 'vue-i18n'

const messages = {
  en: {
    message: {
      hello: 'Hello world',
      login: 'Login',
    },
  },
  fr: {
    message: {
      hello: 'Bonjour le monde',
    },
  },
}

const i18n = createI18n({
  locale: 'en', // 默认显示的语言 
  messages,
})

export default i18n
