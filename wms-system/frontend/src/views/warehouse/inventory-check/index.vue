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

        <el-form-item label="盘点区域" prop="checkArea">
          <el-cascader
            v-model="temp.checkArea"
            :options="areaOptions"
            :props="{ checkStrictly: true }"
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
        checkArea: [],
        manager: '',
        remark: ''
      },
      rules: {
        checkType: [{ required: true, message: '请选择盘点类型', trigger: 'change' }],
        checkArea: [{ required: true, message: '请选择盘点区域', trigger: 'change' }],
        manager: [{ required: true, message: '请输入负责人', trigger: 'blur' }]
      },
      areaOptions: [
        {
          value: 'A区',
          label: 'A区',
          children: [
            { value: 'A1', label: 'A1货架' },
            { value: 'A2', label: 'A2货架' }
          ]
        },
        {
          value: 'B区',
          label: 'B区',
          children: [
            { value: 'B1', label: 'B1货架' },
            { value: 'B2', label: 'B2货架' }
          ]
        }
      ]
    }
  },
  created() {
    this.getList()
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
      // 这里应该调用后端API获取盘点任务列表
      // 模拟数据
      setTimeout(() => {
        this.checkList = [
          {
            checkNo: 'PD' + new Date().getTime(),
            checkType: '全面盘点',
            status: '未开始',
            startTime: new Date().toLocaleString('zh-CN', {
              year: 'numeric',
              month: '2-digit',
              day: '2-digit',
              hour: '2-digit',
              minute: '2-digit'
            }).replace(/\//g, '-'),
            manager: '张三',
            progress: 0
          }
        ]
        this.total = this.checkList.length
        this.listLoading = false
      }, 500)
    },
    handleCreateCheck() {
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          // 这里应该调用后端API创建盘点任务
          const tempData = Object.assign({}, this.temp)
          this.dialogFormVisible = false
          this.$message({
            type: 'success',
            message: '创建成功'
          })
          this.getList()
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