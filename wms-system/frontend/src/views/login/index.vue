<template>
  <div class="login-container">
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on" label-position="left">
      <div class="title-container">
        <h3 class="title">有田食品仓库管理系统</h3>
      </div>

      <el-form-item prop="username">
        <span class="svg-container">
          <i class="el-icon-user" />
        </span>
        <el-input
          ref="username"
          v-model="loginForm.username"
          placeholder="用户名"
          name="username"
          type="text"
          tabindex="1"
          auto-complete="on"
        />
      </el-form-item>

      <el-form-item prop="password">
        <span class="svg-container">
          <i class="el-icon-lock" />
        </span>
        <el-input
          :key="passwordType"
          ref="password"
          v-model="loginForm.password"
          :type="passwordType"
          placeholder="密码"
          name="password"
          tabindex="2"
          auto-complete="on"
          @keyup.enter.native="handleLogin"
        />
        <span class="show-pwd" @click="showPwd">
          <i :class="passwordType === 'password' ? 'el-icon-view' : 'el-icon-hide'" />
        </span>
      </el-form-item>

      <el-button :loading="loading" type="primary" class="login-button" @click.native.prevent="handleLogin">登录</el-button>
      
      <div class="tips">
        <span>没有账号? </span>
        <router-link to="/register">立即注册</router-link>
      </div>
    </el-form>
  </div>
</template>

<script>
import { validUsername } from '@/utils/validate'
import ElementUI from 'element-ui'

export default {
  name: 'Login',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (value.trim().length === 0) {
        callback(new Error('用户名不能为空'))
      } else if (!/^[a-zA-Z0-9_\u4e00-\u9fa5]{2,20}$/.test(value)) {
        callback(new Error('用户名只能包含字母、数字、下划线或中文，长度2-20位'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('密码不能少于6位'))
      } else if (value.length > 20) {
        callback(new Error('密码不能超过20位'))
      } else if (!/^[a-zA-Z0-9_@#$%^&*]{6,20}$/.test(value)) {
        callback(new Error('密码只能包含字母、数字和特殊字符(_@#$%^&*)'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [
          { required: true, trigger: 'blur', validator: validateUsername }
        ],
        password: [
          { required: true, trigger: 'blur', validator: validatePassword }
        ]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    showPwd() {
      this.passwordType = this.passwordType === 'password' ? '' : 'password'
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('user/login', {
            username: this.loginForm.username.trim(),
            password: this.loginForm.password
          })
            .then(async () => {
              try {
                // 获取用户信息
                const { roles } = await this.$store.dispatch('user/getInfo')
                // 生成路由
                const accessRoutes = await this.$store.dispatch('permission/generateRoutes', roles)
                // 添加路由
                accessRoutes.forEach(route => {
                  this.$router.addRoute(route)
                })
                // 使用 push 而不是 replace
                this.$router.push(this.redirect || '/dashboard')
              } catch (error) {
                console.error('登录后处理错误:', error)
                this.$message.error(error.message || '获取用户信息失败')
                await this.$store.dispatch('user/resetToken')
                this.loginForm.password = ''
                this.$nextTick(() => {
                  this.$refs.password.focus()
                })
              } finally {
                this.loading = false
              }
            })
            .catch((error) => {
              console.error('登录处理错误:', error)
              let errorMsg = error.message || '登录失败，请检查用户名和密码'
              
              // 优化错误提示
              if (errorMsg.includes('用户名或密码错误')) {
                this.loginForm.password = ''
                this.$nextTick(() => {
                  this.$refs.password.focus()
                })
              }
              
              this.$message({
                message: errorMsg,
                type: 'error',
                duration: 5000
              })
              
              this.loading = false
            })
        } else {
          console.log('表单验证失败')
          return false
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/styles/components/login.scss';
</style> 