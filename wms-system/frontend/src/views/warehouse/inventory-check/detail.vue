<template>
  <div class="app-container">
    <div class="header">
      <el-page-header @back="goBack" :content="'盘点详情：' + checkNo" />
    </div>

    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>基本信息</span>
          </div>
          <el-descriptions :column="3" border>
            <el-descriptions-item label="盘点单号">{{ checkInfo.checkNo }}</el-descriptions-item>
            <el-descriptions-item label="盘点类型">{{ checkInfo.checkType }}</el-descriptions-item>
            <el-descriptions-item label="盘点区域">{{ checkInfo.checkArea }}</el-descriptions-item>
            <el-descriptions-item label="负责人">{{ checkInfo.manager }}</el-descriptions-item>
            <el-descriptions-item label="开始时间">{{ checkInfo.startTime }}</el-descriptions-item>
            <el-descriptions-item label="完成时间">{{ checkInfo.endTime }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>盘点统计</span>
            <el-button
              style="float: right; padding: 3px 0"
              type="text"
              @click="handleExport">
              <i class="el-icon-download"></i> 导出报告
            </el-button>
          </div>
          <el-row :gutter="20" class="panel-group">
            <el-col :span="6">
              <div class="card-panel">
                <div class="card-panel-icon-wrapper" style="background: #409EFF">
                  <i class="el-icon-goods"></i>
                </div>
                <div class="card-panel-description">
                  <div class="card-panel-text">盘点商品数</div>
                  <count-to :start-val="0" :end-val="statistics.totalItems" :duration="2600" class="card-panel-num"/>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="card-panel">
                <div class="card-panel-icon-wrapper" style="background: #67C23A">
                  <i class="el-icon-check"></i>
                </div>
                <div class="card-panel-description">
                  <div class="card-panel-text">账实相符</div>
                  <count-to :start-val="0" :end-val="statistics.matchItems" :duration="2600" class="card-panel-num"/>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="card-panel">
                <div class="card-panel-icon-wrapper" style="background: #E6A23C">
                  <i class="el-icon-warning"></i>
                </div>
                <div class="card-panel-description">
                  <div class="card-panel-text">盘盈数量</div>
                  <count-to :start-val="0" :end-val="statistics.profitItems" :duration="2600" class="card-panel-num"/>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="card-panel">
                <div class="card-panel-icon-wrapper" style="background: #F56C6C">
                  <i class="el-icon-warning"></i>
                </div>
                <div class="card-panel-description">
                  <div class="card-panel-text">盘亏数量</div>
                  <count-to :start-val="0" :end-val="statistics.lossItems" :duration="2600" class="card-panel-num"/>
                </div>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="box-card" style="margin-top: 20px">
      <div slot="header" class="clearfix">
        <span>盘点明细</span>
        <el-radio-group v-model="listQuery.diffType" size="small" style="float: right" @change="handleFilter">
          <el-radio-button label="">全部</el-radio-button>
          <el-radio-button label="profit">盘盈</el-radio-button>
          <el-radio-button label="loss">盘亏</el-radio-button>
          <el-radio-button label="match">相符</el-radio-button>
        </el-radio-group>
      </div>

      <el-table
        v-loading="listLoading"
        :data="detailList"
        border
        style="width: 100%">
        <el-table-column label="商品编码" prop="code" align="center" />
        <el-table-column label="商品名称" prop="name" align="center" />
        <el-table-column label="规格型号" prop="spec" align="center" />
        <el-table-column label="系统库存" prop="systemQuantity" align="center" />
        <el-table-column label="实际库存" prop="actualQuantity" align="center" />
        <el-table-column label="差异数量" align="center">
          <template slot-scope="{row}">
            <span :class="getDiffClass(row.diff)">{{ row.diff }}</span>
          </template>
        </el-table-column>
        <el-table-column label="差异状态" align="center">
          <template slot-scope="{row}">
            <el-tag :type="getDiffType(row.diff)">
              {{ getDiffLabel(row.diff) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="盘点时间" prop="checkTime" align="center" />
      </el-table>

      <pagination
        v-show="total>0"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="getList" />
    </el-card>
  </div>
</template>

<script>
import CountTo from 'vue-count-to'
import Pagination from '@/components/Pagination'

export default {
  name: 'InventoryCheckDetail',
  components: {
    CountTo,
    Pagination
  },
  data() {
    return {
      checkNo: this.$route.query.id,
      checkInfo: {
        checkNo: '',
        checkType: '',
        checkArea: '',
        manager: '',
        startTime: '',
        endTime: ''
      },
      statistics: {
        totalItems: 0,
        matchItems: 0,
        profitItems: 0,
        lossItems: 0
      },
      listQuery: {
        page: 1,
        limit: 10,
        diffType: ''
      },
      total: 0,
      listLoading: false,
      detailList: []
    }
  },
  created() {
    this.getCheckInfo()
    this.getStatistics()
    this.getList()
  },
  methods: {
    goBack() {
      this.$router.push('/warehouse/inventory-check')
    },
    getCheckInfo() {
      // 模拟获取盘点信息
      this.checkInfo = {
        checkNo: this.checkNo,
        checkType: '全面盘点',
        checkArea: 'A区-A1货架',
        manager: '张三',
        startTime: '2024-03-09 10:00:00',
        endTime: '2024-03-09 11:30:00'
      }
    },
    getStatistics() {
      // 模拟获取统计数据
      this.statistics = {
        totalItems: 100,
        matchItems: 80,
        profitItems: 10,
        lossItems: 10
      }
    },
    getList() {
      this.listLoading = true
      // 模拟获取盘点明细
      setTimeout(() => {
        this.detailList = [
          {
            code: 'SP001',
            name: '测试商品1',
            spec: '规格1',
            systemQuantity: 100,
            actualQuantity: 98,
            diff: -2,
            checkTime: '2024-03-09 10:30:00'
          }
        ]
        this.total = this.detailList.length
        this.listLoading = false
      }, 500)
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleExport() {
      this.$message({
        message: '报告导出中...',
        type: 'success'
      })
    },
    getDiffClass(diff) {
      if (diff > 0) return 'text-success'
      if (diff < 0) return 'text-danger'
      return ''
    },
    getDiffType(diff) {
      if (diff > 0) return 'success'
      if (diff < 0) return 'danger'
      return 'info'
    },
    getDiffLabel(diff) {
      if (diff > 0) return '盘盈'
      if (diff < 0) return '盘亏'
      return '相符'
    }
  }
}
</script>

<style lang="scss" scoped>
.header {
  margin-bottom: 20px;
}

.panel-group {
  margin-top: 18px;

  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
    border-color: rgba(0, 0, 0, .05);
    
    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
      
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

.text-success {
  color: #67C23A;
}

.text-danger {
  color: #F56C6C;
}
</style> 