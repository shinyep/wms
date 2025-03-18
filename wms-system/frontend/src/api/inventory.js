import request from '@/utils/request'

// 获取库存列表
export function getInventoryList(params) {
  return request({
    url: '/api/v1/inventory/',
    method: 'get',
    params
  })
}

// 获取库存详情
export function getInventoryDetail(id) {
  return request({
    url: `/api/v1/inventory/${id}/`,
    method: 'get'
  })
}

// 创建库存记录
export function createInventory(data) {
  return request({
    url: '/api/v1/inventory/',
    method: 'post',
    data
  })
}

// 更新库存记录
export function updateInventory(id, data) {
  return request({
    url: `/api/v1/inventory/${id}/`,
    method: 'put',
    data
  })
}

// 删除库存记录
export function deleteInventory(id) {
  return request({
    url: `/api/v1/inventory/${id}/`,
    method: 'delete'
  })
}

// 获取月度库存统计
export function getMonthlyInventory(warehouseType, year, month) {
  return request({
    url: '/api/v1/inventory/monthly-statistics/',
    method: 'get',
    params: { warehouse_type: warehouseType, year, month }
  })
}

// 导出库存数据
export function exportInventory(params) {
  return request({
    url: '/api/v1/inventory/export/',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

// ================== 盘点功能API ==================

// 创建盘点单
export function createInventoryCheck(data) {
  return request({
    url: '/api/v1/inventory-check/',
    method: 'post',
    data
  })
}

// 获取盘点单列表
export function getInventoryCheckList(params) {
  return request({
    url: '/api/v1/inventory-check/',
    method: 'get',
    params
  })
}

// 获取盘点单详情
export function getInventoryCheckDetail(id) {
  return request({
    url: `/api/v1/inventory-check/${id}/`,
    method: 'get'
  })
}

// 更新盘点单
export function updateInventoryCheck(id, data) {
  return request({
    url: `/api/v1/inventory-check/${id}/`,
    method: 'put',
    data
  })
}

// 删除盘点单
export function deleteInventoryCheck(id) {
  return request({
    url: `/api/v1/inventory-check/${id}/`,
    method: 'delete'
  })
}

// 获取盘点项目列表
export function getCheckItems(checkId, params) {
  return request({
    url: `/api/v1/inventory-check/${checkId}/items/`,
    method: 'get',
    params
  })
}

// 提交盘点结果
export function submitCheckResult(checkId, data) {
  return request({
    url: `/api/v1/inventory-check/${checkId}/submit/`,
    method: 'post',
    data
  })
}

// 更新单个盘点结果
export function updateCheckItem(checkId, itemId, data) {
  const url = itemId 
    ? `/api/v1/inventory-check/${checkId}/items/${itemId}/` 
    : `/api/v1/inventory-check/${checkId}/`;
  
  return request({
    url,
    method: 'put',
    data
  })
}

// 获取盘点统计数据
export function getCheckStatistics(checkId) {
  return request({
    url: `/api/v1/inventory-check/${checkId}/statistics/`,
    method: 'get'
  })
}

// 获取仓库区域树结构
export function getWarehouseAreaTree(warehouseId) {
  return request({
    url: `/api/v1/warehouse/${warehouseId}/area-tree/`,
    method: 'get'
  })
}

// ================== 仓库区域相关API ==================

// 获取仓库所有区域
export function getWarehouseAreas(warehouseId) {
  return request({
    url: `/api/v1/warehouse/${warehouseId}/areas/`,
    method: 'get'
  })
}

// 获取区域详情
export function getAreaDetail(areaId) {
  return request({
    url: `/api/v1/warehouse/area/${areaId}/`,
    method: 'get'
  })
}

// 获取区域内所有货架
export function getAreaShelves(areaId) {
  return request({
    url: `/api/v1/warehouse/area/${areaId}/shelves/`,
    method: 'get'
  })
}

// 获取货架详情
export function getShelfDetail(shelfId) {
  return request({
    url: `/api/v1/warehouse/shelf/${shelfId}/`,
    method: 'get'
  })
}

// 获取货架上的所有货位
export function getShelfLocations(shelfId) {
  return request({
    url: `/api/v1/warehouse/shelf/${shelfId}/locations/`,
    method: 'get'
  })
}

// 获取区域内所有库存商品
export function getAreaInventory(areaId, params) {
  return request({
    url: `/api/v1/inventory/area/${areaId}/`,
    method: 'get',
    params
  })
}

// 获取货架上所有库存商品
export function getShelfInventory(shelfId, params) {
  return request({
    url: `/api/v1/inventory/shelf/${shelfId}/`,
    method: 'get',
    params
  })
}

// 根据区域创建盘点单
export function createAreaInventoryCheck(areaId, data) {
  return request({
    url: `/api/v1/inventory-check/area/${areaId}/`,
    method: 'post',
    data
  })
}

// 根据货架创建盘点单
export function createShelfInventoryCheck(shelfId, data) {
  return request({
    url: `/api/v1/inventory-check/shelf/${shelfId}/`,
    method: 'post',
    data
  })
}

// 获取盘点历史记录
export function getCheckHistory(params) {
  return request({
    url: '/api/v1/inventory-check/history/',
    method: 'get',
    params
  })
}

// 获取商品盘点历史
export function getProductCheckHistory(productId, params) {
  return request({
    url: `/api/v1/inventory-check/product/${productId}/history/`,
    method: 'get',
    params
  })
}

// 按分类筛选盘点商品
export function getCheckItemsByCategory(checkId, categoryId, params) {
  return request({
    url: `/api/v1/inventory-check/${checkId}/category/${categoryId}/`,
    method: 'get',
    params
  })
} 