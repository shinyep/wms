// 获取仓库详情
export function getWarehouse(id) {
  return request({
    url: `/api/v1/warehouse/${id}/`,
    method: 'get'
  })
}

// 获取月度报表
export function getMonthlyReport(params) {
  const config = {
    url: '/api/v1/warehouse/monthly-report/',
    method: 'get',
    params: {
      warehouse_id: params.warehouse_id,
      month: params.month,
      format: params.format || 'json',
      check_only: params.check_only
    },
    timeout: 30000  // 设置30秒超时
  }

  // 根据format参数设置不同的响应类型和请求头
  if (params.format === 'excel') {
    config.responseType = 'blob'
    config.headers = {
      'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }
  } else {
    config.responseType = 'json'
    config.headers = {
      'Accept': 'application/json'
    }
  }

  return request(config)
}

// 导出仓库数据备份
export function exportWarehouseBackup(id) {
  return request({
    url: `/api/v1/warehouse/${id}/backup/`,
    method: 'get',
    responseType: 'blob',
    headers: {
      'Accept': 'application/json'
    },
    timeout: 30000  // 设置30秒超时
  })
}

// 恢复仓库数据备份
export function restoreWarehouseBackup(id, data) {
  return request({
    url: `/api/v1/warehouse/${id}/restore/`,
    method: 'post',
    data,
    headers: {
      'Content-Type': 'application/json'
    },
    timeout: 60000  // 设置60秒超时，因为恢复可能需要更长时间
  })
} 