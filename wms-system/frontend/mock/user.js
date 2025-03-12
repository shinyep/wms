const tokens = {
  admin: {
    token: 'admin-token'
  },
  editor: {
    token: 'editor-token'
  }
}

const users = {
  'admin-token': {
    roles: ['admin'],
    introduction: '我是超级管理员',
    avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    name: '管理员'
  },
  'editor-token': {
    roles: ['editor'],
    introduction: '我是编辑',
    avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    name: '普通用户'
  }
}

module.exports = [
  // 用户登录
  {
    url: '/api/user/login',
    type: 'post',
    response: config => {
      const { username } = config.body
      const token = tokens[username]

      // 模拟登录：允许任何用户名登录
      if (!token) {
        console.log('模拟登录成功:', username, '使用默认admin权限')
        return {
          code: 20000,
          data: {
            token: 'admin-token'
          }
        }
      }

      console.log('模拟登录成功:', username)
      return {
        code: 20000,
        data: token
      }
    }
  },

  // 获取用户信息
  {
    url: '/api/user/info',
    type: 'get',
    response: config => {
      const { token } = config.query
      const info = users[token]

      // 模拟用户信息：如果没有找到对应token的用户，返回管理员信息
      if (!info) {
        console.log('未找到用户信息，使用默认admin信息')
        return {
          code: 20000,
          data: users['admin-token']
        }
      }

      console.log('获取用户信息成功:', info.name)
      return {
        code: 20000,
        data: info
      }
    }
  },

  // 用户登出
  {
    url: '/api/user/logout',
    type: 'post',
    response: _ => {
      console.log('用户登出成功')
      return {
        code: 20000,
        data: 'success'
      }
    }
  }
] 