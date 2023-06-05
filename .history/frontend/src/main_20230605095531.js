import { createApp } from 'vue'
import axios from 'axios'
import App from './App.vue'
import router from './router'
import store from './store/store'
import i18n from './i18n'
import * as Sentry from "@sentry/vue";
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'
import 'bootstrap';


const app = createApp(App)

app.config.globalProperties.$http = axios;
app.config.globalProperties.$http.defaults.baseURL = 'http://frontend:80';//http://0.0.0.0:5000 https://flaskcloud.liuweiqing.top/
app.config.globalProperties.$http.defaults.withCredentials = true; 


app.use(router)
app.use(store)
app.use(i18n)

Sentry.init({
    app,
    dsn: "https://68742d8b5db1471cb398c6c509348e3a@o4505255803551744.ingest.sentry.io/4505255806631936",
    integrations: [
      new Sentry.BrowserTracing({
        // Set `tracePropagationTargets` to control for which URLs distributed tracing should be enabled
        tracePropagationTargets: ["localhost", /^https:\/\/yourserver\.io\/api/],
        routingInstrumentation: Sentry.vueRouterInstrumentation(router),
      }),
      new Sentry.Replay(),
    ],
    // Performance Monitoring
    tracesSampleRate: 1.0, // Capture 100% of the transactions, reduce in production!
    // Session Replay
    replaysSessionSampleRate: 0.1, // This sets the sample rate at 10%. You may want to change it to 100% while in development and then sample at a lower rate in production.
    replaysOnErrorSampleRate: 1.0, // If you're not already sampling the entire session, change the sample rate to 100% when sampling sessions where errors occur.
  });

  app.mount('#app')
