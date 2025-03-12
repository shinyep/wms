import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * 注意: 子菜单只在路由children.length >= 1时出现
 * 详情参见: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   如果设置为true，项目将不会显示在侧边栏中（默认值为false）
 * alwaysShow: true              如果设置为true，将始终显示根菜单
 *                               如果不设置alwaysShow，当项目有多个子路由时，
 *                               它将成为嵌套模式，否则不显示根菜单
 * redirect: noRedirect          如果设置noRedirect将不会在面包屑中重定向
 * name:'router-name'            该名称由<keep-alive>使用（必须设置！！！）
 * meta : {
    roles: ['admin','editor']    控制页面角色（可以设置多个角色）
    title: 'title'               侧边栏和面包屑中显示的名称（推荐设置）
    icon: 'svg-name'/'el-icon-x' 图标显示在侧边栏中
    noCache: true                如果设置为true，页面将不会被缓存（默认值为false）
    affix: true                  如果设置为true，标签将被固定在tags-view中
    breadcrumb: false            如果设置为false，该项将隐藏在面包屑中（默认值为true）
    activeMenu: '/example/list'  如果设置路径，侧边栏将突出显示你设置的路径
  }
 */

/**
 * constantRoutes
 * 没有权限要求的基础页面
 * 所有角色都可以访问
 */
export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/register',
    component: () => import('@/views/register/index'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/error-page/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/error-page/401'),
    hidden: true
  },
  {
    path: '/profile',
    component: Layout,
    redirect: '/profile/index',
    hidden: true,
    children: [
      {
        path: 'index',
        component: () => import('@/views/profile/index'),
        name: 'Profile',
        meta: { title: '个人中心', icon: 'user', noCache: true }
      }
    ]
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        component: () => import('@/views/dashboard/index'),
        name: 'Dashboard',
        meta: { title: '仪表盘', icon: 'dashboard', affix: true }
      }
    ]
  },
  {
    path: '/warehouse',
    component: Layout,
    redirect: '/warehouse/index',
    name: 'Warehouse',
    meta: {
      title: '仓库管理',
      icon: 'el-icon-office-building'
    },
    children: [
      {
        path: 'index',
        component: () => import('@/views/warehouse/index'),
        name: 'WarehouseList',
        meta: { title: '仓库列表', icon: 'el-icon-office-building' }
      },
      {
        path: 'detail/:id',
        component: () => import('@/views/warehouse/detail'),
        name: 'WarehouseDetail',
        meta: { title: '仓库详情', noCache: true },
        hidden: true
      },
      {
        path: 'area',
        component: () => import('@/views/warehouse/area'),
        name: 'WarehouseArea',
        meta: { title: '库区管理', icon: 'el-icon-menu' }
      },
      {
        path: 'location',
        component: () => import('@/views/warehouse/location'),
        name: 'WarehouseLocation',
        meta: { title: '库位管理', icon: 'el-icon-location' }
      },
      {
        path: 'monthly-report',
        component: () => import('@/views/warehouse/monthly-report'),
        name: 'MonthlyReport',
        meta: { title: '月度报表', icon: 'el-icon-s-data' }
      },
      {
        path: 'inventory-check',
        component: () => import('@/views/warehouse/inventory-check/index'),
        name: 'InventoryCheck',
        meta: { title: '盘点管理', icon: 'el-icon-check' }
      },
      {
        path: 'inventory-check/execute',
        component: () => import('@/views/warehouse/inventory-check/execute'),
        name: 'InventoryCheckExecute',
        meta: { title: '执行盘点', noCache: true },
        hidden: true
      },
      {
        path: 'inventory-check/detail',
        component: () => import('@/views/warehouse/inventory-check/detail'),
        name: 'InventoryCheckDetail',
        meta: { title: '盘点详情', noCache: true },
        hidden: true
      },
      {
        path: 'report-list',
        component: () => import('@/views/warehouse/report-list'),
        name: 'ReportList',
        meta: { title: '报表管理', icon: 'el-icon-document' }
      }
    ]
  }
]

/**
 * asyncRoutes
 * 需要根据用户角色动态加载的路由
 */
export const asyncRoutes = [
  {
    path: '/system',
    component: Layout,
    redirect: '/system/admin',
    name: 'System',
    meta: {
      title: '系统管理',
      icon: 'el-icon-setting',
      roles: ['admin']
    },
    children: [
      {
        path: 'admin',
        component: () => import('@/views/warehouse/admin/index'),
        name: 'AdminManagement',
        meta: { title: '管理员账号', icon: 'el-icon-user', roles: ['admin'] }
      }
    ]
  },
  // 404页面必须放在末尾！！！
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  mode: 'hash', // 使用 hash 模式
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
