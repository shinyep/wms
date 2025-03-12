<template>
  <div class="notification-container">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="通知设置" name="settings">
        <el-form label-width="120px">
          <el-form-item label="系统通知">
            <el-switch
              v-model="notificationSettings.system"
              active-text="开启"
              inactive-text="关闭"
            />
          </el-form-item>
          <el-form-item label="任务提醒">
            <el-switch
              v-model="notificationSettings.task"
              active-text="开启"
              inactive-text="关闭"
            />
          </el-form-item>
          <el-form-item label="库存预警">
            <el-switch
              v-model="notificationSettings.inventory"
              active-text="开启"
              inactive-text="关闭"
            />
          </el-form-item>
          <el-form-item label="安全提醒">
            <el-switch
              v-model="notificationSettings.security"
              active-text="开启"
              inactive-text="关闭"
            />
          </el-form-item>
          <el-form-item label="接收方式">
            <el-checkbox-group v-model="notificationSettings.methods">
              <el-checkbox label="站内消息">站内消息</el-checkbox>
              <el-checkbox label="邮件">邮件</el-checkbox>
              <el-checkbox label="短信">短信</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="saveNotificationSettings">保存设置</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="消息列表" name="list">
        <div class="notification-list">
          <el-tabs v-model="messageTab" type="card">
            <el-tab-pane label="全部消息" name="all">
              <message-list :messages="allMessages" />
            </el-tab-pane>
            <el-tab-pane label="未读消息" name="unread">
              <message-list :messages="unreadMessages" />
            </el-tab-pane>
            <el-tab-pane label="已读消息" name="read">
              <message-list :messages="readMessages" />
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import MessageList from './MessageList'

export default {
  components: {
    MessageList
  },
  data() {
    return {
      activeTab: 'settings',
      messageTab: 'all',
      notificationSettings: {
        system: true,
        task: true,
        inventory: true,
        security: true,
        methods: ['站内消息', '邮件']
      },
      messages: [
        {
          id: 1,
          title: '系统维护通知',
          content: '系统将于2025年3月10日凌晨2点至4点进行例行维护，请提前做好准备。',
          type: 'system',
          read: false,
          time: '2025-03-05 10:30:00'
        },
        {
          id: 2,
          title: '库存预警',
          content: '商品A123的库存已低于预警值，请及时补充库存。',
          type: 'inventory',
          read: true,
          time: '2025-03-04 15:20:00'
        },
        {
          id: 3,
          title: '任务分配',
          content: '您有一个新的入库任务需要处理，请及时查看。',
          type: 'task',
          read: false,
          time: '2025-03-03 09:15:00'
        },
        {
          id: 4,
          title: '安全提醒',
          content: '您的账号于昨日在非常用设备上登录，请确认是否为本人操作。',
          type: 'security',
          read: true,
          time: '2025-03-02 18:45:00'
        },
        {
          id: 5,
          title: '系统更新通知',
          content: '系统已更新至最新版本，新增多项功能，请查看更新日志了解详情。',
          type: 'system',
          read: false,
          time: '2025-03-01 11:30:00'
        }
      ]
    }
  },
  computed: {
    allMessages() {
      return this.messages
    },
    unreadMessages() {
      return this.messages.filter(msg => !msg.read)
    },
    readMessages() {
      return this.messages.filter(msg => msg.read)
    }
  },
  methods: {
    saveNotificationSettings() {
      this.$message({
        message: '通知设置保存成功',
        type: 'success'
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.notification-container {
  padding: 20px 0;
}

.notification-list {
  margin-top: 20px;
}
</style> 