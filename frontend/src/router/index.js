import Login from '@/views/Login'
import Project from '@/views/Project'
import Layout from '@/views/Layout/Layout'
import NotFound from '@/views/ErrorPage/NotFound'
import NotAuth from '@/views/ErrorPage/NotAuth'

export const constantRouterMap = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  { path: '/404', component: NotFound, hidden: true },
  { path: '/401', component: NotAuth, hidden: true },
  {
    path: '/',
    component: Layout,
    redirect: 'project',
    children: [{
      path: 'project',
      component: Project,
      name: 'Project',
      meta: { title: 'Project', icon: 'dashboard', noCache: true }
    }]
  }
]

export const asyncRouterMap = [
  {
    path: '/error',
    component: Layout,
    redirect: 'noredirect',
    name: 'errorPages',
    meta: {
      title: 'errorPages',
      icon: '404'
    },
    children: [
      { path: '401', component: NotAuth, name: 'page401', meta: { title: 'page401', noCache: true }},
      { path: '404', component: NotFound, name: 'page404', meta: { title: 'page404', noCache: true }}
    ]
  }
]

export default constantRouterMap

