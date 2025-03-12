<template>
  <div class="app-container">
    <div class="filter-container">
      <el-select v-model="listQuery.warehouse" placeholder="选择仓库" clearable style="width: 200px" class="filter-item" @change="handleWarehouseChange">
        <el-option v-for="item in warehouseOptions" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
      <el-select v-model="listQuery.area" placeholder="选择库区" clearable style="width: 200px" class="filter-item">
        <el-option v-for="item in areaOptions" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
      <el-input v-model="listQuery.code" placeholder="库位编码" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.status" placeholder="状态" clearable style="width: 120px" class="filter-item">
        <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-plus" @click="handleCreate">
        添加
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      stripe
      highlight-current-row
      style="width: 100%;"
    >
      <el-table-column label="ID" prop="id" align="center" width="80">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="所属仓库" min-width="120px">
        <template slot-scope="{row}">
          <span>{{ row.warehouseName }}</span>
        </template>
      </el-table-column>
      <el-table-column label="所属库区" min-width="120px">
        <template slot-scope="{row}">
          <span>{{ row.areaName }}</span>
        </template>
      </el-table-column>
      <el-table-column label="库位编码" min-width="120px">
        <template slot-scope="{row}">
          <span class="link-type" @click="handleUpdate(row)">{{ row.code }}</span>
        </template>
      </el-table-column>
      <el-table-column label="库位类型" align="center" width="110">
        <template slot-scope="{row}">
          <span>{{ row.type | typeFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column label="容量" align="center" width="110">
        <template slot-scope="{row}">
          <span>{{ row.capacity }}</span>
        </template>
      </el-table-column>
      <el-table-column label="已使用" align="center" width="110">
        <template slot-scope="{row}">
          <span>{{ row.used }}</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" class-name="status-col" width="100">
        <template slot-scope="{row}">
          <el-tag :type="row.status | statusFilter">
            {{ row.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            编辑
          </el-button>
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleDelete(row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="100px" style="width: 400px; margin-left:50px;">
        <el-form-item label="所属仓库" prop="warehouse">
          <el-select v-model="temp.warehouse" class="filter-item" placeholder="请选择" @change="handleTempWarehouseChange">
            <el-option v-for="item in warehouseOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属库区" prop="area">
          <el-select v-model="temp.area" class="filter-item" placeholder="请选择">
            <el-option v-for="item in tempAreaOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="库位编码" prop="code">
          <el-input v-model="temp.code" />
        </el-form-item>
        <el-form-item label="库位类型" prop="type">
          <el-select v-model="temp.type" class="filter-item" placeholder="请选择">
            <el-option v-for="item in typeOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="容量" prop="capacity">
          <el-input-number v-model="temp.capacity" :min="0" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="temp.status" class="filter-item" placeholder="请选择">
            <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          确认
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import waves from '@/directive/waves'
import Pagination from '@/components/Pagination'

const statusOptions = [
  { label: '启用', value: 1 },
  { label: '禁用', value: 0 }
]

const typeOptions = [
  { label: '标准货位', value: 'STANDARD' },
  { label: '大件货位', value: 'LARGE' },
  { label: '零散货位', value: 'SMALL' }
]

const warehouseOptions = [
  { label: '主仓库', value: 1 },
  { label: '备用仓库', value: 2 }
]

// 模拟库区数据
const areaOptionsMap = {
  1: [
    { label: 'A区', value: 1 },
    { label: 'B区', value: 2 }
  ],
  2: [
    { label: 'C区', value: 3 },
    { label: 'D区', value: 4 }
  ]
}

export default {
  name: 'WarehouseLocation',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        1: 'success',
        0: 'info'
      }
      return statusMap[status]
    },
    typeFilter(type) {
      const typeMap = {
        'STANDARD': '标准货位',
        'LARGE': '大件货位',
        'SMALL': '零散货位'
      }
      return typeMap[type]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        warehouse: undefined,
        area: undefined,
        code: undefined,
        status: undefined
      },
      warehouseOptions,
      areaOptions: [],
      tempAreaOptions: [],
      statusOptions,
      typeOptions,
      temp: {
        id: undefined,
        warehouse: undefined,
        area: undefined,
        code: '',
        type: 'STANDARD',
        capacity: 100,
        used: 0,
        status: 1
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: '编辑库位',
        create: '创建库位'
      },
      rules: {
        warehouse: [{ required: true, message: '请选择所属仓库', trigger: 'change' }],
        area: [{ required: true, message: '请选择所属库区', trigger: 'change' }],
        code: [{ required: true, message: '库位编码不能为空', trigger: 'blur' }],
        type: [{ required: true, message: '请选择库位类型', trigger: 'change' }],
        capacity: [{ required: true, message: '请输入容量', trigger: 'blur' }]
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      // 模拟数据
      setTimeout(() => {
        this.list = [
          {
            id: 1,
            warehouseName: '主仓库',
            areaName: 'A区',
            code: 'A-01-01',
            type: 'STANDARD',
            capacity: 100,
            used: 80,
            status: 1
          },
          {
            id: 2,
            warehouseName: '主仓库',
            areaName: 'A区',
            code: 'A-01-02',
            type: 'LARGE',
            capacity: 200,
            used: 150,
            status: 1
          }
        ]
        this.total = 2
        this.listLoading = false
      }, 1000)
    },
    handleWarehouseChange(value) {
      this.listQuery.area = undefined
      this.areaOptions = value ? areaOptionsMap[value] : []
    },
    handleTempWarehouseChange(value) {
      this.temp.area = undefined
      this.tempAreaOptions = value ? areaOptionsMap[value] : []
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        warehouse: undefined,
        area: undefined,
        code: '',
        type: 'STANDARD',
        capacity: 100,
        used: 0,
        status: 1
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          this.temp.id = parseInt(Math.random() * 100) + 1024
          this.temp.warehouseName = this.warehouseOptions.find(item => item.value === this.temp.warehouse).label
          this.temp.areaName = this.tempAreaOptions.find(item => item.value === this.temp.area).label
          this.list.unshift(this.temp)
          this.dialogFormVisible = false
          this.$notify({
            title: '成功',
            message: '创建成功',
            type: 'success',
            duration: 2000
          })
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.temp.warehouse = this.warehouseOptions.find(item => item.label === row.warehouseName).value
      this.tempAreaOptions = areaOptionsMap[this.temp.warehouse]
      this.temp.area = this.tempAreaOptions.find(item => item.label === row.areaName).value
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.warehouseName = this.warehouseOptions.find(item => item.value === tempData.warehouse).label
          tempData.areaName = this.tempAreaOptions.find(item => item.value === tempData.area).label
          const index = this.list.findIndex(v => v.id === this.temp.id)
          this.list.splice(index, 1, tempData)
          this.dialogFormVisible = false
          this.$notify({
            title: '成功',
            message: '更新成功',
            type: 'success',
            duration: 2000
          })
        }
      })
    },
    handleDelete(row) {
      this.$confirm('确认删除该库位吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.list.findIndex(v => v.id === row.id)
        this.list.splice(index, 1)
        this.$notify({
          title: '成功',
          message: '删除成功',
          type: 'success',
          duration: 2000
        })
      })
    }
  }
}
</script> 