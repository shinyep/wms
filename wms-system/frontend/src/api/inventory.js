import request from '@/utils/request'

// 获取库存列表
export function getInventoryList(params) {
  return request({
    url: '/inventory/',
    method: 'get',
    params
  })
}

// 获取库存详情
export function getInventoryDetail(id) {
  return request({
    url: `/inventory/${id}/`,
    method: 'get'
  })
}

// 创建库存记录
export function createInventory(data) {
  return request({
    url: '/inventory/',
    method: 'post',
    data
  })
}

// 更新库存记录
export function updateInventory(id, data) {
  return request({
    url: `/inventory/${id}/`,
    method: 'put',
    data
  })
}

// 删除库存记录
export function deleteInventory(id) {
  return request({
    url: `/inventory/${id}/`,
    method: 'delete'
  })
}

// 获取月度库存统计
export function getMonthlyInventory(warehouseType, year, month) {
  return request({
    url: '/inventory/monthly-statistics/',
    method: 'get',
    params: { warehouse_type: warehouseType, year, month }
  })
}

// 导出库存数据
export function exportInventory(params) {
  return request({
    url: '/inventory/export/',
    method: 'get',
    params,
    responseType: 'blob'
  })
} 