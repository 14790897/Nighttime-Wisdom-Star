import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/UserHome.vue'
import Login from '../components/UserLogin.vue'
import Register from '../components/UserRegister.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/Login',
      name: 'Login',
      component: Login
    },
    {
      path: '/Register',
      name: 'Register',
      component: Register
    }
  ]
})
export default router;
