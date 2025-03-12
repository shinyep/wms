const Mock = require('mockjs')

const warehouseList = []
const count = 20

for (let i = 0; i < count; i++) {
  warehouseList.push(Mock.mock({
    id: '@increment',
    name: '仓库 @integer(1, 100)',
    type: '@pick(["finished", "parts", "material"])',
    capacity: '@integer(1000, 10000)',
    capacityUnit: '@pick(["个", "箱", "吨", "平方米"])',
    used: '@integer(0, 1000)',
    manager: '@cname',
    description: '@sentence(10, 20)',
    createTime: '@datetime("yyyy-MM-dd HH:mm:ss")'
  }))
}

module.exports = [
  // 获取仓库列表
  {
    url: '/api/warehouse/list',
    type: 'get',
    response: config => {
      const { name, type, page = 1, limit = 10 } = config.query

      let mockList = warehouseList.filter(item => {
        if (name && item.name.indexOf(name) < 0) return false
        if (type && item.type !== type) return false
        return true
      })

      const pageList = mockList.filter((item, index) => index < limit * page && index >= limit * (page - 1))

      return {
        code: 20000,
        data: {
          total: mockList.length,
          items: pageList
        }
      }
    }
  },

  // 获取仓库详情
  {
    url: '/api/warehouse/[0-9]+',
    type: 'get',
    response: config => {
      const { url } = config
      const id = url.match(/\/api\/warehouse\/(\d+)/)[1]
      
      for (const warehouse of warehouseList) {
        if (warehouse.id === +id) {
          return {
            code: 20000,
            data: warehouse
          }
        }
      }
      
      return {
        code: 50000,
        message: '仓库不存在'
      }
    }
  },

  // 创建仓库
  {
    url: '/api/warehouse',
    type: 'post',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  },

  // 更新仓库
  {
    url: '/api/warehouse/[0-9]+',
    type: 'put',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  },

  // 删除仓库
  {
    url: '/api/warehouse/[0-9]+',
    type: 'delete',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  },

  // 获取仓库月度报表
  {
    url: '/api/warehouse/[0-9]+/report/[0-9]{4}/[0-9]{2}',
    type: 'get',
    response: _ => {
      return {
        code: 20000,
        data: {
          inbound: Array.from({ length: 10 }, () => Mock.mock({
            date: '@date("yyyy-MM-dd")',
            quantity: '@integer(10, 100)',
            operator: '@cname',
            productName: '产品 @integer(1000, 9999)',
            batchNo: 'BN@integer(10000, 99999)',
            remark: '@sentence(5, 10)'
          })),
          outbound: Array.from({ length: 8 }, () => Mock.mock({
            date: '@date("yyyy-MM-dd")',
            quantity: '@integer(5, 50)',
            operator: '@cname',
            productName: '产品 @integer(1000, 9999)',
            destination: '@city',
            remark: '@sentence(5, 10)'
          })),
          inventory: Array.from({ length: 5 }, () => Mock.mock({
            productName: '产品 @integer(1000, 9999)',
            category: '@pick(["A类", "B类", "C类", "D类"])',
            initialQuantity: '@integer(100, 500)',
            inboundQuantity: '@integer(50, 200)',
            outboundQuantity: '@integer(20, 100)',
            finalQuantity: '@integer(150, 600)',
            unit: '@pick(["个", "箱", "吨"])'
          }))
        }
      }
    }
  },

  // 创建月度报表
  {
    url: '/api/warehouse/report',
    type: 'post',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  }
] 