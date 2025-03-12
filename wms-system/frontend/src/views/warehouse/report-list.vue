<template>
  <div class="app-container">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>报表列表</span>
      </div>
      
      <!-- 搜索过滤区域 -->
      <el-form :inline="true" :model="listQuery" class="filter-container">
        <el-form-item label="仓库">
          <el-select v-model="listQuery.warehouse_id" placeholder="选择仓库" clearable style="width: 180px;">
            <el-option v-for="item in warehouseOptions" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="yyyy-MM-dd"
            style="width: 260px;"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="fetchData">搜索</el-button>
          <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 报表列表表格 -->
      <el-table
        v-loading="loading"
        :data="list"
        border
        stripe
        style="width: 100%">
        <el-table-column
          type="index"
          label="序号"
          width="60"
          align="center"
        />
        <el-table-column
          prop="title"
          label="报表标题"
          min-width="200"
          align="center"
        />
        <el-table-column
          prop="warehouse_name"
          label="仓库"
          width="150"
          align="center"
        />
        <el-table-column
          prop="report_date"
          label="报表日期"
          width="120"
          align="center"
        />
        <el-table-column
          prop="creator_name"
          label="创建者"
          width="100"
          align="center"
        />
        <el-table-column
          prop="created_at"
          label="创建时间"
          width="160"
          align="center"
        >
          <template slot-scope="scope">
            {{ scope.row.created_at | formatDate }}
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          width="220"
          align="center"
        >
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="handleView(scope.row)">查看</el-button>
            <el-button size="mini" type="success" @click="handleExport(scope.row)">导出</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <el-pagination
        v-if="total > 0"
        :current-page="listQuery.page"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="listQuery.limit"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        background
        style="margin-top: 20px; text-align: right;"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </el-card>
    
    <!-- 报表详情对话框 -->
    <el-dialog title="报表详情" :visible.sync="dialogVisible" width="90%" top="5vh">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="入库明细" name="inbound">
          <el-table
            v-loading="detailLoading"
            :data="detailData.inbound"
            border
            stripe
            style="width: 100%">
            <el-table-column
              type="index"
              label="序号"
              width="60"
              align="center"
            />
            <el-table-column
              prop="日期"
              label="日期"
              width="120"
              align="center"
            />
            <el-table-column
              prop="品项"
              label="品项"
              min-width="120"
              align="center"
            />
            <el-table-column
              prop="规格/型号"
              label="规格/型号"
              min-width="120"
              align="center"
            />
            <el-table-column
              prop="单位"
              label="单位"
              width="80"
              align="center"
            />
            <el-table-column
              prop="数量"
              label="数量"
              width="80"
              align="center"
            />
            <el-table-column
              prop="单价"
              label="单价"
              width="100"
              align="center"
            >
              <template slot-scope="scope">
                {{ Number(scope.row.单价 || 0).toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column
              prop="金额"
              label="金额"
              width="120"
              align="center"
            >
              <template slot-scope="scope">
                {{ Number(scope.row.金额 || 0).toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column
              prop="经手人"
              label="经手人"
              width="100"
              align="center"
            />
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="出库明细" name="outbound">
          <el-table
            v-loading="detailLoading"
            :data="detailData.outbound"
            border
            stripe
            style="width: 100%">
            <el-table-column
              type="index"
              label="序号"
              width="60"
              align="center"
            />
            <el-table-column
              prop="日期"
              label="日期"
              width="120"
              align="center"
            />
            <el-table-column
              prop="品项"
              label="品项"
              min-width="120"
              align="center"
            />
            <el-table-column
              prop="规格/型号"
              label="规格/型号"
              min-width="120"
              align="center"
            />
            <el-table-column
              prop="单位"
              label="单位"
              width="80"
              align="center"
            />
            <el-table-column
              prop="数量"
              label="数量"
              width="80"
              align="center"
            />
            <el-table-column
              prop="单价"
              label="单价"
              width="100"
              align="center"
            >
              <template slot-scope="scope">
                {{ Number(scope.row.单价 || 0).toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column
              prop="金额"
              label="金额"
              width="120"
              align="center"
            >
              <template slot-scope="scope">
                {{ Number(scope.row.金额 || 0).toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column
              prop="经手人"
              label="经手人"
              width="100"
              align="center"
            />
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="库存明细" name="inventory">
          <el-table
            v-loading="detailLoading"
            :data="detailData.inventory"
            border
            stripe
            style="width: 100%">
            <el-table-column
              type="index"
              label="序号"
              width="60"
              align="center"
            />
            <el-table-column
              prop="位置"
              label="位置"
              min-width="100"
              align="center"
            />
            <el-table-column
              prop="品项"
              label="品项"
              min-width="120"
              align="center"
            />
            <el-table-column
              prop="规格/型号"
              label="规格/型号"
              min-width="120"
              align="center"
            />
            <el-table-column
              prop="单位"
              label="单位"
              width="80"
              align="center"
            />
            <el-table-column
              prop="期初库存"
              label="期初库存"
              width="100"
              align="center"
            />
            <el-table-column
              prop="累计入库"
              label="累计入库"
              width="100"
              align="center"
            />
            <el-table-column
              prop="累计出库"
              label="累计出库"
              width="100"
              align="center"
            />
            <el-table-column
              prop="库存"
              label="库存"
              width="80"
              align="center"
            />
            <el-table-column
              prop="单价"
              label="单价"
              width="100"
              align="center"
            >
              <template slot-scope="scope">
                {{ Number(scope.row.单价 || 0).toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column
              prop="库存金额"
              label="库存金额"
              width="120"
              align="center"
            >
              <template slot-scope="scope">
                {{ Number(scope.row.库存金额 || 0).toFixed(2) }}
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleExportCurrent">导出当前报表</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getReportList, getReportDetail, deleteReport } from '@/api/report'
import { getMonthlyReport } from '@/api/report'
import { getWarehouseList } from '@/api/warehouse'

export default {
  name: 'ReportList',
  filters: {
    formatDate(timestamp) {
      if (!timestamp) return ''
      const date = new Date(timestamp)
      return date.toLocaleString()
    }
  },
  data() {
    return {
      // 列表数据
      list: [],
      total: 0,
      loading: false,
      
      // 查询参数
      listQuery: {
        page: 1,
        limit: 20,
        warehouse_id: undefined
      },
      dateRange: [],
      
      // 选项数据
      warehouseOptions: [],
      
      // 详情数据
      dialogVisible: false,
      detailLoading: false,
      activeTab: 'inbound',
      currentReport: null,
      detailData: {
        inbound: [],
        outbound: [],
        inventory: []
      }
    }
  },
  created() {
    this.fetchOptions()
    this.fetchData()
  },
  methods: {
    // 获取选项数据
    fetchOptions() {
      getWarehouseList({ page_size: 100 }).then(response => {
        this.warehouseOptions = response.data.results || []
      })
    },
    
    // 获取报表列表
    fetchData() {
      this.loading = true
      
      // 构建查询参数
      const params = {
        page: this.listQuery.page,
        page_size: this.listQuery.limit,
        warehouse_id: this.listQuery.warehouse_id
      }
      
      // 添加日期范围过滤
      if (this.dateRange && this.dateRange.length === 2) {
        params.start_date = this.dateRange[0]
        params.end_date = this.dateRange[1]
      }
      
      getReportList(params).then(response => {
        this.list = response.data.results || []
        this.total = response.data.count || 0
      }).catch(error => {
        console.error('获取报表列表失败:', error)
        this.$message.error('获取报表列表失败: ' + (error.message || '未知错误'))
      }).finally(() => {
        this.loading = false
      })
    },
    
    // 重置查询条件
    resetQuery() {
      this.listQuery = {
        page: 1,
        limit: 20,
        warehouse_id: undefined
      }
      this.dateRange = []
      this.fetchData()
    },
    
    // 处理分页大小变化
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.fetchData()
    },
    
    // 处理页码变化
    handleCurrentChange(val) {
      this.listQuery.page = val
      this.fetchData()
    },
    
    // 查看报表详情
    handleView(row) {
      this.currentReport = row
      this.detailLoading = true
      this.dialogVisible = true
      
      getReportDetail(row.id).then(response => {
        const data = response.data
        this.detailData = data.data || { inbound: [], outbound: [], inventory: [] }
      }).catch(error => {
        console.error('获取报表详情失败:', error)
        this.$message.error('获取报表详情失败: ' + (error.message || '未知错误'))
      }).finally(() => {
        this.detailLoading = false
      })
    },
    
    // 导出报表
    handleExport(row) {
      // 从报表日期获取年月
      const date = new Date(row.report_date)
      const year = date.getFullYear()
      const month = date.getMonth() + 1
      
      const params = {
        warehouse_id: row.warehouse,
        month: `${year}-${month.toString().padStart(2, '0')}`,
        format: 'excel'
      }
      
      this.loading = true
      getMonthlyReport(params).then(response => {
        // 直接下载文件
        const blob = new Blob([response], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
        const link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        
        // 组装文件名
        const fileName = `${row.warehouse_name}_月度报表_${year}年${month.toString().padStart(2, '0')}月.xlsx`
        link.download = fileName
        link.click()
        
        this.$message.success('导出成功')
      }).catch(error => {
        console.error('导出报表失败:', error)
        this.$message.error('导出失败: ' + (error.message || '未知错误'))
      }).finally(() => {
        this.loading = false
      })
    },
    
    // 导出当前查看的报表
    handleExportCurrent() {
      if (!this.currentReport) return
      this.handleExport(this.currentReport)
    },
    
    // 删除报表
    handleDelete(row) {
      this.$confirm('此操作将永久删除该报表, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.loading = true
        deleteReport(row.id).then(response => {
          this.$message.success('删除成功')
          this.fetchData() // 重新加载数据
        }).catch(error => {
          console.error('删除报表失败:', error)
          this.$message.error('删除失败: ' + (error.message || '未知错误'))
        }).finally(() => {
          this.loading = false
        })
      }).catch(() => {
        this.$message.info('已取消删除')
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.app-container {
  padding: 20px;
}
.filter-container {
  padding-bottom: 10px;
}
.filter-item {
  margin-bottom: 10px;
}
</style> 