<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.username"
        placeholder="用户名"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      <el-select
        v-model="listQuery.role"
        placeholder="角色"
        clearable
        class="filter-item"
        style="width: 130px"
      >
        <el-option v-for="item in roleOptions" :key="item.key" :label="item.display_name" :value="item.key" />
      </el-select>
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
        添加
      </el-button>
      <el-button
        class="filter-item"
        style="margin-left: 10px;"
        type="info"
        icon="el-icon-refresh"
        @click="refreshList"
      >
        刷新
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
    >
      <el-table-column label="ID" prop="id" align="center" width="80">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="用户名" min-width="110px">
        <template slot-scope="{row}">
          <span>{{ row.username }}</span>
        </template>
      </el-table-column>
      <el-table-column label="姓名" min-width="110px">
        <template slot-scope="{row}">
          <span>{{ row.first_name }}{{ row.last_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="邮箱" min-width="150px">
        <template slot-scope="{row}">
          <span>{{ row.email }}</span>
        </template>
      </el-table-column>
      <el-table-column label="角色" min-width="110px">
        <template slot-scope="{row}">
          <span>{{ getRoleName(row.role) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="等级" min-width="110px">
        <template slot-scope="{row}">
          <span>{{ getLevelName(row.level) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" class-name="status-col" width="100">
        <template slot-scope="{row}">
          <el-tag :type="row.is_active ? 'success' : 'danger'">
            {{ row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" width="150px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.date_joined | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            编辑
          </el-button>
          <el-button v-if="row.is_active" size="mini" type="warning" @click="handleStatusChange(row, false)">
            禁用
          </el-button>
          <el-button v-else size="mini" type="success" @click="handleStatusChange(row, true)">
            启用
          </el-button>
          <el-button v-if="row.id !== 1" size="mini" type="danger" @click="handleDelete(row)">
            删除
          </el-button>
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

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="80px"
        style="width: 400px; margin-left:50px;"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="temp.username" :disabled="dialogStatus==='update'" />
        </el-form-item>
        <el-form-item v-if="dialogStatus==='create'" label="密码" prop="password">
          <el-input v-model="temp.password" type="password" />
        </el-form-item>
        <el-form-item v-if="dialogStatus==='create'" label="确认密码" prop="confirm_password">
          <el-input v-model="temp.confirm_password" type="password" />
        </el-form-item>
        <el-form-item label="姓" prop="first_name">
          <el-input v-model="temp.first_name" />
        </el-form-item>
        <el-form-item label="名" prop="last_name">
          <el-input v-model="temp.last_name" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="temp.email" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="temp.phone" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="temp.role" class="filter-item" placeholder="请选择">
            <el-option v-for="item in roleOptions" :key="item.key" :label="item.display_name" :value="item.key" />
          </el-select>
        </el-form-item>
        <el-form-item label="等级" prop="level">
          <el-select v-model="temp.level" class="filter-item" placeholder="请选择" :disabled="currentUser && currentUser.level < 3">
            <el-option v-for="item in levelOptions" :key="item.key" :label="item.display_name" :value="item.key" />
          </el-select>
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-input v-model="temp.department" />
        </el-form-item>
        <el-form-item label="职位" prop="position">
          <el-input v-model="temp.position" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="temp.is_active" />
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
import { fetchUserList, createUser, updateUser, deleteUser, activateUser, deactivateUser, setUserLevel } from '@/api/user'
import waves from '@/directive/waves'
import Pagination from '@/components/Pagination'

export default {
  name: 'AdminManagement',
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
        username: undefined,
        role: undefined
      },
      roleOptions: [
        { key: 'admin', display_name: '管理员' },
        { key: 'manager', display_name: '仓库经理' },
        { key: 'operator', display_name: '操作员' },
        { key: 'viewer', display_name: '查看者' }
      ],
      levelOptions: [
        { key: 0, display_name: '普通用户' },
        { key: 1, display_name: '高级用户' },
        { key: 2, display_name: '企业用户' },
        { key: 3, display_name: '超级管理员' }
      ],
      temp: {
        id: undefined,
        username: '',
        password: '',
        confirm_password: '',
        first_name: '',
        last_name: '',
        email: '',
        role: 'admin',
        level: 0,
        phone: '',
        department: '',
        position: '',
        is_active: true
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: '编辑管理员',
        create: '创建管理员'
      },
      rules: {
        username: [{ required: true, message: '用户名必须填写', trigger: 'blur' }],
        password: [{ required: true, message: '密码必须填写', trigger: 'blur' }],
        confirm_password: [{ required: true, message: '确认密码必须填写', trigger: 'blur' }],
        email: [
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
        ],
        role: [{ required: true, message: '角色必须选择', trigger: 'change' }]
      }
    }
  },
  created() {
    this.getList()
    this.currentUser = this.$store.getters.user
  },
  methods: {
    getList() {
      this.listLoading = true
      console.log('开始请求用户列表，查询参数:', this.listQuery)
      fetchUserList(this.listQuery).then(response => {
        console.log('用户列表原始响应:', response)
        
        // 兼容不同的API响应格式
        if (response.data && response.data.results) {
          // 标准分页格式
          this.list = response.data.results
          this.total = response.data.count || 0
        } else if (Array.isArray(response.data)) {
          // 数组格式
          this.list = response.data
          this.total = response.data.length
        } else if (Array.isArray(response)) {
          // 直接是数组
          this.list = response
          this.total = response.length
        } else if (response.results) {
          // 直接包含results的格式
          this.list = response.results
          this.total = response.count || response.results.length
        } else {
          // 尝试处理单个用户对象
          if (response && response.id && response.username) {
            this.list = [response]
            this.total = 1
            console.log('单个用户数据:', response)
          } else {
            // 其他情况
            console.error('未知的API响应格式:', response)
            this.list = []
            this.total = 0
          }
        }
        
        console.log('处理后的用户列表:', this.list)
        console.log('用户总数:', this.total)
        
        this.listLoading = false
      }).catch(error => {
        console.error('获取用户列表失败:', error)
        if (error.response) {
          console.error('错误状态:', error.response.status)
          console.error('错误数据:', error.response.data)
        }
        this.$message.error('获取用户列表失败，请稍后再试')
        this.list = []
        this.total = 0
        this.listLoading = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        username: '',
        password: '',
        confirm_password: '',
        first_name: '',
        last_name: '',
        email: '',
        role: 'admin',
        level: 0,
        phone: '',
        department: '',
        position: '',
        is_active: true
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
          createUser(this.temp).then(() => {
            this.dialogFormVisible = false
            this.$notify({
              title: '成功',
              message: '创建管理员成功',
              type: 'success',
              duration: 2000
            })
            this.getList()
          })
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
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
          
          if (this.currentUser && this.currentUser.level < 3 && tempData.level !== this.temp.level) {
            this.$message.error('只有超级管理员才能修改用户等级')
            return
          }
          
          updateUser(tempData.id, tempData).then(() => {
            this.dialogFormVisible = false
            this.$notify({
              title: '成功',
              message: '更新管理员成功',
              type: 'success',
              duration: 2000
            })
            this.getList()
          })
        }
      })
    },
    handleDelete(row) {
      this.$confirm('确认删除该管理员?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteUser(row.id).then(() => {
          this.$notify({
            title: '成功',
            message: '删除成功',
            type: 'success',
            duration: 2000
          })
          this.getList()
        })
      })
    },
    handleStatusChange(row, status) {
      const action = status ? activateUser : deactivateUser
      const statusText = status ? '启用' : '禁用'
      
      this.$confirm(`确认${statusText}该管理员?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        action(row.id).then(() => {
          this.$notify({
            title: '成功',
            message: `${statusText}成功`,
            type: 'success',
            duration: 2000
          })
          this.getList()
        })
      })
    },
    getRoleName(role) {
      const found = this.roleOptions.find(item => item.key === role)
      return found ? found.display_name : role
    },
    getLevelName(level) {
      const found = this.levelOptions.find(item => item.key === level)
      return found ? found.display_name : level
    },
    refreshList() {
      // 清空过滤条件
      this.listQuery = {
        page: 1,
        limit: 20,
        username: undefined,
        role: undefined
      }
      // 重新获取数据
      this.$message.info('正在刷新数据...')
      this.getList()
    }
  }
}
</script> 