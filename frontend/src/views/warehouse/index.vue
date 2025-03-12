<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        placeholder="请输入仓库编号/名称"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
      <el-button
        class="filter-item"
        style="margin-left: 10px;"
        type="primary"
        icon="el-icon-plus"
        @click="handleCreate"
      >
        新增仓库
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
      <el-table-column label="仓库编号" prop="code" align="center" width="150">
        <template slot-scope="{row}">
          <span>{{ row.code }}</span>
        </template>
      </el-table-column>
      
      <el-table-column label="仓库名称" prop="name" align="center" min-width="150">
        <template slot-scope="{row}">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>
      
      <el-table-column label="地址" prop="address" align="center" min-width="200">
        <template slot-scope="{row}">
          <span>{{ row.address }}</span>
        </template>
      </el-table-column>
      
      <el-table-column label="联系人" prop="contact_person" align="center" width="120">
        <template slot-scope="{row}">
          <span>{{ row.contact_person }}</span>
        </template>
      </el-table-column>
      
      <el-table-column label="联系电话" prop="contact_phone" align="center" width="120">
        <template slot-scope="{row}">
          <span>{{ row.contact_phone }}</span>
        </template>
      </el-table-column>
      
      <el-table-column label="状态" prop="status" align="center" width="100">
        <template slot-scope="{row}">
          <el-tag :type="row.is_active ? 'success' : 'info'">
            {{ row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="250" align="center">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="primary"
            @click="handleDetail(scope.row)">详情</el-button>
          <el-button
            size="mini"
            type="success"
            @click="handleMonthlyReport(scope.row)">月度报表</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.row)"
            v-if="checkPermission(['admin'])">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.limit"
      @pagination="getList"
    />
  </div>
</template>

<script>
import { fetchList, deleteWarehouse } from '@/api/warehouse'
import waves from '@/directive/waves'
import Pagination from '@/components/Pagination'

export default {
  name: 'WarehouseList',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        search: undefined
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      fetchList(this.listQuery).then(response => {
        this.list = response.data.results
        this.total = response.data.count
        this.listLoading = false
      }).catch(error => {
        console.error('获取仓库列表失败:', error)
        this.$message.error('获取仓库列表失败: ' + (error.message || '未知错误'))
        this.listLoading = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleCreate() {
      this.$router.push('/warehouse/create')
    },
    handleDetail(row) {
      this.$router.push(`/warehouse/detail/${row.id}`)
    },
    handleMonthlyReport(row) {
      console.log('跳转到月度报表，仓库ID:', row.id)
      this.$router.push({
        name: 'MonthlyReport',
        params: { id: row.id },
        query: { month: this.getCurrentMonth() }
      })
    },
    getCurrentMonth() {
      const date = new Date()
      const year = date.getFullYear()
      const month = (date.getMonth() + 1).toString().padStart(2, '0')
      return `${year}-${month}`
    },
    handleDelete(row) {
      this.$confirm('确认删除该仓库吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteWarehouse(row.id).then(() => {
          this.$message.success('删除成功')
          this.getList()
        }).catch(error => {
          console.error('删除仓库失败:', error)
          this.$message.error('删除失败: ' + (error.message || '未知错误'))
        })
      }).catch(() => {
        this.$message.info('已取消删除')
      })
    }
  }
}
</script>

<style>
  /* No changes to style section */
</style> 