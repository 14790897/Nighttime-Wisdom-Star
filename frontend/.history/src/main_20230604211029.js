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

对不起，我误解了你的问题。你完全正确。当你的前端和 Nginx 在同一个 Docker 容器中时，你应该设置 Axios 的 `baseURL` 为当前容器的服务名称，也就是 Docker Compose 文件中定义的服务名称（在这个例子中是 `frontend`）。然后，你的前端应用可以通过 Nginx 代理将请求发送到后端服务。

在你的例子中，应该将 Axios 的 `baseURL` 设置为 'http://frontend'（不是 'http://frontend:5000'，因为 Nginx 在容器中监听的端口是80，除非你在 Dockerfile 中改变了 Nginx 的监听端口）。然后，当你发送一个以 `/api/` 开头的请求时，Nginx 将会把这个请求代理到后端服务。

我对之前的误解向你表示歉意，我应该更仔细地理解你的问题。希望现在的答复能够解答你的问题。
const app = createApp(App)

app.config.globalProperties.$http = axios;
app.config.globalProperties.$http.defaults.baseURL = '//http://frontend:5000';//http://0.0.0.0:5000 https://flaskcloud.liuweiqing.top/
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
