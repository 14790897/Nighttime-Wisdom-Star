import { createI18n } from 'vue-i18n'

const messages = {
  en: {
    message: {
      hello: 'Hello world',
      login: 'Login',
      login
    },
  },
  cn: {
    message: {
      hello: '你好',
        login: '登录',
    },
  },
}

const i18n = createI18n({
  locale: 'en', // 默认显示的语言 
  messages,
})

export default i18n
