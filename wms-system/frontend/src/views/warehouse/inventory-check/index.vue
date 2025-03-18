<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button type="primary" @click="handleCreateCheck">
        <i class="el-icon-plus"></i> 新建盘点任务
      </el-button>
    </div>

    <!-- 盘点任务列表 -->
    <el-table
      v-loading="listLoading"
      :data="checkList"
      border
      style="width: 100%"
      highlight-current-row>
      
      <el-table-column label="盘点单号" prop="checkNo" align="center" width="180">
        <template slot-scope="{row}">
          <span>{{ row.checkNo }}</span>
        </template>
      </el-table-column>

      <el-table-column label="盘点类型" prop="checkType" align="center" width="120">
        <template slot-scope="{row}">
          <el-tag :type="row.checkType === '全面盘点' ? 'primary' : 'success'">
            {{ row.checkType }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column label="盘点状态" prop="status" align="center" width="120">
        <template slot-scope="{row}">
          <el-tag :type="statusTagType(row.status)">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column label="开始时间" width="180" align="center">
        <template slot-scope="{row}">
          <span>{{ row.startTime }}</span>
        </template>
      </el-table-column>

      <el-table-column label="负责人" prop="manager" align="center" width="120">
        <template slot-scope="{row}">
          <span>{{ row.manager }}</span>
        </template>
      </el-table-column>

      <el-table-column label="盘点进度" prop="progress" align="center" width="200">
        <template slot-scope="{row}">
          <el-progress :percentage="row.progress"></el-progress>
        </template>
      </el-table-column>

      <el-table-column label="操作" align="center" width="250" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button 
            size="mini" 
            type="primary" 
            @click="handleCheck(row)"
            :disabled="row.status === '已完成'">
            {{ row.status === '未开始' ? '开始盘点' : '继续盘点' }}
          </el-button>
          <el-button
            size="mini"
            type="success"
            @click="handleDetail(row)">
            查看详情
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.limit"
      @pagination="getList" />

    <!-- 新建盘点任务对话框 -->
    <el-dialog :title="'新建盘点任务'" :visible.sync="dialogFormVisible">
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="100px"
        style="margin-left: 30px; margin-right: 30px">
        
        <el-form-item label="盘点类型" prop="checkType">
          <el-select v-model="temp.checkType" class="filter-item">
            <el-option label="全面盘点" value="全面盘点" />
            <el-option label="动态盘点" value="动态盘点" />
          </el-select>
        </el-form-item>

        <el-form-item label="选择仓库" prop="warehouseId" v-if="temp.checkType === '全面盘点'">
          <el-select v-model="temp.warehouseId" placeholder="请选择仓库" @change="handleWarehouseChange">
            <el-option
              v-for="item in warehouseOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="盘点区域" prop="checkArea">
          <el-cascader
            v-model="temp.checkArea"
            :options="areaOptions"
            :props="{ 
              checkStrictly: true,
              value: 'id',
              label: 'name',
              children: 'children'
            }"
            :disabled="!temp.warehouseId"
            placeholder="请先选择仓库"
            clearable />
        </el-form-item>

        <el-form-item label="负责人" prop="manager">
          <el-input v-model="temp.manager" />
        </el-form-item>

        <el-form-item label="备注">
          <el-input
            v-model="temp.remark"
            type="textarea"
            :rows="2"
            placeholder="请输入内容" />
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="createData">确认</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { getInventoryCheckList, createInventoryCheck } from '@/api/inventory'
import { getWarehouseList } from '@/api/warehouse'
import { getWarehouseAreaTree } from '@/api/inventory'

// 添加polyfill用于兼容老浏览器
function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

// 检查crypto对象是否存在并提供polyfill
if (typeof window.crypto === 'undefined') {
  window.crypto = {
    randomUUID: generateUUID,
    getRandomValues: function(arr) {
      for (let i = 0; i < arr.length; i++) {
        arr[i] = Math.floor(Math.random() * 256);
      }
      return arr;
    }
  };
} else if (typeof window.crypto.randomUUID === 'undefined') {
  window.crypto.randomUUID = generateUUID;
}

