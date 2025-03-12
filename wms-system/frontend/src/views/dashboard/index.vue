<template>
  <div class="dashboard-container">
    <div class="dashboard-text">欢迎 {{ name }}</div>
    
    <!-- 超级管理员账号管理入口 -->
    <el-row v-if="isSuper" :gutter="20" style="margin-bottom: 30px;">
      <el-col :span="24">
        <el-alert
          title="超级管理员管理区域"
          type="warning"
          :closable="false"
          show-icon>
          <div class="super-admin-panel">
            <el-button type="primary" @click="goToUserAdmin">
              <i class="el-icon-user"></i> 账号管理
            </el-button>
            <span class="super-admin-tip">您当前以超级管理员身份登录，可以管理所有系统账号</span>
          </div>
        </el-alert>
      </el-col>
    </el-row>
    
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="box-card" @click.native="handleCardClick('/warehouse')">
          <div slot="header" class="clearfix">
            <span>仓库管理</span>
          </div>
          <div class="card-panel">
            <div class="card-panel-icon-wrapper">
              <i class="el-icon-office-building"></i>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">仓库数量</div>
              <count-to :start-val="0" :end-val="dashboardData.warehouse_count || 0" :duration="2600" class="card-panel-num"/>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="box-card" @click.native="handleCardClick('/warehouse/monthly-report')">
          <div slot="header" class="clearfix">
            <span>月度报表管理</span>
          </div>
          <div class="card-panel">
            <div class="card-panel-icon-wrapper" style="background: #409EFF;">
              <i class="el-icon-date"></i>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">月度报表</div>
              <div class="card-panel-num">查看和创建</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="box-card" @click.native="handleCardClick('/warehouse/inventory-check')">
          <div slot="header" class="clearfix">
            <span>盘点功能</span>
          </div>
          <div class="card-panel">
            <div class="card-panel-icon-wrapper" style="background: #E6A23C;">
              <i class="el-icon-check"></i>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">库存盘点</div>
              <div class="card-panel-num">开始盘点</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import CountTo from 'vue-count-to'
import { getDashboardData } from '@/api/dashboard'

export default {
  name: 'Dashboard',
  components: {
    CountTo
  },
  data() {
    return {
      dashboardData: {
        warehouse_count: 0,
        report_count: 0,
        inventory_count: 0
      }
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'roles'
    ]),
    isSuper() {
      // 检查当前用户是否为超级管理员(level >= 3)
      const user = this.$store.state.user.user || {}
      return user.level >= 3
    }
  },
  created() {
    this.fetchData()
    // 获取完整用户信息
    if (!this.$store.state.user.user) {
      this.$store.dispatch('user/getInfo')
    }
  },
  methods: {
    handleCardClick(path) {
      this.$router.push(path).catch(err => {
        if (err.name !== 'NavigationDuplicated') {
          throw err
        }
      })
    },
    goToUserAdmin() {
      this.$router.push('/system/admin')
    },
    fetchData() {
      getDashboardData().then(response => {
        console.log('Dashboard response:', response)
        
        // 兼容不同的数据结构
        const data = response.data || response
        if (!data) {
          console.error('返回数据为空')
          return
        }

        console.log('Dashboard data:', data)

        this.dashboardData = {
          warehouse_count: data.warehouse_count || 0,
          report_count: data.report_count || 0,
          inventory_count: data.inventory_count || 0
        }
      }).catch(error => {
        console.error('获取仪表盘数据失败:', error)
        this.$message.error('获取仪表盘数据失败，请稍后重试')
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
    margin-bottom: 30px;
    color: #303133;
    font-weight: bold;
  }
}

.super-admin-panel {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.super-admin-tip {
  margin-left: 15px;
  font-size: 14px;
  color: #666;
}

.el-row {
  margin-bottom: 20px;
}

.box-card {
  cursor: pointer;
  transition: all 0.3s;
  height: 180px;
  margin-bottom: 20px;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  }

  .card-panel {
    height: 108px;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    
    &:hover {
      .card-panel-icon-wrapper {
        transform: scale(1.1);
      }
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
      background: #34bfa3;
      
      i {
        font-size: 32px;
        color: #fff;
      }
    }

    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px 15px 0 0;
      
      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }
      
      .card-panel-num {
        font-size: 22px;
        color: #666;
      }
    }
  }
}

.el-card__header {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}
</style> 