import request from '@/utils/request'
import { getApiPath } from '@/utils/api-config'

// 获取仓库列表
export function fetchList(query) {
  return request({
    url: '/api/v1/warehouse/',
    method: 'get',
    params: query
  })
}

// 为兼容性添加getWarehouseList作为fetchList的别名
export function getWarehouseList(query) {
  return fetchList(query)
}

// 创建仓库
export function createWarehouse(data) {
  return request({
    url: '/api/v1/warehouse/',
    method: 'post',
    data
  })
}

// 更新仓库
export function updateWarehouse(id, data) {
  return request({
    url: `/api/v1/warehouse/${id}/`,
    method: 'put',
    data
  })
}

// 删除仓库
export function deleteWarehouse(id) {
  if (!id) {
    console.error('删除仓库时缺少ID参数')
    return Promise.reject(new Error('删除仓库时缺少ID参数'))
  }
  
  return request({
    url: `/api/v1/warehouse/${id}/`,
    method: 'delete',
    headers: {
      'Content-Type': 'application/json'
    },
    timeout: 10000
  })
}

// 获取仓库详情
export function getWarehouse(id) {
  if (!id) {
    console.error('获取仓库详情时缺少ID参数')
    return Promise.reject(new Error('获取仓库详情时缺少ID参数'))
  }
  
  console.log(`调用getWarehouse API: id=${id}`)
  
  return request({
    url: `/api/v1/warehouse/${id}/`,
    method: 'get',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    timeout: 15000
  }).catch(error => {
    console.error(`获取仓库(ID=${id})详情失败:`, error)
    throw error
  })
}

// 获取仓库区域列表
export function getWarehouseAreaList(warehouseId) {
  return request({
    url: `/api/v1/warehouse/${warehouseId}/areas/`,
    method: 'get'
  })
}

// 创建仓库区域
export function createWarehouseArea(warehouseId, data) {
  return request({
    url: `/api/v1/warehouse/${warehouseId}/areas/`,
    method: 'post',
    data
  })
}

// 更新仓库区域
export function updateWarehouseArea(warehouseId, areaId, data) {
  return request({
    url: `/api/v1/warehouse/${warehouseId}/areas/${areaId}/`,
    method: 'put',
    data
  })
}

// 删除仓库区域
export function deleteWarehouseArea(warehouseId, areaId) {
  return request({
    url: `/api/v1/warehouse/${warehouseId}/areas/${areaId}/`,
    method: 'delete'
  })
}

// 导入Excel
export function importExcel(data) {
  return request({
    url: '/api/v1/warehouse/import/',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 导出Excel
export function exportExcel() {
  return request({
    url: '/api/v1/warehouse/export/',
    method: 'get',
    responseType: 'blob',
    headers: {
      'Authorization': 'Bearer ' + localStorage.getItem('token')
    }
  })
}

// 导出模板
export function exportTemplate(warehouseId) {
  return request({
    url: `/api/v1/warehouse/${warehouseId}/export-template/`,
    method: 'get',
    responseType: 'blob',
    headers: {
      'Authorization': 'Bearer ' + localStorage.getItem('token')
    }
  })
}

// 获取月度报表
export function getMonthlyReport(warehouseId, month) {
  return request({
    url: `/api/v1/warehouse/${warehouseId}/monthly-report/`,
    method: 'get',
    params: { month }
  })
}

// 更新期初库存
export function updateInitialStock(warehouseId, month) {
  return request({
    url: `/api/v1/warehouse/${warehouseId}/update_initial_stock/`,
    method: 'post',
    data: { month }
  })
}

// 更新期初库存（月度报表）
export function updateMonthlyReportInitialStock(data) {
  return request({
    url: '/api/v1/warehouse/monthly-report/update_initial_stock/',
    method: 'post',
    data
  })
}

// 导出仓库数据备份
export function exportWarehouseBackup(id) {
  console.log(`[备份操作] 开始备份仓库: id=${id}`)
  
  // 从配置中获取备份API路径
  const backupUrl = getApiPath('WAREHOUSE', 'BACKUP', id)
  console.log(`[备份操作] 使用备份API路径: ${backupUrl}`)
  
  return request({
    url: backupUrl,
    method: 'get',
    responseType: 'blob', // 指定响应类型为blob
    retry: 2, // 如果失败重试2次
    retryDelay: 3000, // 重试延迟3秒
    timeout: 120000, // 2分钟超时
    _backupOperation: true, // 标记为备份操作
    transformResponse: [function (data) {
      console.log(`[备份操作] 收到备份响应: 类型=${data && data.type}, 大小=${data && data.size} 字节`)
      
      // 检查响应是否是小blob（可能是错误响应）
      if (data instanceof Blob && data.size < 1000 && data.type.includes('json')) {
        return new Promise((resolve, reject) => {
          const reader = new FileReader()
          reader.onload = () => {
            try {
              const result = JSON.parse(reader.result)
              console.error(`[备份操作] 错误: 备份失败`, result)
              return reject(result.error || result.detail || '备份失败')
            } catch (e) {
              console.log(`[备份操作] 小型响应但不是错误JSON`, { size: data.size })
              return resolve(data) // 不是JSON错误，返回原始数据
            }
          }
          reader.onerror = () => {
            console.error('[备份操作] 读取blob失败')
            return resolve(data) // 读取出错，返回原始数据
          }
          reader.readAsText(data)
        })
      }
      
      // 正常的大型blob响应
      return data
    }]
  })
} 