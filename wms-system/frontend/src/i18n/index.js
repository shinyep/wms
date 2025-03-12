import Vue from 'vue'
import VueI18n from 'vue-i18n'
import Cookies from 'js-cookie'

Vue.use(VueI18n)

const messages = {
  zh: {
    common: {
      search: '搜索',
      add: '添加',
      edit: '编辑',
      delete: '删除',
      confirm: '确定',
      cancel: '取消',
      reset: '重置',
      save: '保存',
      back: '返回',
      operation: '操作'
    },
    login: {
      title: '仓库管理系统',
      username: '用户名',
      password: '密码',
      login: '登录',
      remember: '记住密码'
    },
    menu: {
      dashboard: '首页',
      warehouse: '仓库管理',
      product: '商品管理',
      inventory: '库存管理',
      order: '订单管理',
      system: '系统管理'
    }
  },
  en: {
    common: {
      search: 'Search',
      add: 'Add',
      edit: 'Edit',
      delete: 'Delete',
      confirm: 'Confirm',
      cancel: 'Cancel',
      reset: 'Reset',
      save: 'Save',
      back: 'Back',
      operation: 'Operation'
    },
    login: {
      title: 'WMS System',
      username: 'Username',
      password: 'Password',
      login: 'Login',
      remember: 'Remember me'
    },
    menu: {
      dashboard: 'Dashboard',
      warehouse: 'Warehouse',
      product: 'Product',
      inventory: 'Inventory',
      order: 'Order',
      system: 'System'
    }
  }
}

const i18n = new VueI18n({
  locale: Cookies.get('language') || 'zh',
  messages
})

export default i18n 