import Vue from 'vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import App from './App.vue'
import constantRouterMap from './router/index.js'
import store from './store'
import './icons'
import './styles/index.scss'
import 'element-theme-chalk'

Vue.use(ElementUI)

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  routes: constantRouterMap
})

new Vue({
  el: '#app',
  router: router,
  store: store,
  render: h => h(App),
  template: '<App />',
  components: { App }
})

router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) { // 判断该路由是否需要登录权限
    if (store.state.token) { // 通过vuex state获取当前的token是否存在
      next()
    } else {
      next({
        path: '/login',
        query: { redirect: to.fullPath } // 将跳转的路由path作为参数，登录成功后跳转到该路由
      })
    }
  } else {
    next()
  }
})
