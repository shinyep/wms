import { getToken, setToken, removeToken } from '@/utils/auth'
import { login, logout, getInfo, getUserPermissions } from '@/api/user'
import { resetRouter } from '@/router'

const getDefaultState = () => {
  return {
    token: getToken(),
    name: '',
    avatar: '',
    roles: [],
    introduction: '',
    user: null,  // 完整用户信息
    permissions: null  // 用户权限信息
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  },
  SET_INTRODUCTION: (state, introduction) => {
    state.introduction = introduction
  },
  SET_USER: (state, user) => {
    state.user = user
  },
  SET_PERMISSIONS: (state, permissions) => {
    state.permissions = permissions
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      console.log('尝试登录:', username)
      login({ username: username.trim(), password: password })
        .then(response => {
          console.log('登录响应:', response)
          
          // 兼容不同的响应结构
          let token = null
          let userData = null
          
          if (response && typeof response === 'object') {
            // 尝试获取token
            token = response.token || 
                   (response.data && response.data.token) || 
                   (response.data && response.data.access_token)
                   
            // 尝试获取用户数据
            userData = response.user || response.data || response
          }
          
          if (!token) {
            console.error('响应数据结构:', response)
            reject(new Error('登录失败：未获取到访问令牌'))
            return
          }
          
          // 保存token
          commit('SET_TOKEN', token)
          setToken(token)
          console.log('Token已设置:', token)
          
          // 如果响应中包含用户数据，直接保存
          if (userData) {
            commit('SET_USER', userData)
            const username = userData.username || userData.name
            const role = userData.role || 'admin'
            const avatar = userData.avatar || ''
            
            commit('SET_NAME', username)
            commit('SET_AVATAR', avatar)
            commit('SET_ROLES', Array.isArray(role) ? role : [role])
          }
          
          resolve()
        })
        .catch(error => {
          console.error('登录失败:', error)
          reject(error)
        })
    })
  },

  // get user info and permissions
  getInfo({ commit, state, dispatch }) {
    return new Promise((resolve, reject) => {
      if (!state.token) {
        reject(new Error('请先登录'))
        return
      }

      getInfo()
        .then(response => {
          console.log('获取用户信息原始响应:', response)
          
          if (!response) {
            reject(new Error('验证失败，请重新登录'))
            return
          }

          // 尝试不同的数据结构
          let userData = response.data || response
          console.log('解析的用户数据:', userData)

          if (!userData) {
            reject(new Error('获取用户信息失败，请重新登录'))
            return
          }

          // 保存完整的用户信息
          commit('SET_USER', userData)

          // 尝试获取用户信息字段
          const username = userData.username || userData.name || userData.user_name
          const role = userData.role || userData.roles || userData.user_role || 'admin'
          const avatar = userData.avatar || userData.avatar_url || ''

          console.log('提取的用户信息:', { username, role, avatar })

          // 确保角色信息存在
          if (!role) {
            console.error('角色信息缺失:', userData)
            reject(new Error('获取角色信息失败'))
            return
          }

          // 处理角色信息，确保它是数组格式
          const roles = Array.isArray(role) ? role : [role]
          console.log('最终角色信息:', roles)
          
          // 保存用户信息
          commit('SET_ROLES', roles)
          commit('SET_NAME', username)
          commit('SET_AVATAR', avatar)
          
          // 获取用户权限
          dispatch('getPermissions')
            .then(() => {
              resolve({ roles, name: username, avatar })
            })
            .catch(error => {
              console.warn('获取权限失败，但不影响登录:', error)
              resolve({ roles, name: username, avatar })
            })
        })
        .catch(error => {
          console.error('获取用户信息失败:', error)
          reject(error)
        })
    })
  },
  
  // get user permissions
  getPermissions({ commit }) {
    return new Promise((resolve, reject) => {
      getUserPermissions().then(response => {
        console.log('获取用户权限响应:', response)
        
        if (!response) {
          reject(new Error('获取权限失败'))
          return
        }
        
        // 保存权限信息
        commit('SET_PERMISSIONS', response)
        resolve(response)
      }).catch(error => {
        console.error('获取用户权限失败:', error)
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state, dispatch }) {
    return new Promise((resolve, reject) => {
      logout().then(() => {
        commit('SET_TOKEN', '')
        commit('SET_ROLES', [])
        commit('SET_PERMISSIONS', null)
        removeToken()
        resetRouter()

        // 重置访问的视图和缓存的视图
        dispatch('tagsView/delAllViews', null, { root: true })

        commit('RESET_STATE')
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken()
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
