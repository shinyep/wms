import axios from 'axios'
import Vue from 'vue'
import store from '@/store'
import { getToken } from '@/utils/auth'

// 创建一个简单的日志工具，可以按级别记录日志
const logger = {
  debug: (message, data) => {
    console.debug(`[DEBUG] ${message}`, data)
  },
  info: (message, data) => {
    console.info(`[INFO] ${message}`, data)
  },
  warn: (message, data) => {
    console.warn(`[WARN] ${message}`, data)
  },
  error: (message, data) => {
    console.error(`[ERROR] ${message}`, data)
  },
  // 为备份和大文件特别创建的日志方法
  logBackupOperation: (action, details) => {
    console.log(`[BACKUP-OPERATION] ${action}`, details)
    // 在开发工具被打开的情况下，尝试将重要日志存储到sessionStorage
    try {
      const logs = JSON.parse(sessionStorage.getItem('wms_backup_logs') || '[]')
      logs.push({
        timestamp: new Date().toISOString(),
        action,
        details
      })
      // 保留最近的50条记录
      if (logs.length > 50) logs.splice(0, logs.length - 50)
      sessionStorage.setItem('wms_backup_logs', JSON.stringify(logs))
    } catch (e) {
      console.error('无法保存日志到sessionStorage', e)
    }
  }
}

// 备份响应处理函数
function handleBackupResponse(response) {
  console.log(`[备份操作] 处理响应:`, {
    type: response.type,
    size: response.size,
    headers: response.headers
  })
  
  // 如果是JSON响应，说明可能是错误信息
  if (response.type.includes('json')) {
    return response.text().then(text => {
      try {
        const data = JSON.parse(text)
        // 检查是否是完整的备份数据
        if (data.warehouse && data.inventory !== undefined && data.transactions !== undefined) {
          // 是完整的备份数据，转换为blob并下载
          const blob = new Blob([JSON.stringify(data, null, 2)], { 
            type: 'application/json' 
          })
          return Promise.resolve(blob)
        } else if (data.error || data.detail) {
          // 确实是错误信息
          return Promise.reject(new Error(data.error || data.detail))
        }
        // 其他情况返回原始数据
        return Promise.resolve(data)
      } catch (e) {
        console.error('[备份操作] JSON解析失败:', e)
        return Promise.reject(new Error('备份数据格式错误'))
      }
    })
  }
  
  // 如果是二进制数据，直接返回
  return Promise.resolve(response)
}

