import request from '@/utils/request'

// 获取用户列表
export function fetchUserList(query) {
  return request({
    url: '/api/v1/user/',
    method: 'get',
    params: query
  })
}

// 获取用户详情
export function fetchUser(id) {
  return request({
    url: `/api/v1/user/${id}/`,
    method: 'get'
  })
}

// 创建用户
export function createUser(data) {
  return request({
    url: '/api/v1/user/',
    method: 'post',
    data
  })
}

// 更新用户
export function updateUser(id, data) {
  return request({
    url: `/api/v1/user/${id}/`,
    method: 'patch',
    data
  })
}

// 删除用户
export function deleteUser(id) {
  return request({
    url: `/api/v1/user/${id}/`,
    method: 'delete',
    headers: {
      'Content-Type': 'application/json'
    },
    _isShowError: true
  })
}

// 激活用户
export function activateUser(id) {
  return request({
    url: `/api/v1/user/${id}/activate/`,
    method: 'post'
  })
}

// 禁用用户
export function deactivateUser(id) {
  return request({
    url: `/api/v1/user/${id}/deactivate/`,
    method: 'post'
  })
}

// 设置用户等级
export function setUserLevel(id, level) {
  return request({
    url: `/api/v1/user/${id}/set-level/`,
    method: 'post',
    data: { level }
  })
}

// 用户注册
export function register(data) {
  return request({
    url: '/api/v1/user/register/',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

// 用户登录
export function login(data) {
  return request({
    url: '/api/v1/user/login/',
    method: 'post',
    data: {
      username: data.username,
      password: data.password
    },
    headers: {
      'Content-Type': 'application/json'
    },
    _isShowError: true  // 允许显示错误提示
  })
}

// 获取用户信息
export function getInfo() {
  return request({
    url: '/api/v1/user/info/',
    method: 'get'
  })
}

// 获取用户权限
export function getUserPermissions() {
  return request({
    url: '/api/v1/user/permissions/',
    method: 'get'
  })
}

// 用户登出
export function logout() {
  return request({
    url: '/api/v1/user/logout/',
    method: 'get'
  })
}
