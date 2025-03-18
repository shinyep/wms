import request from '@/utils/request'

// 获取盘点单列表
export function getStockCheckList(params) {
  return request({
    url: '/inventory/stock-checks/',
    method: 'get',
    params
  })
}

// 获取盘点单详情
export function getStockCheckDetail(id) {
  return request({
    url: `/inventory/stock-checks/${id}/`,
    method: 'get'
  })
}

// 创建盘点单
export function createStockCheck(data) {
  return request({
    url: '/inventory/stock-checks/',
    method: 'post',
    data
  })
}

// 更新盘点单
export function updateStockCheck(id, data) {
  return request({
    url: `/inventory/stock-checks/${id}/`,
    method: 'put',
    data
  })
}

// 删除盘点单
export function deleteStockCheck(id) {
  return request({
    url: `/inventory/stock-checks/${id}/`,
    method: 'delete'
  })
}

// 开始盘点
export function startStockCheck(id) {
  return request({
    url: `/inventory/stock-checks/${id}/start_check/`,
    method: 'post'
  })
}

// 完成盘点
export function completeStockCheck(id, adjustInventory = false) {
  return request({
    url: `/inventory/stock-checks/${id}/complete_check/`,
    method: 'post',
    data: { adjust_inventory: adjustInventory }
  })
}

// 取消盘点
export function cancelStockCheck(id) {
  return request({
    url: `/inventory/stock-checks/${id}/cancel_check/`,
    method: 'post'
  })
}

// 导出盘点单
export function exportStockCheck(id) {
  return request({
    url: `/inventory/stock-checks/${id}/export_check/`,
    method: 'get',
    responseType: 'blob'
  })
}

// 获取盘点明细列表
export function getStockCheckItemList(params) {
  return request({
    url: '/inventory/stock-check-items/',
    method: 'get',
    params
  })
}

// 更新盘点明细的实际数量
export function updateStockCheckItemQuantity(id, actualQuantity) {
  return request({
    url: `/inventory/stock-check-items/${id}/update_actual_quantity/`,
    method: 'post',
    data: { actual_quantity: actualQuantity }
  })
}