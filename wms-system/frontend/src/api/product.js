import request from '@/utils/request'

// 获取商品列表
export function getProductList(query) {
  return request({
    url: '/product/',
    method: 'get',
    params: query
  })
}

// 获取商品详情
export function getProduct(id) {
  return request({
    url: `/product/${id}/`,
    method: 'get'
  })
}

// 创建商品
export function createProduct(data) {
  return request({
    url: '/product/',
    method: 'post',
    data
  })
}

// 更新商品
export function updateProduct(id, data) {
  return request({
    url: `/product/${id}/`,
    method: 'put',
    data
  })
}

// 删除商品
export function deleteProduct(id) {
  return request({
    url: `/product/${id}/`,
    method: 'delete'
  })
} 