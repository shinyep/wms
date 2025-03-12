const state = {
  title: 'WMS System',
  fixedHeader: true,
  sidebarLogo: true,
  showSettings: true,
  tagsView: true,
  showFooter: true,
  footerText: '© 2024 WMS System'
}

const mutations = {
  CHANGE_SETTING: (state, { key, value }) => {
    if (Object.prototype.hasOwnProperty.call(state, key)) {
      state[key] = value
    }
  }
}

const actions = {
  changeSetting({ commit }, data) {
    commit('CHANGE_SETTING', data)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
} 