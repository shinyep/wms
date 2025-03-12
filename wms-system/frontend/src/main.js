import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// 导入Element UI中文语言包
import locale from 'element-ui/lib/locale/lang/zh-CN'

import '@/assets/styles/style.scss' // global css

import i18n from './lang' // internationalization
import './icons' // icon
import './permission' // permission control

// 导入调试工具（仅在开发环境或需要排查问题时使用）
import './utils/debug'

// 使用Element UI并设置中文
Vue.use(ElementUI, { locale })

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  i18n,
  render: h => h(App)
}) 