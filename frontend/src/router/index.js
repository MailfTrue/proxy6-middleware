import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { layout: 'auth' }
  },
  {
    path: '/proxy',
    name: 'My Proxy',
    component: () => import("../views/MyProxy")
  },
  {
    path: '/buy',
    name: 'Buy Proxy',
    component: () => import("../views/BuyProxy")
  },
  {
    path: '/wallet',
    name: 'Wallet',
    component: () => import("../views/Wallet")
  }
]

const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  const publicPages = ['/login'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('user');

  if (authRequired && !loggedIn) {
    next('/login');
  } else {
    next();
  }
});

export default router
