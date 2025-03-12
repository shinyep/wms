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
export default {
  name: 'InventoryCheckExecute',
  data() {
    return {
      checkNo: this.$route.query.id,
      checkMode: 'scan',
      scanCode: '',
      manualForm: {
        code: '',
        quantity: 0
      },
      checkInfo: {
        checkNo: '',
        checkType: '',
        checkArea: '',
        manager: '',
        startTime: '',
        progress: 0
      },
      checkRecords: []
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
      // 模拟获取盘点信息
      this.checkInfo = {
        checkNo: this.checkNo,
        checkType: '全面盘点',
        checkArea: 'A区-A1货架',
        manager: '张三',
        startTime: '2024-03-09 10:00:00',
        progress: 30
      }
    },
    getCheckRecords() {
      // 模拟获取盘点记录
      this.checkRecords = [
        {
          code: 'SP001',
          name: '测试商品1',
          spec: '规格1',
          systemQuantity: 100,
          actualQuantity: 98,
          diff: -2,
          checkTime: '2024-03-09 10:30:00'
        }
      ]
    },
    handleScan() {
      if (!this.scanCode) {
        this.$message.warning('请输入商品条码')
        return
      }
      // 模拟扫码盘点
      this.checkRecords.unshift({
        code: this.scanCode,
        name: '扫码商品',
        spec: '规格X',
        systemQuantity: 100,
        actualQuantity: 100,
        diff: 0,
        checkTime: new Date().toLocaleString()
      })
      this.scanCode = ''
    },
    handleManualSubmit() {
      if (!this.manualForm.code) {
        this.$message.warning('请输入商品编码')
        return
      }
      // 模拟手动盘点
      this.checkRecords.unshift({
        code: this.manualForm.code,
        name: '手动商品',
        spec: '规格Y',
        systemQuantity: 100,
        actualQuantity: this.manualForm.quantity,
        diff: this.manualForm.quantity - 100,
        checkTime: new Date().toLocaleString()
      })
      this.manualForm.code = ''
      this.manualForm.quantity = 0
    },
    handleDelete(row) {
      const index = this.checkRecords.indexOf(row)
      this.checkRecords.splice(index, 1)
      this.$message.success('删除成功')
    },
    handleSave() {
      // 保存盘点记录
      this.$message.success('保存成功')
    },
    handleFinish() {
      this.$confirm('确认完成此次盘点任务?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 完成盘点任务
        this.$message.success('盘点任务已完成')
        this.$router.push('/warehouse/inventory-check')
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