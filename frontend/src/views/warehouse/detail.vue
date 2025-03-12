<template>
  <div class="app-container">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>仓库基本信息</span>
        <div style="float: right;">
          <!-- 备份按钮组 -->
          <el-button-group>
            <el-button
              type="primary"
              size="small"
              icon="el-icon-download"
              @click="handleBackupData"
              :loading="backupLoading"
            >
              备份数据
            </el-button>
            <el-upload
              class="upload-backup"
              action="#"
              :show-file-list="false"
              :auto-upload="false"
              :on-change="handleRestoreFile"
              accept=".json"
            >
              <el-button
                type="warning"
                size="small"
                icon="el-icon-upload2"
                :loading="restoreLoading"
              >
                恢复备份
              </el-button>
            </el-upload>
          </el-button-group>
          <!-- 上次备份时间 -->
          <span v-if="lastBackupTime" class="backup-time">
            上次备份: {{ formatBackupTime(lastBackupTime) }}
          </span>
        </div>
      </div>
      <!-- 进度条 -->
      <el-progress 
        v-if="backupProgress > 0 && backupProgress < 100"
        :percentage="backupProgress"
        :format="progressFormat"
        class="backup-progress"
      ></el-progress>
      <div v-loading="loading">
        <el-descriptions :column="2" border v-if="warehouseInfo">
          <el-descriptions-item label="仓库名称">{{ warehouseInfo.name }}</el-descriptions-item>
          <el-descriptions-item label="仓库编码">{{ warehouseInfo.code }}</el-descriptions-item>
          <el-descriptions-item label="联系人">{{ warehouseInfo.contact_person }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ warehouseInfo.contact_phone }}</el-descriptions-item>
          <el-descriptions-item label="地址">{{ warehouseInfo.address }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="warehouseInfo.is_active ? 'success' : 'danger'">
              {{ warehouseInfo.is_active ? '启用' : '禁用' }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>
  </div>
</template>

<script>
import { getWarehouse, exportWarehouseBackup, restoreWarehouseBackup } from '@/api/warehouse'
import { getMonthlyReport } from '@/api/report'

export default {
  name: 'WarehouseDetail',
  data() {
    return {
      loading: false,
      backupLoading: false,
      restoreLoading: false,
      backupProgress: 0,
      lastBackupTime: null,
      warehouseInfo: null,
      selectedMonth: '',
      inboundList: [],
      outboundList: [],
      inventoryList: []
    }
  },
  created() {
    this.fetchWarehouseInfo()
  },
  methods: {
    async fetchWarehouseInfo() {
      try {
        const warehouseId = this.$route.params.id
        if (!warehouseId) {
          this.$message.error('未找到仓库ID')
          return
        }

        this.loading = true
        const response = await getWarehouse(warehouseId)
        if (response?.data) {
          this.warehouseInfo = response.data
        } else {
          this.$message.error('获取仓库信息失败：响应数据为空')
        }
      } catch (error) {
        console.error('获取仓库信息失败:', error)
        this.$message.error('获取仓库信息失败：' + (error.message || '未知错误'))
      } finally {
        this.loading = false
      }
    },
    fetchReportData() {
      this.loading = true
      const params = {
        warehouse_id: this.$route.params.id,
        month: this.selectedMonth,
        format: 'json'
      }
      
      getMonthlyReport(params)
        .then(response => {
          if (response?.data) {
            this.inboundList = response.data.inbound || []
            this.outboundList = response.data.outbound || []
            this.inventoryList = response.data.inventory || []
            
            const total = this.inboundList.length + this.outboundList.length + this.inventoryList.length
            if (total > 0) {
              this.$message.success(`成功加载 ${total} 条记录`)
            } else {
              this.$message.info('当前月份没有任何数据记录')
            }
          }
        })
        .catch(error => {
          console.error('获取报表数据失败:', error)
          this.$message.error('获取报表数据失败：' + (error.message || '未知错误'))
        })
        .finally(() => {
          this.loading = false
        })
    },
    handleBackupData() {
      const warehouseId = this.$route.params.id
      if (!warehouseId) {
        this.$message.error('未找到仓库ID')
        return
      }

      this.backupLoading = true
      this.backupProgress = 10

      // 获取仓库名称用于文件命名
      const warehouseName = this.warehouseInfo?.name || ''
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
      const fileName = `warehouse_${warehouseName}_${warehouseId}_backup_${timestamp}.json`

      exportWarehouseBackup(warehouseId)
        .then(response => {
          this.backupProgress = 50
          // 创建一个Blob对象
          const blob = new Blob([response], { type: 'application/json' })
          
          if (window.navigator.msSaveOrOpenBlob) {
            window.navigator.msSaveBlob(blob, fileName)
          } else {
            const link = document.createElement('a')
            link.href = window.URL.createObjectURL(blob)
            link.download = fileName
            link.style.display = 'none'
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
            window.URL.revokeObjectURL(link.href)
          }
          
          this.lastBackupTime = new Date()
          this.backupProgress = 100
          this.$message.success('备份数据成功')

          // 3秒后隐藏进度条
          setTimeout(() => {
            this.backupProgress = 0
          }, 3000)
        })
        .catch(error => {
          console.error('备份数据失败：', error)
          this.$message.error('备份数据失败：' + (error.message || '未知错误'))
          this.backupProgress = 0
        })
        .finally(() => {
          this.backupLoading = false
        })
    },
    handleRestoreFile(file) {
      if (!file) {
        return
      }

      const warehouseId = this.$route.params.id
      if (!warehouseId) {
        this.$message.error('未找到仓库ID')
        return
      }

      // 确认是否要恢复数据
      this.$confirm('恢复备份数据将覆盖当前数据，是否继续？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.restoreLoading = true
        
        // 读取文件内容
        const reader = new FileReader()
        reader.onload = async (e) => {
          try {
            const data = JSON.parse(e.target.result)
            await restoreWarehouseBackup(warehouseId, data)
            this.$message.success('恢复备份成功')
            // 重新加载仓库信息
            await this.fetchWarehouseInfo()
          } catch (error) {
            console.error('恢复备份失败：', error)
            this.$message.error('恢复备份失败：' + (error.message || '文件格式错误'))
          } finally {
            this.restoreLoading = false
          }
        }
        reader.onerror = () => {
          this.$message.error('读取备份文件失败')
          this.restoreLoading = false
        }
        reader.readAsText(file.raw)
      }).catch(() => {
        // 用户取消操作
      })
    },
    formatBackupTime(time) {
      if (!time) return ''
      const now = new Date()
      const backup = new Date(time)
      const diff = now - backup

      // 如果在1小时内
      if (diff < 3600000) {
        const minutes = Math.floor(diff / 60000)
        return `${minutes}分钟前`
      }
      // 如果在24小时内
      if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000)
        return `${hours}小时前`
      }
      // 其他情况显示具体日期
      return backup.toLocaleString()
    },
    progressFormat(percentage) {
      if (percentage === 100) {
        return '完成'
      }
      return `${percentage}%`
    }
  }
}
</script>

<style>
.app-container {
  padding: 20px;
}
.box-card {
  margin-bottom: 20px;
}
.upload-backup {
  display: inline-block;
}
.backup-time {
  margin-left: 15px;
  font-size: 12px;
  color: #909399;
  vertical-align: middle;
}
.backup-progress {
  margin: 10px 0;
}
.el-button-group {
  margin-right: 10px;
  vertical-align: middle;
}
.el-button-group .el-upload {
  display: inline-block;
}
.el-button-group .el-button {
  margin-left: -1px;
}
</style> 