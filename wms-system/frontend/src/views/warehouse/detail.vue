<template>
  <div class="app-container">
    <!-- 顶部操作栏 -->
    <div class="operation-header">
      <el-button v-if="loadError" type="primary" icon="el-icon-refresh" @click="retryLoading">重新加载</el-button>
    </div>

    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>仓库基本信息</span>
        <div style="float: right;">
          <!-- 备份按钮组 -->
          <el-button-group class="margin-right-10">
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
          <!-- 添加直接导出按钮 -->
          <el-button
            type="warning"
            size="small"
            icon="el-icon-download"
            class="margin-left-10"
            @click="directExport"
            title="直接导出当前表格数据，无需API请求"
          >
            导出当前表格
          </el-button>
        </div>
      </div>
      <!-- 备份进度条 -->
      <el-progress 
        v-if="backupProgress > 0 && backupProgress < 100"
        :percentage="backupProgress"
        :format="progressFormat"
        class="backup-progress"
      ></el-progress>
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

    <el-card class="box-card" style="margin-top: 20px;">
      <div slot="header" class="clearfix">
        <span>月度报表</span>
        <el-date-picker
          v-model="selectedMonth"
          type="month"
          placeholder="选择月份"
          format="yyyy年MM月"
          value-format="yyyy-MM"
          style="float: right; margin-left: 10px;"
          @change="fetchReportData"
        />
        <el-upload
          class="excel-upload"
          :action="'#'"
          :auto-upload="false"
          :show-file-list="false"
          :on-change="handleImportFile"
          accept=".xlsx, .xls"
          style="float: right; margin-right: 10px;"
        >
          <el-button type="primary" size="small" icon="el-icon-upload2">
            导入报表
          </el-button>
        </el-upload>
        <!-- 恢复按钮 -->
        <el-button
          type="warning"
          size="small"
          icon="el-icon-refresh-left"
          style="float: right; margin-right: 10px;"
          @click="handleRecover"
        >
          恢复数据
        </el-button>
        <!-- 新增：从备份恢复按钮 -->
        <el-button
          type="success"
          size="small"
          icon="el-icon-time"
          style="float: right; margin-right: 10px;"
          @click="handleRestoreFromBackup"
          :disabled="!backupTime"
        >
          从备份恢复
        </el-button>
        <el-button
          type="info"
          size="small"
          icon="el-icon-document"
          style="float: right; margin-right: 10px;"
          @click="downloadTemplate"
        >
          下载模板
        </el-button>
        <el-button
          type="warning"
          size="small"
          icon="el-icon-download"
          style="float: right; margin-right: 10px;"
          @click="handleExport"
        >
          导出报表
        </el-button>
        <el-button
          type="success"
          size="small"
          icon="el-icon-refresh"
          style="float: right; margin-right: 10px;"
          @click="handleUpdateInitialStock"
        >
          更新期初库存
        </el-button>
      </div>
      
      <el-tabs v-model="activeTab">
        <el-tab-pane label="入库明细" name="inbound">
          <div class="operation-container">
            <div class="action-buttons">
              <el-button type="primary" size="small" icon="el-icon-plus" @click="handleAdd('inbound')">新增入库记录</el-button>
            </div>
            <div class="search-box">
              <el-input
                v-model="inboundSearchText"
                placeholder="搜索入库记录..."
                prefix-icon="el-icon-search"
                style="width: 300px"
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
            v-loading="loading"
            element-loading-text="加载数据中..."
            :data="filteredInboundList"
            border
            stripe
            style="width: 100%">
            <template slot="empty">
              <el-empty description="暂无入库数据" :image-size="100">
                <el-button type="primary" size="small" @click="handleAdd('inbound')">添加数据</el-button>
              </el-empty>
            </template>
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
            <el-table-column
              label="操作"
              width="150"
              align="center"
            >
              <template slot-scope="scope">
                <el-button type="text" size="small" icon="el-icon-edit" @click="handleEdit('inbound', scope.row, scope.$index)">编辑</el-button>
                <el-button type="text" size="small" icon="el-icon-delete" class="delete-btn" @click="handleDelete('inbound', scope.row, scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="出库明细" name="outbound">
          <div class="operation-container">
            <div class="action-buttons">
              <el-button type="primary" size="small" icon="el-icon-plus" @click="handleAdd('outbound')">新增出库记录</el-button>
            </div>
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
            v-loading="loading"
            element-loading-text="加载数据中..."
            :data="filteredOutboundList"
            border
            stripe
            style="width: 100%">
            <template slot="empty">
              <el-empty description="暂无出库数据" :image-size="100">
                <el-button type="primary" size="small" @click="handleAdd('outbound')">添加数据</el-button>
              </el-empty>
            </template>
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
            <el-table-column
              label="操作"
              width="150"
              align="center"
            >
              <template slot-scope="scope">
                <el-button type="text" size="small" icon="el-icon-edit" @click="handleEdit('outbound', scope.row, scope.$index)">编辑</el-button>
                <el-button type="text" size="small" icon="el-icon-delete" class="delete-btn" @click="handleDelete('outbound', scope.row, scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="库存明细" name="inventory">
          <div class="operation-container">
            <div class="action-buttons">
              <el-button type="primary" size="small" icon="el-icon-plus" @click="handleAdd('inventory')">新增库存记录</el-button>
              <el-button type="success" size="small" icon="el-icon-refresh" @click="handleUpdateStatistics">更新累计统计</el-button>
            </div>
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
            v-loading="loading"
            element-loading-text="加载数据中..."
            :data="filteredInventoryList"
            border
            stripe
            style="width: 100%">
            <template slot="empty">
              <el-empty description="暂无库存数据" :image-size="100">
                <el-button type="primary" size="small" @click="handleAdd('inventory')">添加数据</el-button>
              </el-empty>
            </template>
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
            <el-table-column
              label="操作"
              width="300"
              align="center"
            >
              <template slot-scope="scope">
                <el-button type="text" size="small" icon="el-icon-top" @click="handleMonthlyInbound(scope.row)">本月入库</el-button>
                <el-button type="text" size="small" icon="el-icon-bottom" @click="handleMonthlyOutbound(scope.row)">本月出库</el-button>
                <el-button type="text" size="small" icon="el-icon-edit" @click="handleEdit('inventory', scope.row, scope.$index)">编辑</el-button>
                <el-button type="text" size="small" icon="el-icon-delete" class="delete-btn" @click="handleDelete('inventory', scope.row, scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 编辑/新增入库记录对话框 -->
    <el-dialog :title="dialogStatus === 'create' ? '新增入库记录' : '编辑入库记录'" :visible.sync="inboundDialogVisible" width="500px">
      <el-form ref="inboundForm" :model="currentRecord" :rules="inboundRules" label-width="100px">
        <el-form-item label="日期" prop="日期">
          <el-date-picker 
            v-model="currentRecord.日期" 
            type="date" 
            placeholder="选择日期" 
            style="width: 100%" 
            value-format="yyyy-MM-dd"
            :picker-options="datePickerOptions">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="品项" prop="品项">
          <el-input v-model="currentRecord.品项" placeholder="请输入品项"></el-input>
        </el-form-item>
        <el-form-item label="规格/型号" prop="规格/型号">
          <el-input v-model="currentRecord['规格/型号']" placeholder="请输入规格/型号"></el-input>
        </el-form-item>
        <el-form-item label="单位" prop="单位">
          <el-input v-model="currentRecord.单位" placeholder="请输入单位"></el-input>
        </el-form-item>
        <el-form-item label="数量" prop="数量">
          <el-input-number v-model="currentRecord.数量" :min="0" :precision="0" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="单价" prop="单价">
          <el-input-number v-model="currentRecord.单价" :min="0" :precision="2" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="经手人" prop="经手人">
          <el-select v-model="currentRecord.经手人" placeholder="请选择经手人" style="width: 100%" filterable allow-create default-first-option>
            <el-option v-for="person in handlerList" :key="person" :label="person" :value="person"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="inboundDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitInboundForm">确 定</el-button>
      </div>
    </el-dialog>

    <!-- 编辑/新增出库记录对话框 -->
    <el-dialog :title="dialogStatus === 'create' ? '新增出库记录' : '编辑出库记录'" :visible.sync="outboundDialogVisible" width="500px">
      <el-form ref="outboundForm" :model="currentRecord" :rules="outboundRules" label-width="100px">
        <el-form-item label="日期" prop="日期">
          <el-date-picker 
            v-model="currentRecord.日期" 
            type="date" 
            placeholder="选择日期" 
            style="width: 100%" 
            value-format="yyyy-MM-dd"
            :picker-options="datePickerOptions">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="品项" prop="品项">
          <el-input v-model="currentRecord.品项" placeholder="请输入品项"></el-input>
        </el-form-item>
        <el-form-item label="规格/型号" prop="规格/型号">
          <el-input v-model="currentRecord['规格/型号']" placeholder="请输入规格/型号"></el-input>
        </el-form-item>
        <el-form-item label="单位" prop="单位">
          <el-input v-model="currentRecord.单位" placeholder="请输入单位"></el-input>
        </el-form-item>
        <el-form-item label="数量" prop="数量">
          <el-input-number v-model="currentRecord.数量" :min="0" :precision="0" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="单价" prop="单价">
          <el-input-number v-model="currentRecord.单价" :min="0" :precision="2" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="经手人" prop="经手人">
          <el-select v-model="currentRecord.经手人" placeholder="请选择经手人" style="width: 100%" filterable allow-create default-first-option>
            <el-option v-for="person in handlerList" :key="person" :label="person" :value="person"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="outboundDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitOutboundForm">确 定</el-button>
      </div>
    </el-dialog>

    <!-- 编辑/新增库存记录对话框 -->
    <el-dialog :title="dialogStatus === 'create' ? '新增库存记录' : '编辑库存记录'" :visible.sync="inventoryDialogVisible" width="500px">
      <el-form ref="inventoryForm" :model="currentRecord" :rules="inventoryRules" label-width="100px">
        <el-form-item label="位置" prop="位置">
          <el-input v-model="currentRecord.位置" placeholder="请输入位置"></el-input>
        </el-form-item>
        <el-form-item label="品项" prop="品项">
          <el-input v-model="currentRecord.品项" placeholder="请输入品项"></el-input>
        </el-form-item>
        <el-form-item label="规格/型号" prop="规格/型号">
          <el-input v-model="currentRecord['规格/型号']" placeholder="请输入规格/型号"></el-input>
        </el-form-item>
        <el-form-item label="单位" prop="单位">
          <el-input v-model="currentRecord.单位" placeholder="请输入单位"></el-input>
        </el-form-item>
        <el-form-item label="期初库存" prop="期初库存">
          <el-input-number v-model="currentRecord.期初库存" :min="0" :precision="0" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="累计入库" prop="累计入库">
          <el-input-number v-model="currentRecord.累计入库" :min="0" :precision="0" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="累计出库" prop="累计出库">
          <el-input-number v-model="currentRecord.累计出库" :min="0" :precision="0" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="单价" prop="单价">
          <el-input-number v-model="currentRecord.单价" :min="0" :precision="2" style="width: 100%"></el-input-number>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="inventoryDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitInventoryForm">确 定</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import axios from 'axios'
