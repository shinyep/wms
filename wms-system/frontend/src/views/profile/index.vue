<template>
  <div class="app-container">
    <div v-if="user">
      <el-row :gutter="20">
        <el-col :span="6" :xs="24">
          <user-card :user="user" />
          <el-card style="margin-top:20px;">
            <div slot="header" class="clearfix">
              <span>登录信息</span>
            </div>
            <div class="user-login-info">
              <div class="info-item">
                <span class="info-label">上次登录时间：</span>
                <span class="info-value">{{ lastLoginTime }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">上次登录IP：</span>
                <span class="info-value">{{ lastLoginIp }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">登录次数：</span>
                <span class="info-value">{{ loginCount }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="18" :xs="24">
          <el-card>
            <el-tabs v-model="activeTab">
              <el-tab-pane label="个人资料" name="account">
                <account :user="user" />
              </el-tab-pane>
              <el-tab-pane label="修改密码" name="password">
                <password />
              </el-tab-pane>
              <el-tab-pane label="消息通知" name="notification">
                <notification />
              </el-tab-pane>
              <el-tab-pane label="操作日志" name="activity">
                <activity />
              </el-tab-pane>
              <el-tab-pane label="安全设置" name="security">
                <security />
              </el-tab-pane>
            </el-tabs>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import UserCard from './components/UserCard'
import Account from './components/Account'
import Password from './components/Password'
import Notification from './components/Notification'
import Activity from './components/Activity'
import Security from './components/Security'

export default {
  name: 'Profile',
  components: { 
    UserCard, 
    Account, 
    Password,
    Notification,
    Activity,
    Security
  },
  data() {
    return {
      activeTab: 'account',
      // 模拟数据
      lastLoginTime: '2025-03-05 08:30:43',
      lastLoginIp: '192.168.1.100',
      loginCount: 42
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'avatar',
      'roles'
    ]),
    user() {
      return {
        name: this.name,
        avatar: this.avatar,
        roles: this.roles,
        email: 'admin@example.com',
        phone: '138****1234',
        department: '技术部',
        position: '系统管理员'
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.user-login-info {
  .info-item {
    margin-bottom: 10px;
    font-size: 14px;
    
    .info-label {
      color: #606266;
      margin-right: 5px;
    }
    
    .info-value {
      color: #333;
      font-weight: 500;
    }
  }
}
</style> 