export default {
  name: 'InventoryCheck',
  components: { Pagination },
  data() {
    return {
      listLoading: false,
      checkList: [],
      total: 0,
      listQuery: {
        page: 1,
        limit: 10
      },
      dialogFormVisible: false,
      temp: {
        checkType: '全面盘点',
        warehouseId: '',
        checkArea: [],
        manager: '',
        remark: ''
      },
      rules: {
        checkType: [{ required: true, message: '请选择盘点类型', trigger: 'change' }],
        warehouseId: [{ required: true, message: '请选择仓库', trigger: 'change' }],
        checkArea: [{ required: true, message: '请选择盘点区域', trigger: 'change' }],
        manager: [{ required: true, message: '请输入负责人', trigger: 'blur' }]
      },
      warehouseOptions: [],
      areaOptions: [],
      areaLoading: false
    }
  },
  created() {
    this.getList()
    this.getWarehouses()
  },
  methods: {
    statusTagType(status) {
      const statusMap = {
        '未开始': 'info',
        '进行中': 'warning',
        '已完成': 'success',
        '已取消': 'danger'
      }
      return statusMap[status]
    },
    getList() {
      this.listLoading = true
      getInventoryCheckList(this.listQuery).then(response => {
        this.checkList = response.data.results || []
        this.total = response.data.count || 0
        this.listLoading = false
      }).catch(() => {
        this.listLoading = false
        this.checkList = []
        this.total = 0
      })
    },
    getWarehouses() {
      getWarehouseList().then(response => {
        this.warehouseOptions = response.data.results || []
      }).catch(() => {
        this.$message.error('获取仓库列表失败')
      })
    },
    handleWarehouseChange(warehouseId) {
      this.temp.checkArea = []
      this.areaOptions = []
      this.areaLoading = true
      
      getWarehouseAreaTree(warehouseId).then(response => {
        this.areaOptions = response.data || []
        this.areaLoading = false
      }).catch(() => {
        this.areaLoading = false
        this.$message.error('获取仓库区域结构失败')
      })
    },
    handleCreateCheck() {
      this.dialogFormVisible = true
      this.temp = {
        checkType: '全面盘点',
        warehouseId: '',
        checkArea: [],
        manager: '',
        remark: ''
      }
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          
          // 处理级联选择器的数据
          const areaData = {
            warehouseId: tempData.warehouseId,
            areaId: typeof tempData.checkArea[0] === 'object' ? tempData.checkArea[0].id : tempData.checkArea[0],
            shelfId: tempData.checkArea.length > 1 ? 
              (typeof tempData.checkArea[1] === 'object' ? tempData.checkArea[1].id : tempData.checkArea[1]) : null
          }
          
          const data = {
            check_type: tempData.checkType,
            manager: tempData.manager,
            remark: tempData.remark,
            ...areaData
          }
          
          createInventoryCheck(data).then(() => {
            this.dialogFormVisible = false
            this.$message({
              type: 'success',
              message: '创建成功'
            })
            this.getList()
          }).catch(error => {
            this.$message.error('创建失败: ' + (error.message || '未知错误'))
          })
        }
      })
    },
    handleCheck(row) {
      // 跳转到盘点执行页面
      this.$router.push({
        path: '/warehouse/inventory-check/execute',
        query: { id: row.checkNo }
      })
    },
    handleDetail(row) {
      // 跳转到盘点详情页面
      this.$router.push({
        path: '/warehouse/inventory-check/detail',
        query: { id: row.checkNo }
      })
    },
    // 获取区域信息文本
    getAreaInfoText(warehouseId, checkArea) {
      let result = ''
      
      // 查找仓库名称
      const warehouse = this.warehouseOptions.find(w => w.id === warehouseId)
      if (warehouse) {
        result += warehouse.name
      }
      
      // 区域和货架信息
      if (checkArea && checkArea.length > 0) {
        // 查找区域名称
        const findAreaName = (options, id) => {
          for (const option of options) {
            if (option.id === id) {
              return option.name
            }
            if (option.children && option.children.length > 0) {
              const name = findAreaName(option.children, id)
              if (name) return name
            }
          }
          return null
        }
        
        const areaId = typeof checkArea[0] === 'object' ? checkArea[0].id : checkArea[0]
        const areaName = findAreaName(this.areaOptions, areaId)
        if (areaName) {
          result += ' - ' + areaName
        }
        
        if (checkArea.length > 1) {
          const shelfId = typeof checkArea[1] === 'object' ? checkArea[1].id : checkArea[1]
          const shelfName = findAreaName(this.areaOptions, shelfId)
          if (shelfName) {
            result += ' - ' + shelfName
          }
        }
      }
      
      return result || '未指定区域'
    }
  }
}
</script>

<style lang="scss" scoped>
.filter-container {
  padding-bottom: 10px;
  .filter-item {
    display: inline-block;
    vertical-align: middle;
    margin-bottom: 10px;
  }
}
</style> 