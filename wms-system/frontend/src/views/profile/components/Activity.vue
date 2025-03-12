<template>
  <div class="activity-container">
    <div class="filter-container">
      <el-form :inline="true" :model="filterForm" class="demo-form-inline">
        <el-form-item label="操作类型">
          <el-select v-model="filterForm.type" placeholder="全部" clearable>
            <el-option label="登录" value="login" />
            <el-option label="查询" value="query" />
            <el-option label="新增" value="create" />
            <el-option label="修改" value="update" />
            <el-option label="删除" value="delete" />
            <el-option label="导出" value="export" />
            <el-option label="导入" value="import" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="filterForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="yyyy-MM-dd"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-table
      v-loading="loading"
      :data="activityList"
      border
      style="width: 100%"
    >
      <el-table-column
        prop="time"
        label="操作时间"
        width="180"
        sortable
      />
      <el-table-column
        prop="type"
        label="操作类型"
        width="100"
      >
        <template slot-scope="scope">
          <el-tag :type="getTagType(scope.row.type)">{{ getTypeName(scope.row.type) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        prop="module"
        label="操作模块"
        width="120"
      />
      <el-table-column
        prop="content"
        label="操作内容"
      />
      <el-table-column
        prop="ip"
        label="IP地址"
        width="140"
      />
      <el-table-column
        prop="status"
        label="状态"
        width="80"
      >
        <template slot-scope="scope">
          <el-tag :type="scope.row.status === 'success' ? 'success' : 'danger'">
            {{ scope.row.status === 'success' ? '成功' : '失败' }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-container">
      <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 30, 50]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      currentPage: 1,
      pageSize: 10,
      total: 0,
      filterForm: {
        type: '',
        dateRange: []
      },
      activityList: [
        {
          id: 1,
          time: '2025-03-05 08:30:43',
          type: 'login',
          module: '系统',
          content: '用户登录',
          ip: '192.168.1.100',
          status: 'success'
        },
        {
          id: 2,
          time: '2025-03-05 09:15:22',
          type: 'query',
          module: '仓库管理',
          content: '查询仓库列表',
          ip: '192.168.1.100',
          status: 'success'
        },
        {
          id: 3,
          time: '2025-03-05 10:05:37',
          type: 'create',
          module: '库区管理',
          content: '新增库区：A区',
          ip: '192.168.1.100',
          status: 'success'
        },
        {
          id: 4,
          time: '2025-03-05 11:30:15',
          type: 'update',
          module: '库位管理',
          content: '修改库位：A-001',
          ip: '192.168.1.100',
          status: 'success'
        },
        {
          id: 5,
          time: '2025-03-05 14:20:08',
          type: 'delete',
          module: '库位管理',
          content: '删除库位：B-002',
          ip: '192.168.1.100',
          status: 'success'
        },
        {
          id: 6,
          time: '2025-03-05 15:45:33',
          type: 'export',
          module: '仓库管理',
          content: '导出仓库数据',
          ip: '192.168.1.100',
          status: 'success'
        },
        {
          id: 7,
          time: '2025-03-05 16:30:21',
          type: 'import',
          module: '库存管理',
          content: '导入库存数据',
          ip: '192.168.1.100',
          status: 'fail'
        }
      ]
    }
  },
  computed: {
    total() {
      return this.activityList.length
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.loading = true
      // 模拟API请求
      setTimeout(() => {
        this.loading = false
      }, 500)
    },
    getTagType(type) {
      const typeMap = {
        login: 'info',
        query: 'info',
        create: 'success',
        update: 'warning',
        delete: 'danger',
        export: 'primary',
        import: 'primary'
      }
      return typeMap[type] || 'info'
    },
    getTypeName(type) {
      const typeMap = {
        login: '登录',
        query: '查询',
        create: '新增',
        update: '修改',
        delete: '删除',
        export: '导出',
        import: '导入'
      }
      return typeMap[type] || '其他'
    },
    handleFilter() {
      this.currentPage = 1
      this.fetchData()
    },
    resetFilter() {
      this.filterForm = {
        type: '',
        dateRange: []
      }
      this.fetchData()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.fetchData()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.fetchData()
    }
  }
}
</script>

<style lang="scss" scoped>
.activity-container {
  padding: 20px 0;
}

.filter-container {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style> 