// 创建axios实例
const service = axios.create({
  // 使用环境变量中的API基础路径
  baseURL: '',  // 不设置baseURL，因为我们在API调用中已经包含了完整的路径
  // withCredentials: true, // 跨域请求时发送cookies
  timeout: 60000 // 增加请求超时时间到60秒
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么
    const logInfo = {
      url: config.url,
      method: config.method,
      params: config.params,
      headers: { ...config.headers },
      baseURL: config.baseURL,
      timeout: config.timeout
    }
    
    // 对于大型请求，不记录完整数据，避免日志过大
    if (config.data) {
      if (typeof config.data === 'object' && Object.keys(config.data).length > 10) {
        logInfo.data = '数据对象过大，已省略'
        logInfo.dataSize = JSON.stringify(config.data).length + ' 字节'
      } else {
        logInfo.data = config.data
      }
    }

    logger.info('发送请求', logInfo)
    
    // 检测是否为备份相关操作
    if (config.url && (config.url.includes('/backup') || config.url.includes('export'))) {
      logger.logBackupOperation('开始请求', { 
        url: config.url,
        method: config.method,
        time: new Date().toISOString(),
        responseType: config.responseType || 'json'
      })
      
      // 为备份请求特别设置
      if (!config.responseType && config.url.includes('/backup')) {
        logger.info('自动为备份请求设置responseType=blob', { url: config.url })
        config.responseType = 'blob'
      }
      
      // 为备份请求增加超时时间
      if (config.timeout < 120000) {
        const originalTimeout = config.timeout
        config.timeout = 120000 // 为备份请求设置2分钟超时
        logger.info(`增加备份请求超时时间`, { 
          url: config.url, 
          originalTimeout, 
          newTimeout: config.timeout 
        })
      }
    }
    
    // 设置默认的 Content-Type
    if (config.method === 'post' || config.method === 'put' || config.method === 'patch') {
      if (!config.headers['Content-Type']) {
        config.headers['Content-Type'] = 'application/json'
      }
    }
    
    if (store.getters.token) {
      // 让每个请求携带token，使用 Bearer 认证方案
      const token = getToken()
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`
        logger.debug('已添加授权头', { token: `Bearer ${token.substring(0, 10)}...` })
      }
    }
    
    // 标记备份请求
    if (config.url.includes('/backup/')) {
      config._isBackup = true
    }
    
    return config
  },
  error => {
    // 处理请求错误
    logger.error('请求配置错误', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  async response => {
    // 备份请求的特殊处理
    if (response.config._isBackup) {
      return handleBackupResponse(response.data)
    }
    
    const config = response.config
    const url = config.url
    const isBackupOperation = url && (url.includes('/backup') || url.includes('export'))
    
    // 对于备份操作，记录特殊日志
    if (isBackupOperation) {
      logger.logBackupOperation('收到响应', {
        url,
        status: response.status,
        headers: response.headers,
        time: new Date().toISOString(),
        contentType: response.headers['content-type'],
        contentLength: response.headers['content-length'] || '未知',
        dataType: typeof response.data,
        isBlob: response.data instanceof Blob,
        blobSize: response.data instanceof Blob ? response.data.size : '非Blob'
      })
    }
    
    // 基本响应日志
    const logInfo = {
      url: config.url,
      method: config.method,
      status: response.status,
      statusText: response.statusText,
      contentType: response.headers['content-type'],
      contentLength: response.headers['content-length']
    }
    
    // 对于普通JSON响应，记录数据，大型二进制响应不记录内容
    if (response.data && !(response.data instanceof Blob)) {
      if (typeof response.data === 'object' && Object.keys(response.data).length > 10) {
        logInfo.data = '数据对象过大，已省略'
        logInfo.dataKeys = Object.keys(response.data)
      } else {
        logInfo.data = response.data
      }
    } else if (response.data instanceof Blob) {
      logInfo.dataType = 'Blob'
      logInfo.blobSize = response.data.size
      logInfo.blobType = response.data.type
    }
    
    logger.info('收到响应', logInfo)
    
    // 如果是blob类型的响应，做特殊处理
    if (response.config.responseType === 'blob') {
      // 检查blob响应是否过小（可能是错误信息）
      if (response.data instanceof Blob && response.data.size < 1000) {
        logger.warn('可能的错误响应 - Blob大小异常小', { 
          size: response.data.size, 
          type: response.data.type,
          url: config.url
        })
        
        // 尝试解析小的blob，看是否为JSON错误信息
        return new Promise((resolve, reject) => {
          const reader = new FileReader()
          reader.onload = () => {
            try {
              // 尝试解析为JSON
              const result = JSON.parse(reader.result)
              logger.error('Blob中发现JSON错误信息', result)
              
              if (result.error || result.detail || result.message) {
                // 这是一个错误响应
                const errorMsg = result.error || result.detail || result.message || '未知错误'
                reject(new Error(errorMsg))
              } else {
                // 看起来是有效的小型JSON响应
                resolve(result)
              }
            } catch (e) {
              // 不是JSON，返回原始blob
              logger.info('小型Blob不是JSON格式，按正常响应处理', {
                content: reader.result.substring(0, 100) + '...',
                size: response.data.size
              })
              resolve(response.data)
            }
          }
          reader.onerror = () => {
            // 无法读取blob，返回原始响应
            logger.warn('无法读取Blob内容', { size: response.data.size })
            resolve(response.data)
          }
          reader.readAsText(response.data)
        })
      }
      return response.data
    }

    // 如果响应成功，返回响应数据
    if (response.status === 200 || response.status === 201) {
      return response.data
    }

    // 处理其他情况
    const errorMsg = response.data?.message || response.data?.detail || '请求错误'
    logger.error('响应状态非200/201错误', { 
      status: response.status, 
      message: errorMsg,
      data: response.data
    })
    return Promise.reject(new Error(errorMsg))
  },
  async error => {
    // 备份请求的错误处理
    if (error.config._isBackup) {
      console.error('[备份操作] 请求失败:', error)
      return Promise.reject(new Error('备份过程中发生网络错误'))
    }
    
    // 检查是否是备份相关操作
    const config = error.config
    const url = config?.url || ''
    const isBackupOperation = url && (url.includes('/backup') || url.includes('export'))
    
    if (isBackupOperation) {
      logger.logBackupOperation('请求错误', {
        url,
        method: config?.method,
        status: error.response?.status,
        statusText: error.response?.statusText,
        message: error.message,
        time: new Date().toISOString(),
        errorType: error.name,
        timeout: config?.timeout,
        responseType: config?.responseType,
        headers: error.response?.headers
      })
    }
    
    logger.error('请求错误详情', {
      url: config?.url,
      method: config?.method,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      message: error.message,
      code: error.code,
      stack: error.stack
    })
    
    // 添加重试逻辑
    if (config && config.retry && config.retry > 0 && (config.method?.toLowerCase() === 'get')) {
      // 设置重试计数器
      config.__retryCount = config.__retryCount || 0
      
      // 检查是否已经达到最大重试次数
      if (config.__retryCount < config.retry) {
        // 增加重试计数
        config.__retryCount += 1
        logger.info(`正在重试请求`, { 
          url: config.url, 
          attempt: `${config.__retryCount}/${config.retry}`,
          delay: config.retryDelay || 1000
        })
        
        // 为备份请求特殊处理
        if (isBackupOperation) {
          logger.logBackupOperation('重试备份请求', {
            url,
            attempt: `${config.__retryCount}/${config.retry}`,
            time: new Date().toISOString()
          })
          
          // 增加超时时间，避免大型备份因超时失败
          if (config.timeout) {
            const newTimeout = config.timeout * 1.5
            logger.info(`增加重试超时时间`, {
              original: config.timeout,
              new: newTimeout
            })
            config.timeout = newTimeout
          }
        }
        
        // 创建新的Promise来处理重试延迟
        const retryDelay = config.retryDelay || 1000
        return new Promise(resolve => {
          setTimeout(() => {
            logger.info(`执行重试请求`, { url: config.url, attempt: config.__retryCount })
            resolve(service(config))
          }, retryDelay)
        })
      }
    }
    
    let message = '请求错误'
    
    if (error.response) {
      const status = error.response.status
      const data = error.response.data
      
      switch (status) {
        case 400:
          if (data) {
            if (typeof data === 'string') {
              message = data
            } else if (data.detail) {
              message = data.detail
            } else if (data.message) {
              message = data.message
            } else if (data.error) {
              message = data.error
            } else if (data.non_field_errors && Array.isArray(data.non_field_errors)) {
              message = data.non_field_errors[0]
            } else {
              // 处理字段错误
              const fieldErrors = []
              let hasErrors = false
              
              for (const field in data) {
                if (Array.isArray(data[field])) {
                  hasErrors = true
                  fieldErrors.push(`${field}: ${data[field][0]}`)
                }
              }
              
              // 如果没有具体的字段错误信息，默认使用通用错误消息
              message = hasErrors ? fieldErrors.join('; ') : '登录失败，请检查用户名和密码'
            }
          } else {
            message = '请求参数错误'
          }
          break
        case 401:
          message = '未授权，请重新登录'
          // 清除token并跳转到登录页
          store.dispatch('user/resetToken').then(() => {
            location.reload()
          })
          break
        case 403:
          message = '拒绝访问'
          break
        case 404:
          message = `请求的资源不存在: ${error.config?.url || '未知URL'}`
          break
        case 500:
          message = '服务器内部错误'
          break
        default:
          if (data) {
            if (typeof data === 'string') {
              message = data
            } else if (data.detail) {
              message = data.detail
            } else if (data.message) {
              message = data.message
            } else if (data.error) {
              message = data.error
            } else {
              message = `请求失败 (${status})`
            }
          }
      }
    } else if (error.request) {
      message = '服务器无响应'
      logger.error('服务器无响应', { 
        request: {
          url: error.config?.url,
          method: error.config?.method,
          timeout: error.config?.timeout
        },
        error: error.request
      })
    } else {
      message = error.message || '请求出错'
      logger.error('请求设置错误', { message: error.message, stack: error.stack })
    }
    
    // 显示错误信息
    if (error.config?._isShowError !== false) {
      Vue.prototype.$message({
        message: message,
        type: 'error',
        duration: 5 * 1000
      })
    }
    
    return Promise.reject(new Error(message))
  }
)

export default service
