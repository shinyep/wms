import router from './router'
import store from './store'
import Vue from 'vue'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import { getToken } from '@/utils/auth'
import getPageTitle from '@/utils/get-page-title'

NProgress.configure({ showSpinner: false })

// 修改白名单，添加注册页面
const whiteList = ['/login', '/register', '/auth-redirect']

router.beforeEach(async(to, from, next) => {
  NProgress.start()

  // 设置页面标题
  document.title = getPageTitle(to.meta.title)

  // 获取token
  const hasToken = getToken()
  console.log('当前token:', hasToken, '目标路由:', to.path)

  if (hasToken) {
    if (to.path === '/login') {
      // 已登录，访问登录页则重定向到首页
      next('/dashboard')
      NProgress.done()
    } else {
      // 检查是否已经有角色信息
      const hasRoles = store.getters.roles && store.getters.roles.length > 0
      
      if (hasRoles) {
        next()
      } else {
        try {
          // 获取用户信息
          const { roles } = await store.dispatch('user/getInfo')
          // 生成路由
          const accessRoutes = await store.dispatch('permission/generateRoutes', roles)
          // 添加路由
          accessRoutes.forEach(route => {
            router.addRoute(route)
          })
          // 继续原来的导航
          next({ ...to, replace: true })
        } catch (error) {
          // 发生错误重置令牌并重定向到登录页面
          await store.dispatch('user/resetToken')
          Vue.prototype.$message.error(error.message || '获取用户信息失败')
          next('/login')
          NProgress.done()
        }
      }
    }
  } else {
    /* 没有token */
    if (whiteList.indexOf(to.path) !== -1) {
      // 在免登录白名单中，直接进入
      next()
    } else {
      // 其他无权访问的页面将重定向到登录页面
      next('/login')
      NProgress.done()
    }
  }
})

router.afterEach(() => {
  NProgress.done()
}) 