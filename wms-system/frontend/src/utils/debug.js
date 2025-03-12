/**
 * 仓库管理系统调试工具
 * 主要用于开发和排错阶段
 */

import { API_BASE_PREFIX, getApiPath } from './api-config'

const debug = {
  /**
   * 获取会话存储中的备份日志
   * 在控制台运行: window.wmsDebug.getBackupLogs()
   */
  getBackupLogs() {
    try {
      const logs = JSON.parse(sessionStorage.getItem('wms_backup_logs') || '[]')
      console.log('备份操作日志:', logs)
      
      // 打印最后一次备份操作的详细信息
      if (logs.length > 0) {
        console.log('最近一次备份操作:', logs[logs.length - 1])
      }
      
      return logs
    } catch (e) {
      console.error('无法获取备份日志:', e)
      return []
    }
  },
  
  /**
   * 测试文件下载功能
   * 在控制台运行: window.wmsDebug.testDownload()
   */
  testDownload() {
    const testData = JSON.stringify({ test: 'data', time: new Date().toISOString() })
    const blob = new Blob([testData], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'test-download.json'
    a.click()
    URL.revokeObjectURL(url)
    console.log('测试下载已触发，请检查是否成功下载文件')
  },
  
  /**
   * 检查浏览器缓存状态
   * 在控制台运行: window.wmsDebug.checkCacheState()
   */
  checkCacheState() {
    const cacheInfo = {
      serviceWorker: 'navigator.serviceWorker' in window,
      caches: 'caches' in window,
      localStorage: !!window.localStorage,
      sessionStorage: !!window.sessionStorage,
      indexedDB: !!window.indexedDB
    }
    
    console.log('浏览器缓存状态:', cacheInfo)
    
    // 检查是否打开了开发者工具的禁用缓存选项
    console.log('提示: 请在开发者工具的Network面板勾选"Disable cache"选项来禁用缓存')
    
    return cacheInfo
  },
  
  /**
   * 检查网络请求状态
   * 在控制台运行: window.wmsDebug.checkNetworkState()
   */
  checkNetworkState() {
    const networkInfo = {
      online: navigator.onLine,
      connection: navigator.connection ? {
        type: navigator.connection.type,
        effectiveType: navigator.connection.effectiveType,
        downlink: navigator.connection.downlink,
        rtt: navigator.connection.rtt
      } : '不支持'
    }
    
    console.log('网络状态:', networkInfo)
    
    // 使用fetch API进行简单测试
    fetch('/api/v1/ping', { 
      method: 'GET',
      cache: 'no-cache',
      headers: { 'pragma': 'no-cache', 'cache-control': 'no-cache' }
    })
      .then(response => {
        console.log('网络测试成功:', {
          status: response.status,
          headers: Object.fromEntries([...response.headers.entries()]),
          ok: response.ok
        })
      })
      .catch(error => {
        console.error('网络测试失败:', error)
      })
    
    return networkInfo
  },
  
  /**
   * 模拟备份请求（不实际备份，仅测试请求流程）
   * 在控制台运行: window.wmsDebug.simulateBackup(仓库ID)
   */
  simulateBackup(warehouseId) {
    if (!warehouseId) {
      console.error('请提供仓库ID')
      return
    }
    
    console.log(`开始模拟备份请求: warehouseId=${warehouseId}`)
    
    // 获取当前的token
    const token = localStorage.getItem('token') || sessionStorage.getItem('token') || ''
    if (!token) {
      console.error('未登录，无法测试')
      return
    }
    
    // 清除之前的日志
    sessionStorage.removeItem('wms_backup_logs')
    
    // 获取备份API路径
    const backupUrl = getApiPath('WAREHOUSE', 'BACKUP', warehouseId)
    console.log(`使用备份API路径: ${backupUrl}`)
    
    // 使用fetch手动发送备份请求
    fetch(backupUrl, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json, application/octet-stream',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'X-Debug-Mode': 'true'
      }
    })
      .then(response => {
        console.log('备份请求响应:', {
          status: response.status,
          statusText: response.statusText,
          headers: Object.fromEntries([...response.headers.entries()]),
          type: response.type,
          ok: response.ok
        })
        
        // 读取响应内容
        return response.blob()
      })
      .then(blob => {
        console.log('备份内容:', {
          size: blob.size,
          type: blob.type
        })
        
        // 如果是小文件，可能是错误信息，尝试读取
        if (blob.size < 1000) {
          const reader = new FileReader()
          reader.onload = () => {
            try {
              const text = reader.result
              console.log('小型响应内容:', text)
              
              try {
                const json = JSON.parse(text)
                console.log('解析为JSON:', json)
              } catch (e) {
                console.log('不是有效的JSON格式')
              }
            } catch (e) {
              console.error('无法读取响应内容:', e)
            }
          }
          reader.readAsText(blob)
        }
        
        return blob
      })
      .catch(error => {
        console.error('备份请求失败:', error)
      })
  },
  
  /**
   * 显示浏览器所有存储信息
   * 在控制台运行: window.wmsDebug.showStorageInfo()
   */
  showStorageInfo() {
    // localStorage内容
    const localStorageInfo = {}
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i)
      localStorageInfo[key] = localStorage.getItem(key)
    }
    
    // sessionStorage内容
    const sessionStorageInfo = {}
    for (let i = 0; i < sessionStorage.length; i++) {
      const key = sessionStorage.key(i)
      sessionStorageInfo[key] = sessionStorage.getItem(key)
    }
    
    // 获取cookie
    const cookieInfo = document.cookie.split(';').reduce((acc, item) => {
      const [key, value] = item.trim().split('=')
      if (key) acc[key] = value
      return acc
    }, {})
    
    const storageInfo = {
      localStorage: localStorageInfo,
      sessionStorage: sessionStorageInfo,
      cookies: cookieInfo
    }
    
    console.log('存储信息:', storageInfo)
    return storageInfo
  },
  
  /**
   * 检测指定API路径是否存在
   * 在控制台运行: window.wmsDebug.checkApiExists('/api/路径')
   */
  checkApiExists(apiPath) {
    if (!apiPath) {
      console.error('请提供要检测的API路径')
      return
    }
    
    console.log(`开始检测API路径是否存在: ${apiPath}`)
    
    // 获取当前token
    const token = localStorage.getItem('token') || sessionStorage.getItem('token') || ''
    
    // 不发送实际请求，只检查OPTIONS方法确认路径是否存在
    fetch(apiPath, {
      method: 'OPTIONS',
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
        'X-Debug-Check': 'true'
      }
    })
    .then(response => {
      console.log('API路径检测结果:', {
        exists: response.ok,
        status: response.status,
        statusText: response.statusText,
        headers: Object.fromEntries([...response.headers.entries()])
      })
      
      if (response.ok) {
        console.log(`✓ API路径存在: ${apiPath}`)
      } else {
        console.error(`✗ API路径不存在: ${apiPath}`)
        
        // 尝试几个可能的替代路径
        const pathParts = apiPath.split('/')
        const alternativePaths = []
        
        // 去掉或添加开头的斜杠
        if (apiPath.startsWith('/')) {
          alternativePaths.push(apiPath.substring(1))
        } else {
          alternativePaths.push('/' + apiPath)
        }
        
        // 尝试不同的API版本格式
        if (apiPath.includes('/api/v1/')) {
          alternativePaths.push(apiPath.replace('/api/v1/', '/api/'))
          alternativePaths.push(apiPath.replace('/api/v1/', '/api/v2/'))
        } else if (apiPath.includes('/api/')) {
          alternativePaths.push(apiPath.replace('/api/', '/api/v1/'))
        }
        
        // 对于仓库相关API，尝试不同的路径格式
        if (apiPath.includes('/warehouse/')) {
          alternativePaths.push(apiPath.replace('/warehouse/', '/warehouses/'))
        } else if (apiPath.includes('/warehouses/')) {
          alternativePaths.push(apiPath.replace('/warehouses/', '/warehouse/'))
        }
        
        console.log('可能的替代路径:', alternativePaths)
      }
      
      return response
    })
    .catch(error => {
      console.error('API路径检测出错:', error)
    })
  },
  
  /**
   * 测试所有可能的备份API路径
   * 在控制台运行: window.wmsDebug.testBackupPaths(仓库ID)
   */
  testBackupPaths(warehouseId) {
    if (!warehouseId) {
      console.error('请提供仓库ID')
      return
    }
    
    // 配置路径
    const configPath = getApiPath('WAREHOUSE', 'BACKUP', warehouseId)
    
    // 可能的路径组合
    const possiblePaths = [
      configPath, // 配置的路径
      `/api/v1/warehouse/${warehouseId}/backup/`,
      `/api/warehouse/${warehouseId}/backup/`,
      `/warehouse/${warehouseId}/backup/`,
      `/api/v1/warehouses/${warehouseId}/backup/`,
      `/api/warehouses/${warehouseId}/backup/`,
      `/warehouses/${warehouseId}/backup/`,
      `/api/v1/warehouse/warehouses/${warehouseId}/backup/`,
      `/warehouse/warehouses/${warehouseId}/backup/`
    ]
    
    console.log(`开始测试仓库ID=${warehouseId}的备份API可能路径:`)
    console.log(`当前配置的路径: ${configPath}`)
    
    // 去重
    const uniquePaths = [...new Set(possiblePaths)]
    uniquePaths.forEach(path => {
      this.checkApiExists(path)
    })
  }
}

// 将调试对象挂载到全局window对象上，方便在控制台中调用
window.wmsDebug = debug

export default debug 