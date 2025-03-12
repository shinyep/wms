<template>
  <el-form
    ref="passwordForm"
    :model="passwordForm"
    :rules="passwordRules"
    label-width="100px"
  >
    <el-form-item label="旧密码" prop="oldPassword">
      <el-input
        v-model="passwordForm.oldPassword"
        type="password"
        placeholder="请输入旧密码"
        show-password
      />
    </el-form-item>
    <el-form-item label="新密码" prop="newPassword">
      <el-input
        v-model="passwordForm.newPassword"
        type="password"
        placeholder="请输入新密码"
        show-password
      />
    </el-form-item>
    <el-form-item label="确认密码" prop="confirmPassword">
      <el-input
        v-model="passwordForm.confirmPassword"
        type="password"
        placeholder="请再次输入新密码"
        show-password
      />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" :loading="loading" @click="handleChangePassword">
        修改密码
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  data() {
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== this.passwordForm.newPassword) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    return {
      loading: false,
      passwordForm: {
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      passwordRules: {
        oldPassword: [
          { required: true, message: '请输入旧密码', trigger: 'blur' },
          { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
        ],
        newPassword: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请再次输入新密码', trigger: 'blur' },
          { validator: validateConfirmPassword, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    handleChangePassword() {
      this.$refs.passwordForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$message({
            message: '密码修改成功，请重新登录',
            type: 'success',
            duration: 5 * 1000
          })
          this.loading = false
          // 在实际应用中，这里应该调用API修改密码
          // 然后退出登录
          setTimeout(() => {
            this.$store.dispatch('user/logout').then(() => {
              this.$router.push('/login')
            })
          }, 1500)
        }
      })
    }
  }
}
</script> 