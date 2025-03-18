<template>
  <div class="app-container">
    <div class="header">
      <el-page-header @back="goBack" :content="'盘点任务：' + checkNo" />
    </div>

    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>盘点信息</span>
      </div>
      <el-descriptions class="margin-top" :column="3" border>
        <el-descriptions-item label="盘点单号">{{ checkInfo.checkNo }}</el-descriptions-item>
        <el-descriptions-item label="盘点类型">{{ checkInfo.checkType }}</el-descriptions-item>
        <el-descriptions-item label="盘点区域">{{ checkInfo.checkArea }}</el-descriptions-item>
        <el-descriptions-item label="负责人">{{ checkInfo.manager }}</el-descriptions-item>
        <el-descriptions-item label="开始时间">{{ checkInfo.startTime }}</el-descriptions-item>
        <el-descriptions-item label="盘点进度">
          <el-progress :percentage="checkInfo.progress"></el-progress>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card class="box-card" style="margin-top: 20px">
      <div slot="header" class="clearfix">
        <span>盘点操作</span>
        <el-radio-group v-model="checkMode" size="small" style="float: right">
          <el-radio-button label="scan">扫码盘点</el-radio-button>
          <el-radio-button label="manual">手动盘点</el-radio-button>
        </el-radio-group>
      </div>

      <!-- 扫码盘点模式 -->
      <div v-if="checkMode === 'scan'" class="scan-mode">
        <el-input
          v-model="scanCode"
          placeholder="请扫描商品条码"
          @keyup.enter.native="handleScan"
          clearable>
          <template slot="prepend">商品条码</template>
        </el-input>
        <div class="scan-tip">
          <i class="el-icon-warning"></i>
          请将扫描枪对准商品条码进行扫描，或手动输入条码后按回车
        </div>
      </div>

      <!-- 手动盘点模式 -->
      <div v-else class="manual-mode">
        <el-form :inline="true" class="demo-form-inline">
          <el-form-item label="商品编码">
            <el-input v-model="manualForm.code" placeholder="请输入商品编码" />
          </el-form-item>
          <el-form-item label="实际数量">
            <el-input-number v-model="manualForm.quantity" :min="0" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleManualSubmit">提交</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 盘点记录表格 -->
      <div class="check-records">
        <el-table
          :data="checkRecords"
          border
          style="width: 100%">
          <el-table-column label="商品编码" prop="code" align="center" />
          <el-table-column label="商品名称" prop="name" align="center" />
          <el-table-column label="规格型号" prop="spec" align="center" />
          <el-table-column label="系统库存" prop="systemQuantity" align="center" />
          <el-table-column label="实际库存" prop="actualQuantity" align="center" />
          <el-table-column label="差异数量" align="center">
            <template slot-scope="{row}">
              <span :class="{ 'text-red': row.diff < 0 }">{{ row.diff }}</span>
            </template>
          </el-table-column>
          <el-table-column label="盘点时间" prop="checkTime" align="center" />
          <el-table-column label="操作" align="center" width="120">
            <template slot-scope="{row}">
              <el-button 
                size="mini" 
                type="danger" 
                @click="handleDelete(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <div class="footer-actions">
      <el-button type="primary" @click="handleFinish">完成盘点</el-button>
      <el-button @click="handleSave">保存</el-button>
    </div>
  </div>
</template>

<script>
import { getInventoryCheckDetail, getCheckItems, submitCheckResult, updateCheckItem } from '@/api/inventory'

export default {
  name: 'InventoryCheckExecute',
  data() {
    return {
      checkNo: this.$route.query.id,
      checkInfo: {
        checkNo: '',
        checkType: '',
        checkArea: '',
        manager: '',
        startTime: '',
        progress: 0
      },
      checkMode: 'manual', // 默认为手动盘点模式
      scanCode: '',
      manualForm: {
        code: '',
        quantity: 1
      },
      checkRecords: [],
      loading: false
    }
  },
  created() {
    this.getCheckInfo()
    this.getCheckRecords()
  },
  methods: {
    goBack() {
      this.$router.push('/warehouse/inventory-check')
    },
    getCheckInfo() {
      this.loading = true
      getInventoryCheckDetail(this.checkNo).then(response => {
        this.checkInfo = response.data
        this.loading = false
      }).catch(error => {
        this.loading = false
        this.$message.error('获取盘点信息失败: ' + (error.message || '未知错误'))
      })
    },
    getCheckRecords() {
      this.loading = true
      getCheckItems(this.checkNo).then(response => {
        this.checkRecords = response.data || []
        this.loading = false
      }).catch(error => {
        this.loading = false
        this.$message.error('获取盘点记录失败: ' + (error.message || '未知错误'))
      })
    },
    handleScan() {
      if (!this.scanCode) {
        this.$message.warning('请输入商品条码')
        return
      }
      
      // 构建盘点数据
      const data = {
        code: this.scanCode,
        actual_quantity: 1
      }
      
      this.submitCheckData(data)
      this.scanCode = ''
    },
    handleManualSubmit() {
      if (!this.manualForm.code) {
        this.$message.warning('请输入商品编码')
        return
      }
      
      if (this.manualForm.quantity <= 0) {
        this.$message.warning('实际数量必须大于0')
        return
      }
      
      // 构建盘点数据
      const data = {
        code: this.manualForm.code,
        actual_quantity: this.manualForm.quantity
      }
      
      this.submitCheckData(data)
      this.manualForm.code = ''
      this.manualForm.quantity = 1
    },
    submitCheckData(data) {
      this.loading = true
      submitCheckResult(this.checkNo, data).then(response => {
        this.$message.success('盘点记录已添加')
        // 刷新数据
        this.getCheckRecords()
        // 更新盘点信息（主要是进度）
        this.getCheckInfo()
        this.loading = false
      }).catch(error => {
        this.loading = false
        this.$message.error('添加盘点记录失败: ' + (error.message || '未知错误'))
      })
    },
    handleDelete(row) {
      this.$confirm('确认删除该盘点记录?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.loading = true
        updateCheckItem(this.checkNo, row.id, { deleted: true }).then(() => {
          this.$message.success('删除成功')
          // 刷新数据
          this.getCheckRecords()
          this.loading = false
        }).catch(error => {
          this.loading = false
          this.$message.error('删除失败: ' + (error.message || '未知错误'))
        })
      }).catch(() => {})
    },
    handleSave() {
      this.$message.success('盘点数据已保存')
    },
    handleFinish() {
      this.$confirm('确认完成盘点?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.loading = true
        // 提交完成状态
        updateCheckItem(this.checkNo, null, { status: '已完成', progress: 100 }).then(() => {
          this.$message.success('盘点已完成')
          this.$router.push('/warehouse/inventory-check')
        }).catch(error => {
          this.loading = false
          this.$message.error('完成盘点失败: ' + (error.message || '未知错误'))
        })
      }).catch(() => {})
    }
  }
}
</script>

<style lang="scss" scoped>
.header {
  margin-bottom: 20px;
}

.scan-mode {
  width: 500px;
  margin: 0 auto;
  .scan-tip {
    margin-top: 10px;
    color: #909399;
    font-size: 14px;
    i {
      margin-right: 5px;
    }
  }
}

.manual-mode {
  margin-bottom: 20px;
}

.check-records {
  margin-top: 20px;
}

.text-red {
  color: #F56C6C;
}

.footer-actions {
  margin-top: 20px;
  text-align: center;
}
</style> 