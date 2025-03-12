<template>
  <div class="register-container">
    <el-form ref="registerForm" :model="registerForm" :rules="registerRules" class="register-form" auto-complete="on" label-position="left">
      <div class="title-container">
        <h3 class="title">用户注册</h3>
      </div>

      <el-form-item prop="username">
        <span class="svg-container">
          <i class="el-icon-user" />
        </span>
        <el-input
          ref="username"
          v-model="registerForm.username"
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
          v-model="registerForm.password"
          :type="passwordType"
          placeholder="密码"
          name="password"
          tabindex="2"
          auto-complete="on"
        />
        <span class="show-pwd" @click="showPwd">
          <i :class="passwordType === 'password' ? 'el-icon-view' : 'el-icon-hide'" />
        </span>
      </el-form-item>

      <el-form-item prop="confirm_password">
        <span class="svg-container">
          <i class="el-icon-lock" />
        </span>
        <el-input
          :key="passwordType + 'confirm'"
          ref="confirm_password"
          v-model="registerForm.confirm_password"
          :type="passwordType"
          placeholder="确认密码"
          name="confirm_password"
          tabindex="3"
          auto-complete="on"
        />
        <span class="show-pwd" @click="showPwd">
          <i :class="passwordType === 'password' ? 'el-icon-view' : 'el-icon-hide'" />
        </span>
      </el-form-item>

      <el-form-item prop="email">
        <span class="svg-container">
          <i class="el-icon-message" />
        </span>
        <el-input
          ref="email"
          v-model="registerForm.email"
          placeholder="邮箱"
          name="email"
          type="text"
          tabindex="4"
          auto-complete="on"
        />
      </el-form-item>

      <el-form-item prop="phone">
        <span class="svg-container">
          <i class="el-icon-phone" />
        </span>
        <el-input
          ref="phone"
          v-model="registerForm.phone"
          placeholder="手机号"
          name="phone"
          type="text"
          tabindex="5"
          auto-complete="on"
        />
      </el-form-item>

      <el-form-item prop="first_name">
        <span class="svg-container">
          <i class="el-icon-user" />
        </span>
        <el-input
          ref="first_name"
          v-model="registerForm.first_name"
          placeholder="姓"
          name="first_name"
          type="text"
          tabindex="6"
          auto-complete="on"
        />
      </el-form-item>

      <el-form-item prop="last_name">
        <span class="svg-container">
          <i class="el-icon-user" />
        </span>
        <el-input
          ref="last_name"
          v-model="registerForm.last_name"
          placeholder="名"
          name="last_name"
          type="text"
          tabindex="7"
          auto-complete="on"
        />
      </el-form-item>

      <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:15px;" @click.native.prevent="handleRegister">注册</el-button>
      <div class="tips">
        <span>已有账号? </span>
        <router-link to="/login">立即登录</router-link>
      </div>
    </el-form>
  </div>
</template>

<script>
import { register } from '@/api/user'
import ElementUI from 'element-ui'

export default {
  name: 'Register',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (value.trim().length === 0) {
        callback(new Error('用户名不能为空'))
      } else if (value.length < 3) {
        callback(new Error('用户名不能少于3个字符'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('密码不能少于6位'))
      } else {
        callback()
      }
    }
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== this.registerForm.password) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    }
    const validateEmail = (rule, value, callback) => {
      if (value && !/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/.test(value)) {
        callback(new Error('请输入有效的邮箱地址'))
      } else {
        callback()
      }
    }
    const validatePhone = (rule, value, callback) => {
      if (value && !/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入有效的手机号码'))
      } else {
        callback()
      }
    }
    return {
      registerForm: {
        username: '',
        password: '',
        confirm_password: '',
        email: '',
        phone: '',
        first_name: '',
        last_name: ''
      },
      registerRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }],
        confirm_password: [{ required: true, trigger: 'blur', validator: validateConfirmPassword }],
        email: [{ trigger: 'blur', validator: validateEmail }],
        phone: [{ trigger: 'blur', validator: validatePhone }]
      },
      loading: false,
      passwordType: 'password'
    }
  },
  methods: {
    showPwd() {
      this.passwordType = this.passwordType === 'password' ? '' : 'password'
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleRegister() {
      this.$refs.registerForm.validate(valid => {
        if (valid) {
          this.loading = true
          
          // 确保所有字段符合后端要求
          const formData = {
            username: this.registerForm.username,
            password: this.registerForm.password,
            confirm_password: this.registerForm.confirm_password,
            email: this.registerForm.email || '',
            phone: this.registerForm.phone || '',
            first_name: this.registerForm.first_name || '',
            last_name: this.registerForm.last_name || ''
          }
          
          console.log('准备提交的表单数据:', formData)
          
          // 直接使用fetch API进行提交，绕过axios的处理
          fetch('/api/v1/user/register/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
          })
          .then(response => {
            console.log('注册原始响应:', response)
            
            if (response.ok) {
              return response.json()
            } else {
              if (response.status === 400) {
                return response.json().then(data => {
                  throw { response: { status: 400, data } }
                })
              }
              throw new Error(`注册请求失败，状态码: ${response.status}`)
            }
          })
          .then(data => {
            console.log('注册响应数据:', data)
            this.$message.success('注册成功')
            
            // 注册成功后自动登录
            const loginData = {
              username: this.registerForm.username,
              password: this.registerForm.password
            }
            
            return fetch('/api/v1/user/login/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(loginData)
            })
          })
          .then(response => {
            if (response.ok) {
              return response.json()
            }
            throw new Error('登录请求失败')
          })
          .then(data => {
            console.log('登录响应数据:', data)
            // 保存token并跳转
            if (data.token) {
              this.$store.commit('user/SET_TOKEN', data.token)
              this.$router.push('/dashboard')
            } else {
              // 如果没有token，跳转到登录页
              this.$message.info('请使用您的新账号登录')
              setTimeout(() => {
                this.$router.push('/login')
              }, 1500)
            }
          })
          .catch(error => {
            console.error('注册错误:', error)
            
            // 增强错误处理
            let errorMessage = '注册失败，请检查信息是否正确'
            
            if (error.response) {
              console.error('错误响应:', error.response)
              const status = error.response.status
              const data = error.response.data
              
              if (status === 400) {
                if (typeof data === 'object') {
                  // 处理字段错误
                  const fieldErrors = []
                  for (const key in data) {
                    if (Array.isArray(data[key])) {
                      fieldErrors.push(`${key}: ${data[key].join(', ')}`)
                    } else if (typeof data[key] === 'string') {
                      fieldErrors.push(`${key}: ${data[key]}`)
                    }
                  }
                  
                  if (fieldErrors.length > 0) {
                    errorMessage = '注册信息有误: ' + fieldErrors.join('; ')
                  }
                } else if (typeof data === 'string') {
                  errorMessage = data
                }
              }
            } else if (error.message) {
              errorMessage = error.message
            }
            
            this.$message.error(errorMessage)
          })
          .finally(() => {
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

<style lang="scss">
$bg:#283443;
$light_gray:#fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .register-container .el-input input {
    color: $cursor;
  }
}

.register-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;

.register-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .register-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 80px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;
    text-align: center;
    
    a {
      color: #42b983;
    }
  }
}
</style> 