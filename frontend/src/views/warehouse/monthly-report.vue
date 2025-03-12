<template>
  <div class="app-container">
    <!-- 仓库基本信息 -->
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>仓库基本信息</span>
      </div>
      <el-descriptions :column="2" border>
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
    </el-card>

    <!-- 月度报表 -->
    <el-card class="box-card" style="margin-top: 20px;">
      <div slot="header" class="clearfix">
        <span>月度报表</span>
        <el-date-picker
          v-model="listQuery.month"
          type="month"
          placeholder="选择月份"
          format="yyyy年MM月"
          value-format="yyyy-MM"
          style="float: right; margin-left: 10px;"
          @change="handleMonthChange"
        />
      </div>

      <el-tabs v-model="activeTab">
        <!-- 入库明细 -->
        <el-tab-pane label="入库明细" name="inbound">
          <div class="table-operations">
            <el-button type="primary" size="small" @click="handleAdd('inbound')">新增入库记录</el-button>
          </div>
          <el-table
            v-loading="loading"
            :data="inboundList"
            border
            stripe
            style="width: 100%">
            <el-table-column type="index" label="序号" width="50" align="center" />
            <el-table-column prop="日期" label="日期" width="100" align="center" />
            <el-table-column prop="品项" label="品项" min-width="120" />
            <el-table-column prop="规格/型号" label="规格/型号" width="120" />
            <el-table-column prop="单位" label="单位" width="80" align="center" />
            <el-table-column prop="数量" label="数量" width="100" align="right" />
            <el-table-column prop="单价" label="单价" width="100" align="right" />
            <el-table-column prop="金额" label="金额" width="120" align="right" />
            <el-table-column prop="经手人" label="经手人" width="100" align="center" />
            <el-table-column label="操作" width="150" align="center">
              <template slot-scope="scope">
                <el-button type="text" size="small" @click="handleEdit('inbound', scope.row)">编辑</el-button>
                <el-button type="text" size="small" style="color: #F56C6C" @click="handleDelete('inbound', scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 出库明细 -->
        <el-tab-pane label="出库明细" name="outbound">
          <div class="table-operations">
            <el-button type="primary" size="small" @click="handleAdd('outbound')">新增出库记录</el-button>
          </div>
          <el-table
            v-loading="loading"
            :data="outboundList"
            border
            stripe
            style="width: 100%">
            <el-table-column type="index" label="序号" width="50" align="center" />
            <el-table-column prop="日期" label="日期" width="100" align="center" />
            <el-table-column prop="品项" label="品项" min-width="120" />
            <el-table-column prop="规格/型号" label="规格/型号" width="120" />
            <el-table-column prop="单位" label="单位" width="80" align="center" />
            <el-table-column prop="数量" label="数量" width="100" align="right" />
            <el-table-column prop="单价" label="单价" width="100" align="right" />
            <el-table-column prop="金额" label="金额" width="120" align="right" />
            <el-table-column prop="经手人" label="经手人" width="100" align="center" />
            <el-table-column label="操作" width="150" align="center">
              <template slot-scope="scope">
                <el-button type="text" size="small" @click="handleEdit('outbound', scope.row)">编辑</el-button>
                <el-button type="text" size="small" style="color: #F56C6C" @click="handleDelete('outbound', scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 库存明细 -->
        <el-tab-pane label="库存明细" name="inventory">
          <div class="table-operations">
            <el-button type="primary" size="small" @click="handleAdd('inventory')">新增库存记录</el-button>
          </div>
          <el-table
            v-loading="loading"
            :data="inventoryList"
            border
            stripe
            style="width: 100%">
            <el-table-column type="index" label="序号" width="50" align="center" />
            <el-table-column prop="位置" label="位置" width="100" align="center" />
            <el-table-column prop="品项" label="品项" min-width="120" />
            <el-table-column prop="规格/型号" label="规格/型号" width="120" />
            <el-table-column prop="单位" label="单位" width="80" align="center" />
            <el-table-column prop="期初库存" label="期初库存" width="100" align="right" />
            <el-table-column prop="累计入库" label="累计入库" width="100" align="right" />
            <el-table-column prop="累计出库" label="累计出库" width="100" align="right" />
            <el-table-column prop="库存" label="库存" width="100" align="right">
              <template slot-scope="scope">
                <span :class="{'zero-inventory': Number(scope.row.库存) === 0}">{{ scope.row.库存 }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="单价" label="单价" width="100" align="right" />
            <el-table-column prop="库存金额" label="库存金额" width="120" align="right">
              <template slot-scope="scope">
                <span :class="{'zero-inventory': Number(scope.row.库存金额) === 0}">{{ scope.row.库存金额 }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" align="center">
              <template slot-scope="scope">
                <el-button type="text" size="small" @click="handleEdit('inventory', scope.row)">编辑</el-button>
                <el-button type="text" size="small" style="color: #F56C6C" @click="handleDelete('inventory', scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>

      <!-- 新增/编辑对话框 -->
      <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="600px">
        <el-form ref="form" :model="form" :rules="rules" label-width="100px">
          <!-- 入库/出库表单 -->
          <template v-if="['inbound', 'outbound'].includes(currentType)">
            <el-form-item label="日期" prop="日期">
              <el-date-picker
                v-model="form.日期"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
                value-format="yyyy-MM-dd"
              />
            </el-form-item>
            <el-form-item label="品项" prop="品项">
              <el-input v-model="form.品项" />
            </el-form-item>
            <el-form-item label="规格/型号" prop="规格/型号">
              <el-input v-model="form.规格/型号" />
            </el-form-item>
            <el-form-item label="单位" prop="单位">
              <el-input v-model="form.单位" />
            </el-form-item>
            <el-form-item label="数量" prop="数量">
              <el-input-number v-model="form.数量" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
            <el-form-item label="单价" prop="单价">
              <el-input-number v-model="form.单价" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
            <el-form-item label="金额" prop="金额">
              <el-input-number v-model="form.金额" :min="0" :precision="2" style="width: 100%" disabled />
            </el-form-item>
          </template>

          <!-- 库存表单 -->
          <template v-else>
            <el-form-item label="位置" prop="位置">
              <el-input v-model="form.位置" />
            </el-form-item>
            <el-form-item label="品项" prop="品项">
              <el-input v-model="form.品项" />
            </el-form-item>
            <el-form-item label="规格/型号" prop="规格/型号">
              <el-input v-model="form.规格/型号" />
            </el-form-item>
            <el-form-item label="单位" prop="单位">
              <el-input v-model="form.单位" />
            </el-form-item>
            <el-form-item label="库存" prop="库存">
              <el-input-number v-model="form.库存" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
            <el-form-item label="单价" prop="单价">
              <el-input-number v-model="form.单价" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
            <el-form-item label="库存金额" prop="库存金额">
              <el-input-number v-model="form.库存金额" :min="0" :precision="2" style="width: 100%" disabled />
            </el-form-item>
          </template>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="handleSubmit">确 定</el-button>
        </div>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'
import { getWarehouse, getMonthlyReport } from '@/api/warehouse'
import { createRecord, updateRecord, deleteRecord } from '@/api/report'

export default {
  name: 'MonthlyReport',
  data() {
    return {
      warehouseInfo: {},
      listQuery: {
        warehouse_id: '',
        month: ''
      },
      activeTab: 'inbound',
      inboundList: [],
      outboundList: [],
      inventoryList: [],
      loading: false,
      loadingText: '',
      
      // 对话框相关数据
      dialogVisible: false,
      dialogTitle: '',
      currentType: '',
      isEdit: false,
      editingRecord: null,
      
      // 表单数据
      form: {
        日期: '',
        品项: '',
        '规格/型号': '',
        单位: '',
        数量: 0,
        单价: 0,
        金额: 0,
        位置: '',
        库存: 0,
        库存金额: 0
      },
      rules: {
        日期: [{ required: true, message: '请选择日期', trigger: 'change' }],
        品项: [{ required: true, message: '请输入品项', trigger: 'blur' }],
        单位: [{ required: true, message: '请输入单位', trigger: 'blur' }],
        数量: [{ required: true, message: '请输入数量', trigger: 'blur' }],
        单价: [{ required: true, message: '请输入单价', trigger: 'blur' }],
        位置: [{ required: true, message: '请输入位置', trigger: 'blur' }],
        库存: [{ required: true, message: '请输入库存', trigger: 'blur' }]
      }
    }
  },
  watch: {
    // 监听数量和单价的变化，自动计算金额
    'form.数量'(val) {
      if (val && this.form.单价) {
        this.form.金额 = val * this.form.单价
      }
    },
    'form.单价'(val) {
      if (val && this.form.数量) {
        this.form.金额 = val * this.form.数量
      }
    },
    // 监听库存和单价的变化，自动计算库存金额
    'form.库存'(val) {
      if (val && this.form.单价) {
        this.form.库存金额 = val * this.form.单价
      }
    }
  },
  created() {
    const month = this.$route.query.month
    if (month) {
      this.listQuery.month = month
    } else {
      this.listQuery.month = this.getCurrentMonth()
    }
    this.fetchWarehouseInfo()
  },
  methods: {
    // 获取仓库基本信息
    async fetchWarehouseInfo() {
      try {
        const warehouseId = this.$route.params.id
        if (!warehouseId) {
          this.$message.error('未找到仓库ID')
          return
        }

        console.log('获取仓库信息，ID:', warehouseId)
        const response = await getWarehouse(warehouseId)
        console.log('仓库信息响应:', response)
        
        if (response?.data) {
          console.log('仓库信息:', response.data)
          this.warehouseInfo = response.data
          // 设置仓库ID到查询参数
          this.listQuery.warehouse_id = this.warehouseInfo.id
          // 加载报表数据
          await this.fetchData()
        } else {
          console.error('仓库信息响应数据为空')
          this.$message.error('获取仓库信息失败：响应数据为空')
        }
      } catch (error) {
        console.error('获取仓库信息失败:', error)
        this.$message.error('获取仓库信息失败：' + (error.message || '未知错误'))
      }
    },

    getCurrentMonth() {
      const date = new Date()
      const year = date.getFullYear()
      const month = (date.getMonth() + 1).toString().padStart(2, '0')
      return `${year}-${month}`
    },

    handleMonthChange() {
      this.fetchData()
    },
    
    // 获取报表数据
    async fetchData() {
      if (!this.listQuery.warehouse_id || !this.listQuery.month) {
        console.warn('缺少必要参数:', this.listQuery)
        this.$message.warning('请选择仓库和月份')
        return
      }

      // 重置数据
      this.inboundList = []
      this.outboundList = []
      this.inventoryList = []
      
      this.loading = true
      this.loadingText = '正在获取数据...'

      try {
        const params = {
          warehouse_id: this.listQuery.warehouse_id,
          month: this.listQuery.month,
          format: 'json',
          check_only: false
        }
        console.log('请求月度报表，参数:', params)
        
        const response = await getMonthlyReport(params)
        console.log('月度报表响应:', response)

        if (response?.data) {
          // 检查响应类型
          if (typeof response.data === 'object') {
            console.log('月度报表数据:', response.data)
            this.inboundList = response.data.inbound || []
            this.outboundList = response.data.outbound || []
            this.inventoryList = response.data.inventory || []

            const total = this.inboundList.length + this.outboundList.length + this.inventoryList.length
            if (total > 0) {
              this.$message.success(`成功加载 ${total} 条记录`)
            } else {
              this.$message.info('当前月份没有任何数据记录')
            }
          } else {
            console.error('响应格式错误:', typeof response.data)
            this.$message.error('数据格式错误，请联系管理员')
          }
        } else {
          console.error('月度报表响应数据为空')
          this.$message.error('获取月度报表失败：响应数据为空')
        }
      } catch (error) {
        console.error('获取数据失败:', error)
        let errorMsg = '获取数据失败'
        if (error.response?.data?.error) {
          errorMsg += '：' + error.response.data.error
        } else if (error.message) {
          errorMsg += '：' + error.message
        }
        this.$message.error(errorMsg)
      } finally {
        this.loading = false
        this.loadingText = ''
      }
    },

    // 新增记录
    handleAdd(type) {
      this.isEdit = false
      this.currentType = type
      this.dialogTitle = `新增${type === 'inbound' ? '入库' : type === 'outbound' ? '出库' : '库存'}记录`
      this.form = {
        日期: this.getCurrentMonth() + '-01',
        品项: '',
        '规格/型号': '',
        单位: '',
        数量: 0,
        单价: 0,
        金额: 0
      }
      if (type === 'inventory') {
        this.form = {
          位置: '',
          品项: '',
          '规格/型号': '',
          单位: '',
          库存: 0,
          单价: 0,
          库存金额: 0
        }
      }
      this.dialogVisible = true
    },

    // 编辑记录
    handleEdit(type, row) {
      this.isEdit = true
      this.currentType = type
      this.dialogTitle = `编辑${type === 'inbound' ? '入库' : type === 'outbound' ? '出库' : '库存'}记录`
      this.editingRecord = row
      this.form = { ...row }
      this.dialogVisible = true
    },

    // 删除记录
    handleDelete(type, row) {
      this.$confirm('确认删除该记录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await deleteRecord({
            warehouse_id: this.listQuery.warehouse_id,
            month: this.listQuery.month,
            record_type: type,
            record_id: row.id
          })
          this.$message.success('删除成功')
          this.fetchData()
        } catch (error) {
          this.$message.error('删除失败：' + (error.message || '未知错误'))
        }
      }).catch(() => {})
    },

    // 提交表单
    handleSubmit() {
      this.$refs.form.validate(async valid => {
        if (valid) {
          try {
            const params = {
              warehouse_id: this.listQuery.warehouse_id,
              month: this.listQuery.month,
              record_type: this.currentType,
              record_data: this.form
            }
            
            if (this.isEdit) {
              params.record_id = this.editingRecord.id
              await updateRecord(params)
              this.$message.success('更新成功')
            } else {
              await createRecord(params)
              this.$message.success('创建成功')
            }
            
            this.dialogVisible = false
            this.fetchData()
          } catch (error) {
            this.$message.error((this.isEdit ? '更新' : '创建') + '失败：' + (error.message || '未知错误'))
          }
        }
      })
    },

    // 导出Excel报表
    handleExport() {
      if (!this.listQuery.warehouse_id || !this.listQuery.month) {
        this.$message.warning('请选择仓库和月份')
        return
      }

      const params = {
        warehouse_id: this.listQuery.warehouse_id,
        month: this.listQuery.month,
        format: 'excel'
      }
      
      this.loading = true
      this.loadingText = '正在导出报表...'
      
      getMonthlyReport(params)
        .then(response => {
          // 检查响应类型
          if (response.data instanceof Blob) {
            const blob = new Blob([response.data], {
              type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            })
            const fileName = `${this.warehouseInfo.name}_月度报表_${this.listQuery.month}.xlsx`
            const link = document.createElement('a')
            link.href = window.URL.createObjectURL(blob)
            link.download = fileName
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
            window.URL.revokeObjectURL(link.href)
            this.$message.success('导出成功')
          } else {
            throw new Error('导出失败：响应格式错误')
          }
        })
        .catch(error => {
          console.error('导出报表失败:', error)
          this.$message.error('导出报表失败：' + (error.message || '未知错误'))
        })
        .finally(() => {
          this.loading = false
          this.loadingText = ''
        })
    }
  }
}
</script>

<style>
.app-container {
  padding: 20px;
}
.table-operations {
  margin-bottom: 16px;
}
.el-table .cell {
  white-space: nowrap;
}
</style> 