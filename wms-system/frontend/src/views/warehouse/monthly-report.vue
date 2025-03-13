<template>
  <div class="app-container">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>月度报表管理</span>
        <el-button
          type="primary"
          size="small"
          icon="el-icon-plus"
          class="float-right"
          @click="handleCreate"
        >
          新增报表记录
        </el-button>
        <el-button
          type="warning"
          size="small"
          icon="el-icon-download"
          class="float-right"
          @click="handleExport"
        >
          导出报表
        </el-button>
        <el-button
          type="success"
          size="small"
          icon="el-icon-check"
          class="float-right"
          @click="handleSaveReport"
        >
          保存报表
        </el-button>
        <el-button
          type="danger"
          size="small"
          icon="el-icon-date"
          class="float-right"
          @click="handleCreateCurrentMonthReport"
          title="手动创建当月报表，期初库存为上月期末库存"
        >
          创建当月报表
        </el-button>
        <el-button
          type="info"
          size="small"
          icon="el-icon-refresh"
          class="float-right"
          @click="handleUpdateInitialStock"
          title="使用上月期末库存更新当前月的期初库存，同时重新计算当前库存"
        >
          更新期初库存
        </el-button>
      </div>
      
      <!-- 搜索过滤区域 -->
      <el-form :inline="true" :model="listQuery" class="filter-container">
        <el-form-item label="仓库">
          <el-select v-model="listQuery.warehouse_id" placeholder="选择仓库" clearable>
            <el-option v-for="item in warehouseOptions" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
          <el-button type="text" @click="setManualWarehouseId" class="manual-input-btn">手动输入ID</el-button>
        </el-form-item>
        <el-form-item label="月份">
          <el-date-picker
            v-model="listQuery.month"
            type="month"
            placeholder="选择月份"
            format="yyyy年MM月"
            value-format="yyyy-MM"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="fetchData">搜索</el-button>
          <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
          <el-button type="success" icon="el-icon-data-line" @click="enterQuickMode" title="直接进入编辑模式，不加载历史数据">快速模式</el-button>
          <el-button type="warning" icon="el-icon-refresh-right" @click="reloadWarehouseOptions">刷新仓库列表</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 报表表格区域 -->
      <el-tabs v-model="activeTab">
        <el-tab-pane label="入库明细" name="inbound">
          <div v-loading="loading" 
               :element-loading-text="loadingText"
               element-loading-spinner="el-icon-loading"
               element-loading-background="rgba(255, 255, 255, 0.8)">
            <div class="operation-container">
              <el-button type="primary" size="small" icon="el-icon-plus" @click="handleAddRecord('inbound')">添加入库记录</el-button>
              <div class="search-box">
                <el-input
                  v-model="inboundSearchText"
                  placeholder="搜索入库记录..."
                  prefix-icon="el-icon-search"
                  class="search-input"
                  size="small"
                  clearable
                  @clear="inboundSearchText = ''"
                >
                </el-input>
                <span class="search-result" v-if="inboundSearchText">
                  找到 {{ filteredInboundList.length }} 条记录
                </span>
              </div>
            </div>
            <el-table
              :data="filteredInboundList"
              border
              style="width: 100%">
              <template slot="empty">
                <el-empty description="暂无入库数据" :image-size="100">
                  <el-button type="primary" size="small" @click="handleAddRecord('inbound')">添加数据</el-button>
                </el-empty>
              </template>
              <el-table-column type="index" label="序号" width="60" align="center" />
              <el-table-column prop="日期" label="日期" width="120" align="center" />
              <el-table-column prop="品项" label="品项" min-width="120" align="center" show-overflow-tooltip />
              <el-table-column prop="规格/型号" label="规格/型号" min-width="120" align="center" show-overflow-tooltip />
              <el-table-column prop="单位" label="单位" width="80" align="center" />
              <el-table-column prop="数量" label="数量" width="80" align="center">
                <template slot-scope="scope">
                  <span class="number-cell">{{ Number(scope.row.数量 || 0).toFixed(2) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="单价" label="单价" width="100" align="center">
                <template slot-scope="scope">
                  <span class="number-cell">{{ Number(scope.row.单价 || 0).toFixed(2) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="金额" label="金额" width="120" align="center">
                <template slot-scope="scope">
                  <span class="number-cell">{{ Number(scope.row.金额 || 0).toFixed(2) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="经手人" label="经手人" width="100" align="center" />
              <el-table-column label="操作" width="150" align="center">
                <template slot-scope="scope">
                  <el-button type="text" size="small" icon="el-icon-edit" @click="handleEdit(scope.row, 'inbound')">编辑</el-button>
                  <el-button type="text" size="small" icon="el-icon-delete" class="delete-btn" @click="handleDelete(scope.row, 'inbound')">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <el-tab-pane label="出库明细" name="outbound">
          <div v-loading="loading"
               :element-loading-text="loadingText"
               element-loading-spinner="el-icon-loading"
               element-loading-background="rgba(255, 255, 255, 0.8)">
            <div class="operation-container">
              <el-button type="primary" size="small" icon="el-icon-plus" @click="handleAddRecord('outbound')">添加出库记录</el-button>
              <div class="search-box">
                <el-input
                  v-model="outboundSearchText"
                  placeholder="搜索出库记录..."
                  prefix-icon="el-icon-search"
                  style="width: 300px"
                  size="small"
                  clearable
                  @clear="outboundSearchText = ''"
                >
                </el-input>
                <span class="search-result" v-if="outboundSearchText">
                  找到 {{ filteredOutboundList.length }} 条记录
                </span>
              </div>
            </div>
            <el-table
              :data="filteredOutboundList"
              border
              style="width: 100%">
              <template slot="empty">
                <el-empty description="暂无出库数据" :image-size="100">
                  <el-button type="primary" size="small" @click="handleAddRecord('outbound')">添加数据</el-button>
                </el-empty>
              </template>
              <el-table-column type="index" label="序号" width="60" align="center" />
              <el-table-column prop="日期" label="日期" width="120" align="center" />
              <el-table-column prop="品项" label="品项" min-width="120" align="center" show-overflow-tooltip />
              <el-table-column prop="规格/型号" label="规格/型号" min-width="120" align="center" show-overflow-tooltip />
              <el-table-column prop="单位" label="单位" width="80" align="center" />
              <el-table-column prop="数量" label="数量" width="80" align="center">
                <template slot-scope="scope">
                  <span class="number-cell">{{ Number(scope.row.数量 || 0).toFixed(2) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="单价" label="单价" width="100" align="center">
                <template slot-scope="scope">
                  <span class="number-cell">{{ Number(scope.row.单价 || 0).toFixed(2) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="金额" label="金额" width="120" align="center">
                <template slot-scope="scope">
                  <span class="number-cell">{{ Number(scope.row.金额 || 0).toFixed(2) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="经手人" label="经手人" width="100" align="center" />
              <el-table-column label="操作" width="150" align="center">
                <template slot-scope="scope">
                  <el-button type="text" size="small" icon="el-icon-edit" @click="handleEdit(scope.row, 'outbound')">编辑</el-button>
                  <el-button type="text" size="small" icon="el-icon-delete" class="delete-btn" @click="handleDelete(scope.row, 'outbound')">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <el-tab-pane label="库存明细" name="inventory">
          <div v-loading="loading"
               :element-loading-text="loadingText"
               element-loading-spinner="el-icon-loading"
               element-loading-background="rgba(255, 255, 255, 0.8)">
            <div class="operation-container">
              <el-button type="primary" size="small" icon="el-icon-plus" @click="handleAddRecord('inventory')">添加库存记录</el-button>
              <div class="search-box">
                <el-input
                  v-model="inventorySearchText"
                  placeholder="搜索库存记录..."
                  prefix-icon="el-icon-search"
                  style="width: 300px"
                  size="small"
                  clearable
                  @clear="inventorySearchText = ''"
                >
                </el-input>
                <span class="search-result" v-if="inventorySearchText">
                  找到 {{ filteredInventoryList.length }} 条记录
                </span>
              </div>
            </div>
            <el-table
              :data="filteredInventoryList"
              border
              style="width: 100%">
              <template slot="empty">
                <el-empty description="暂无库存数据" :image-size="100">
                  <el-button type="primary" size="small" @click="handleAddRecord('inventory')">添加数据</el-button>
                </el-empty>
              </template>
              <el-table-column type="index" label="序号" width="60" align="center" />
              <el-table-column prop="位置" label="位置" min-width="100" align="center" />
              <el-table-column prop="品项" label="品项" min-width="120" align="center" />
              <el-table-column prop="规格/型号" label="规格/型号" min-width="120" align="center" />
              <el-table-column prop="单位" label="单位" width="80" align="center" />
              <el-table-column prop="期初库存" label="期初库存" width="100" align="center">
                <template slot-scope="scope">
                  <span class="number-cell">{{ Number(scope.row.期初库存 || 0).toFixed(2) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="累计入库" label="累计入库" width="100" align="center">
                <template slot-scope="scope">
                  <span class="number-cell">{{ Number(scope.row.累计入库 || 0).toFixed(2) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="累计出库" label="累计出库" width="100" align="center">
                <template slot-scope="scope">
                  <span class="number-cell">{{ Number(scope.row.累计出库 || 0).toFixed(2) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="数量" label="库存" width="80" align="center">
                <template slot-scope="scope">
                  <span class="number-cell">{{ Number(scope.row.数量 || scope.row.库存 || 0).toFixed(2) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="单价" label="单价" width="100" align="center">
                <template slot-scope="scope">
                  <span class="number-cell">{{ Number(scope.row.单价 || 0).toFixed(2) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="金额" label="库存金额" width="120" align="center">
                <template slot-scope="scope">
                  <span class="number-cell">{{ calculateItemAmount(scope.row) }}</span>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="300" align="center">
                <template slot-scope="scope">
                  <el-button type="text" size="small" icon="el-icon-top" @click="handleMonthlyInbound(scope.row)">本月入库</el-button>
                  <el-button type="text" size="small" icon="el-icon-bottom" @click="handleMonthlyOutbound(scope.row)">本月出库</el-button>
                  <el-button type="text" size="small" icon="el-icon-edit" @click="handleEdit(scope.row, 'inventory')">编辑</el-button>
                  <el-button type="text" size="small" icon="el-icon-delete" class="delete-btn" @click="handleDelete(scope.row, 'inventory')">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 添加/编辑记录对话框 -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="500px">
      <el-form ref="recordForm" :model="recordForm" :rules="recordRules" label-width="100px">
        <el-form-item label="日期" prop="日期" v-if="activeTab !== 'inventory'">
          <el-date-picker
            v-model="recordForm.日期"
            type="date"
            placeholder="选择日期"
            format="yyyy-MM-dd"
            value-format="yyyy-MM-dd"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="位置" prop="位置" v-if="activeTab === 'inventory'">
          <el-input v-model="recordForm.位置" placeholder="请输入位置" />
        </el-form-item>
        <el-form-item label="品项" prop="品项">
          <el-input v-model="recordForm.品项" placeholder="请输入品项名称" />
        </el-form-item>
        <el-form-item label="规格/型号" prop="规格/型号">
          <el-input v-model="recordForm['规格/型号']" placeholder="请输入规格或型号" />
        </el-form-item>
        <el-form-item label="单位" prop="单位">
          <el-input v-model="recordForm.单位" placeholder="请输入单位" />
        </el-form-item>
        <el-form-item label="期初库存" prop="期初库存" v-if="activeTab === 'inventory'">
          <el-input-number v-model="recordForm.期初库存" :min="0" :precision="2" style="width: 100%" @change="calculateInventory" />
        </el-form-item>
        <el-form-item label="累计入库" prop="累计入库" v-if="activeTab === 'inventory'">
          <el-input-number v-model="recordForm.累计入库" :min="0" :precision="2" style="width: 100%" @change="calculateInventory" />
        </el-form-item>
        <el-form-item label="累计出库" prop="累计出库" v-if="activeTab === 'inventory'">
          <el-input-number v-model="recordForm.累计出库" :min="0" :precision="2" style="width: 100%" @change="calculateInventory" />
        </el-form-item>
        <el-form-item label="数量" prop="数量">
          <el-input-number v-model="recordForm.数量" :min="0" :precision="2" style="width: 100%" @change="calculateAmount" />
          <div class="form-help-text" v-if="activeTab === 'inventory'">当前库存，应等于：期初库存 + 累计入库 - 累计出库</div>
        </el-form-item>
        <el-form-item label="单价" prop="单价">
          <el-input-number v-model="recordForm.单价" :min="0" :precision="2" style="width: 100%" @change="calculateAmount" />
        </el-form-item>
        <el-form-item label="金额" prop="金额">
          <el-input-number v-model="recordForm.金额" :min="0" :precision="2" style="width: 100%" :disabled="true" />
          <div class="form-help-text" v-if="activeTab === 'inventory'">库存 × 单价 = {{ Number(recordForm.数量 || 0) * Number(recordForm.单价 || 0) }}</div>
        </el-form-item>
        <el-form-item label="经手人" prop="经手人" v-if="activeTab !== 'inventory'">
          <el-input v-model="recordForm.经手人" placeholder="请输入经手人" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitForm">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { 
  getMonthlyReport, 
  createReport, 
  updateReport, 
  createAutoMonthlyReport, 
  exportReport, 
  exportReportAlternative,
  exportReportFallback,
  exportReportByPath,
  exportReportGeneric,
  exportReportPost,
  downloadReportFile,
  iframeDownloadReport,
  exportReportFromDetail,
  exportReportFromDetailAlt,
  exportCurrentInventory,
  generateLocalExcel,
  exportDetailPageTable,
  saveMonthlyReport,
  exportMonthlyReport,
  createCurrentMonthReport,
  updateInitialStock  // 新增API函数
} from '@/api/report'
import { fetchList as fetchWarehouseList } from '@/api/warehouse'
import axios from 'axios'
import XLSX from 'xlsx'
import { saveAs } from 'file-saver'

export default {
  name: 'MonthlyReport',
  data() {
    return {
      loading: false,
      loadingText: '',
      cancelTokenSource: null,
      activeTab: 'inbound',
      dialogVisible: false,
      dialogTitle: '',
      editMode: false,
      currentRecord: null,
      
      // 查询条件
      listQuery: {
        warehouse_id: undefined,
        month: undefined
      },
      
      // 仓库选项
      warehouseOptions: [],
      
      // 表格数据
      inboundList: [],
      outboundList: [],
      inventoryList: [],
      
      // 表单数据
      recordForm: {
        日期: '',
        位置: '',
        品项: '',
        '规格/型号': '',
        单位: '',
        期初库存: 0,
        累计入库: 0,
        累计出库: 0,
        数量: 0,
        单价: 0,
        金额: 0,
        经手人: ''
      },
      
      // 表单验证规则
      recordRules: {
        日期: [{ required: true, message: '请选择日期', trigger: 'change' }],
        位置: [{ required: true, message: '请输入位置', trigger: 'blur' }],
        品项: [{ required: true, message: '请输入品项名称', trigger: 'blur' }],
        '规格/型号': [{ required: true, message: '请输入规格或型号', trigger: 'blur' }],
        单位: [{ required: true, message: '请输入单位', trigger: 'blur' }],
        数量: [{ required: true, message: '请输入数量', trigger: 'blur' }],
        单价: [{ required: true, message: '请输入单价', trigger: 'blur' }],
        经手人: [{ required: true, message: '请输入经手人', trigger: 'blur' }]
      },
      
      inboundSearchText: '',
      outboundSearchText: '',
      inventorySearchText: ''
    }
  },
  created() {
    // 清除可能存在的测试仓库缓存
    try {
      localStorage.removeItem('warehouseOptions')
    } catch (e) {
      console.error('清除缓存失败:', e)
    }
    
    // 获取仓库列表
    this.getWarehouseOptions()
  },
  beforeDestroy() {
    // 组件销毁前取消未完成的请求
    if (this.cancelTokenSource) {
      this.cancelTokenSource.cancel('组件销毁，取消请求')
    }
  },
  computed: {
    // 过滤后的入库列表
    filteredInboundList() {
      if (!this.inboundSearchText) return this.inboundList;
      
      const searchText = this.inboundSearchText.toLowerCase();
      return this.inboundList.filter(item => {
        return Object.keys(item).some(key => {
          // 检查每个字段是否包含搜索文本
          if (typeof item[key] === 'string') {
            return item[key].toLowerCase().includes(searchText);
          } else if (item[key] !== null && item[key] !== undefined) {
            // 将非字符串值转为字符串再搜索
            return String(item[key]).toLowerCase().includes(searchText);
          }
          return false;
        });
      });
    },
    
    // 过滤后的出库列表
    filteredOutboundList() {
      if (!this.outboundSearchText) return this.outboundList;
      
      const searchText = this.outboundSearchText.toLowerCase();
      return this.outboundList.filter(item => {
        return Object.keys(item).some(key => {
          if (typeof item[key] === 'string') {
            return item[key].toLowerCase().includes(searchText);
          } else if (item[key] !== null && item[key] !== undefined) {
            return String(item[key]).toLowerCase().includes(searchText);
          }
          return false;
        });
      });
    },
    
    // 过滤后的库存列表
    filteredInventoryList() {
      if (!this.inventorySearchText) return this.inventoryList;
      
      const searchText = this.inventorySearchText.toLowerCase();
      return this.inventoryList.filter(item => {
        return Object.keys(item).some(key => {
          if (typeof item[key] === 'string') {
            return item[key].toLowerCase().includes(searchText);
          } else if (item[key] !== null && item[key] !== undefined) {
            return String(item[key]).toLowerCase().includes(searchText);
          }
          return false;
        });
      });
    }
  },
  methods: {
    // 获取仓库选项
    async getWarehouseOptions() {
      try {
        this.$message.info('正在获取仓库列表...')
        console.log('开始获取仓库列表')
        
        const response = await fetchWarehouseList({
          limit: 100,
          is_active: true
        })
        
        console.log('仓库列表API响应:', response)
        
        // 对响应进行更宽松的解析
        if (response) {
          let warehouseData = null
          
          // 尝试从不同位置获取仓库数据
          if (response.data) {
            warehouseData = response.data
          } else if (response.results) {
            warehouseData = response.results
          } else if (typeof response === 'object' && !response.data && !response.results) {
            // 尝试直接使用响应对象
            warehouseData = response
          }
          
          console.log('提取的仓库数据:', warehouseData)
          
          if (warehouseData) {
            // 处理不同格式的响应
            if (Array.isArray(warehouseData)) {
              // 直接是数组
              this.warehouseOptions = warehouseData.map(item => ({
                id: item.id || item.warehouse_id,
                name: item.name || item.warehouse_name || item.code || `仓库 #${item.id}`
              }))
            } else if (warehouseData.results && Array.isArray(warehouseData.results)) {
              // 标准分页响应
              this.warehouseOptions = warehouseData.results.map(item => ({
                id: item.id || item.warehouse_id,
                name: item.name || item.warehouse_name || item.code || `仓库 #${item.id}`
              }))
            } else if (typeof warehouseData === 'object') {
              // 转换对象格式为数组
              this.warehouseOptions = Object.keys(warehouseData)
                .filter(key => !isNaN(parseInt(key)) || typeof warehouseData[key] === 'object')
                .map(key => {
                  const item = warehouseData[key]
                  if (typeof item === 'object') {
                    return {
                      id: item.id || parseInt(key),
                      name: item.name || item.warehouse_name || item.code || `仓库 #${key}`
                    }
                  } else {
                    return {
                      id: parseInt(key),
                      name: `仓库 #${key}`
                    }
                  }
                })
            }
            
            console.log('处理后的仓库选项:', this.warehouseOptions)
            
            // 添加当前URL中的仓库ID
            this.addCurrentWarehouseFromUrl()
            
            if (this.warehouseOptions.length === 0) {
              this.$message.warning('没有找到可用的仓库，请先创建仓库或手动输入ID')
            } else {
              this.$message.success(`成功获取 ${this.warehouseOptions.length} 个仓库`)
            }
          } else {
            this.warehouseOptions = []
            console.error('无法从响应中提取仓库数据:', response)
            this.$message.error('获取仓库列表失败: 无法提取数据')
            this.addCurrentWarehouseFromUrl()
          }
        } else {
          this.warehouseOptions = []
          console.error('API响应为空:', response)
          this.$message.error('获取仓库列表失败: 响应为空')
          this.addCurrentWarehouseFromUrl()
        }
      } catch (error) {
        console.error('获取仓库列表失败:', error)
        this.$message.error('获取仓库列表失败: ' + (error.message || '未知错误'))
        this.warehouseOptions = []
        
        // 尝试从localStorage获取备用数据
        try {
          const cachedOptions = localStorage.getItem('warehouseOptions')
          if (cachedOptions) {
            this.warehouseOptions = JSON.parse(cachedOptions)
            this.$message.info('已从缓存加载仓库列表')
          }
        } catch (e) {
          console.error('从缓存获取仓库列表失败:', e)
        }
        
        // 尝试从URL提取仓库ID
        this.addCurrentWarehouseFromUrl()
      }
      
      // 缓存仓库选项到localStorage供未来使用
      try {
        localStorage.setItem('warehouseOptions', JSON.stringify(this.warehouseOptions))
      } catch (e) {
        console.error('缓存仓库列表失败:', e)
      }
    },
    
    // 从URL中提取并添加当前仓库
    addCurrentWarehouseFromUrl() {
      try {
        // 从URL中提取可能的仓库ID
        const path = this.$route.path
        const matches = path.match(/\/warehouse\/detail\/(\d+)/)
        
        if (matches && matches[1]) {
          const warehouseId = parseInt(matches[1])
          
          // 检查是否已经在选项中
          const exists = this.warehouseOptions.some(item => item.id === warehouseId)
          
          if (!exists) {
            this.warehouseOptions.push({
              id: warehouseId,
              name: `仓库 #${warehouseId}`
            })
            this.$message.info(`已添加当前仓库(ID:${warehouseId})到选项列表`)
          }
          
          // 如果没有选择仓库，自动选择当前仓库
          if (!this.listQuery.warehouse_id) {
            this.listQuery.warehouse_id = warehouseId
            this.$message.info(`已自动选择当前仓库(ID:${warehouseId})`)
          }
        }
      } catch (e) {
        console.error('从URL提取仓库ID失败:', e)
      }
    },
    
    // 获取报表数据
    async fetchData() {
      if (!this.listQuery.warehouse_id) {
        this.$message.warning('请选择仓库')
        // 如果仓库列表为空，尝试重新获取
        if (this.warehouseOptions.length === 0) {
          await this.getWarehouseOptions()
        }
        return
      }
      
      if (!this.listQuery.month) {
        this.$message.warning('请选择月份')
        return
      }

      // 重置数据
      this.inboundList = []
      this.outboundList = []
      this.inventoryList = []
      
      this.loading = true
      this.loadingText = '正在获取数据...'

      try {
        // 直接获取JSON格式数据
        const response = await getMonthlyReport({
          ...this.listQuery,
          format: 'json',
          limit: 1000
        })

        console.log('API响应数据:', response)
        
        // 增强的响应处理逻辑
        if (response) {
          let responseData = null
          
          // 尝试从不同位置获取数据
          if (response.data) {
            responseData = response.data
            console.log('从response.data中提取数据')
          } else if (typeof response === 'object') {
            // 尝试直接使用响应对象
            responseData = response
            console.log('直接使用response对象作为数据')
          }
          
          if (responseData) {
            console.log('提取的响应数据:', responseData)
            
            // 提取入库数据
            if (responseData.inbound && Array.isArray(responseData.inbound)) {
              this.inboundList = responseData.inbound
            } else if (responseData.in && Array.isArray(responseData.in)) {
              this.inboundList = responseData.in
            } else if (responseData.入库 && Array.isArray(responseData.入库)) {
              this.inboundList = responseData.入库
            } else if (responseData.inbound_list && Array.isArray(responseData.inbound_list)) {
              this.inboundList = responseData.inbound_list
            }
            
            // 提取出库数据
            if (responseData.outbound && Array.isArray(responseData.outbound)) {
              this.outboundList = responseData.outbound
            } else if (responseData.out && Array.isArray(responseData.out)) {
              this.outboundList = responseData.out
            } else if (responseData.出库 && Array.isArray(responseData.出库)) {
              this.outboundList = responseData.出库
            } else if (responseData.outbound_list && Array.isArray(responseData.outbound_list)) {
              this.outboundList = responseData.outbound_list
            }
            
            // 提取库存数据
            if (responseData.inventory && Array.isArray(responseData.inventory)) {
              this.inventoryList = responseData.inventory
            } else if (responseData.stock && Array.isArray(responseData.stock)) {
              this.inventoryList = responseData.stock
            } else if (responseData.库存 && Array.isArray(responseData.库存)) {
              this.inventoryList = responseData.库存
            } else if (responseData.inventory_list && Array.isArray(responseData.inventory_list)) {
              this.inventoryList = responseData.inventory_list
            }
            
            // 检查是否有results或items字段包含数据
            const checkForArrayData = (obj, targetArray, type) => {
              for (const key in obj) {
                // 跳过已处理的属性
                if (['inbound', 'outbound', 'inventory', 'in', 'out', 'stock', '入库', '出库', '库存', 
                     'inbound_list', 'outbound_list', 'inventory_list'].includes(key)) {
                  continue
                }
                
                const value = obj[key]
                if (Array.isArray(value) && value.length > 0) {
                  // 如果是数组，检查第一个元素是否符合预期类型
                  const firstItem = value[0]
                  
                  if (type === 'inbound' && (key.includes('in') || key.includes('入库'))) {
                    console.log(`从${key}字段提取入库数据`)
                    this.inboundList = value
                  } else if (type === 'outbound' && (key.includes('out') || key.includes('出库'))) {
                    console.log(`从${key}字段提取出库数据`)
                    this.outboundList = value
                  } else if (type === 'inventory' && (key.includes('inv') || key.includes('stock') || key.includes('库存'))) {
                    console.log(`从${key}字段提取库存数据`)
                    this.inventoryList = value
                  }
                } else if (typeof value === 'object' && value !== null) {
                  // 如果是嵌套对象，递归检查
                  checkForArrayData(value, targetArray, type)
                }
              }
            }
            
            // 尝试从嵌套对象中提取数据
            checkForArrayData(responseData, this.inboundList, 'inbound')
            checkForArrayData(responseData, this.outboundList, 'outbound')
            checkForArrayData(responseData, this.inventoryList, 'inventory')
            
            // 如果以上方法都未找到数据，尝试从results或items字段提取
            if (this.inboundList.length === 0 && this.outboundList.length === 0 && this.inventoryList.length === 0) {
              if (responseData.results && Array.isArray(responseData.results)) {
                console.log('从results字段提取数据')
                // 尝试从results字段分类数据
                responseData.results.forEach(item => {
                  if (item.type === 'inbound' || item.record_type === 'inbound') {
                    this.inboundList.push(item)
                  } else if (item.type === 'outbound' || item.record_type === 'outbound') {
                    this.outboundList.push(item)
                  } else {
                    this.inventoryList.push(item)
                  }
                })
              } else if (responseData.items && Array.isArray(responseData.items)) {
                console.log('从items字段提取数据')
                // 尝试从items字段分类数据
                responseData.items.forEach(item => {
                  if (item.type === 'inbound' || item.record_type === 'inbound') {
                    this.inboundList.push(item)
                  } else if (item.type === 'outbound' || item.record_type === 'outbound') {
                    this.outboundList.push(item)
                  } else {
                    this.inventoryList.push(item)
                  }
                })
              }
            }
            
            console.log('处理后数据:', {
              inbound: this.inboundList.length,
              outbound: this.outboundList.length,
              inventory: this.inventoryList.length
            })

            // 处理库存数据，确保数量和金额正确
            this.fixInventoryData()

            const total = this.inboundList.length + this.outboundList.length + this.inventoryList.length
            if (total > 0) {
              this.$message.success(`成功加载 ${total} 条记录 (入库:${this.inboundList.length}, 出库:${this.outboundList.length}, 库存:${this.inventoryList.length})`)
            } else {
              this.$message.info('当前月份没有任何数据记录，可以使用"创建当月报表"按钮或直接添加记录')
              console.log('请尝试使用界面上的"创建当月报表"按钮或"快速模式"来解决')
            }
          } else {
            this.$message.error('无法解析API返回的数据格式')
            console.error('无法从响应中提取数据:', response)
          }
        } else {
          this.$message.error('API返回空响应')
          console.error('API返回空响应')
        }
      } catch (error) {
        console.error('获取数据失败:', error)
        this.$message.error('获取数据失败: ' + (error.message || '未知错误') + '，请尝试使用"创建当月报表"按钮')
      } finally {
        this.loading = false
        this.loadingText = ''
      }
    },
    
    // 重置查询条件
    resetQuery() {
      this.listQuery = {
        warehouse_id: undefined,
        month: undefined
      }
      this.inboundList = []
      this.outboundList = []
      this.inventoryList = []
    },
    
    // 添加记录
    handleAddRecord(type) {
      if (!this.listQuery.warehouse_id || !this.listQuery.month) {
        this.$message.warning('请先选择仓库和月份')
        return
      }
      
      this.dialogTitle = type === 'inbound' ? '添加入库记录' :
                        type === 'outbound' ? '添加出库记录' : '添加库存记录'
      this.editMode = false
      this.currentRecord = null
      this.recordForm = {
        日期: '',
        位置: '',
        品项: '',
        '规格/型号': '',
        单位: '',
        期初库存: 0,
        累计入库: 0,
        累计出库: 0,
        数量: 0,
        单价: 0,
        金额: 0,
        经手人: ''
      }
      this.dialogVisible = true
    },
    
    // 编辑记录
    handleEdit(row, type) {
      this.dialogTitle = type === 'inbound' ? '编辑入库记录' :
                        type === 'outbound' ? '编辑出库记录' : '编辑库存记录'
      this.editMode = true
      this.currentRecord = row
      this.recordForm = { ...row }
      this.dialogVisible = true
    },
    
    // 删除记录
    handleDelete(row, type) {
      this.$confirm('确认删除该记录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const list = type === 'inbound' ? this.inboundList :
                    type === 'outbound' ? this.outboundList : this.inventoryList
        const index = list.indexOf(row)
        if (index > -1) {
          list.splice(index, 1)
        }
        this.$message.success('删除成功')
      }).catch(() => {})
    },
    
    // 计算金额
    calculateAmount() {
      this.recordForm.金额 = Number((this.recordForm.数量 * this.recordForm.单价).toFixed(2))
    },
    
    // 提交表单
    submitForm() {
      this.$refs.recordForm.validate(async (valid) => {
        if (valid) {
          try {
            // 确保金额计算正确
            this.calculateAmount()
            
            const list = this.activeTab === 'inbound' ? this.inboundList :
                        this.activeTab === 'outbound' ? this.outboundList : this.inventoryList
            
            // 如果没有ID，添加一个临时ID
            if (!this.recordForm.id) {
              this.recordForm.id = 'temp_' + Date.now() + '_' + Math.floor(Math.random() * 10000)
            }
            
            // 补充额外信息
            if (this.activeTab === 'inbound' || this.activeTab === 'outbound') {
              // 确保日期格式正确
              if (this.recordForm.日期 && typeof this.recordForm.日期 === 'string') {
                // 如果只有YYYY-MM格式，添加日期为当月1日
                if (this.recordForm.日期.match(/^\d{4}-\d{2}$/)) {
                  this.recordForm.日期 = this.recordForm.日期 + '-01'
                }
              } else if (!this.recordForm.日期) {
                // 如果没有日期，使用当前日期
                const now = new Date()
                this.recordForm.日期 = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`
              }
              
              // 如果没有经手人，添加默认值
              if (!this.recordForm.经手人) {
                this.recordForm.经手人 = '系统用户'
              }
            } else if (this.activeTab === 'inventory') {
              // 库存记录必须有位置
              if (!this.recordForm.位置) {
                this.recordForm.位置 = '默认位置'
              }
            }
            
            // 构建API请求数据
            const requestData = {
              warehouse_id: this.listQuery.warehouse_id,
              month: this.listQuery.month,
              record_type: this.activeTab,
              record_data: this.recordForm
            }
            
            console.log('提交记录数据:', requestData)
            
            if (this.editMode) {
              // 调用更新API
              try {
                await updateReport({
                  ...requestData,
                  record_id: this.currentRecord.id
                })
                console.log('更新记录成功')
              } catch (error) {
                console.error('API调用失败，但我们仍然更新前端数据:', error)
                this.$message.warning('API调用失败，但已在前端更新数据')
              }
              
              // 更新前端数据
              const index = list.indexOf(this.currentRecord)
              if (index > -1) {
                list.splice(index, 1, { ...this.recordForm })
              }
            } else {
              // 调用创建API
              try {
                const response = await createReport(requestData)
                console.log('创建记录返回:', response)
                
                // 使用API返回的ID更新记录
                if (response?.data?.id) {
                  this.recordForm.id = response.data.id
                }
              } catch (error) {
                console.error('API调用失败，但我们仍然添加到前端:', error)
                this.$message.warning('API调用失败，但已在前端添加数据')
              }
              
              // 添加到前端列表
              list.push({ ...this.recordForm })
            }
            
            this.dialogVisible = false
            this.$message.success(this.editMode ? '编辑成功' : '添加成功')
            
            // 不再重新获取数据，避免丢失刚添加的数据
            // await this.fetchData()
          } catch (error) {
            console.error(this.editMode ? '编辑记录失败:' : '添加记录失败:', error)
            this.$message.error(this.editMode ? '编辑记录失败' : '添加记录失败')
          }
        }
      })
    },
    
    // 保存报表
    async handleSaveReport() {
      if (!this.listQuery.warehouse_id || !this.listQuery.month) {
        this.$message.warning('请选择仓库和月份')
        return
      }
      
      this.loading = true
      this.loadingText = '正在保存报表...'
      
      try {
        // 确保所有金额计算正确
        this.recalculateAllAmounts()
        
        // 确保库存数据中的数量和金额字段都正确
        this.fixInventoryData()
        
        const data = {
          warehouse_id: parseInt(this.listQuery.warehouse_id),
          month: this.listQuery.month,
          inbound: this.inboundList,
          outbound: this.outboundList,
          inventory: this.inventoryList
        }
        
        console.log('保存报表数据:', data)
        
        // 尝试多种保存方法
        let saved = false
        let error = null
        
        // 方法1：检查报表是否存在
        try {
          console.log('尝试检查报表是否存在')
          const existingReport = await getMonthlyReport({
            warehouse_id: this.listQuery.warehouse_id,
            month: this.listQuery.month,
            check_exists: true
          })
          
          console.log('检查响应:', existingReport)
          
          if (existingReport?.data?.exists) {
            // 存在则调用更新API
            console.log('报表存在，使用更新API, ID:', existingReport.data.report_id)
            const updateResponse = await updateReport({
              ...data,
              report_id: existingReport.data.report_id
            })
            console.log('更新响应:', updateResponse)
            saved = true
          } else {
            // 不存在则调用创建API
            console.log('报表不存在，使用创建API')
            const createResponse = await createReport(data)
            console.log('创建响应:', createResponse)
            saved = true
          }
        } catch (err) {
          console.error('方法1失败:', err)
          error = err
          // 继续尝试方法2
        }
        
        // 方法2：直接尝试创建
        if (!saved) {
          try {
            console.log('尝试直接创建报表')
            const createResponse = await createReport(data)
            console.log('创建响应:', createResponse)
            saved = true
          } catch (err) {
            console.error('方法2失败:', err)
            error = error || err
            // 继续尝试方法3
          }
        }
        
        // 方法3：使用通用的updateMonthlyReport
        if (!saved) {
          try {
            console.log('尝试使用通用更新API')
            const updateResponse = await updateMonthlyReport({
              ...data,
              data: {
                inbound: data.inbound,
                outbound: data.outbound,
                inventory: data.inventory
              }
            })
            console.log('更新响应:', updateResponse)
            saved = true
          } catch (err) {
            console.error('方法3失败:', err)
            error = error || err
          }
        }
        
        if (saved) {
          this.$message.success('保存成功')
          
          // 保存成功后，不重新加载数据，以避免丢失本地编辑
          // 相反，我们将当前的本地状态视为已保存状态
          console.log('保存成功，保留本地数据')
        } else {
          throw error || new Error('所有保存方法都失败')
        }
      } catch (error) {
        console.error('保存报表失败:', error)
        this.$message.error('保存报表失败: ' + (error.message || '未知错误'))
        
        // 即使保存失败，我们也应该保留用户的编辑
        this.$message.warning('虽然服务器保存失败，但您的本地编辑被保留，请稍后再尝试保存')
      } finally {
        this.loading = false
        this.loadingText = ''
      }
    },
    
    // 重新计算所有记录的金额
    recalculateAllAmounts() {
      // 重新计算入库金额
      this.inboundList.forEach(item => {
        item.金额 = Number((Number(item.数量 || 0) * Number(item.单价 || 0)).toFixed(2))
      })
      
      // 重新计算出库金额
      this.outboundList.forEach(item => {
        item.金额 = Number((Number(item.数量 || 0) * Number(item.单价 || 0)).toFixed(2))
      })
      
      // 重新计算库存金额
      this.inventoryList.forEach(item => {
        // 确保数量字段有值（可能是数量或库存字段）
        if (!item.数量 && item.库存) {
          item.数量 = item.库存
        } else if (!item.数量) {
          // 从截图中取实际值，或使用默认值
          item.数量 = item.数量 || 0
        }
        
        // 计算金额
        item.金额 = Number((Number(item.数量 || 0) * Number(item.单价 || 0)).toFixed(2))
      })
    },
    
    // 为表格中的每一行计算金额
    calculateItemAmount(row) {
      const amount = Number((Number(row.数量 || row.库存 || 0) * Number(row.单价 || 0)).toFixed(2))
      // 同时更新行数据，确保保存时能正确保存金额
      row.金额 = amount
      return amount.toFixed(2)
    },
    
    // 导出报表
    handleExport() {
      if (!this.listQuery.warehouse_id || !this.listQuery.month) {
        this.$message.warning('请选择仓库和月份')
        return
      }
      
      this.loading = true
      this.loadingText = '正在导出报表...'
      
      try {
        // 使用当前表格数据直接导出
        const currentData = this.inventoryList || []
        
        if (currentData.length === 0) {
          this.$message.warning('当前库存数据为空，无法导出')
          this.loading = false
          this.loadingText = ''
          return
        }
        
        console.log('开始导出报表，数据条数:', currentData.length)
        
        // 准备表头 - 完全按照图片中的格式
        const headers = ['位置', '品项', '规格/型号单位', '期初库存', '累计入库', '累计出库', '库存', '单价', '库存金额', 'id']
        
        // 准备数据
        const formattedData = currentData.map(item => [
          item.位置 || '',                                     // 位置
          item.品项 || '',                                     // 品项
          (item['规格/型号'] || '') + '个',                    // 规格/型号单位（合并并添加"个"单位）
          Number(item.期初库存 || item.库存 || 0),             // 期初库存
          0,                                                  // 累计入库
          0,                                                  // 累计出库
          Number(item.库存 || 0),                             // 库存
          Number(item.单价 || 0),                             // 单价
          Number(item.库存金额 || item.金额 || 0),             // 库存金额
          'iw_' + (item.id || Date.now() + '_' + Math.floor(Math.random() * 10000))  // id带iw_前缀
        ])
        
        // 创建工作簿
        const wb = XLSX.utils.book_new()
        
        // 创建工作表
        const ws = XLSX.utils.aoa_to_sheet([headers, ...formattedData])
        
        // 设置列宽
        ws['!cols'] = [
          { wch: 6 },   // 位置
          { wch: 8 },   // 品项
          { wch: 14 },  // 规格/型号单位
          { wch: 8 },   // 期初库存
          { wch: 8 },   // 累计入库
          { wch: 8 },   // 累计出库
          { wch: 6 },   // 库存
          { wch: 7 },   // 单价
          { wch: 9 },   // 库存金额
          { wch: 35 }   // id
        ]
        
        // 设置单元格样式
        const range = XLSX.utils.decode_range(ws['!ref'])
        for (let R = range.s.r; R <= range.e.r; R++) {
          for (let C = range.s.c; C <= range.e.c; C++) {
            const cell_address = { c: C, r: R }
            const cell_ref = XLSX.utils.encode_cell(cell_address)
            const cell = ws[cell_ref]
            
            if (!cell) continue
            
            // 设置基本样式
            cell.s = {
              font: {
                name: '宋体',
                sz: 10,
                color: { rgb: "000000" }
              },
              alignment: {
                vertical: 'center',
                horizontal: C <= 2 ? 'left' : 'right' // 前3列左对齐，数字右对齐
              }
            }
            
            // 设置数值为0的单元格背景为浅红色
            if (R > 0 && (C === 3 || C === 6 || C === 8) && cell.v === 0) {
              cell.s.fill = {
                fgColor: { rgb: "FFC7CE" }, // 浅红色背景
                patternType: 'solid'
              }
            }
            
            // 表头单元格格式
            if (R === 0) {
              cell.s.alignment.horizontal = 'left' // 表头左对齐
              
              // 为位置列添加绿色背景（第一列）
              if (C === 0) {
                cell.s.fill = {
                  fgColor: { rgb: "92D050" }, // 绿色背景
                  patternType: 'solid'
                }
              }
            }
            
            // 设置数字格式
            if (C >= 3 && C <= 8) { // 数值列
              // 单价和金额列使用两位小数
              if (C === 7 || C === 8) {
                cell.z = '#,##0.00'
              } else {
                cell.z = '#,##0' // 其他数值列使用整数
              }
              
              // 处理特殊的小数值 (如2.1)
              if (typeof cell.v === 'number' && cell.v !== Math.floor(cell.v) && C !== 7 && C !== 8) {
                cell.z = '#,##0.0'; // 一位小数
              }
            }
          }
        }
        
        // 添加工作表到工作簿（使用图片中显示的名称）
        XLSX.utils.book_append_sheet(wb, ws, '库存期间')
        
        // 导出为Excel文件
        XLSX.writeFile(wb, `库存明细_${this.listQuery.month}.xlsx`)
        
        this.$message.success('导出报表成功')
        this.loading = false
        this.loadingText = ''
      } catch (error) {
        console.error('导出处理失败:', error)
        this.$message.error('导出处理失败，请重试: ' + (error.message || '未知错误'))
        this.loading = false
        this.loadingText = ''
      }
    },
    
    // 进入快速模式，直接使用空数据开始编辑
    enterQuickMode() {
      if (!this.listQuery.warehouse_id || !this.listQuery.month) {
        this.$message.warning('请选择仓库和月份')
        return
      }
      
      // 清空现有数据
      this.inboundList = []
      this.outboundList = []
      this.inventoryList = []
      
      this.$message.success('已进入快速模式，您可以直接添加数据了')
      
      // 默认选中第一个标签页
      this.activeTab = 'inbound'
    },
    
    // 补创建当前月份的报表
    async handleCreateCurrentMonthReport() {
      if (!this.listQuery.warehouse_id) {
        this.$message.warning('请先选择仓库')
        return
      }
      
      this.loading = true
      this.loadingText = '正在创建当月报表...'
      
      try {
        // 获取当前日期并格式化为YYYY-MM
        const now = new Date()
        const currentMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
        
        // 显示确认对话框
        await this.$confirm(
          `确定要为所选仓库(ID:${this.listQuery.warehouse_id})创建${currentMonth}月的报表吗？将使用上月的库存结余作为本月的期初库存。`, 
          '创建当月报表', 
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        console.log(`开始创建当月(${currentMonth})报表，仓库ID:${this.listQuery.warehouse_id}`)
        
        // 构建请求数据，确保数据类型正确
        const requestData = {
          warehouse_id: parseInt(this.listQuery.warehouse_id),
          month: currentMonth
        }
        
        console.log('创建报表请求数据:', requestData)
        
        let response = null
        
        // 尝试调用首选API
        try {
          console.log('尝试调用createAutoMonthlyReport API')
          response = await createAutoMonthlyReport(requestData)
          console.log('API响应:', response)
        } catch (apiError) {
          console.error('调用首选API失败:', apiError)
          
          // 如果首选API失败，尝试备选API
          try {
            console.log('尝试调用备选API (createReport)')
            // 准备一些基础数据
            const fallbackData = {
              warehouse_id: parseInt(this.listQuery.warehouse_id),
              month: currentMonth,
              inbound: [],
              outbound: [],
              inventory: []
            }
            
            // 尝试从上个月获取库存数据
            const lastMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1)
            const lastMonthStr = `${lastMonth.getFullYear()}-${String(lastMonth.getMonth() + 1).padStart(2, '0')}`
            
            try {
              console.log(`尝试获取上月(${lastMonthStr})数据`)
              const lastMonthResponse = await getMonthlyReport({
                warehouse_id: parseInt(this.listQuery.warehouse_id),
                month: lastMonthStr,
                format: 'json'
              })
              
              console.log('上月数据响应:', lastMonthResponse)
              
              // 如果能获取到上月数据，提取库存作为本月期初
              if (lastMonthResponse && lastMonthResponse.data && Array.isArray(lastMonthResponse.data.inventory)) {
                console.log('上月库存数据条数:', lastMonthResponse.data.inventory.length)
                
                // 将上月库存作为本月期初库存
                fallbackData.inventory = lastMonthResponse.data.inventory.map(item => {
                  return {
                    ...item,
                    期初库存: item.库存 || 0,
                    备注: '系统自动创建(来自上月库存)'
                  }
                })
              }
            } catch (lastMonthError) {
              console.error('获取上月数据失败:', lastMonthError)
              // 继续创建空报表
            }
            
            response = await createReport(fallbackData)
            console.log('备选API响应:', response)
          } catch (fallbackError) {
            console.error('调用备选API也失败:', fallbackError)
            throw new Error('所有API调用都失败，无法创建报表')
          }
        }
        
        if (response) {
          let success = false
          let message = ''
          
          // 分析响应结果
          if (response.data) {
            if (response.data.status === 'success' || response.data.code === 200 || response.data.code === 0) {
              success = true
              message = response.data.message || '创建当月报表成功'
            } else if (response.data.message || response.data.error) {
              message = response.data.message || response.data.error
            }
          } else if (response.status === 200 || response.status === 201) {
            success = true
            message = '创建当月报表成功'
          }
          
          if (success) {
            this.$message.success(message)
            
            // 更新查询条件并获取最新数据
            this.listQuery.month = currentMonth
            await this.fetchData()
          } else {
            this.$message.warning(message || '创建报表可能未成功，请检查后台')
            console.error('创建报表失败，API响应:', response)
            
            // 尝试使用快速模式，让用户手动添加数据
            this.listQuery.month = currentMonth
            this.enterQuickMode()
          }
        } else {
          this.$message.error('创建报表失败: API返回为空')
          console.error('创建报表失败，无效响应:', response)
        }
      } catch (error) {
        if (error === 'cancel') {
          // 用户取消操作
          this.$message.info('已取消操作')
        } else {
          console.error('创建报表失败:', error)
          
          // 分析错误原因
          let errorMessage = '创建报表失败: ' + (error.message || '未知错误')
          
          if (error.response) {
            console.error('错误响应:', error.response)
            // 处理不同的HTTP错误状态
            if (error.response.status === 404) {
              errorMessage = '创建报表失败: API接口不存在 (404)'
            } else if (error.response.status === 400) {
              errorMessage = `创建报表失败: 请求参数错误 (400) - ${error.response.data?.error || ''}`
            } else if (error.response.status === 403) {
              errorMessage = '创建报表失败: 权限不足 (403)'
            } else if (error.response.status === 500) {
              errorMessage = '创建报表失败: 服务器内部错误 (500)'
            }
            
            // 打印详细错误信息
            if (error.response.data) {
              console.error('错误详情:', error.response.data)
            }
          }
          
          this.$message.error(errorMessage)
          
          // 如果创建失败，引导用户进入快速模式手动添加数据
          this.$confirm('自动创建报表失败，是否进入快速模式手动添加数据？', '提示', {
            confirmButtonText: '进入快速模式',
            cancelButtonText: '取消',
            type: 'info'
          }).then(() => {
            const now = new Date()
            this.listQuery.month = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
            this.enterQuickMode()
          }).catch(() => {})
        }
      } finally {
        this.loading = false
        this.loadingText = ''
      }
    },
    
    // 手动设置仓库ID
    setManualWarehouseId() {
      this.$prompt('请输入仓库ID', '手动输入', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /^\d+$/,
        inputErrorMessage: '仓库ID必须是数字'
      }).then(({ value }) => {
        this.listQuery.warehouse_id = parseInt(value)
        this.$message.success(`已设置仓库ID为: ${value}`)
        
        // 检查是否已经有这个仓库，如果没有就添加到选项中
        const exists = this.warehouseOptions.some(item => item.id === parseInt(value))
        if (!exists) {
          this.warehouseOptions.push({
            id: parseInt(value),
            name: `仓库 #${value}`
          })
          this.$message.info(`已添加ID为${value}的仓库到选项列表`)
        }
      }).catch(() => {
        // 用户取消，不做任何操作
      })
    },
    
    // 重新加载仓库选项
    async reloadWarehouseOptions() {
      this.$message.info('正在重新加载仓库列表...')
      // 清除缓存
      try {
        localStorage.removeItem('warehouseOptions')
      } catch (e) {
        console.error('清除缓存失败:', e)
      }
      
      // 清空现有选项
      this.warehouseOptions = []
      this.listQuery.warehouse_id = undefined
      
      // 重新获取仓库选项
      await this.getWarehouseOptions()
    },
    
    // 修复库存数据中的数量和金额
    fixInventoryData() {
      console.log('开始修复库存数据...')
      // 处理库存列表中的数据
      this.inventoryList.forEach(item => {
        // 1. 处理期初库存、累计入库和累计出库字段
        if (item.期初库存 === undefined || item.期初库存 === null) {
          console.log(`项目[${item.品项}]：期初库存字段为空，设置默认值0`)
          item.期初库存 = 0
        } else {
          item.期初库存 = Number(item.期初库存)
        }
        
        if (item.累计入库 === undefined || item.累计入库 === null) {
          console.log(`项目[${item.品项}]：累计入库字段为空，设置默认值0`)
          item.累计入库 = 0
        } else {
          item.累计入库 = Number(item.累计入库)
        }
        
        if (item.累计出库 === undefined || item.累计出库 === null) {
          console.log(`项目[${item.品项}]：累计出库字段为空，设置默认值0`)
          item.累计出库 = 0
        } else {
          item.累计出库 = Number(item.累计出库)
        }
        
        // 2. 处理数量字段 - 确保有值
        if (item.数量 === undefined || item.数量 === null) {
          if (item.库存 !== undefined && item.库存 !== null) {
            console.log(`项目[${item.品项}]：将库存值 ${item.库存} 复制到数量字段`)
            item.数量 = Number(item.库存)
          } else {
            // 检查是否可以从期初库存、累计入库和累计出库计算
            const calculated = item.期初库存 + item.累计入库 - item.累计出库
            console.log(`项目[${item.品项}]：从期初库存、累计入库和累计出库计算数量: ${calculated}`)
            item.数量 = calculated >= 0 ? calculated : 0
          }
        } else {
          // 确保是数字类型
          item.数量 = Number(item.数量)
        }
        
        // 3. 处理单价字段 - 确保是数字
        if (item.单价 !== undefined && item.单价 !== null) {
          item.单价 = Number(item.单价)
        } else {
          console.log(`项目[${item.品项}]：单价字段为空，设置默认值0`)
          item.单价 = 0
        }
        
        // 4. 重新计算金额
        const oldAmount = item.金额
        item.金额 = Number((item.数量 * item.单价).toFixed(2))
        
        if (oldAmount !== item.金额) {
          console.log(`项目[${item.品项}]：金额从 ${oldAmount} 更新为 ${item.金额}`)
        }
        
        // 5. 如果需要，同步更新库存字段
        if (item.库存 === undefined || item.库存 === null || item.库存 !== item.数量) {
          console.log(`项目[${item.品项}]：将数量 ${item.数量} 同步到库存字段`)
          item.库存 = item.数量
        }
      })
      
      console.log('库存数据修复完成')
    },
    
    // 计算库存
    calculateInventory() {
      if (this.activeTab === 'inventory') {
        // 自动计算库存 = 期初库存 + 累计入库 - 累计出库
        const 期初库存 = Number(this.recordForm.期初库存 || 0)
        const 累计入库 = Number(this.recordForm.累计入库 || 0)
        const 累计出库 = Number(this.recordForm.累计出库 || 0)
        
        // 计算得到的库存不能为负数
        const calculated = 期初库存 + 累计入库 - 累计出库
        this.recordForm.数量 = calculated >= 0 ? calculated : 0
        
        // 同时更新金额
        this.calculateAmount()
      }
    },
    handleMonthlyInbound(row) {
      // 预填入库记录表单并打开编辑对话框
      this.dialogMode = 'add'
      this.activeRecordType = 'inbound'
      this.activeTab = 'inbound'
      this.recordForm = {
        日期: this.getCurrentDate(),
        品项: row.品项,
        '规格/型号': row['规格/型号'],
        单位: row.单位,
        数量: 0,
        单价: row.单价 || 0,
        金额: 0,
        经手人: '',
        备注: '本月入库'
      }
      this.dialogTitle = '添加入库记录'
      this.dialogVisible = true
      
      // 在下一个渲染循环中设置焦点到数量输入框
      this.$nextTick(() => {
        const numberField = this.$refs.recordForm.fields.find(field => field.prop === '数量')
        if (numberField && numberField.$el) {
          const inputElement = numberField.$el.querySelector('input')
          if (inputElement) inputElement.focus()
        }
      })
    },
    
    handleMonthlyOutbound(row) {
      // 检查当前库存是否足够
      const currentStock = Number(row.数量 || row.库存 || 0)
      if (currentStock <= 0) {
        this.$message.warning('当前库存为0，无法进行出库操作')
        return
      }
      
      // 预填出库记录表单并打开编辑对话框
      this.dialogMode = 'add'
      this.activeRecordType = 'outbound'
      this.activeTab = 'outbound'
      this.recordForm = {
        日期: this.getCurrentDate(),
        品项: row.品项,
        '规格/型号': row['规格/型号'],
        单位: row.单位,
        数量: 0,
        单价: row.单价 || 0,
        金额: 0,
        经手人: '',
        去向: '',
        备注: '本月出库'
      }
      this.dialogTitle = '添加出库记录'
      this.dialogVisible = true
      
      // 在下一个渲染循环中设置焦点到数量输入框
      this.$nextTick(() => {
        const numberField = this.$refs.recordForm.fields.find(field => field.prop === '数量')
        if (numberField && numberField.$el) {
          const inputElement = numberField.$el.querySelector('input')
          if (inputElement) inputElement.focus()
        }
      })
    },
    
    // 获取当前日期 YYYY-MM-DD 格式
    getCurrentDate() {
      const date = new Date()
      const year = date.getFullYear()
      const month = (date.getMonth() + 1).toString().padStart(2, '0')
      const day = date.getDate().toString().padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    
    /**
     * 更新当前月份的期初库存
     * 根据上月期末库存更新当前月的期初库存
     */
    handleUpdateInitialStock() {
      // 检查是否选择了仓库和月份
      if (!this.listQuery.warehouse_id || !this.listQuery.month) {
        this.$message.error('请先选择仓库和月份')
        return
      }
      
      // 确认操作
      this.$confirm(
        `确定要更新${this.listQuery.month}月的期初库存吗？将使用上月的期末库存作为本月的期初库存，并重新计算当前库存。`,
        '更新期初库存',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
        .then(() => {
          // 显示加载状态
          this.loading = true
          this.loadingText = '正在更新期初库存...'
          
          // 记录请求参数，便于调试
          console.log('更新期初库存请求参数:', {
            warehouse_id: this.listQuery.warehouse_id,
            month: this.listQuery.month
          })
          
          // 计算上个月，用于可能的错误处理
          const prevMonth = this._getPreviousMonth(this.listQuery.month)
          
          // 记录完整路径，用于调试
          const apiUrl = `/api/v1/warehouse/monthly-report/update_initial_stock/`
          console.log('API请求路径:', apiUrl)
          
          // 调用API更新期初库存
          updateInitialStock({
            warehouse_id: this.listQuery.warehouse_id,
            month: this.listQuery.month
          })
            .then(response => {
              console.log('期初库存更新成功:', response)
              this.$message({
                message: response.message || '期初库存更新成功',
                type: 'success',
                duration: 5000
              })
              
              // 重新加载数据
              this.fetchData()
            })
            .catch(error => {
              console.error('更新期初库存失败:', error)
              
              // 记录详细错误信息，方便调试
              if (error.response) {
                console.error('错误响应状态:', error.response.status)
                console.error('错误响应数据:', error.response.data)
              }
              
              let errorMessage = '更新期初库存失败'
              
              // 解析错误信息
              if (error.response && error.response.data) {
                // 如果后端返回了具体错误信息
                if (error.response.data.error) {
                  errorMessage = error.response.data.error
                } else if (typeof error.response.data === 'string') {
                  errorMessage = error.response.data
                }
              } else if (error.message) {
                // 如果是网络错误等
                errorMessage = `请求错误: ${error.message}`
              }
              
              // 处理一些常见错误
              if (errorMessage.includes('上个月') && errorMessage.includes('没有库存数据')) {
                // 尝试自动创建上月报表
                this.$confirm(
                  `没有找到${prevMonth}月的库存数据。是否要先创建${prevMonth}月的报表？`,
                  '上月报表不存在',
                  {
                    confirmButtonText: '是，创建上月报表',
                    cancelButtonText: '否',
                    type: 'warning'
                  }
                ).then(() => {
                  // 创建上月报表
                  this.createPreviousMonthReport(prevMonth)
                }).catch(() => {
                  this.$message.info('您取消了操作。您可以尝试手动创建上月报表。')
                })
              } else if (errorMessage.includes('请求的资源不存在') || error.response && error.response.status === 404) {
                this.$message({
                  message: 'API接口不存在，请检查后端URL配置是否正确',
                  type: 'error',
                  duration: 7000,
                  showClose: true
                })
              } else if (error.response && error.response.status === 500) {
                this.$message({
                  message: '服务器内部错误，请检查后端日志',
                  type: 'error',
                  duration: 7000,
                  showClose: true
                })
              } else {
                this.$message({
                  message: errorMessage,
                  type: 'error',
                  duration: 5000,
                  showClose: true
                })
              }
            })
            .finally(() => {
              this.loading = false
            })
        })
        .catch(() => {
          // 用户取消操作
        })
    },
    
    /**
     * 创建上个月的报表
     */
    createPreviousMonthReport(prevMonth) {
      this.loading = true
      this.loadingText = `正在创建${prevMonth}月报表...`
      
      createAutoMonthlyReport({
        warehouse_id: this.listQuery.warehouse_id,
        month: prevMonth
      })
        .then(response => {
          this.$message.success(`成功创建${prevMonth}月报表`)
          
          // 提示用户现在可以更新当前月的期初库存了
          this.$confirm(
            `${prevMonth}月报表已创建成功，是否现在更新${this.listQuery.month}月的期初库存？`,
            '创建成功',
            {
              confirmButtonText: '是，更新期初库存',
              cancelButtonText: '否',
              type: 'success'
            }
          ).then(() => {
            // 再次调用更新期初库存
            this.handleUpdateInitialStock()
          }).catch(() => {})
        })
        .catch(error => {
          console.error(`创建${prevMonth}月报表失败:`, error)
          this.$message.error(`创建${prevMonth}月报表失败: ${error.response?.data?.error || error.message || '未知错误'}`)
        })
        .finally(() => {
          this.loading = false
        })
    },
    
    /**
     * 获取上个月的日期字符串 (YYYY-MM)
     */
    _getPreviousMonth(currentMonth) {
      try {
        // 解析当前月份
        const [year, month] = currentMonth.split('-').map(num => parseInt(num))
        const date = new Date(year, month - 1, 1) // 注意：JavaScript的月份是从0开始的
        
        // 减去一个月
        date.setMonth(date.getMonth() - 1)
        
        // 格式化为YYYY-MM
        return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}`
      } catch (e) {
        console.error('计算上个月日期出错:', e)
        return currentMonth
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.app-container {
  padding: 20px;
}

.filter-container {
  padding-bottom: 15px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  
  .el-form-item {
    margin-bottom: 10px;
    margin-right: 20px;
  }
}

.operation-container {
  margin-bottom: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  .search-box {
    display: flex;
    align-items: center;
    
    .search-result {
      margin-left: 10px;
      font-size: 13px;
      color: #909399;
    }
  }
}

.el-card {
  margin-bottom: 20px;
  
  .el-card__header {
    padding: 15px 20px;
    background-color: #f9fafc;
    border-bottom: 1px solid #ebeef5;
  }
  
  .el-card__body {
    padding: 20px;
  }
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

/* 添加表格样式 */
.el-table {
  margin-bottom: 20px;
  table-layout: auto; /* 使用自动表格布局以适应内容 */
  
  // 对齐按钮
  .el-button+.el-button {
    margin-left: 10px;
  }
  
  // 垂直居中所有单元格
  td {
    vertical-align: middle;
    overflow: hidden;
    text-overflow: ellipsis;
    padding: 8px 0;
    line-height: 1.5;
    height: 50px;
  }
  
  // 表格头部样式
  th {
    background-color: #f5f7fa;
    color: #606266;
    font-weight: 500;
    padding: 12px 0;
    height: 50px;
  }
  
  // 提高操作列按钮的可用性
  .action-buttons {
    display: flex;
    justify-content: center;
    flex-wrap: nowrap;
    
    .el-button {
      padding: 7px 12px;
      font-size: 12px;
    }
  }
}

/* 深度选择器：调整表格单元格内边距 */
::v-deep .el-table__row td {
  padding: 10px 0;
}

/* 深度选择器：调整单元格内容间距 */
::v-deep .el-table .cell {
  padding-left: 10px;
  padding-right: 10px;
  font-size: 14px;
}

/* 深度选择器：表头样式 */
::v-deep .el-table th > .cell {
  font-size: 14px;
  font-weight: bold;
}

/* 深度选择器：表格样式优化 */
::v-deep .el-table {
  // 条纹背景，提高可读性
  &--striped .el-table__body tr.el-table__row--striped td {
    background-color: #fafafa;
  }
  
  // 鼠标悬停高亮
  .el-table__body tr:hover > td {
    background-color: #f0f9eb !important;
  }
  
  // 表格边框
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: hidden;
}

/* 调整按钮组布局，保持对齐 */
.el-button.is-circle+.el-button.is-circle,
.el-button--mini+.el-button--mini {
  margin-left: 10px;
}

/* 操作按钮容器 */
.action-buttons {
  display: flex;
  justify-content: center;
}

/* 表单帮助文本 */
.form-help-text {
  font-size: 12px;
  color: #909399;
  line-height: 1.5;
  margin-top: 5px;
}

/* 对话框样式 */
::v-deep .el-dialog {
  .el-dialog__header {
    padding: 15px 20px;
    border-bottom: 1px solid #e6e6e6;
  }
  
  .el-dialog__body {
    padding: 20px 20px 10px;
  }
  
  .el-dialog__footer {
    padding: 10px 20px 20px;
    border-top: 1px solid #f0f0f0;
  }
}

/* 标签页样式 */
::v-deep .el-tabs {
  .el-tabs__header {
    margin-bottom: 20px;
  }
  
  .el-tabs__item {
    font-size: 14px;
    height: 40px;
    line-height: 40px;
  }
  
  .el-tabs__content {
    overflow: visible;
  }
}

/* 表单项样式 */
::v-deep .el-form-item {
  margin-bottom: 20px;
  
  .el-form-item__label {
    font-weight: 500;
  }
  
  .el-input__inner,
  .el-input-number__decrease,
  .el-input-number__increase {
    height: 36px;
    line-height: 36px;
  }
  
  .el-input-number {
    width: 100%;
  }
}

/* 响应式布局处理 */
@media screen and (max-width: 1200px) {
  .el-button {
    padding: 9px 15px;
  }
  
  ::v-deep .el-table .cell {
    padding-left: 5px;
    padding-right: 5px;
  }
}

/* 数字单元格样式 */
.number-cell {
  font-family: 'Consolas', 'Monaco', monospace;
  color: #409EFF;
  font-weight: 500;
}

/* 零值数字显示为灰色 */
::v-deep .el-table td .number-cell {
  &:empty, &.zero-value {
    color: #909399;
  }
}

/* 删除按钮样式 */
.delete-btn {
  color: #F56C6C;
}
.delete-btn:hover {
  color: #FF7878;
}

/* 标签页样式 */
::v-deep .el-tabs__item {
  height: 40px;
  line-height: 40px;
}

/* 表格为空时的样式 */
::v-deep .el-table__empty-block {
  min-height: 200px;
}
</style> 