import request from '@/utils/request'
import { getWarehouse, importExcel, exportTemplate, exportWarehouseBackup, restoreWarehouseBackup } from '@/api/warehouse'
import { getMonthlyReport, updateMonthlyReport, updateInitialStock } from '@/api/report'
import * as XLSX from 'xlsx'
import { saveAs } from 'file-saver'
import moment from 'moment'

export default {
  name: 'WarehouseDetail',
  data() {
    // 创建日期验证器，确保日期在所选月份内
    const validateDateInMonth = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请选择日期'))
        return
      }
      
      if (!this.selectedMonth) {
        callback()
        return
      }
      
      const [selectedYear, selectedMonth] = this.selectedMonth.split('-')
      const [year, month] = value.split('-')
      
      if (year !== selectedYear || month !== selectedMonth) {
        callback(new Error(`日期必须在${selectedYear}年${selectedMonth}月内`))
        return
      }
      
      callback()
    }
    
    return {
      warehouseInfo: {},
      selectedMonth: '',
      activeTab: 'inbound',
      loading: false,
      loadingText: '',
      warehouseId: null,
      warehouseName: '',
      inboundList: [],
      outboundList: [],
      inventoryList: [],
      // 新增：删除历史记录和最后删除时间
      deleteHistory: [], // 存储最近删除的记录
      lastDeleteTime: null, // 记录最后一次删除的时间
      // 对话框相关
      dialogStatus: 'create', // 'create' or 'update'
      currentRecord: {}, // 当前编辑的记录
      currentIndex: -1, // 当前编辑记录的索引
      inboundDialogVisible: false,
      outboundDialogVisible: false,
      inventoryDialogVisible: false,
      // 日期选择器选项
      datePickerOptions: {
        disabledDate: time => {
          if (!this.selectedMonth) {
            return false
          }
          const [year, month] = this.selectedMonth.split('-')
          const start = new Date(parseInt(year), parseInt(month) - 1, 1)
          const end = new Date(parseInt(year), parseInt(month), 0)
          return time.getTime() < start || time.getTime() > end
        }
      },
      // 表单验证规则
      inboundRules: {
        日期: [
          { required: true, message: '请选择日期', trigger: 'change' },
          { validator: validateDateInMonth, trigger: 'change' }
        ],
        品项: [{ required: true, message: '请输入品项', trigger: 'blur' }],
        单位: [{ required: true, message: '请输入单位', trigger: 'blur' }],
        数量: [{ required: true, message: '请输入数量', trigger: 'blur' }],
        单价: [{ required: true, message: '请输入单价', trigger: 'blur' }],
        经手人: [{ required: true, message: '请输入经手人', trigger: 'blur' }]
      },
      outboundRules: {
        日期: [
          { required: true, message: '请选择日期', trigger: 'change' },
          { validator: validateDateInMonth, trigger: 'change' }
        ],
        品项: [{ required: true, message: '请输入品项', trigger: 'blur' }],
        单位: [{ required: true, message: '请输入单位', trigger: 'blur' }],
        数量: [{ required: true, message: '请输入数量', trigger: 'blur' }],
        单价: [{ required: true, message: '请输入单价', trigger: 'blur' }],
        经手人: [{ required: true, message: '请输入经手人', trigger: 'blur' }]
      },
      inventoryRules: {
        位置: [{ required: true, message: '请输入位置', trigger: 'blur' }],
        品项: [{ required: true, message: '请输入品项', trigger: 'blur' }],
        单位: [{ required: true, message: '请输入单位', trigger: 'blur' }],
        期初库存: [{ required: true, message: '请输入期初库存', trigger: 'blur' }],
        单价: [{ required: true, message: '请输入单价', trigger: 'blur' }]
      },
      loadError: false,
      
      // 搜索文本字段 - 确保这些字段有默认值
      inboundSearchText: '',
      outboundSearchText: '',
      inventorySearchText: '',
      
      // 新增：报表数据备份
      reportBackup: {
        inbound: [],
        outbound: [],
        inventory: []
      },
      backupTime: null,
      handlerList: ['林福远', '黄伟恒', '叶平', '李海成', '梁立金', '王秋华', '黄善智', '黄善财', '黄家佳', '张录彬', '韦永强', '李思达'],
      backupLoading: false,
      restoreLoading: false,
      lastBackupTime: null,
      backupProgress: 0
    }
  },
  created() {
    console.log('组件创建，路由参数:', this.$route.params)
    const id = this.$route.params.id
    if (!id) {
      console.error('路由参数中没有仓库ID')
      this.$message.error('无法获取仓库ID，请返回列表页重试')
      // 使用模拟数据以显示UI
      this.warehouseInfo = {
        name: '模拟仓库(created)',
        code: 'WH-MOCK',
        contact_person: '模拟联系人',
        contact_phone: '13800138000',
        address: '模拟地址',
        is_active: true
      }
    } else {
      console.log('准备获取仓库信息，ID:', id)
      this.fetchWarehouseInfo()
    }
    
    this.selectedMonth = this.getCurrentMonth()
    console.log('当前选择的月份:', this.selectedMonth)
    
    this.fetchReportData()
  },
  methods: {
    getCurrentMonth() {
      const date = new Date()
      const year = date.getFullYear()
      const month = (date.getMonth() + 1).toString().padStart(2, '0')
      return `${year}-${month}`
    },
    fetchWarehouseInfo() {
      const id = this.$route.params.id
      if (!id) {
        this.$message.error('仓库ID不存在')
        return
      }
      
      console.log('开始获取仓库信息，ID:', id)
      
      // 添加本地loading指示器
      const loading = this.$loading({
        lock: true,
        text: '加载仓库信息...',
        spinner: 'el-icon-loading',
        background: 'rgba(255, 255, 255, 0.7)'
      })
      
      // 设置请求超时
      const timeout = setTimeout(() => {
        loading.close()
        this.$message.error('获取仓库信息超时，请重试')
      }, 15000)
      
      // 尝试使用原始API函数
      getWarehouse(id)
        .then(response => {
          clearTimeout(timeout)
          console.log('获取到仓库信息响应:', response)
          
          if (response && response.data) {
            console.log('仓库信息数据:', response.data)
            this.warehouseInfo = response.data
          } else {
            // 尝试直接使用返回的数据
            console.log('直接使用返回的数据:', response)
            if (response && typeof response === 'object' && Object.keys(response).length > 0) {
              this.warehouseInfo = response
            } else {
              this.$message.error('未获取到仓库信息')
              console.warn('仓库信息响应为空或格式不正确:', response)
              
              // 在开发模式下使用模拟数据
              if (process.env.NODE_ENV !== 'production') {
                console.log('使用模拟数据')
                this.warehouseInfo = {
                  name: '测试仓库',
                  code: 'WH-001',
                  contact_person: '测试联系人',
                  contact_phone: '13800138000',
                  address: '测试地址',
                  is_active: true
                }
              }
            }
          }
        })
        .catch(error => {
          clearTimeout(timeout)
          console.error('获取仓库信息失败:', error)
          this.$message.error('获取仓库信息失败：' + (error.message || '未知错误'))
          
          // 使用备用方法重试
          this.fetchWarehouseInfoFallback(id)
        })
        .finally(() => {
          clearTimeout(timeout)
          loading.close()
        })
    },
    
    // 备用方法，直接使用request而不是API函数
    fetchWarehouseInfoFallback(id) {
      console.log('使用备用方法获取仓库信息:', id)
      
      const loading = this.$loading({
        lock: true,
        text: '重新获取仓库信息...',
        spinner: 'el-icon-loading',
        background: 'rgba(255, 255, 255, 0.7)'
      })
      
      request({
        url: `/api/v1/warehouse/${id}/`,
        method: 'get'
      })
        .then(response => {
          console.log('备用方法获取到仓库信息:', response)
          
          if (response && typeof response === 'object') {
            this.warehouseInfo = response
          } else {
            console.warn('备用方法获取的数据格式不正确:', response)
            
            // 使用模拟数据
            this.warehouseInfo = {
              name: '测试仓库(备用)',
              code: 'WH-001',
              contact_person: '测试联系人',
              contact_phone: '13800138000',
              address: '测试地址',
              is_active: true
            }
          }
        })
        .catch(error => {
          console.error('备用方法获取仓库信息失败:', error)
          this.$message.error('重试获取仓库信息失败，将使用模拟数据')
          
          // 使用模拟数据
          this.warehouseInfo = {
            name: '测试仓库(模拟)',
            code: 'WH-001',
            contact_person: '测试联系人',
            contact_phone: '13800138000',
            address: '测试地址',
            is_active: true
          }
        })
        .finally(() => {
          loading.close()
        })
    },
    fetchReportData() {
      if (!this.$route.params.id) {
        this.$message.error('仓库ID不存在')
        this.loadError = true
        return
      }
      
      this.loading = true
      this.loadError = false
      this.inboundList = []
      this.outboundList = []
      this.inventoryList = []
      
      // 设置请求超时，确保loading状态会被清除
      const loadingTimeout = setTimeout(() => {
        this.loading = false
        this.loadError = true
        this.$message.error('获取报表数据超时，请重试')
      }, 20000)
      
      const params = {
        warehouse_id: this.$route.params.id,
        month: this.selectedMonth,
        format: 'json'
      }
      
      console.log('开始获取月度报表数据:', params)
      
      getMonthlyReport(params)
        .then(response => {
          clearTimeout(loadingTimeout)
          console.log('获取到月度报表数据:', response)
          
          // 检查响应格式是否正确
          if (response && response.inbound !== undefined) {
            // 处理入库数据
            if (Array.isArray(response.inbound)) {
              // 确保所有入库记录日期在所选月份内
              response.inbound.forEach(item => {
                if (item.日期) {
                  item.日期 = this.ensureDateInSelectedMonth(item.日期)
                }
                // 确保规格/型号字段为字符串类型
                if (item['规格/型号'] !== undefined && typeof item['规格/型号'] !== 'string') {
                  item['规格/型号'] = String(item['规格/型号'] || '')
                }
                // 确保品项字段为字符串类型
                if (item.品项 !== undefined && typeof item.品项 !== 'string') {
                  item.品项 = String(item.品项 || '')
                }
              })
              this.inboundList = response.inbound
              console.log(`入库数据: ${this.inboundList.length}条`)
            }
            
            // 处理出库数据
            if (Array.isArray(response.outbound)) {
              // 确保所有出库记录日期在所选月份内
              response.outbound.forEach(item => {
                if (item.日期) {
                  item.日期 = this.ensureDateInSelectedMonth(item.日期)
                }
                // 确保规格/型号字段为字符串类型
                if (item['规格/型号'] !== undefined && typeof item['规格/型号'] !== 'string') {
                  item['规格/型号'] = String(item['规格/型号'] || '')
                }
                // 确保品项字段为字符串类型
                if (item.品项 !== undefined && typeof item.品项 !== 'string') {
                  item.品项 = String(item.品项 || '')
                }
              })
              this.outboundList = response.outbound
              console.log(`出库数据: ${this.outboundList.length}条`)
            }
            
            // 处理库存数据
            if (Array.isArray(response.inventory)) {
              // 确保类型正确
              response.inventory.forEach(item => {
                // 确保规格/型号字段为字符串类型
                if (item['规格/型号'] !== undefined && typeof item['规格/型号'] !== 'string') {
                  item['规格/型号'] = String(item['规格/型号'] || '')
                }
                // 确保品项字段为字符串类型
                if (item.品项 !== undefined && typeof item.品项 !== 'string') {
                  item.品项 = String(item.品项 || '')
                }
              })
              this.inventoryList = response.inventory
              console.log(`库存数据: ${this.inventoryList.length}条`)
            }
            
            // 加载数据后立即创建备份
            this.createDataBackup()
            
            // 加载数据后立即强制执行一次统计更新
            this.$nextTick(() => {
              console.log('数据加载完成，立即执行统计更新...')
              this.updateInventoryStatistics(false) // 传入false参数表示不显示通知
              
              // 强制UI刷新
              this.forceSyncInventoryTable()
            })
            
            // 检查是否所有列表都为空
            if (this.inboundList.length === 0 && this.outboundList.length === 0 && this.inventoryList.length === 0) {
              this.$message.info('当前月份暂无数据，您可以点击"新增"按钮添加数据')
            }
            
            // 清除错误状态
            this.loadError = false
          } else {
            console.warn('API返回的数据格式不正确:', response)
            this.$message.warning('获取数据格式不正确，请联系管理员')
            this.loadError = true
          }
        })
        .catch(error => {
          clearTimeout(loadingTimeout)
          console.error('获取报表数据失败:', error)
          this.$message.error('获取报表数据失败: ' + (error.message || '未知错误'))
          this.loadError = true
        })
        .finally(() => {
          clearTimeout(loadingTimeout)
          this.loading = false
        })
    },
    handleExport() {
      if (!this.selectedMonth) {
        this.$message.warning('请先选择月份')
        return
      }
      
      this.loading = true
      
      const params = {
        warehouse_id: this.$route.params.id,
        month: this.selectedMonth,
        format: 'excel'
      }
      
      getMonthlyReport(params)
        .then(response => {
          // 直接创建下载链接
          const blob = new Blob([response], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
          const link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          
          // 获取仓库名称
          const warehouseName = this.warehouseInfo.name || '仓库'
          
          // 组装文件名
          const fileName = `${warehouseName}_月度报表_${this.selectedMonth.replace('-', '年')}月.xlsx`
          link.download = fileName
          link.click()
          
          this.$message.success('导出成功')
        })
        .catch(error => {
          console.error('导出月度报表失败:', error)
          this.$message.error('导出月度报表失败：' + (error.message || '未知错误'))
        })
        .finally(() => {
          this.loading = false
        })
    },
    
    // 新增记录
    handleAdd(type) {
      this.dialogStatus = 'create'
      this.currentIndex = -1
      
      // 根据选择的月份生成默认日期（月份的第一天）
      const defaultDate = this.getDefaultDateForSelectedMonth()
      
      if (type === 'inbound') {
        this.currentRecord = {
          日期: defaultDate,
          品项: '',
          '规格/型号': '',
          单位: '',
          数量: 0,
          单价: 0,
          经手人: ''
        }
        this.inboundDialogVisible = true
      } else if (type === 'outbound') {
        this.currentRecord = {
          日期: defaultDate,
          品项: '',
          '规格/型号': '',
          单位: '',
          数量: 0,
          单价: 0,
          经手人: ''
        }
        this.outboundDialogVisible = true
      } else if (type === 'inventory') {
        this.currentRecord = {
          位置: '',
          品项: '',
          '规格/型号': '',
          单位: '',
          期初库存: 0,
          累计入库: 0,
          累计出库: 0,
          单价: 0
        }
        this.inventoryDialogVisible = true
      }
    },
    
    // 根据选择的月份返回默认日期
    getDefaultDateForSelectedMonth() {
      if (!this.selectedMonth) {
        return this.getCurrentDay()
      }
      
      // 解析选择的月份（格式为YYYY-MM）
      const [year, month] = this.selectedMonth.split('-')
      
      // 创建所选月份的第15天作为默认日期（月中）
      return `${year}-${month}-15`
    },
    
    // 编辑记录
    handleEdit(type, row, index) {
      this.dialogStatus = 'update'
      this.currentIndex = index
      
      if (type === 'inbound') {
        this.currentRecord = { ...row }
        this.inboundDialogVisible = true
      } else if (type === 'outbound') {
        this.currentRecord = { ...row }
        this.outboundDialogVisible = true
      } else if (type === 'inventory') {
        this.currentRecord = { ...row }
        this.inventoryDialogVisible = true
      }
    },
    
    // 删除记录
    handleDelete(type, row, index) {
      if (type === 'inventory') {
        const itemName = row.品项?.trim() || ''
        const spec = row['规格/型号']?.trim() || ''
        
        // 检查是否是最后一条相同品项的记录
        const sameItems = this.inventoryList.filter(item => {
          const currentItemName = item.品项?.trim() || ''
          const currentSpec = item['规格/型号']?.trim() || ''
          return currentItemName === itemName && currentSpec === spec
        })
        
        if (sameItems.length === 1) {
          // 如果是最后一条记录，显示特殊警告
          this.$confirm(
            `警告：这是该品项的最后一条记录，删除后将无法显示该品项的库存信息。确定要删除吗？\n\n品项：${itemName}\n规格：${spec}`,
            '删除警告',
            {
              confirmButtonText: '确定删除',
              cancelButtonText: '取消',
              type: 'error'
            }
          ).then(() => {
            this.executeDelete(type, row, index)
          }).catch(() => {
            this.$message.info('已取消删除')
          })
        } else {
          // 正常删除确认
          this.$confirm(
            `确认删除该记录吗？\n品项：${itemName}\n规格：${spec}`,
            '删除确认',
            {
              confirmButtonText: '确定',
              cancelButtonText: '取消',
              type: 'warning'
            }
          ).then(() => {
            this.executeDelete(type, row, index)
          }).catch(() => {
            this.$message.info('已取消删除')
          })
        }
      } else {
        // 其他类型的删除（入库、出库）
        this.$confirm('确认删除该记录?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.executeDelete(type, row, index)
        }).catch(() => {
          this.$message.info('已取消删除')
        })
      }
    },

    // 执行删除操作
    executeDelete(type, row, index) {
      try {
        // 在删除前创建完整备份
        this.createDataBackup()
        
        if (type === 'inventory') {
          // 记录删除前的库存数量
          const beforeCount = this.inventoryList.length
          
          // 保存被删除的记录到历史记录中
          const deletedItem = JSON.parse(JSON.stringify(this.inventoryList[index]))
          this.deleteHistory.push({
            type: 'inventory',
            item: deletedItem,
            timestamp: new Date().getTime()
          })
          this.lastDeleteTime = new Date().getTime()
          
          // 记录详细信息用于调试
          console.log(`准备删除库存项: 索引=${index}, 品项=${deletedItem.品项}, 规格=${deletedItem['规格/型号']}`)
          
          // 只删除当前选中的记录
          this.inventoryList.splice(index, 1)
          
          // 记录删除后的库存数量
          const afterCount = this.inventoryList.length
          console.log(`删除完成: 删除前=${beforeCount}条, 删除后=${afterCount}条, 差异=${beforeCount - afterCount}条`)
          
          // 显示撤销选项
          const h = this.$createElement
          this.$notify({
            title: '删除成功',
            message: h('div', null, [
              h('span', null, '记录已删除 '),
              h('el-button', {
                props: {
                  type: 'text',
                  size: 'mini'
                },
                on: {
                  click: () => this.handleUndo()
                }
              }, '撤销')
            ]),
            type: 'success',
            duration: 5000
          })
        } else if (type === 'inbound') {
          this.inboundList.splice(index, 1)
          this.$message.success('删除成功')
        } else if (type === 'outbound') {
          this.outboundList.splice(index, 1)
          this.$message.success('删除成功')
        }
        
        // 更新库存统计
        this.updateInventoryStatistics(false)
        
        // 保存更改
        this.$nextTick(() => {
          this.saveReportData(true)
        })
      } catch (error) {
        console.error('删除操作失败:', error)
        this.$message.error('删除失败: ' + (error.message || '未知错误'))
        
        // 发生错误时尝试从备份恢复
        this.restoreFromBackup()
      }
    },

    // 撤销删除
    handleUndo() {
      try {
        if (this.deleteHistory.length > 0) {
          const lastDelete = this.deleteHistory[this.deleteHistory.length - 1]
          const currentTime = new Date().getTime()
          
          // 检查是否在5秒内的删除操作
          if (currentTime - lastDelete.timestamp <= 5000) {
            if (lastDelete.type === 'inventory') {
              // 恢复删除的记录
              this.inventoryList.push(lastDelete.item)
              this.deleteHistory.pop() // 移除已恢复的记录
              
              // 更新库存统计
              this.updateInventoryStatistics(false)
              
              // 保存更改
              this.$nextTick(() => {
                this.saveReportData(true)
              })
              
              this.$message.success('已恢复删除的记录')
            }
          } else {
            this.$message.warning('撤销时间已超过5秒，请使用恢复功能')
          }
        }
      } catch (error) {
        console.error('撤销操作失败:', error)
        this.$message.error('撤销失败: ' + (error.message || '未知错误'))
      }
    },

    // 恢复数据
    async handleRecover() {
      try {
        // 显示加载状态
        const loading = this.$loading({
          lock: true,
          text: '正在恢复数据...',
          spinner: 'el-icon-loading',
          background: 'rgba(255, 255, 255, 0.7)'
        })
        
        // 尝试从本地备份恢复
        if (this.backupTime) {
          // 计算备份时间与当前时间的差值（分钟）
          const backupAgeMinutes = (new Date().getTime() - this.backupTime) / (1000 * 60)
          
          // 如果备份时间在30分钟内，优先使用本地备份
          if (backupAgeMinutes <= 30) {
            const restored = this.restoreFromBackup()
            if (restored) {
              // 保存恢复的数据到服务器
              await this.saveReportData(true)
              loading.close()
              this.$message.success('已从本地备份恢复数据')
              return
            }
          }
        }
        
        // 如果本地备份不可用或太旧，则从服务器重新获取
        this.deleteHistory = []
        this.lastDeleteTime = null
        
        // 重新获取报表数据
        await this.fetchReportData()
        
        loading.close()
        this.$message.success('已从服务器恢复数据')
      } catch (error) {
        console.error('恢复数据失败:', error)
        this.$message.error('恢复数据失败: ' + (error.message || '未知错误'))
      }
    },
    
    // 获取当前日期
    getCurrentDay() {
      const date = new Date()
      const year = date.getFullYear()
      const month = (date.getMonth() + 1).toString().padStart(2, '0')
      const day = date.getDate().toString().padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    
    // 提交入库表单
    submitInboundForm() {
      this.$refs.inboundForm.validate(valid => {
        if (valid) {
          // 确保日期在所选月份范围内
          this.currentRecord.日期 = this.ensureDateInSelectedMonth(this.currentRecord.日期)
          
          // 计算金额
          this.currentRecord.金额 = this.currentRecord.数量 * this.currentRecord.单价
          
          const isNewRecord = this.dialogStatus === 'create';
          const recordDescription = isNewRecord ? 
            `添加新入库记录: 品项=${this.currentRecord.品项}, 规格=${this.currentRecord['规格/型号']}, 数量=${this.currentRecord.数量}` :
            `更新入库记录: 品项=${this.currentRecord.品项}, 规格=${this.currentRecord['规格/型号']}, 数量=${this.currentRecord.数量}`;
          
          console.log('准备保存入库记录:', recordDescription);
          
          if (isNewRecord) {
            this.inboundList.push({ ...this.currentRecord })
          } else {
            this.inboundList.splice(this.currentIndex, 1, { ...this.currentRecord })
          }
          
          // 关闭对话框
          this.inboundDialogVisible = false
          
          // 立即强制执行一次库存统计
          console.log('入库表单提交成功，立即更新库存统计...')
          this.updateInventoryStatistics(true) // 显示通知
          
          // 确保UI更新后再保存数据到服务器
          this.$nextTick(() => {
            // 保存数据
            this.saveReportData(true).then(() => {
              // 保存完成后执行后续操作
              this.$message.success(`成功${isNewRecord ? '添加' : '更新'}入库记录并更新库存数据`);
              
              // 延迟切换到库存标签页，让用户先看到成功消息
              setTimeout(() => {
                // 切换到库存明细标签
                this.activeTab = 'inventory'
                
                // 重新获取一次报表数据，确保数据完整性
                // this.fetchReportData() // 这样会导致所有数据重新加载，不够高效
                
                // 强制再进行一次库存统计和UI更新
                setTimeout(() => {
                  this.updateInventoryStatistics(false)
                  this.forceSyncInventoryTable()
                  console.log('入库操作完成，已更新库存统计并切换到库存标签页')
                }, 300)
              }, 1000) // 延迟1秒切换，让用户看到提示
            }).catch(error => {
              console.error('保存入库数据失败:', error)
              this.$message.error('保存入库数据失败: ' + (error.message || '未知错误'))
            })
          })
        } else {
          return false
        }
      })
    },
    
    // 提交出库表单
    submitOutboundForm() {
      this.$refs.outboundForm.validate(valid => {
        if (valid) {
          // 确保日期在所选月份范围内
          this.currentRecord.日期 = this.ensureDateInSelectedMonth(this.currentRecord.日期)
          
          // 计算金额
          this.currentRecord.金额 = this.currentRecord.数量 * this.currentRecord.单价
          
          if (this.dialogStatus === 'create') {
            this.outboundList.push({ ...this.currentRecord })
          } else {
            this.outboundList.splice(this.currentIndex, 1, { ...this.currentRecord })
          }
          
          // 先更新库存统计，然后再保存
          this.updateInventoryStatistics(false)
          
          // 关闭对话框
          this.outboundDialogVisible = false
          
          // 保存数据并在保存完成后切换到库存标签页
          this.$nextTick(() => {
            this.saveReportData(true).then(() => {
              // 保存完成后切换到库存明细标签
              this.activeTab = 'inventory'
            })
          })
        } else {
          return false
        }
      })
    },
    
    // 提交库存表单
    submitInventoryForm() {
      this.$refs.inventoryForm.validate(valid => {
        if (valid) {
          // 计算库存和库存金额
          this.currentRecord.库存 = Number(this.currentRecord.期初库存) + Number(this.currentRecord.累计入库) - Number(this.currentRecord.累计出库)
          this.currentRecord.库存金额 = this.currentRecord.库存 * this.currentRecord.单价
          
          if (this.dialogStatus === 'create') {
            this.inventoryList.push({ ...this.currentRecord })
          } else {
            this.inventoryList.splice(this.currentIndex, 1, { ...this.currentRecord })
          }
          
          this.saveReportData()
          this.inventoryDialogVisible = false
        } else {
          return false
        }
      })
    },
    
    // 保存报表数据
    saveReportData(skipStatistics = false) {
      this.loading = true
      
      // 记录保存前的数据量
      const beforeSaveCount = {
        inbound: this.inboundList.length,
        outbound: this.outboundList.length,
        inventory: this.inventoryList.length
      }
      console.log('保存前数据量:', beforeSaveCount)
      
      // 在保存前合并相同品项
      if (!skipStatistics) {
        this.mergeInventoryItems()
      }
      
      // 安全检查：确保合并后的数据不会导致大量数据丢失
      if (beforeSaveCount.inventory > 10 && this.inventoryList.length < beforeSaveCount.inventory * 0.7) {
        console.error(`警告: 保存前检测到数据可能丢失! 保存前: ${beforeSaveCount.inventory}条, 当前: ${this.inventoryList.length}条`)
        this.$message.error('检测到数据可能丢失，已取消保存操作')
        this.loading = false
        
        // 尝试从备份恢复
        if (this.backupTime) {
          this.$confirm('检测到数据可能丢失，是否从备份恢复?', '数据异常', {
            confirmButtonText: '从备份恢复',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.restoreFromBackup()
          }).catch(() => {
            this.$message.info('已取消恢复操作')
          })
        }
        
        return Promise.reject(new Error('检测到数据可能丢失，已取消保存操作'))
      }
      
      // 在保存前确保所有入库和出库记录的日期都在所选月份范围内
      this.inboundList.forEach(item => {
        item.日期 = this.ensureDateInSelectedMonth(item.日期)
        if (!item.id) {
          item.id = 'in_' + Date.now() + '_' + Math.floor(Math.random() * 10000)
        }
      })
      
      this.outboundList.forEach(item => {
        item.日期 = this.ensureDateInSelectedMonth(item.日期)
        if (!item.id) {
          item.id = 'out_' + Date.now() + '_' + Math.floor(Math.random() * 10000)
        }
      })
      
      this.inventoryList.forEach(item => {
        if (!item.id) {
          item.id = 'inv_' + Date.now() + '_' + Math.floor(Math.random() * 10000)
        }
      })
      
      const params = {
        warehouse_id: this.$route.params.id,
        month: this.selectedMonth,
        data: {
          inbound: this.inboundList,
          outbound: this.outboundList,
          inventory: this.inventoryList
        }
      }
      
      console.log('保存报表数据:', params)
      
      // 记录当前数据状态，用于判断是否需要重新加载
      const currentInventoryData = JSON.stringify(this.inventoryList)
      const currentInventoryMap = new Map();
      
      // 创建库存数据的映射，方便后续合并
      this.inventoryList.forEach(item => {
        if (item.品项 && item['规格/型号']) {
          // 使用安全的字符串处理
          const itemName = typeof item.品项 === 'string' ? item.品项.trim() : String(item.品项 || '');
          const spec = typeof item['规格/型号'] === 'string' ? item['规格/型号'].trim() : String(item['规格/型号'] || '');
          const key = `${itemName}|${spec}`;
          currentInventoryMap.set(key, item);
        }
      });
      
      // 返回Promise以支持链式调用
      return new Promise((resolve, reject) => {
        updateMonthlyReport(params)
          .then(response => {
            console.log('保存报表数据成功:', response)
            this.$message.success('保存成功')
            
            // 保存成功后创建新的备份
            this.createDataBackup()
            
            // 仅在必要时重新加载数据，优先保留当前计算的库存数据
            if (response && response.data) {
              console.log('服务器返回了更新后的数据')
              
              // 更新入库和出库数据，但确保日期始终在所选月份内
              if (response.data.inbound) {
                // 确保所有入库记录日期在所选月份内
                response.data.inbound.forEach(item => {
                  item.日期 = this.ensureDateInSelectedMonth(item.日期)
                })
                this.inboundList = response.data.inbound
                console.log('更新入库数据，条数:', this.inboundList.length)
              }
              
              if (response.data.outbound) {
                // 确保所有出库记录日期在所选月份内
                response.data.outbound.forEach(item => {
                  item.日期 = this.ensureDateInSelectedMonth(item.日期)
                })
                this.outboundList = response.data.outbound
                console.log('更新出库数据，条数:', this.outboundList.length)
              }
              
              // 服务器返回的库存数据可能不包含最新的统计结果
              // 这里改为更保守的策略，保留前端统计的结果，只接收新的库存记录
              if (response.data.inventory) {
                console.log('收到服务器返回的库存数据，条数:', response.data.inventory.length)
                
                // 安全检查：确保服务器返回的数据不会导致大量数据丢失
                if (this.inventoryList.length > 10 && response.data.inventory.length < this.inventoryList.length * 0.7) {
                  console.error(`警告: 服务器返回的数据可能不完整! 本地: ${this.inventoryList.length}条, 服务器: ${response.data.inventory.length}条`)
                  this.$message.warning('服务器返回的数据可能不完整，将保留本地数据')
                  
                  // 不使用服务器返回的数据，保留本地数据
                  resolve()
                  return
                }
                
                // 创建一个Map来存储唯一的库存项
                const uniqueInventoryMap = new Map()
                
                // 首先处理本地数据
                this.inventoryList.forEach(item => {
                  if (item.品项 && item['规格/型号']) {
                    const itemName = typeof item.品项 === 'string' ? item.品项.trim() : String(item.品项 || '')
                    const spec = typeof item['规格/型号'] === 'string' ? item['规格/型号'].trim() : String(item['规格/型号'] || '')
                    const key = `${itemName}|${spec}`
                    uniqueInventoryMap.set(key, item)
                  }
                })
                
                // 然后处理服务器返回的数据，只添加本地不存在的项
                response.data.inventory.forEach(serverItem => {
                  if (serverItem.品项 && serverItem['规格/型号']) {
                    const itemName = typeof serverItem.品项 === 'string' ? serverItem.品项.trim() : String(serverItem.品项 || '')
                    const spec = typeof serverItem['规格/型号'] === 'string' ? serverItem['规格/型号'].trim() : String(serverItem['规格/型号'] || '')
                    const key = `${itemName}|${spec}`
                    
                    // 只有当本地没有这个库存项时才添加
                    if (!uniqueInventoryMap.has(key)) {
                      uniqueInventoryMap.set(key, serverItem)
                    }
                  }
                })
                
                // 将Map转换回数组
                this.inventoryList = Array.from(uniqueInventoryMap.values())
                console.log('合并库存数据后，总条数:', this.inventoryList.length)
              }
              
              // 确保统计与最新数据一致
              this.$nextTick(() => {
                console.log('保存后，立即重新执行一次统计更新...')
                this.updateInventoryStatistics(false)
                
                // 确保UI更新
                this.forceSyncInventoryTable()
              })
            }
            
            // 完成后解析Promise
            resolve()
          })
          .catch(error => {
            console.error('保存报表数据失败:', error)
            
            // 特殊处理403权限错误
            if (error.response && error.response.status === 403) {
              this.$message.error('权限不足：您的账号级别无法执行此操作，请联系管理员升级权限')
            } else {
              this.$message.error('保存报表数据失败: ' + (error.message || '未知错误'))
            }
            
            // 失败后拒绝Promise
            reject(error)
          })
          .finally(() => {
            this.loading = false
          })
      })
    },
    
    // 添加库存统计方法
    updateInventoryStatistics(showNotification = true) {
      try {
        console.log('【库存统计开始】当前选择月份:', this.selectedMonth)
        
        // 先合并相同品项
        this.mergeInventoryItems()
        
        // 重新计算入库和出库统计
        const inboundMap = new Map()
        const outboundMap = new Map()
        
        // 添加一个安全trim函数
        const safeTrim = (value) => {
          if (typeof value === 'string') {
            return value.trim()
          }
          return value ? String(value) : ''
        }
        
        // 添加详细品项调试：记录所有品项
        console.log('========== 调试：所有入库品项 ==========')
        this.inboundList.forEach((item, idx) => {
          console.log(`入库记录[${idx}]: 品项='${item.品项}' 规格='${item['规格/型号']}' 数量=${item.数量} 日期=${item.日期}`)
          // 检查是否有额外空格
          if(typeof item.品项 === 'string' && item.品项.trim() !== item.品项) {
            console.log(`警告: 品项'${item.品项}'含有前后空格`)
          }
          if(typeof item['规格/型号'] === 'string' && item['规格/型号'].trim() !== item['规格/型号']) {
            console.log(`警告: 规格'${item['规格/型号']}'含有前后空格`)
          }
        })
        
        // 记录当前库存品项
        console.log('========== 调试：所有库存品项 ==========')
        this.inventoryList.forEach((item, idx) => {
          console.log(`库存记录[${idx}]: 品项='${item.品项}' 规格='${item['规格/型号']}' 期初=${item.期初库存} 累计入库=${item.累计入库}`)
        })
        
        // 根据当前选择的月份，重新统计所有库存数据
        // 清晰明了地输出入库和库存的对应关系
        
        // 第一步：先将入库数据按品项+型号分组，计算每组的入库总量
        // 对入库数据分组计算
        this.inboundList.forEach((item, index) => {
          if (!item) return // 跳过空记录
          const itemName = safeTrim(item.品项)
          const spec = safeTrim(item['规格/型号'])
          if (!itemName) return // 跳过无品项的记录
          
          const key = `${itemName}|${spec}`
          
          console.log(`处理入库记录[${index}]: 生成Key='${key}'`)
          
          // 特别检查"套管"
          if(itemName.includes('套管')) {
            console.log(`发现套管入库记录: 原始品项='${item.品项}' 规格='${item['规格/型号']}' 处理后Key='${key}'`)
          }
          
          if (!inboundMap.has(key)) {
            inboundMap.set(key, {
              品项: itemName,
              '规格/型号': spec,
              单位: item.单位 || '个',
              总入库量: 0,
              单价: Number(item.单价 || 0)
            })
            console.log(`创建新入库统计项: key='${key}'`)
          }
          
          const mapItem = inboundMap.get(key)
          const quantity = parseInt(item.数量 || 0)
          mapItem.总入库量 += quantity
          
          if (quantity > 0) {
            mapItem.单价 = Number(item.单价 || 0)
          }
          
          console.log(`【处理入库】序号:${index+1}, 品项:'${itemName}', 规格:'${spec}', 数量:${quantity}, 累计:${mapItem.总入库量}`)
        })
        
        // 打印inboundMap内容
        console.log('========== 调试：入库统计结果 ==========')
        inboundMap.forEach((value, key) => {
          console.log(`统计Key='${key}': 品项='${value.品项}' 规格='${value['规格/型号']}' 总入库量=${value.总入库量}`)
        })
        
        console.log(`【入库统计】完成统计${inboundMap.size}个不同品项的入库数据`)
        
        // 第二步：对出库数据分组计算
        this.outboundList.forEach((item, index) => {
          if (!item) return // 跳过空记录
          const itemName = safeTrim(item.品项)
          const spec = safeTrim(item['规格/型号'])
          if (!itemName) return // 跳过无品项的记录
          
          const key = `${itemName}|${spec}`
          
          if (!outboundMap.has(key)) {
            outboundMap.set(key, {
              品项: itemName,
              '规格/型号': spec,
              总出库量: 0
            })
          }
          
          const mapItem = outboundMap.get(key)
          const quantity = parseInt(item.数量 || 0)
          mapItem.总出库量 += quantity
          
          console.log(`【处理出库】序号:${index+1}, 品项:'${itemName}', 规格:'${spec}', 数量:${quantity}, 累计:${mapItem.总出库量}`)
        })
        
        console.log(`【出库统计】完成统计${outboundMap.size}个不同品项的出库数据`)
        
        // 第三步：处理库存数据
        // 创建新的库存列表
        const newInventoryList = []
        const processedKeys = new Set() // 追踪已处理的品项
        
        // 首先处理现有库存数据
        this.inventoryList.forEach((item, index) => {
          if (!item) return // 跳过空记录
          
          const itemName = safeTrim(item.品项)
          const spec = safeTrim(item['规格/型号'])
          if (!itemName) return // 跳过无品项的记录
          
          const key = `${itemName}|${spec}`
          
          console.log(`处理库存[${index}]: 生成Key='${key}'`)
          
          // 特别检查"套管"
          if(itemName.includes('套管')) {
            console.log(`发现套管库存记录: 原始品项='${item.品项}' 规格='${item['规格/型号']}' 处理后Key='${key}'`)
          }
          
          // 记录处理前的数据，用于对比
          const oldData = {
            期初库存: parseInt(item.期初库存 || 0),
            累计入库: parseInt(item.累计入库 || 0),
            累计出库: parseInt(item.累计出库 || 0),
            库存: parseInt(item.库存 || 0)
          }
          
          // 创建新的库存记录，复制原始数据
          const newItem = { ...item }
          
          // 更新累计入库和累计出库
          if (inboundMap.has(key)) {
            // 直接使用统计的总入库量
            newItem.累计入库 = inboundMap.get(key).总入库量
            console.log(`【更新库存】品项:'${itemName}', 规格:'${spec}', 累计入库从${oldData.累计入库}更新为${newItem.累计入库}`)
            
            // 特别检查"套管"
            if(itemName.includes('套管')) {
              console.log(`套管库存更新: 从inboundMap找到key='${key}', 更新累计入库为${newItem.累计入库}`)
            }
          } else {
            // 如果没有入库数据，设置为0
            newItem.累计入库 = 0
            console.log(`【未入库】品项:'${itemName}', 规格:'${spec}'没有入库记录，累计入库设为0`)
            
            // 特别检查"套管"
            if(itemName.includes('套管')) {
              console.log(`警告: 套管库存记录未在inboundMap中找到匹配项! key='${key}'`)
              console.log(`inboundMap中的所有key:`)
              inboundMap.forEach((v, k) => console.log(`- '${k}'`))
            }
          }
          
          if (outboundMap.has(key)) {
            // 直接使用统计的总出库量
            newItem.累计出库 = outboundMap.get(key).总出库量
          } else {
            // 如果没有出库数据，设置为0
            newItem.累计出库 = 0
          }
          
          // 重新计算库存和库存金额
          newItem.库存 = parseInt(newItem.期初库存 || 0) + parseInt(newItem.累计入库 || 0) - parseInt(newItem.累计出库 || 0)
          newItem.库存金额 = newItem.库存 * parseFloat(newItem.单价 || 0)
          
          // 添加到新库存列表
          newInventoryList.push(newItem)
          
          // 标记为已处理
          processedKeys.add(key)
          
          // 输出库存更新详情
          console.log(`【库存结果】品项:'${itemName}', 规格:'${spec}', 期初:${newItem.期初库存}, 入库:${newItem.累计入库}, 出库:${newItem.累计出库}, 库存:${newItem.库存}`)
        })
        
        // 处理没有对应库存记录的入库数据（新增品项）
        inboundMap.forEach((inboundStats, key) => {
          if (!processedKeys.has(key)) {
            // 查找对应的出库数据
            let outboundQuantity = 0
            if (outboundMap.has(key)) {
              outboundQuantity = outboundMap.get(key).总出库量
            }
            
            // 创建新的库存记录
            const newItem = {
              id: 'inv_auto_' + Date.now() + '_' + Math.floor(Math.random() * 10000),
              位置: '',
              品项: inboundStats.品项,
              '规格/型号': inboundStats['规格/型号'],
              单位: inboundStats.单位,
              期初库存: 0,
              累计入库: inboundStats.总入库量,
              累计出库: outboundQuantity,
              库存: inboundStats.总入库量 - outboundQuantity,
              单价: inboundStats.单价,
              库存金额: (inboundStats.总入库量 - outboundQuantity) * inboundStats.单价
            }
            
            // 添加到新库存列表
            newInventoryList.push(newItem)
            
            // 标记为已处理
            processedKeys.add(key)
            
            console.log(`【新增库存】品项:'${inboundStats.品项}', 规格:'${inboundStats['规格/型号']}', 累计入库:${inboundStats.总入库量}, 库存:${newItem.库存}`)
            
            // 特别检查"套管"
            if(inboundStats.品项.includes('套管')) {
              console.log(`自动创建了套管的新库存记录: 品项='${inboundStats.品项}' 规格='${inboundStats['规格/型号']}' 累计入库=${inboundStats.总入库量}`)
            }
          }
        })
        
        // 处理只有出库没有入库的品项
        outboundMap.forEach((outboundStats, key) => {
          if (!processedKeys.has(key)) {
            // 创建新的库存记录
            const newItem = {
              id: 'inv_auto_' + Date.now() + '_' + Math.floor(Math.random() * 10000),
              位置: '',
              品项: outboundStats.品项,
              '规格/型号': outboundStats['规格/型号'],
              单位: '个',
              期初库存: 0,
              累计入库: 0,
              累计出库: outboundStats.总出库量,
              库存: -outboundStats.总出库量, // 可能是负数，因为没有入库
              单价: 0,
              库存金额: 0
            }
            
            // 添加到新库存列表
            newInventoryList.push(newItem)
            
            // 标记为已处理
            processedKeys.add(key)
            
            console.log(`【异常出库】品项:'${outboundStats.品项}', 无入库记录但有出库:${outboundStats.总出库量}`)
          }
        })
        
        // 替换原有库存列表
        this.inventoryList = newInventoryList
        
        console.log(`【库存更新完成】共更新${this.inventoryList.length}条库存记录`)
        
        // 强化UI更新机制
        this.forceSyncInventoryTable()
        
        // 显示通知
        if (showNotification) {
          this.$notify({
            title: '库存更新完成',
            message: `已更新${this.selectedMonth}月份的库存数据，包含${this.inventoryList.length}条记录`,
            type: 'success',
            duration: 3000
          })
        }
      } catch (error) {
        console.error('库存统计更新出错:', error)
        this.$message.error('库存统计更新失败: ' + error.message)
      }
    },
    
    // 新增强制同步库存表格方法
    forceSyncInventoryTable() {
      try {
        this.$nextTick(() => {
          // 获取库存表格的实例并刷新
          const inventoryTable = this.$el ? this.$el.querySelector('.el-tab-pane[label="库存明细"] .el-table') : null
          if (inventoryTable && inventoryTable.__vue__) {
            inventoryTable.__vue__.doLayout()
          }
          
          // 立即强制重新渲染
          this.$forceUpdate()
          
          // 使用延时确保DOM完全更新
          setTimeout(() => {
            this.$forceUpdate()
            
            // 如果当前不在库存标签页，强制切换一下
            if (this.activeTab !== 'inventory') {
              const oldTab = this.activeTab
              this.activeTab = 'inventory'
              
              // 强制切换回原来的标签，但确保数据已刷新
              setTimeout(() => {
                this.activeTab = oldTab
              }, 100)
            }
          }, 200)
        })
      } catch (error) {
        console.error('强制同步表格失败:', error)
      }
    },
    // 应用解析后的数据
    applyParsedData(inboundData, outboundData, inventoryData) {
      this.loading = true
      
      // 处理数据格式，确保包含必要字段
      const processedInbound = inboundData.map(item => {
        // 确保金额计算正确
        const amount = Number(item['数量'] || 0) * Number(item['单价'] || 0)
        // 确保日期在所选月份内
        const adjustedDate = this.ensureDateInSelectedMonth(item['日期'])
        return {
          ...item,
          日期: adjustedDate,
          金额: amount,
          id: 'in_' + Date.now() + '_' + Math.floor(Math.random() * 10000)
        }
      })
      
      const processedOutbound = outboundData.map(item => {
        const amount = Number(item['数量'] || 0) * Number(item['单价'] || 0)
        return {
          ...item,
          金额: amount,
          id: 'out_' + Date.now() + '_' + Math.floor(Math.random() * 10000)
        }
      })
      
      const processedInventory = inventoryData.map(item => {
        // 计算库存和库存金额
        const stock = Number(item['期初库存'] || 0) + Number(item['累计入库'] || 0) - Number(item['累计出库'] || 0)
        const stockAmount = stock * Number(item['单价'] || 0)
        return {
          ...item,
          库存: stock,
          库存金额: stockAmount,
          id: 'inv_' + Date.now() + '_' + Math.floor(Math.random() * 10000)
        }
      })
      
      // 替换当前数据
      this.inboundList = processedInbound
      this.outboundList = processedOutbound
      this.inventoryList = processedInventory
      
      // 在保存前更新库存统计数据
      this.updateInventoryStatistics()
      
      // 保存到服务器
      this.saveReportData()
      
      this.$message.success('Excel数据已成功应用')
    },
    retryLoading() {
      this.loadError = false
      this.fetchReportData()
    },
    // 处理文件导入
    handleImportFile(file) {
      if (!file) {
        return
      }
      
      // 检查文件类型
      const fileExtension = file.name.split('.').pop().toLowerCase()
      if (['xlsx', 'xls'].indexOf(fileExtension) < 0) {
        this.$message.error('请上传Excel文件(.xlsx或.xls)')
        return
      }
      
      // 检查文件大小，限制为10MB
      const isLt10M = file.size / 1024 / 1024 < 10
      if (!isLt10M) {
        this.$message.error('文件大小不能超过10MB')
        return
      }
      
      // 添加选项：是否使用服务器导入还是本地解析
      this.$confirm('请选择导入方式', '导入选项', {
        confirmButtonText: '服务器导入',
        cancelButtonText: '本地解析',
        distinguishCancelAndClose: true,
        type: 'info'
      }).then(() => {
        // 确认按钮，使用服务器导入
        this.uploadExcelFile(file)
      }).catch(action => {
        if (action === 'cancel') {
          // 取消按钮，使用本地解析
          this.parseExcelLocally(file)
        }
      })
    },
    
    // 上传Excel文件
    uploadExcelFile(file) {
      const loading = this.$loading({
        lock: true,
        text: '正在导入数据...',
        spinner: 'el-icon-loading',
        background: 'rgba(255, 255, 255, 0.7)'
      })
      
      const formData = new FormData()
      formData.append('file', file.raw)
      formData.append('warehouse_id', this.$route.params.id)
      formData.append('month', this.selectedMonth)
      
      console.log('开始导入Excel文件:', file.name)
      
      // 使用axios直接发送请求，避免request方法可能的问题
      axios({
        url: process.env.VUE_APP_BASE_API + '/api/v1/warehouse/import/',
        method: 'post',
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': 'Bearer ' + localStorage.getItem('token')
        }
      })
        .then(response => {
          console.log('导入成功:', response)
          this.$message.success('数据导入成功')
          
          // 刷新数据
          this.fetchReportData()
        })
        .catch(error => {
          console.error('导入失败:', error)
          
          // 尝试备用导入方法
          this.tryAlternativeImport(file)
        })
        .finally(() => {
          loading.close()
        })
    },
    
    // 添加备用导入方法
    tryAlternativeImport(file) {
      console.log('尝试使用备用方法导入文件')
      
      const loading = this.$loading({
        lock: true,
        text: '尝试备用导入方法...',
        spinner: 'el-icon-loading',
        background: 'rgba(255, 255, 255, 0.7)'
      })
      
      const formData = new FormData()
      formData.append('file', file.raw)
      formData.append('warehouse_id', this.$route.params.id)
      formData.append('month', this.selectedMonth)
      formData.append('multi_sheet', 'true') // 明确指定这是多sheet文件
      
      // 使用原始request方法发送
      request({
        url: '/api/v1/warehouse/import-multi-sheet/',
        method: 'post',
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
        .then(response => {
          console.log('备用方法导入成功:', response)
          this.$message.success('数据导入成功')
          
          // 刷新数据
          this.fetchReportData()
        })
        .catch(error => {
          console.error('备用方法导入失败:', error)
          
          // 提供更具体的错误信息以便于用户理解和解决问题
          let errorMsg = '导入失败: '
          
          if (error.response) {
            // 服务器返回了错误状态码
            const status = error.response.status
            if (status === 405) {
              errorMsg += 'API接口不支持POST方法，请联系管理员检查API配置'
            } else if (status === 413) {
              errorMsg += '文件过大，超出服务器接受限制'
            } else if (status === 400) {
              errorMsg += error.response.data.message || '请求参数错误，请检查Excel文件格式是否符合要求'
            } else if (status === 500) {
              errorMsg += '服务器内部错误，请联系管理员'
            } else {
              errorMsg += `服务器返回错误(${status}): ${error.response.data.message || '未知错误'}`
            }
          } else if (error.request) {
            // 请求发送成功但没有收到响应
            errorMsg += '服务器无响应，请检查网络连接或联系管理员'
          } else {
            // 请求配置有误
            errorMsg += error.message || '未知错误'
          }
          
          this.$message.error(errorMsg)
          
          // 添加额外提示
          this.$notify({
            title: '导入建议',
            message: '请确保Excel文件有3个工作表，分别命名为"入库明细"、"出库明细"和"库存明细"，并符合导入模板格式',
            type: 'info',
            duration: 8000
          })
        })
        .finally(() => {
          loading.close()
        })
    },
    
    // 修改下载模板方法，确保生成的模板符合要求
    downloadTemplate() {
      const loading = this.$loading({
        lock: true,
        text: '正在生成模板...',
        spinner: 'el-icon-loading',
        background: 'rgba(255, 255, 255, 0.7)'
      })
      
      const warehouseId = this.$route.params.id
      
      // 添加参数指定需要多sheet模板
      exportTemplate(warehouseId)
        .then(response => {
          const blob = new Blob([response], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
          const link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          link.download = `仓库月度报表导入模板.xlsx`
          link.click()
          
          this.$message.success('模板下载成功')
          
          // 添加使用指南提示
          this.$notify({
            title: '模板使用指南',
            message: '下载的Excel模板包含3个工作表，分别对应入库明细、出库明细和库存明细。请按照模板格式填写数据后再导入。',
            type: 'info',
            duration: 10000
          })
        })
        .catch(error => {
          console.error('模板下载失败:', error)
          this.$message.error('模板下载失败: ' + (error.message || '未知错误'))
          
          // 尝试备用方法下载模板
          this.downloadTemplateFallback(warehouseId)
        })
        .finally(() => {
          loading.close()
        })
    },
    
    // 添加备用模板下载方法
    downloadTemplateFallback(warehouseId) {
      const loading = this.$loading({
        lock: true,
        text: '尝试备用方法下载模板...',
        spinner: 'el-icon-loading',
        background: 'rgba(255, 255, 255, 0.7)'
      })
      
      // 直接使用axios下载
      axios({
        url: process.env.VUE_APP_BASE_API + `/api/v1/warehouse/${warehouseId}/export-template/`,
        method: 'get',
        responseType: 'blob',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('token')
        }
      })
        .then(response => {
          const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
          const link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          link.download = `仓库月度报表导入模板.xlsx`
          link.click()
          
          this.$message.success('模板下载成功')
        })
        .catch(error => {
          console.error('备用方法模板下载失败:', error)
          this.$message.error('模板下载失败，请联系管理员')
        })
        .finally(() => {
          loading.close()
        })
    },
    // 修改parseExcelLocally方法
    parseExcelLocally(file) {
      const loading = this.$loading({
        lock: true,
        text: '正在解析Excel文件...',
        spinner: 'el-icon-loading',
        background: 'rgba(255, 255, 255, 0.7)'
      });
      
      if (!XLSX) {
        loading.close();
        this.$message.error('解析库未正确加载，请刷新页面重试');
        console.error('XLSX库未加载:', XLSX);
        return;
      }

      console.log('准备解析Excel文件，XLSX库状态:', !!XLSX);

      const reader = new FileReader();
      
      reader.onload = e => {
        try {
          if (!e.target || !e.target.result) {
            throw new Error('文件读取失败，未获取到文件内容');
          }
          
          console.log('文件读取成功，开始解析...');
          const data = new Uint8Array(e.target.result);
          
          let workbook;
          try {
            workbook = XLSX.read(data, { type: 'array' });
          } catch (parseError) {
            console.error('Excel解析错误:', parseError);
            this.$message.error('Excel文件格式错误，请确保上传有效的Excel文件');
            loading.close();
            return;
          }
          
          if (!workbook || !workbook.SheetNames || workbook.SheetNames.length === 0) {
            this.$message.error('Excel文件结构无效，未找到任何工作表');
            loading.close();
            return;
          }
          
          console.log('找到工作表:', workbook.SheetNames);
          
          // 特别处理用户的Excel表格
          let inboundData = [];
          let outboundData = [];
          let inventoryData = [];
          
          // 处理第一个工作表作为入库数据
          if (workbook.SheetNames.length > 0) {
            try {
              const sheetName = workbook.SheetNames[0];
              const sheet = workbook.Sheets[sheetName];
              
              // 直接按照A-I列获取数据，跳过前面的标题行
              const rawData = XLSX.utils.sheet_to_json(sheet, {
                range: 3,
                header: "A"
              });
              
              // 转换列名和处理数据
              inboundData = rawData.map(row => {
                if (row.C) { // C列是品项，确保有数据
                  return {
                    日期: this.formatExcelDate(row.B), // B列是日期
                    品项: row.C,
                    '规格/型号': row.D || '',
                    单位: row.E || '个',
                    数量: this.convertToNumber(row.F || 0),
                    单价: this.convertToNumber(row.G || 0),
                    金额: this.convertToNumber(row.H || 0),
                    经手人: row.I || ''
                  };
                }
                return null;
              }).filter(item => item !== null);
              
              console.log(`从第一个工作表提取了${inboundData.length}条入库数据`);
            } catch(e) {
              console.error('处理入库数据出错:', e);
            }
          }
          
          // 处理第二个工作表作为出库数据
          if (workbook.SheetNames.length > 1) {
            try {
              const sheetName = workbook.SheetNames[1];
              const sheet = workbook.Sheets[sheetName];
              
              // 同样按照A-I列获取数据
              const rawData = XLSX.utils.sheet_to_json(sheet, {
                range: 3,
                header: "A"
              });
              
              // 转换列名和处理数据
              outboundData = rawData.map(row => {
                if (row.C) { // C列是品项，确保有数据
                  return {
                    日期: this.formatExcelDate(row.B), // B列是日期
                    品项: row.C,
                    '规格/型号': row.D || '',
                    单位: row.E || '个',
                    数量: this.convertToNumber(row.F || 0),
                    单价: this.convertToNumber(row.G || 0),
                    金额: this.convertToNumber(row.H || 0),
                    经手人: row.I || ''
                  };
                }
                return null;
              }).filter(item => item !== null);
              
              console.log(`从第二个工作表提取了${outboundData.length}条出库数据`);
            } catch(e) {
              console.error('处理出库数据出错:', e);
            }
          }
          
          // 处理第三个工作表作为库存数据
          if (workbook.SheetNames.length > 2) {
            try {
              const sheetName = workbook.SheetNames[2];
              const sheet = workbook.Sheets[sheetName];
              
              // 按照A-K列获取数据
              const rawData = XLSX.utils.sheet_to_json(sheet, {
                range: 3,
                header: "A"
              });
              
              // 转换列名和处理数据
              inventoryData = rawData.map(row => {
                if (row.C) { // C列是品项，确保有数据
                  return {
                    位置: row.B || '',
                    品项: row.C,
                    '规格/型号': row.D || '',
                    单位: row.E || '个',
                    期初库存: this.convertToNumber(row.F || 0),
                    累计入库: this.convertToNumber(row.G || 0),
                    累计出库: this.convertToNumber(row.H || 0),
                    库存: this.convertToNumber(row.I || 0),
                    单价: this.convertToNumber(row.J || 0),
                    库存金额: this.convertToNumber(row.K || 0)
                  };
                }
                return null;
              }).filter(item => item !== null);
              
              console.log(`从第三个工作表提取了${inventoryData.length}条库存数据`);
            } catch(e) {
              console.error('处理库存数据出错:', e);
            }
          }
          
          loading.close();
          
          if (inboundData.length > 0 || outboundData.length > 0 || inventoryData.length > 0) {
            // 数据有效，提示用户确认是否应用
            this.$confirm(`已成功解析Excel文件，发现入库记录${inboundData.length}条，出库记录${outboundData.length}条，库存记录${inventoryData.length}条。是否应用到当前报表?`, '确认', {
              confirmButtonText: '确定',
              cancelButtonText: '取消',
              type: 'warning'
            }).then(() => {
              // 应用解析后的数据
              this.applyParsedData(inboundData, outboundData, inventoryData);
            }).catch(() => {
              this.$message.info('已取消导入');
            });
          } else {
            this.$message.warning('未能从Excel文件中提取有效数据。请确保Excel的工作表顺序为：入库、出库、库存，且每个表从第4行开始有数据。');
          }
        } catch (error) {
          loading.close();
          console.error('Excel解析过程出错:', error);
          this.$message.error('解析Excel文件失败:' + error.message);
        }
      };
      
      reader.onerror = error => {
        loading.close();
        console.error('文件读取错误:', error);
        this.$message.error('文件读取失败');
      };
      
      try {
        reader.readAsArrayBuffer(file.raw);
      } catch (error) {
        loading.close();
        console.error('启动文件读取失败:', error);
        this.$message.error('无法读取文件:' + error.message);
      }
    },
    
    // 添加日期格式化方法
    formatExcelDate(dateValue) {
      if (!dateValue) return this.getCurrentDay();
      
      try {
        // 如果是日期对象，转换为ISO字符串后提取日期部分
        if (dateValue instanceof Date) {
          return dateValue.toISOString().split('T')[0];
        }
        
        // 处理不同的日期格式
        const dateStr = String(dateValue);
        
        // 处理 "2025/1/13" 格式
        if (dateStr.includes('/')) {
          const parts = dateStr.split('/');
          if (parts.length === 3) {
            const year = parts[0].padStart(4, '20'); // 如果年份只有两位，前面加上"20"
            const month = parts[1].padStart(2, '0');
            const day = parts[2].padStart(2, '0');
            return `${year}-${month}-${day}`;
          }
        }
        
        // 处理 "2025-1-13" 格式
        if (dateStr.includes('-')) {
          const parts = dateStr.split('-');
          if (parts.length === 3) {
            const year = parts[0].padStart(4, '20');
            const month = parts[1].padStart(2, '0');
            const day = parts[2].padStart(2, '0');
            return `${year}-${month}-${day}`;
          }
        }
        
        // 尝试使用 Date 解析
        const date = new Date(dateStr);
        if (!isNaN(date.getTime())) {
          const year = date.getFullYear();
          const month = (date.getMonth() + 1).toString().padStart(2, '0');
          const day = date.getDate().toString().padStart(2, '0');
          return `${year}-${month}-${day}`;
        }
      } catch (e) {
        console.error('日期格式化错误:', e);
      }
      
      // 如果所有尝试都失败，返回当前日期
      return this.getCurrentDay();
    },
    // 数字转换辅助方法
    convertToNumber(value, defaultValue = null) {
      if (value === undefined || value === null || value === '') {
        return defaultValue
      }
      
      try {
        // 如果是字符串，去除可能的非数字字符
        if (typeof value === 'string') {
          // 移除可能的货币符号和分组分隔符
          value = value.replace(/[¥$,]/g, '')
        }
        
        const num = Number(value)
        return isNaN(num) ? defaultValue : num
      } catch (e) {
        console.error('数字转换错误:', e)
        return defaultValue
      }
    },
    handleUpdateStatistics() {
      this.updateInventoryStatistics()
    },
    // 确保日期在所选月份范围内
    ensureDateInSelectedMonth(dateStr) {
      if (!dateStr || !this.selectedMonth) {
        return dateStr
      }
      
      try {
        // 获取所选月份的年和月
        const [selectedYear, selectedMonth] = this.selectedMonth.split('-')
        
        // 从日期字符串中获取年、月、日
        const [year, month, day] = dateStr.split('-')
        
        // 如果月份不匹配，则调整日期到所选月份
        if (year !== selectedYear || month !== selectedMonth) {
          console.log(`调整日期: 从 ${dateStr} 到 ${selectedYear}-${selectedMonth} 月范围内`)
          
          // 获取所选月份的最后一天
          const lastDay = new Date(parseInt(selectedYear), parseInt(selectedMonth), 0).getDate()
          
          // 如果原日期的天数超过了所选月份的最后一天，则使用所选月份的最后一天
          const adjustedDay = Math.min(parseInt(day), lastDay).toString().padStart(2, '0')
          
          // 返回调整后的日期
          return `${selectedYear}-${selectedMonth}-${adjustedDay}`
        }
        
        return dateStr
      } catch (e) {
        console.error('日期调整错误:', e)
        return dateStr
      }
    },
    // 直接导出当前表格数据
    directExport() {
      this.loading = true
      this.loadingText = '正在导出数据...'
      
      try {
        console.log('开始直接导出库存数据')
        
        // 创建工作簿
        const workbook = XLSX.utils.book_new()
        
        // 处理库存数据，如果有的话
        if (this.inventoryList && this.inventoryList.length > 0) {
          console.log(`导出${this.inventoryList.length}条库存数据`)
          const inventoryWS = XLSX.utils.json_to_sheet(this.inventoryList)
          XLSX.utils.book_append_sheet(workbook, inventoryWS, '库存明细')
        } else {
          // 如果没有库存数据，检查其他数据
          console.log('库存数据为空，尝试导出其他数据')
        }
        
        // 尝试添加入库/出库数据
        if (this.inboundList && this.inboundList.length > 0) {
          console.log(`导出${this.inboundList.length}条入库数据`)
          const inboundWS = XLSX.utils.json_to_sheet(this.inboundList)
          XLSX.utils.book_append_sheet(workbook, inboundWS, '入库明细')
        }
        
        if (this.outboundList && this.outboundList.length > 0) {
          console.log(`导出${this.outboundList.length}条出库数据`)
          const outboundWS = XLSX.utils.json_to_sheet(this.outboundList)
          XLSX.utils.book_append_sheet(workbook, outboundWS, '出库明细')
        }
        
        // 确保有数据可以导出
        if (workbook.SheetNames.length === 0) {
          throw new Error('没有可导出的数据')
        }
        
        // 获取当前月份
        const now = new Date()
        const currentMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
        
        // 获取仓库名称或ID
        const warehouseName = this.warehouseName || `仓库${this.warehouseId}`
        
        // 生成Excel文件
        const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' })
        const blob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
        
        // 创建下载链接
        const link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = `${warehouseName}_${currentMonth}.xlsx`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        
        this.$message.success('导出数据成功')
      } catch (error) {
        console.error('本地导出Excel失败:', error)
        this.$message.error('导出失败: ' + (error.message || '未知错误'))
      } finally {
        this.loading = false
        this.loadingText = ''
      }
    },
    handleMonthlyInbound(row) {
      // 打开入库对话框并预填数据
      this.dialogStatus = 'create'
      this.currentRecord = {
        日期: this.getCurrentDay(),
        品项: row.品项,
        '规格/型号': row['规格/型号'],
        单位: row.单位,
        数量: 0,
        单价: row.单价 || 0,
        金额: 0,
        经手人: '',
        备注: '本月入库'
      }
      // 打开入库对话框
      this.inboundDialogVisible = true
      
      // 设置焦点到数量输入框（在下一个渲染循环中）
      this.$nextTick(() => {
        const numberInput = this.$refs.inboundForm.fields.find(field => field.prop === '数量')
        if (numberInput && numberInput.$el) {
          const inputElement = numberInput.$el.querySelector('input')
          if (inputElement) inputElement.focus()
        }
      })
    },
    
    handleMonthlyOutbound(row) {
      // 检查当前库存是否足够
      if (Number(row.库存) <= 0) {
        this.$message.warning('当前库存为0，无法进行出库操作')
        return
      }
      
      // 打开出库对话框并预填数据
      this.dialogStatus = 'create'
      this.currentRecord = {
        日期: this.getCurrentDay(),
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
      // 打开出库对话框
      this.outboundDialogVisible = true
      
      // 设置焦点到数量输入框（在下一个渲染循环中）
      this.$nextTick(() => {
        const numberInput = this.$refs.outboundForm.fields.find(field => field.prop === '数量')
        if (numberInput && numberInput.$el) {
          const inputElement = numberInput.$el.querySelector('input')
          if (inputElement) inputElement.focus()
        }
      })
    },
    /**
     * 更新当前月份的期初库存
     * 根据上月期末库存更新当前月的期初库存
     */
    async handleUpdateInitialStock() {
      try {
        // 计算当前库存总数
        const totalItems = this.inventoryList.reduce((sum, item) => sum + (parseInt(item.库存) || 0), 0)
        
        // 计算上月入库和出库总额
        const totalInbound = this.inboundList.reduce((sum, item) => sum + (parseFloat(item.金额) || 0), 0)
        const totalOutbound = this.outboundList.reduce((sum, item) => sum + (parseFloat(item.金额) || 0), 0)
        
        // 显示确认对话框
        await this.$confirm(
          `确定要更新${this.selectedMonth}月的期初库存吗？将使用上月的期末库存作为本月的期初库存。`,
          '更新期初库存',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        // 显示加载状态
        this.loading = true
        
        try {
          // 调用API更新期初库存
          const response = await updateInitialStock({
            warehouse_id: this.$route.params.id,
            month: this.selectedMonth
          })
          
          // 显示成功消息，包含统计信息
          this.$message.success(`更新成功！当前库存总数：${totalItems}件，上月入库总额：${totalInbound.toFixed(2)}元，出库总额：${totalOutbound.toFixed(2)}元`)
          
          // 重新加载报表数据
          await this.fetchReportData()
        } finally {
          this.loading = false
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('更新期初库存失败:', error)
          this.$message.error('更新期初库存失败: ' + (error.message || '未知错误'))
        }
      }
    },
    // 新增：合并库存中相同品项和规格的记录
    mergeInventoryItems() {
      try {
        console.log('开始合并相同品项的库存记录...')
        
        // 记录合并前的数量
        const beforeCount = this.inventoryList.length
        if (beforeCount === 0) {
          console.log('库存列表为空，跳过合并操作')
          return
        }
        
        // 创建备份
        const originalInventory = JSON.parse(JSON.stringify(this.inventoryList))
        
        // 创建Map来存储合并后的记录
        const mergedMap = new Map()
        
        // 遍历库存列表进行合并
        this.inventoryList.forEach((item, index) => {
          if (!item) {
            console.log(`警告: 索引${index}的库存项为空，已跳过`)
            return
          }
          
          const itemName = typeof item.品项 === 'string' ? item.品项.trim() : String(item.品项 || '')
          const spec = typeof item['规格/型号'] === 'string' ? item['规格/型号'].trim() : String(item['规格/型号'] || '')
          
          if (!itemName) {
            console.log(`警告: 索引${index}的库存项没有品项名称，已跳过`)
            return
          }
          
          const key = `${itemName}|${spec}`
          
          if (!mergedMap.has(key)) {
            // 如果是新品项，创建新记录
            mergedMap.set(key, {
              ...item,
              期初库存: parseInt(item.期初库存 || 0),
              累计入库: parseInt(item.累计入库 || 0),
              累计出库: parseInt(item.累计出库 || 0),
              库存: parseInt(item.库存 || 0),
              单价: parseFloat(item.单价 || 0),
              库存金额: parseFloat(item.库存金额 || 0)
            })
          } else {
            // 如果已存在，合并数量
            const existingItem = mergedMap.get(key)
            existingItem.期初库存 += parseInt(item.期初库存 || 0)
            existingItem.累计入库 += parseInt(item.累计入库 || 0)
            existingItem.累计出库 += parseInt(item.累计出库 || 0)
            existingItem.库存 = existingItem.期初库存 + existingItem.累计入库 - existingItem.累计出库
            
            // 使用最新的单价，并重新计算库存金额
            if (parseFloat(item.单价 || 0) > 0) {
              existingItem.单价 = parseFloat(item.单价)
            }
            existingItem.库存金额 = existingItem.库存 * existingItem.单价
            
            // 保留最新的位置信息
            if (item.位置) {
              existingItem.位置 = item.位置
            }
            
            console.log(`合并品项: ${itemName}, 规格: ${spec}, 当前库存: ${existingItem.库存}`)
          }
        })
        
        // 更新库存列表为合并后的数据
        const mergedInventory = Array.from(mergedMap.values())
        
        // 安全检查：确保合并后的数据不会导致大量数据丢失
        if (beforeCount > 10 && mergedInventory.length < beforeCount * 0.7) {
          console.error(`警告: 合并操作可能导致数据丢失! 合并前: ${beforeCount}条, 合并后: ${mergedInventory.length}条`)
          this.$message.warning('检测到合并操作可能导致数据丢失，已取消合并')
          return
        }
        
        this.inventoryList = mergedInventory
        
        console.log(`合并完成，从${beforeCount}条记录合并为${this.inventoryList.length}条记录`)
        
        // 强制更新UI
        this.forceSyncInventoryTable()
        
      } catch (error) {
        console.error('合并库存记录时出错:', error)
        this.$message.error('合并库存记录失败: ' + error.message)
      }
    },
    // 创建数据备份
    createDataBackup() {
      try {
        console.log('创建数据备份...')
        this.reportBackup = {
          inbound: JSON.parse(JSON.stringify(this.inboundList)),
          outbound: JSON.parse(JSON.stringify(this.outboundList)),
          inventory: JSON.parse(JSON.stringify(this.inventoryList))
        }
        this.backupTime = new Date().getTime()
        console.log(`备份完成，共备份入库${this.reportBackup.inbound.length}条，出库${this.reportBackup.outbound.length}条，库存${this.reportBackup.inventory.length}条`)
      } catch (error) {
        console.error('创建数据备份失败:', error)
      }
    },
    // 从备份恢复数据
    restoreFromBackup() {
      try {
        if (!this.reportBackup || !this.backupTime) {
          this.$message.warning('没有可用的数据备份')
          return false
        }
        
        console.log('从备份恢复数据...')
        this.inboundList = JSON.parse(JSON.stringify(this.reportBackup.inbound))
        this.outboundList = JSON.parse(JSON.stringify(this.reportBackup.outbound))
        this.inventoryList = JSON.parse(JSON.stringify(this.reportBackup.inventory))
        
        console.log(`恢复完成，共恢复入库${this.inboundList.length}条，出库${this.outboundList.length}条，库存${this.inventoryList.length}条`)
        
        // 更新库存统计
        this.updateInventoryStatistics(false)
        
        // 强制UI刷新
        this.forceSyncInventoryTable()
        
        return true
      } catch (error) {
        console.error('从备份恢复数据失败:', error)
        return false
      }
    },
    // 从备份恢复数据
    handleRestoreFromBackup() {
      this.restoreFromBackup()
    },
    handleBackupData() {
      const warehouseId = this.$route.params.id
      if (!warehouseId) {
        this.$message.error('未找到仓库ID')
        return
      }

      this.$confirm('确定要备份当前仓库数据吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.backupLoading = true
        this.backupProgress = 10

        // 获取仓库名称用于文件命名
        const warehouseName = this.warehouseInfo?.name || ''
        const timestamp = moment().format('YYYY-MM-DD_HH-mm-ss')
        const fileName = `warehouse_${warehouseName}_${warehouseId}_backup_${timestamp}.json`

        // 显示loading
        const loading = this.$loading({
          lock: true,
          text: '正在备份数据...',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        })

        exportWarehouseBackup(warehouseId)
          .then(response => {
            this.backupProgress = 50
            if (!response) {
              throw new Error('备份数据响应为空')
            }

            // 检查响应类型
            if (response instanceof Blob) {
              // 如果是错误响应
              if (response.type.includes('json')) {
                return response.text().then(text => {
                  try {
                    const data = JSON.parse(text)
                    // 检查是否是完整的备份数据
                    if (data.warehouse && data.inventory !== undefined && data.transactions !== undefined) {
                      // 是完整的备份数据，创建下载
                      const blob = new Blob([text], { type: 'application/json' })
                      saveAs(blob, fileName)
                      this.lastBackupTime = new Date()
                      this.backupProgress = 100
                      this.$message.success('备份数据成功')
                      return
                    }
                    // 如果不是完整的备份数据，可能是错误信息
                    console.error('备份API返回JSON错误:', data)
                    throw new Error(data.message || data.error || data.detail || '备份失败')
                  } catch (e) {
                    console.error('解析备份响应失败:', e, '原始文本:', text)
                    throw new Error('备份过程中发生错误: ' + (e.message || '未知错误'))
                  }
                })
              }
              
              // 检查Blob大小，如果太小可能是错误响应
              if (response.size < 100) {
                return response.text().then(text => {
                  console.warn('备份响应内容过小，可能是错误:', text)
                  if (text && text.trim()) {
                    throw new Error('备份失败: ' + text)
                  }
                  throw new Error('备份响应内容异常')
                }).catch(e => {
                  console.error('读取小型备份响应失败:', e)
                  throw new Error('备份过程中发生错误，响应内容异常')
                })
              }
              
              this.backupProgress = 75
              // 使用file-saver进行下载
              saveAs(response, fileName)
              
              this.lastBackupTime = new Date()
              this.backupProgress = 100
              this.$message.success('备份数据成功')

              // 3秒后隐藏进度条
              setTimeout(() => {
                this.backupProgress = 0
              }, 3000)
            } else {
              throw new Error('响应格式不正确')
            }
          })
          .catch(error => {
            console.error('备份数据失败详情：', error)
            // 显示更详细的错误信息
            let errorMsg = error.message || '备份数据失败，请重试'
            
            // 如果是网络错误，提供更具体的提示
            if (error.name === 'NetworkError' || errorMsg.includes('network')) {
              errorMsg = '网络连接错误，请检查网络后重试'
            }
            
            // 如果是超时错误
            if (errorMsg.includes('timeout')) {
              errorMsg = '备份请求超时，数据量可能过大，请稍后重试'
            }
            
            this.$message.error(errorMsg)
            this.backupProgress = 0
          })
          .finally(() => {
            this.backupLoading = false
            loading.close()
          })
      }).catch(() => {
        // 用户取消操作
        this.backupProgress = 0
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
            // 重新加载仓库信息和报表数据
            await this.fetchWarehouseInfo()
            if (this.selectedMonth) {
              await this.fetchReportData()
            }
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
      return moment(backup).format('YYYY-MM-DD HH:mm:ss')
    },

    progressFormat(percentage) {
      if (percentage === 100) {
        return '完成'
      }
      return `${percentage}%`
    }
  },
  computed: {
    filteredInboundList() {
      if (!this.inboundSearchText) return this.inboundList;
      const searchText = this.inboundSearchText.toLowerCase();
      return this.inboundList.filter(item => {
        return (item.品项 || '').toLowerCase().includes(searchText) ||
               (item['规格/型号'] || '').toLowerCase().includes(searchText) ||
               (item.单位 || '').toLowerCase().includes(searchText) ||
               (item.经手人 || '').toLowerCase().includes(searchText) ||
               (item.日期 || '').includes(searchText);
      });
    },
    filteredOutboundList() {
      if (!this.outboundSearchText) return this.outboundList;
      const searchText = this.outboundSearchText.toLowerCase();
      return this.outboundList.filter(item => {
        return (item.品项 || '').toLowerCase().includes(searchText) ||
               (item['规格/型号'] || '').toLowerCase().includes(searchText) ||
               (item.单位 || '').toLowerCase().includes(searchText) ||
               (item.经手人 || '').toLowerCase().includes(searchText) ||
               (item.日期 || '').includes(searchText);
      });
    },
    filteredInventoryList() {
      if (!this.inventorySearchText) return this.inventoryList;
      const searchText = this.inventorySearchText.toLowerCase();
      return this.inventoryList.filter(item => {
        return (item.位置 || '').toLowerCase().includes(searchText) ||
               (item.品项 || '').toLowerCase().includes(searchText) ||
               (item['规格/型号'] || '').toLowerCase().includes(searchText) ||
               (item.单位 || '').toLowerCase().includes(searchText);
      });
    }
  }
}
</script>

<style lang="scss" scoped>
.app-container {
  padding: 20px;
}
.box-card {
  margin-bottom: 20px;
}
.operation-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;

  .action-buttons {
    display: flex;
  }
  
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
.delete-btn {
  color: #F56C6C;
}
.el-input-number {
  width: 100%;
}
.operation-header {
  margin-bottom: 15px;
}
.excel-upload {
  display: inline-block;
}
.el-date-editor.el-input {
  width: 150px;
}
.backup-progress {
  margin: 15px 0;
  .el-progress-bar__outer {
    background-color: #f5f7fa;
  }
  .el-progress-bar__inner {
    transition: all 0.3s ease;
  }
}
.backup-loading {
  background: rgba(0, 0, 0, 0.7) !important;
  .el-loading-text {
    color: #fff;
    font-size: 14px;
  }
}
.backup-time {
  margin-left: 10px;
  font-size: 13px;
  color: #909399;
}
</style> 