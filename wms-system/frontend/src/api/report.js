import request from '@/utils/request'
import axios from 'axios'
import XLSX from 'xlsx'
import { saveAs } from 'file-saver'

// 创建一个通用的请求配置生成器
const createRequestConfig = (params = {}, timeout = 30000) => {
  const source = axios.CancelToken.source()
  const config = {
    cancelToken: source.token,
    timeout: timeout,
    _isShowError: true
  }
  
  if (params) {
    config.params = params
  }
  
  return { config, source }
}

/**
 * 获取月度报表数据
 * @param {Object} params - 查询参数
 * @param {number} params.warehouse_id - 仓库ID
 * @param {string} params.month - 月份，格式：YYYY-MM
 * @param {string} params.format - 响应格式，'json'或'excel'
 * @param {number} params.limit - 限制返回的条数
 * @returns {Promise} - 响应Promise
 */
export function getMonthlyReport(params) {
  const { config, source } = createRequestConfig(params)
  
  // 设置请求超时自动取消
  const timeoutId = setTimeout(() => {
    source.cancel('请求超时自动取消')
  }, config.timeout)

  // 判断是否为excel格式，设置相应的responseType
  const isExcel = params.format === 'excel'
  
  return request({
    url: '/api/v1/warehouse/monthly-report/',
    method: 'get',
    ...config,
    responseType: isExcel ? 'blob' : 'json',
    _onComplete: () => {
      clearTimeout(timeoutId)
    }
  }).catch(error => {
    clearTimeout(timeoutId)
    throw error
  })
}

/**
 * 创建报表
 * @param {Object} data - 报表数据
 * @returns {Promise} - 响应Promise
 */
export function createReport(data) {
  return request({
    url: '/api/v1/warehouse/reports/',
    method: 'post',
    data
  })
}

/**
 * 获取报表列表
 * @param {Object} params - 查询参数
 * @returns {Promise} - 响应Promise
 */
export function getReportList(params) {
  return request({
    url: '/api/v1/warehouse/reports/',
    method: 'get',
    params
  })
}

/**
 * 获取报表详情
 * @param {number} id - 报表ID
 * @returns {Promise} - 响应Promise
 */
export function getReportDetail(id) {
  return request({
    url: `/api/v1/warehouse/reports/${id}/`,
    method: 'get'
  })
}

/**
 * 更新报表
 * @param {number} id - 报表ID
 * @param {Object} data - 报表数据
 * @returns {Promise} - 响应Promise
 */
