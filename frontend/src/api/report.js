import request from '@/utils/request'

// 创建报表记录
export function createRecord(data) {
  return request({
    url: '/api/v1/warehouse/create_record/',
    method: 'post',
    data
  })
}

// 更新报表记录
export function updateRecord(data) {
  return request({
    url: '/api/v1/warehouse/update_record/',
    method: 'put',
    data
  })
}

// 删除报表记录
export function deleteRecord(params) {
  return request({
    url: '/api/v1/warehouse/delete_record/',
    method: 'delete',
    params
  })
}

// 获取报表列表
export function getReportList(params) {
  return request({
    url: '/api/v1/reports/',
    method: 'get',
    params
  })
}

// 获取报表详情
export function getReportDetail(id) {
  return request({
    url: `/api/v1/reports/${id}/`,
    method: 'get'
  })
} 