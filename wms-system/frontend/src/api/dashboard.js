import request from '@/utils/request'

export function getDashboardData() {
  return request({
    url: '/api/v1/warehouse/dashboard/',
    method: 'get',
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

export function getStockTrend() {
  return request({
    url: '/api/v1/warehouse/stock-trend/',
    method: 'get',
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

export function getStockCategory() {
  return request({
    url: '/api/v1/warehouse/stock-category/',
    method: 'get',
    headers: {
      'Content-Type': 'application/json'
    }
  })
} 