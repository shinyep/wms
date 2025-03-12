<template>
  <div class="message-list">
    <div v-if="messages.length === 0" class="empty-message">
      <i class="el-icon-message"></i>
      <p>暂无消息</p>
    </div>
    <el-card v-for="message in messages" :key="message.id" class="message-item" shadow="hover">
      <div class="message-header">
        <div class="message-title">
          <el-tag v-if="!message.read" type="danger" size="mini">未读</el-tag>
          <el-tag v-else type="info" size="mini">已读</el-tag>
          <span class="title-text">{{ message.title }}</span>
        </div>
        <div class="message-time">{{ message.time }}</div>
      </div>
      <div class="message-content">{{ message.content }}</div>
      <div class="message-footer">
        <el-tag size="mini" :type="getTagType(message.type)">{{ getTypeName(message.type) }}</el-tag>
        <div class="message-actions">
          <el-button v-if="!message.read" type="text" size="mini" @click="markAsRead(message)">标为已读</el-button>
          <el-button type="text" size="mini" @click="deleteMessage(message)">删除</el-button>
        </div>
      </div>
    </el-card>
    <div class="pagination-container">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="50"
        :page-size="10"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    messages: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    getTagType(type) {
      const typeMap = {
        system: 'primary',
        task: 'success',
        inventory: 'warning',
        security: 'danger'
      }
      return typeMap[type] || 'info'
    },
    getTypeName(type) {
      const typeMap = {
        system: '系统通知',
        task: '任务提醒',
        inventory: '库存预警',
        security: '安全提醒'
      }
      return typeMap[type] || '其他'
    },
    markAsRead(message) {
      this.$set(message, 'read', true)
      this.$message({
        message: '已将消息标记为已读',
        type: 'success'
      })
    },
    deleteMessage(message) {
      this.$confirm('确定要删除这条消息吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.messages.findIndex(item => item.id === message.id)
        if (index !== -1) {
          this.messages.splice(index, 1)
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
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
    }
  }
}
</script>

<style lang="scss" scoped>
.message-list {
  padding: 10px 0;
}

.empty-message {
  text-align: center;
  padding: 40px 0;
  color: #909399;
  
  i {
    font-size: 48px;
    margin-bottom: 10px;
  }
  
  p {
    font-size: 16px;
  }
}

.message-item {
  margin-bottom: 15px;
  
  .message-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    
    .message-title {
      display: flex;
      align-items: center;
      
      .title-text {
        margin-left: 8px;
        font-weight: bold;
      }
    }
    
    .message-time {
      color: #909399;
      font-size: 12px;
    }
  }
  
  .message-content {
    margin-bottom: 10px;
    color: #606266;
    line-height: 1.6;
  }
  
  .message-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .message-actions {
      .el-button {
        padding: 0 5px;
      }
    }
  }
}

.pagination-container {
  text-align: center;
  margin-top: 20px;
}
</style> 