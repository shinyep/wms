<template>
  <div class="user-profile">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="基本资料" name="basic">
        <el-form ref="form" :model="userForm" :rules="rules" label-width="100px">
          <el-form-item label="用户名" prop="name">
            <el-input v-model.trim="userForm.name" disabled />
          </el-form-item>
          <el-form-item label="真实姓名" prop="realName">
            <el-input v-model.trim="userForm.realName" placeholder="请输入真实姓名" />
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model.trim="userForm.email" placeholder="请输入邮箱" />
          </el-form-item>
          <el-form-item label="手机号码" prop="phone">
            <el-input v-model.trim="userForm.phone" placeholder="请输入手机号码" />
          </el-form-item>
          <el-form-item label="部门" prop="department">
            <el-input v-model.trim="userForm.department" disabled />
          </el-form-item>
          <el-form-item label="职位" prop="position">
            <el-input v-model.trim="userForm.position" disabled />
          </el-form-item>
          <el-form-item label="角色">
            <el-tag v-for="(role, index) in user.roles" :key="index" style="margin-right: 8px;">
              {{ roleNames[role] || role }}
            </el-tag>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="loading" @click="updateUserInfo">保存修改</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="个人简介" name="introduction">
        <el-form ref="introForm" :model="introForm" label-width="100px">
          <el-form-item label="个人简介">
            <el-input
              v-model.trim="introForm.introduction"
              type="textarea"
              :rows="6"
              placeholder="请输入个人简介"
            />
          </el-form-item>
          <el-form-item label="兴趣爱好">
            <el-select
              v-model="introForm.interests"
              multiple
              filterable
              allow-create
              default-first-option
              placeholder="请选择兴趣爱好"
              style="width: 100%"
            >
              <el-option
                v-for="item in interestOptions"
                :key="item"
                :label="item"
                :value="item"
              />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="introLoading" @click="updateIntroduction">保存简介</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="头像设置" name="avatar">
        <div class="avatar-uploader-container">
          <div class="current-avatar">
            <p>当前头像</p>
            <img :src="user.avatar" class="avatar-img">
          </div>
          <div class="upload-container">
            <p>上传新头像</p>
            <el-upload
              class="avatar-uploader"
              action="#"
              :show-file-list="false"
              :before-upload="beforeAvatarUpload"
              :http-request="handleAvatarUpload"
            >
              <img v-if="imageUrl" :src="imageUrl" class="avatar-img">
              <i v-else class="el-icon-plus avatar-uploader-icon"></i>
            </el-upload>
            <div class="upload-tip">
              <p>支持JPG、PNG格式，文件大小不超过2MB</p>
            </div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      default: () => {
        return {
          name: '',
          avatar: '',
          roles: [],
          email: '',
          phone: '',
          department: '',
          position: ''
        }
      }
    }
  },
  data() {
    const validateEmail = (rule, value, callback) => {
      const emailRegex = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
      if (value && !emailRegex.test(value)) {
        callback(new Error('请输入正确的邮箱格式'))
      } else {
        callback()
      }
    }
    const validatePhone = (rule, value, callback) => {
      const phoneRegex = /^1[3-9]\d{9}$/
      if (value && !phoneRegex.test(value)) {
        callback(new Error('请输入正确的手机号码'))
      } else {
        callback()
      }
    }
    return {
      activeTab: 'basic',
      loading: false,
      introLoading: false,
      imageUrl: '',
      roleNames: {
        admin: '管理员',
        editor: '编辑',
        warehouse: '仓库管理员'
      },
      userForm: {
        name: this.user.name,
        realName: '张三',
        email: this.user.email,
        phone: this.user.phone,
        department: this.user.department,
        position: this.user.position
      },
      rules: {
        realName: [
          { required: true, message: '请输入真实姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { validator: validateEmail, trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入手机号码', trigger: 'blur' },
          { validator: validatePhone, trigger: 'blur' }
        ]
      },
      introForm: {
        introduction: '我是一名系统管理员，负责仓库管理系统的日常维护和管理工作。',
        interests: ['阅读', '旅行', '编程']
      },
      interestOptions: ['阅读', '旅行', '编程', '音乐', '电影', '摄影', '健身', '烹饪', '游戏']
    }
  },
  watch: {
    user: {
      handler(val) {
        this.userForm = {
          name: val.name,
          realName: '张三',
          email: val.email,
          phone: val.phone,
          department: val.department,
          position: val.position
        }
      },
      immediate: true
    }
  },
  methods: {
    updateUserInfo() {
      this.$refs.form.validate(valid => {
        if (valid) {
          this.loading = true
          // 模拟API请求
          setTimeout(() => {
            this.$message({
              message: '个人资料修改成功',
              type: 'success'
            })
            this.loading = false
          }, 1000)
        }
      })
    },
    updateIntroduction() {
      this.introLoading = true
      // 模拟API请求
      setTimeout(() => {
        this.$message({
          message: '个人简介修改成功',
          type: 'success'
        })
        this.introLoading = false
      }, 1000)
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 或 PNG 格式!')
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!')
      }
      return isJPG && isLt2M
    },
    handleAvatarUpload(options) {
      const file = options.file
      // 模拟上传
      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = () => {
        this.imageUrl = reader.result
        // 模拟API请求
        setTimeout(() => {
          this.$message({
            message: '头像上传成功',
            type: 'success'
          })
        }, 1000)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.user-profile {
  padding: 20px 0;
}

.avatar-uploader-container {
  display: flex;
  flex-wrap: wrap;
  
  .current-avatar, .upload-container {
    margin-right: 50px;
    margin-bottom: 20px;
    
    p {
      margin-bottom: 10px;
      font-weight: 500;
    }
  }
}

.avatar-img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: block;
}

.avatar-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 100px;
  height: 100px;
  
  &:hover {
    border-color: #409EFF;
  }
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  line-height: 100px;
  text-align: center;
}

.upload-tip {
  margin-top: 10px;
  color: #606266;
  font-size: 12px;
}
</style> 