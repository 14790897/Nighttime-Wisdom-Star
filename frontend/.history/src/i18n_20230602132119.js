import { createI18n } from 'vue-i18n'

const messages = {
  en: {
    message: {
      hello: 'Hello world',
      login: 'Login',
      loginfailed:'Login failed. Please check your username and password.',
      register: 'Register',
      registerfailed:'Register failed. ',
    },
  },
  cn: {
    message: {
      hello: '你好',
        login: '登录',
        loginfailed:'登录失败，请检查用户名和密码。',
        register: '注册',
    },
  },
}

const i18n = createI18n({
  locale: 'en', // 默认显示的语言 
  messages,
})

export default i18n
