import axios from 'axios'
import { Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'

// 创建axios实例
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API,
  timeout: 30000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    console.log('发送请求:', {
      url: config.url,
      method: config.method,
      params: config.params,
      data: config.data
    })
    
    if (store.getters.token) {
      config.headers['Authorization'] = 'Bearer ' + getToken()
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    console.log('收到响应:', {
      url: response.config.url,
      status: response.status,
      data: response.data
    })
    
    const res = response.data
    
    // 如果响应类型是blob（用于文件下载），直接返回响应
    if (response.config.responseType === 'blob') {
      return response
    }
    
    // 如果响应中包含错误信息
    if (res.code && res.code !== 200) {
      Message({
        message: res.message || '请求失败',
        type: 'error',
        duration: 5 * 1000
      })
      return Promise.reject(new Error(res.message || '请求失败'))
    }
    
    return response
  },
  error => {
    console.error('响应错误:', error)
    console.error('错误响应:', error.response)
    
    let message = '请求失败'
    if (error.response) {
      // 服务器返回了错误状态码
      if (error.response.data && error.response.data.error) {
        message = error.response.data.error
      } else if (error.response.data && error.response.data.message) {
        message = error.response.data.message
      } else {
        message = `请求失败: ${error.response.status}`
      }
    } else if (error.message) {
      if (error.message.includes('timeout')) {
        message = '请求超时'
      } else {
        message = error.message
      }
    }
    
    Message({
      message: message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service 