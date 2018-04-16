import Vue from 'vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import App from './App.vue'
import constantRouterMap from './router/index.js'
import store from './store'
import './icons'
import './styles/index.scss'
import 'element-theme-chalk'
import { getToken } from '@/utils/auth'

Vue.use(ElementUI)
Vue.use(VueRouter)

const router = new VueRouter({
  // mode: 'history',
  routes: constantRouterMap
})

router.beforeEach((to, from, next) => {
  try {
    var tmp = getToken()
    console.log(tmp)
    if (tmp === undefined) {
      console.log('Token is undefined')
    }
  } catch (e) {
    console.log(e)
  }
  if (getToken() === undefined && to.path !== '/login') { // 通过vuex state获取当前的token是否存在
    next('/login')
  } else {
    next()
  }
})

new Vue({
  el: '#app',
  router: router,
  store: store,
  render: h => h(App),
  template: '<App />',
  components: { App }
})
