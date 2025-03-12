<template>
  <div class="security-container">
    <el-card class="security-card">
      <div slot="header" class="clearfix">
        <span>账号安全</span>
      </div>
      <el-form label-width="120px">
        <el-form-item label="登录密码">
          <div class="security-item">
            <span>定期修改密码可以提高账号安全性</span>
            <el-button type="primary" size="small" @click="showPasswordDialog">修改密码</el-button>
          </div>
        </el-form-item>
        <el-form-item label="绑定手机">
          <div class="security-item">
            <span>已绑定：{{ maskPhone(userInfo.phone) }}</span>
            <el-button type="primary" size="small" @click="showPhoneDialog">修改</el-button>
          </div>
        </el-form-item>
        <el-form-item label="绑定邮箱">
          <div class="security-item">
            <span>已绑定：{{ maskEmail(userInfo.email) }}</span>
            <el-button type="primary" size="small" @click="showEmailDialog">修改</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="security-card">
      <div slot="header" class="clearfix">
        <span>登录保护</span>
      </div>
      <el-form label-width="120px">
        <el-form-item label="登录验证">
          <div class="security-item">
            <span>开启后，登录时需要进行安全验证</span>
            <el-switch
              v-model="securitySettings.loginVerification"
              active-text="已开启"
              inactive-text="已关闭"
            />
          </div>
        </el-form-item>
        <el-form-item label="异地登录提醒">
          <div class="security-item">
            <span>开启后，异地登录将发送提醒</span>
            <el-switch
              v-model="securitySettings.loginAlert"
              active-text="已开启"
              inactive-text="已关闭"
            />
          </div>
        </el-form-item>
        <el-form-item label="登录IP限制">
          <div class="security-item">
            <span>开启后，只允许指定IP登录</span>
            <el-switch
              v-model="securitySettings.ipRestriction"
              active-text="已开启"
              inactive-text="已关闭"
              @change="handleIpRestrictionChange"
            />
          </div>
        </el-form-item>
        <el-form-item v-if="securitySettings.ipRestriction" label="允许的IP">
          <el-input
            v-model="securitySettings.allowedIps"
            type="textarea"
            :rows="3"
            placeholder="请输入允许登录的IP地址，多个IP请用逗号分隔"
          />
        </el-form-item>
      </el-form>
      <div class="form-actions">
        <el-button type="primary" @click="saveSecuritySettings">保存设置</el-button>
      </div>
    </el-card>

    <el-card class="security-card">
      <div slot="header" class="clearfix">
        <span>登录设备管理</span>
      </div>
      <el-table
        :data="loginDevices"
        style="width: 100%"
      >
        <el-table-column
          prop="device"
          label="设备/浏览器"
          width="180"
        />
        <el-table-column
          prop="ip"
          label="IP地址"
          width="140"
        />
        <el-table-column
          prop="location"
          label="登录地点"
          width="140"
        />
        <el-table-column
          prop="time"
          label="最近登录时间"
          width="180"
        />
        <el-table-column
          prop="status"
          label="状态"
        >
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 'current' ? 'success' : 'info'">
              {{ scope.row.status === 'current' ? '当前设备' : '其他设备' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          width="120"
        >
          <template slot-scope="scope">
            <el-button
              v-if="scope.row.status !== 'current'"
              type="text"
              size="small"
              @click="removeDevice(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 修改密码对话框 -->
    <el-dialog title="修改密码" :visible.sync="passwordDialogVisible" width="500px">
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
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="passwordDialogVisible = false">取 消</el-button>
        <el-button type="primary" :loading="passwordLoading" @click="handleChangePassword">确 定</el-button>
      </div>
    </el-dialog>

    <!-- 修改手机对话框 -->
    <el-dialog title="修改手机号" :visible.sync="phoneDialogVisible" width="500px">
      <el-form
        ref="phoneForm"
        :model="phoneForm"
        :rules="phoneRules"
        label-width="100px"
      >
        <el-form-item label="新手机号" prop="phone">
          <el-input
            v-model="phoneForm.phone"
            placeholder="请输入新手机号"
          />
        </el-form-item>
        <el-form-item label="验证码" prop="code">
          <div class="verification-code">
            <el-input
              v-model="phoneForm.code"
              placeholder="请输入验证码"
            />
            <el-button
              type="primary"
              :disabled="phoneCodeTimer > 0"
              @click="sendPhoneCode"
            >
              {{ phoneCodeTimer > 0 ? `${phoneCodeTimer}秒后重新获取` : '获取验证码' }}
            </el-button>
          </div>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="phoneDialogVisible = false">取 消</el-button>
        <el-button type="primary" :loading="phoneLoading" @click="handleChangePhone">确 定</el-button>
      </div>
    </el-dialog>

    <!-- 修改邮箱对话框 -->
    <el-dialog title="修改邮箱" :visible.sync="emailDialogVisible" width="500px">
      <el-form
        ref="emailForm"
        :model="emailForm"
        :rules="emailRules"
        label-width="100px"
      >
        <el-form-item label="新邮箱" prop="email">
          <el-input
            v-model="emailForm.email"
            placeholder="请输入新邮箱"
          />
        </el-form-item>
        <el-form-item label="验证码" prop="code">
          <div class="verification-code">
            <el-input
              v-model="emailForm.code"
              placeholder="请输入验证码"
            />
            <el-button
              type="primary"
              :disabled="emailCodeTimer > 0"
              @click="sendEmailCode"
            >
              {{ emailCodeTimer > 0 ? `${emailCodeTimer}秒后重新获取` : '获取验证码' }}
            </el-button>
          </div>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="emailDialogVisible = false">取 消</el-button>
        <el-button type="primary" :loading="emailLoading" @click="handleChangeEmail">确 定</el-button>
      </div>
    </el-dialog>
  </div>
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
    const validatePhone = (rule, value, callback) => {
      const phoneRegex = /^1[3-9]\d{9}$/
      if (!phoneRegex.test(value)) {
        callback(new Error('请输入正确的手机号码'))
      } else {
        callback()
      }
    }
    const validateEmail = (rule, value, callback) => {
      const emailRegex = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
      if (!emailRegex.test(value)) {
        callback(new Error('请输入正确的邮箱格式'))
      } else {
        callback()
      }
    }
    return {
      userInfo: {
        phone: '13812345678',
        email: 'admin@example.com'
      },
      securitySettings: {
        loginVerification: true,
        loginAlert: true,
        ipRestriction: false,
        allowedIps: ''
      },
      loginDevices: [
        {
          id: 1,
          device: 'Chrome 98.0.4758.102 / Windows 10',
          ip: '192.168.1.100',
          location: '广东省广州市',
          time: '2025-03-05 08:30:43',
          status: 'current'
        },
        {
          id: 2,
          device: 'Safari 15.3 / macOS',
          ip: '192.168.1.101',
          location: '广东省深圳市',
          time: '2025-03-04 15:20:00',
          status: 'other'
        },
        {
          id: 3,
          device: 'Firefox 97.0 / Windows 10',
          ip: '192.168.1.102',
          location: '广东省东莞市',
          time: '2025-03-03 09:15:00',
          status: 'other'
        }
      ],
      // 密码修改相关
      passwordDialogVisible: false,
      passwordLoading: false,
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
      },
      // 手机修改相关
      phoneDialogVisible: false,
      phoneLoading: false,
      phoneCodeTimer: 0,
      phoneForm: {
        phone: '',
        code: ''
      },
      phoneRules: {
        phone: [
          { required: true, message: '请输入手机号码', trigger: 'blur' },
          { validator: validatePhone, trigger: 'blur' }
        ],
        code: [
          { required: true, message: '请输入验证码', trigger: 'blur' },
          { len: 6, message: '验证码长度为6位', trigger: 'blur' }
        ]
      },
      // 邮箱修改相关
      emailDialogVisible: false,
      emailLoading: false,
      emailCodeTimer: 0,
      emailForm: {
        email: '',
        code: ''
      },
      emailRules: {
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { validator: validateEmail, trigger: 'blur' }
        ],
        code: [
          { required: true, message: '请输入验证码', trigger: 'blur' },
          { len: 6, message: '验证码长度为6位', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    // 通用方法
    maskPhone(phone) {
      if (!phone) return ''
      return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
    },
    maskEmail(email) {
      if (!email) return ''
      const parts = email.split('@')
      if (parts.length !== 2) return email
      const name = parts[0]
      const domain = parts[1]
      let maskedName = name
      if (name.length > 2) {
        maskedName = name.substr(0, 1) + '****' + name.substr(-1)
      }
      return maskedName + '@' + domain
    },
    
    // 安全设置相关
    handleIpRestrictionChange(val) {
      if (val && !this.securitySettings.allowedIps) {
        this.securitySettings.allowedIps = '192.168.1.100'
      }
    },
    saveSecuritySettings() {
      this.$message({
        message: '安全设置保存成功',
        type: 'success'
      })
    },
    removeDevice(device) {
      this.$confirm('确定要删除该登录设备记录吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.loginDevices.findIndex(item => item.id === device.id)
        if (index !== -1) {
          this.loginDevices.splice(index, 1)
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
        }
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    
    // 密码修改相关
    showPasswordDialog() {
      this.passwordDialogVisible = true
      this.passwordForm = {
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    },
    handleChangePassword() {
      this.$refs.passwordForm.validate(valid => {
        if (valid) {
          this.passwordLoading = true
          // 模拟API请求
          setTimeout(() => {
            this.$message({
              message: '密码修改成功，请重新登录',
              type: 'success'
            })
            this.passwordLoading = false
            this.passwordDialogVisible = false
            // 在实际应用中，这里应该调用API修改密码
            // 然后退出登录
            setTimeout(() => {
              this.$store.dispatch('user/logout').then(() => {
                this.$router.push('/login')
              })
            }, 1500)
          }, 1000)
        }
      })
    },
    
    // 手机修改相关
    showPhoneDialog() {
      this.phoneDialogVisible = true
      this.phoneForm = {
        phone: '',
        code: ''
      }
    },
    sendPhoneCode() {
      this.$refs.phoneForm.validateField('phone', (errorMessage) => {
        if (errorMessage) {
          return
        }
        this.phoneCodeTimer = 60
        const timer = setInterval(() => {
          this.phoneCodeTimer--
          if (this.phoneCodeTimer <= 0) {
            clearInterval(timer)
          }
        }, 1000)
        this.$message({
          message: '验证码已发送至您的手机',
          type: 'success'
        })
      })
    },
    handleChangePhone() {
      this.$refs.phoneForm.validate(valid => {
        if (valid) {
          this.phoneLoading = true
          // 模拟API请求
          setTimeout(() => {
            this.userInfo.phone = this.phoneForm.phone
            this.$message({
              message: '手机号修改成功',
              type: 'success'
            })
            this.phoneLoading = false
            this.phoneDialogVisible = false
          }, 1000)
        }
      })
    },
    
    // 邮箱修改相关
    showEmailDialog() {
      this.emailDialogVisible = true
      this.emailForm = {
        email: '',
        code: ''
      }
    },
    sendEmailCode() {
      this.$refs.emailForm.validateField('email', (errorMessage) => {
        if (errorMessage) {
          return
        }
        this.emailCodeTimer = 60
        const timer = setInterval(() => {
          this.emailCodeTimer--
          if (this.emailCodeTimer <= 0) {
            clearInterval(timer)
          }
        }, 1000)
        this.$message({
          message: '验证码已发送至您的邮箱',
          type: 'success'
        })
      })
    },
    handleChangeEmail() {
      this.$refs.emailForm.validate(valid => {
        if (valid) {
          this.emailLoading = true
          // 模拟API请求
          setTimeout(() => {
            this.userInfo.email = this.emailForm.email
            this.$message({
              message: '邮箱修改成功',
              type: 'success'
            })
            this.emailLoading = false
            this.emailDialogVisible = false
          }, 1000)
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.security-container {
  padding: 20px 0;
}

.security-card {
  margin-bottom: 20px;
}

.security-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-actions {
  text-align: center;
  margin-top: 20px;
}

.verification-code {
  display: flex;
  
  .el-input {
    margin-right: 10px;
  }
  
  .el-button {
    white-space: nowrap;
  }
}
</style> 