export function updateReport(id, data) {
  return request({
    url: `/api/v1/warehouse/reports/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除报表
 * @param {number} id - 报表ID
 * @returns {Promise} - 响应Promise
 */
export function deleteReport(id) {
  return request({
    url: `/api/v1/warehouse/reports/${id}/`,
    method: 'delete'
  })
}

// 创建报表记录
export function createRecord(data) {
  return request({
    url: '/api/v1/warehouse/create-record/',
    method: 'post',
    data
  })
}

// 更新报表记录
export function updateRecord(data) {
  return request({
    url: '/api/v1/warehouse/update-record/',
    method: 'put',
    data
  })
}

// 删除报表记录
export function deleteRecord(params) {
  return request({
    url: '/api/v1/warehouse/delete-record/',
    method: 'delete',
    params
  })
}

// 导出报表
export function exportReport(params) {
  return request({
    url: '/api/v1/warehouse/export_report/',
    method: 'get',
    params: { ...params, format: 'excel' },
    responseType: 'blob',
    timeout: 60000 // 增加超时时间，因为导出可能需要较长时间
  })
}

// 备选导出报表方法（如果上面的方法不可用）
export function exportReportAlternative(params) {
  return request({
    url: '/api/v1/warehouse/reports/export/',
    method: 'get',
    params: { ...params, format: 'excel' },
    responseType: 'blob',
    timeout: 60000
  })
}

/**
 * 更新月度报表数据
 * @param {Object} data - 报表数据
 * @param {string} data.warehouse_id - 仓库ID
 * @param {string} data.month - 月份，格式：YYYY-MM
 * @param {Object} data.data - 报表详细数据，包含inbound、outbound和inventory
 * @returns {Promise} - 响应Promise
 */
export function updateMonthlyReport(data) {
  return request({
    url: '/api/v1/warehouse/update_monthly_report/',
    method: 'post',
    data,
    timeout: 60000 // 增加超时时间，适用于大量数据
  })
}

/**
 * 自动创建月度报表
 * 根据上个月的报表数据自动创建当月报表，期初库存为上月期末库存
 * @param {Object} data - 报表数据
 * @param {string} data.warehouse_id - 仓库ID
 * @param {string} data.month - 月份，格式：YYYY-MM
 * @returns {Promise} - 响应Promise
 */
export function createAutoMonthlyReport(data) {
  // 确保数据格式正确
  const formattedData = {
    warehouse_id: data.warehouse_id,
    month: data.month
  }
  
  // 打印请求数据以便调试
  console.log('自动创建月度报表请求数据:', formattedData)
  
  return request({
    url: '/api/v1/warehouse/create_auto_monthly_report/',
    method: 'post',
    data: formattedData,
    timeout: 60000, // 增加超时时间
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

// 再添加一个备选导出方法
export function exportReportFallback(params) {
  const { warehouse_id, month, format } = params
  
  // 尝试直接拼接完整的导出URL
  return request({
    url: `/api/v1/warehouse/${warehouse_id}/export-report/${month}/`,
    method: 'get',
    params: { format },
    responseType: 'blob',
    timeout: 60000
  })
}

// 添加更多可能的导出路径格式
export function exportReportByPath(params) {
  const { warehouse_id, month } = params
  
  // 尝试直接请求后端API路径
  return request({
    url: `/api/v1/warehouse/${warehouse_id}/reports/${month}/export/`,
    method: 'get',
    params: { format: 'excel' },
    responseType: 'blob',
    timeout: 60000
  })
}

// 尝试另一种通用路径格式
export function exportReportGeneric(params) {
  const { warehouse_id, month } = params
  
  return request({
    url: `/api/v1/reports/export/`,
    method: 'get',
    params: {
      warehouse_id,
      month,
      format: 'excel'
    },
    responseType: 'blob',
    timeout: 60000
  })
}

// 尝试使用POST方法导出
export function exportReportPost(params) {
  const { warehouse_id, month } = params
  
  return request({
    url: `/api/v1/warehouse/export/`,
    method: 'post',
    data: {
      warehouse_id,
      month,
      format: 'excel'
    },
    responseType: 'blob',
    timeout: 60000
  })
}

// 直接从后端下载Excel文件
export function downloadReportFile(params) {
  const { warehouse_id, month } = params
  
  // 创建完整的URL用于下载
  const baseURL = process.env.VUE_APP_BASE_API || ''
  const fullURL = `${baseURL}/api/v1/warehouse/${warehouse_id}/monthly-report/?month=${month}&format=excel`
  
  // 返回一个Promise，用于处理下载逻辑
  return new Promise((resolve, reject) => {
    try {
      // 创建一个隐藏的a标签
      const link = document.createElement('a')
      link.href = fullURL
      link.target = '_blank'
      link.setAttribute('download', `月度报表_${month}.xlsx`)
      document.body.appendChild(link)
      
      // 触发点击事件
      link.click()
      
      // 移除链接元素
      document.body.removeChild(link)
      
      // 模拟成功响应
      setTimeout(() => {
        resolve(new Blob(['下载已开始'], { type: 'text/plain' }))
      }, 1000)
    } catch (error) {
      reject(error)
    }
  })
}

// 使用iframe下载文件
export function iframeDownloadReport(params) {
  const { warehouse_id, month } = params
  
  // 创建完整的URL用于下载
  const baseURL = process.env.VUE_APP_BASE_API || ''
  const fullURL = `${baseURL}/api/v1/warehouse/${warehouse_id}/reports/${month}/download/`
  
  // 返回一个Promise
  return new Promise((resolve, reject) => {
    try {
      // 创建一个隐藏的iframe
      const iframe = document.createElement('iframe')
      iframe.style.display = 'none'
      iframe.src = fullURL
      document.body.appendChild(iframe)
      
      // 设置超时，移除iframe
      setTimeout(() => {
        document.body.removeChild(iframe)
        resolve(new Blob(['下载已开始'], { type: 'text/plain' }))
      }, 5000)
    } catch (error) {
      reject(error)
    }
  })
}

// 从仓库详情页导出报表
export function exportReportFromDetail(warehouse_id, month) {
  return request({
    url: `/api/v1/warehouse/${warehouse_id}/detail/export/`,
    method: 'get',
    params: { month, format: 'excel' },
    responseType: 'blob',
    timeout: 60000
  })
}

// 适用于详情页的另一种导出格式
export function exportReportFromDetailAlt(warehouse_id, month) {
  return request({
    url: `/api/v1/warehouse/detail/${warehouse_id}/report/${month}/`,
    method: 'get',
    params: { format: 'excel' },
    responseType: 'blob',
    timeout: 60000
  })
}

// 尝试直接从仓库详情获取并下载当前数据
export function exportCurrentInventory(warehouse_id, month) {
  return request({
    url: `/api/v1/warehouse/${warehouse_id}/inventory/export/`,
    method: 'get',
    params: { month, format: 'excel' },
    responseType: 'blob',
    timeout: 60000 
  })
}

// 本地生成Excel文件导出（不依赖后端API）
export function generateLocalExcel(reportData, month) {
  return new Promise((resolve, reject) => {
    try {
      console.log('开始生成本地Excel文件，数据:', reportData)
      
      // 准备工作表数据
      const inboundData = reportData.inbound || []
      const outboundData = reportData.outbound || []
      const inventoryData = reportData.inventory || []
      
      // 创建工作簿
      const workbook = XLSX.utils.book_new()
      
      // 添加入库明细工作表
      if (inboundData.length > 0) {
        const inboundWS = XLSX.utils.json_to_sheet(inboundData)
        XLSX.utils.book_append_sheet(workbook, inboundWS, '入库明细')
      }
      
      // 添加出库明细工作表
      if (outboundData.length > 0) {
        const outboundWS = XLSX.utils.json_to_sheet(outboundData)
        XLSX.utils.book_append_sheet(workbook, outboundWS, '出库明细')
      }
      
      // 添加库存明细工作表
      if (inventoryData.length > 0) {
        const inventoryWS = XLSX.utils.json_to_sheet(inventoryData)
        XLSX.utils.book_append_sheet(workbook, inventoryWS, '库存明细')
      }
      
      // 生成Excel文件
      const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' })
      const blob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
      
      // 解析Promise
      resolve(blob)
    } catch (error) {
      console.error('本地生成Excel文件失败:', error)
      reject(error)
    }
  })
}

// 导出仓库详情页的库存数据
export function exportDetailPageTable(tableData, filename) {
  return new Promise((resolve, reject) => {
    try {
      // 创建工作簿和工作表
      const workbook = XLSX.utils.book_new()
      const worksheet = XLSX.utils.json_to_sheet(tableData)
      
      // 添加工作表到工作簿
      XLSX.utils.book_append_sheet(workbook, worksheet, '仓库库存')
      
      // 生成Excel文件
      const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' })
      const blob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
      
      // 解析Promise
      resolve(blob)
    } catch (error) {
      console.error('导出表格数据失败:', error)
      reject(error)
    }
  })
}

// 专门处理月度报表导出的新函数
export function exportMonthlyReport(params) {
  const { warehouse_id, month } = params
  
  // 尝试所有可能的API路径
  const exportPaths = [
    `/api/v1/warehouse/${warehouse_id}/monthly-report/`,
    `/api/v1/warehouse/monthly-report/`,
    `/api/v1/warehouse/${warehouse_id}/reports/monthly/`,
    `/api/v1/warehouse/reports/${warehouse_id}/monthly/`,
    `/api/v1/reports/monthly/${warehouse_id}/`
  ]
  
  // 返回一个Promise数组
  const exportPromises = exportPaths.map(path => {
    return request({
      url: path,
      method: 'get',
      params: { 
        month,
        format: 'excel',
        warehouse_id 
      },
      responseType: 'blob',
      timeout: 60000,
      validateStatus: status => status >= 200 && status < 300
    }).catch(error => {
      console.warn(`导出路径 ${path} 失败:`, error)
      return Promise.reject(error)
    })
  })
  
  // 使用Promise.any尝试所有路径，返回第一个成功的结果
  return Promise.any(exportPromises)
}

// 导出固定模板格式的Excel
export function exportTemplateExcel(data, month) {
  return new Promise((resolve, reject) => {
    try {
      console.log('开始导出Excel模板，数据条数:', data.length)
      
      // 创建工作簿
      const workbook = XLSX.utils.book_new()
      
      // 定义表头
      const headers = [
        ['位置', '品项', '规格/型号', '期初库存', '累计入库', '累计出库', '库存', '单位', '单价', '库存金额', 'id']
      ]
      
      // 处理数据，确保格式正确
      const formattedData = data.map(item => [
        item.位置 || '',                                    // 位置
        item.品项 || '',                                    // 品项
        (item['规格/型号'] || '') + '',                     // 规格/型号
        Number(item.期初库存 || item.库存 || 0),            // 期初库存
        0,                                                 // 累计入库
        0,                                                 // 累计出库
        Number(item.库存 || 0),                            // 库存
        '个',                                              // 单位
        Number(item.单价 || 0),                            // 单价
        Number(item.库存金额 || item.金额 || 0),            // 库存金额
        'iw_' + (item.id || '')                           // id
      ])
      
      console.log('格式化后的数据:', formattedData.length, '条')
      
      // 创建工作表
      const worksheet = XLSX.utils.aoa_to_sheet([...headers, ...formattedData])
      
      // 设置列宽
      worksheet['!cols'] = [
        { wch: 5 },   // 位置
        { wch: 8 },   // 品项
        { wch: 12 },  // 规格/型号
        { wch: 8 },   // 期初库存
        { wch: 8 },   // 累计入库
        { wch: 8 },   // 累计出库
        { wch: 6 },   // 库存
        { wch: 4 },   // 单位
        { wch: 8 },   // 单价
        { wch: 10 },  // 库存金额
        { wch: 40 }   // id
      ]
      
      // 添加工作表到工作簿
      XLSX.utils.book_append_sheet(workbook, worksheet, '库存期间')
      
      // 生成Excel文件 - 明确使用二进制格式
      const excelBuffer = XLSX.write(workbook, { 
        bookType: 'xlsx', 
        type: 'binary',
        cellStyles: true
      })
      
      // 转换二进制字符串为ArrayBuffer
      const s2ab = s => {
        const buf = new ArrayBuffer(s.length)
        const view = new Uint8Array(buf)
        for (let i = 0; i < s.length; i++) {
          view[i] = s.charCodeAt(i) & 0xFF
        }
        return buf
      }
      
      // 创建Blob对象
      const blob = new Blob([s2ab(excelBuffer)], { 
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
      })
      
      console.log('Excel生成完成，准备返回Blob')
      resolve(blob)
    } catch (error) {
      console.error('生成Excel模板失败:', error)
      reject(error)
    }
  })
}

/**
 * 更新指定月份的期初库存数据
 * @param {Object} data - 请求参数
 * @param {number} data.warehouse_id - 仓库ID
 * @param {string} data.month - 月份，格式：YYYY-MM
 * @returns {Promise} - 请求结果
 */
export function updateInitialStock(data) {
  console.log('调用updateInitialStock API，参数:', data);
  return request({
    url: '/api/v1/warehouse/monthly-report/update_initial_stock/',
    method: 'post',
    data
  })
} 