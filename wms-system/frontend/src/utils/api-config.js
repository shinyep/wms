/**
 * API 配置文件
 * 用于统一管理API路径前缀和配置
 */

// API基础路径前缀
export const API_BASE_PREFIX = '/api/v1'

// 各模块API子路径
export const API_PATHS = {
  // 仓库模块API路径
  WAREHOUSE: {
    BASE: `${API_BASE_PREFIX}/warehouse`,
    BACKUP: (id) => `${API_BASE_PREFIX}/warehouse/${id}/backup/`,
    DETAIL: (id) => `${API_BASE_PREFIX}/warehouse/${id}/`,
    EXPORT: `${API_BASE_PREFIX}/warehouse/export/`,
    IMPORT: `${API_BASE_PREFIX}/warehouse/import/`,
    MONTHLY_REPORT: (id, month) => `${API_BASE_PREFIX}/warehouse/${id}/monthly-report/${month ? month : ''}`,
    AREA: (id) => `${API_BASE_PREFIX}/warehouse/${id}/areas/`,
    AREA_DETAIL: (warehouseId, areaId) => `${API_BASE_PREFIX}/warehouse/${warehouseId}/areas/${areaId}/`,
  },
  
  // 其他模块可以在此添加...
}

/**
 * 获取正确的API路径
 * 如果环境变量或配置有覆盖，则使用覆盖的路径
 */
export function getApiPath(module, path, ...params) {
  try {
    // 如果传入的是函数，则执行它并传入参数
    if (typeof API_PATHS[module][path] === 'function') {
      return API_PATHS[module][path](...params)
    }
    // 否则直接返回路径字符串
    return API_PATHS[module][path]
  } catch (error) {
    console.error(`获取API路径错误: module=${module}, path=${path}`, error)
    // 返回一个可能的路径，避免前端崩溃
    return `${API_BASE_PREFIX}/${module.toLowerCase()}/${path.toLowerCase()}/`
  }
}

export default {
  API_BASE_PREFIX,
  API_PATHS,
  getApiPath
} 