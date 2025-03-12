import request from '@/utils/request'

// 获取出入库记录列表
export function getTransactionList(params) {
  return request({
    url: '/transaction/',
    method: 'get',
    params
  })
}

// 获取出入库记录详情
export function getTransactionDetail(id) {
  return request({
    url: `/transaction/${id}/`,
    method: 'get'
  })
}

// 创建出入库记录
export function createTransaction(data) {
  return request({
    url: '/transaction/',
    method: 'post',
    data
  })
}

// 更新出入库记录
export function updateTransaction(id, data) {
  return request({
    url: `/transaction/${id}/`,
    method: 'put',
    data
  })
}

// 删除出入库记录
export function deleteTransaction(id) {
  return request({
    url: `/transaction/${id}/`,
    method: 'delete'
  })
}

// 获取月度统计数据
export function getMonthlyStatistics(warehouseType, year) {
  return request({
    url: '/transaction/monthly-statistics/',
    method: 'get',
    params: { warehouse_type: warehouseType, year }
  })
}

// 获取热门商品统计
export function getTopItemsStatistics(warehouseType, params) {
  return request({
    url: '/transaction/top-items/',
    method: 'get',
    params: { warehouse_type: warehouseType, ...params }
  })
}

// 导出出入库记录
export function exportTransactionList(params) {
  return request({
    url: '/transaction/export/',
    method: 'get',
    params,
    responseType: 'blob'
  })
} 