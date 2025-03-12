{
  path: 'monthly-report/:id',
  component: () => import('@/views/warehouse/monthly-report'),
  name: 'MonthlyReport',
  meta: { title: '月度报表', noCache: true },
  hidden: true
},
{
  path: 'report-list',
  component: () => import('@/views/warehouse/report-list'),
  name: 'ReportList',
  meta: { title: '报表管理', icon: 'el-icon-document' }
} 