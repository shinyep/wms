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
        v-if="$store.getters.canAddWarehouse || $store.getters.isSuperAdmin"
      >
        新增仓库
      </el-button>
      <el-button
        class="filter-item"
        style="margin-left: 10px;"
        type="success"
        icon="el-icon-upload2"
        @click="handleImport"
        v-if="$store.getters.canAddWarehouse || $store.getters.isSuperAdmin"
      >
        导入
      </el-button>
      <el-button
        class="filter-item"
        style="margin-left: 10px;"
        type="warning"
        icon="el-icon-download"
        @click="handleExport"
        v-if="$store.getters.canViewWarehouse || $store.getters.isSuperAdmin"
      >
        导出
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
      <el-table-column label="仓库编号" prop="code" align="center" width="150">
        <template slot-scope="{row}">
          <span>{{ row.code }}</span>
        </template>
      </el-table-column>
      <el-table-column label="仓库名称" prop="name" align="center" min-width="150">
        <template slot-scope="{row}">
          <el-link type="primary" @click="handleDetail(row)">{{ row.name }}</el-link>
        </template>
      </el-table-column>
      <el-table-column label="仓库地址" prop="address" align="center" min-width="200">
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
          <el-tag :type="row.status === 'active' ? 'success' : 'info'">
            {{ row.status === 'active' ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button v-if="$store.getters.canEditWarehouse || $store.getters.isSuperAdmin" type="primary" size="mini" @click="handleUpdate(row)">
            编辑
          </el-button>
          <el-button
            v-if="($store.getters.canEditWarehouse || $store.getters.isSuperAdmin) && row.status === 'active'"
            size="mini"
            type="warning"
            @click="handleModifyStatus(row, 'inactive')"
          >
            禁用
          </el-button>
          <el-button
            v-if="($store.getters.canEditWarehouse || $store.getters.isSuperAdmin) && row.status !== 'active'"
            size="mini"
            type="success"
            @click="handleModifyStatus(row, 'active')"
          >
            启用
          </el-button>
          <el-button
            v-if="$store.getters.canDeleteWarehouse || $store.getters.isSuperAdmin"
            size="mini"
            type="danger"
            @click="handleDelete(row)"
          >
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
        label-width="100px"
        style="width: 400px; margin-left:50px;"
      >
        <el-form-item label="仓库编号" prop="code">
          <el-input v-model="temp.code" placeholder="请输入仓库编号"/>
        </el-form-item>
        <el-form-item label="仓库名称" prop="name">
          <el-input v-model="temp.name" placeholder="请输入仓库名称"/>
        </el-form-item>
        <el-form-item label="仓库地址" prop="address">
          <el-input v-model="temp.address" type="textarea" :rows="2" placeholder="请输入仓库地址"/>
        </el-form-item>
        <el-form-item label="联系人" prop="contact_person">
          <el-input v-model="temp.contact_person" placeholder="请输入联系人"/>
        </el-form-item>
        <el-form-item label="联系电话" prop="contact_phone">
          <el-input v-model="temp.contact_phone" placeholder="请输入联系电话"/>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="temp.status" class="filter-item" placeholder="请选择">
            <el-option label="启用" value="active"/>
            <el-option label="禁用" value="inactive"/>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          确定
        </el-button>
      </div>
    </el-dialog>

    <!-- 导入对话框 -->
    <el-dialog title="导入Excel" :visible.sync="importVisible" width="400px">
      <el-upload
        class="upload-demo"
        drag
        action="#"
        :http-request="uploadFile"
        :show-file-list="false"
        accept=".xlsx,.xls"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip">只能上传xlsx/xls文件</div>
      </el-upload>
    </el-dialog>
  </div>
</template>

<script>
import { fetchList, createWarehouse, updateWarehouse, deleteWarehouse, importExcel, exportExcel } from '@/api/warehouse'
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
      },
      temp: {
        id: undefined,
        code: '',
        name: '',
        address: '',
        contact_person: '',
        contact_phone: '',
        status: 'active'
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: '编辑仓库',
        create: '新增仓库'
      },
      rules: {
        code: [{ required: true, message: '仓库编号不能为空', trigger: 'blur' }],
        name: [{ required: true, message: '仓库名称不能为空', trigger: 'blur' }],
        address: [{ required: true, message: '仓库地址不能为空', trigger: 'blur' }],
        contact_person: [{ required: true, message: '联系人不能为空', trigger: 'blur' }],
        contact_phone: [{ required: true, message: '联系电话不能为空', trigger: 'blur' }]
      },
      importVisible: false
    }
  },
  created() {
    this.getList()
    console.log('超级管理员权限:', this.$store.getters.isSuperAdmin)
    console.log('添加仓库权限:', this.$store.getters.canAddWarehouse)
    console.log('删除仓库权限:', this.$store.getters.canDeleteWarehouse)
    console.log('所有权限:', this.$store.getters.permissions)
  },
  methods: {
    getList() {
      this.listLoading = true
      fetchList(this.listQuery).then(response => {
        // 兼容两种数据格式
        const data = response.data || response
        this.list = data.results
        this.total = data.count
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
        code: '',
        name: '',
        address: '',
        contact_person: '',
        contact_phone: '',
        status: 'active'
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
          createWarehouse(this.temp).then(() => {
            this.dialogFormVisible = false
            this.getList()
            this.$notify({
              title: '成功',
              message: '创建成功',
              type: 'success',
              duration: 2000
            })
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
          updateWarehouse(tempData.id, tempData).then(() => {
            this.dialogFormVisible = false
            this.getList()
            this.$notify({
              title: '成功',
              message: '更新成功',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleModifyStatus(row, status) {
      const statusText = status === 'active' ? '启用' : '禁用'
      this.$confirm(`确认要${statusText}该仓库吗?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        updateWarehouse(row.id, { status }).then(() => {
          this.$notify({
            title: '成功',
            message: `${statusText}成功`,
            type: 'success',
            duration: 2000
          })
          row.status = status
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消操作'
        })
      })
    },
    handleDelete(row) {
      this.$confirm("确认删除该仓库吗？", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        this.listLoading = true;
        deleteWarehouse(row.id)
          .then(() => {
            this.$message({
              type: 'success',
              message: '删除成功!'
            });
            this.getList();
          })
          .catch(error => {
            console.error('删除仓库失败:', error);
            this.$message({
              type: 'error',
              message: '删除失败: ' + (error.message || '未知错误')
            });
          })
          .finally(() => {
            this.listLoading = false;
          });
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });          
      });
    },
    handleDetail(row) {
      this.$router.push(`/warehouse/detail/${row.id}`)
    },
    handleImport() {
      this.importVisible = true
    },
    async uploadFile(params) {
      try {
        const formData = new FormData()
        formData.append('file', params.file)
        await importExcel(formData)
        this.$message.success('导入成功')
        this.importVisible = false
        this.getList()
      } catch (error) {
        this.$message.error(error.message || '导入失败')
      }
    },
    async handleExport() {
      try {
        this.$message({
          type: 'info',
          message: '正在导出...'
        })
        
        const response = await exportExcel()
        
        if (!response.data) {
          throw new Error('导出失败：未收到数据')
        }
        
        // 创建Blob对象
        const blob = new Blob([response.data], {
          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })
        
        // 生成文件名
        const filename = `仓库列表_${new Date().getTime()}.xlsx`
        
        // 创建下载链接
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.style.display = 'none'
        link.href = url
        link.download = filename
        
        // 添加到页面并触发下载
        document.body.appendChild(link)
        link.click()
        
        // 清理
        setTimeout(() => {
          document.body.removeChild(link)
          window.URL.revokeObjectURL(url)
        }, 100)
        
        this.$message({
          type: 'success',
          message: '导出成功'
        })
      } catch (error) {
        console.error('导出失败:', error)
        this.$message.error(error.message || '导出失败，请稍后重试')
      }
    }
  }
}
</script>