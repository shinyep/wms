<template>
  <el-card style="margin-bottom:20px;">
    <div slot="header" class="clearfix">
      <span>个人信息</span>
    </div>

    <div class="user-profile">
      <div class="box-center">
        <el-avatar :size="100" :src="user.avatar" />
      </div>
      <div class="box-center">
        <div class="user-name text-center">{{ user.name }}</div>
        <div class="user-role text-center text-muted">
          {{ roles }}
        </div>
      </div>
    </div>

    <div class="user-bio">
      <div class="user-education user-bio-section">
        <div class="user-bio-section-header"><i class="el-icon-trophy" />角色</div>
        <div class="user-bio-section-body">
          <div v-for="(role, index) in user.roles" :key="index" class="text-muted">
            {{ roleNames[role] || role }}
          </div>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      default: () => {
        return {
          name: '',
          avatar: '',
          roles: []
        }
      }
    }
  },
  data() {
    return {
      roleNames: {
        admin: '管理员',
        editor: '编辑',
        warehouse: '仓库管理员'
      }
    }
  },
  computed: {
    roles() {
      if (this.user.roles && this.user.roles.length > 0) {
        return this.user.roles.map(role => this.roleNames[role] || role).join('，')
      }
      return '无角色'
    }
  }
}
</script>

<style lang="scss" scoped>
.box-center {
  margin: 0 auto;
  display: table;
}

.text-muted {
  color: #777;
}

.user-profile {
  .user-name {
    font-weight: bold;
    font-size: 20px;
    margin: 10px 0;
  }

  .box-center {
    padding-top: 10px;
  }

  .user-role {
    padding-top: 10px;
    font-weight: 400;
  }
}

.user-bio {
  margin-top: 20px;
  color: #606266;

  .user-bio-section {
    margin-bottom: 15px;

    .user-bio-section-header {
      border-bottom: 1px solid #dfe6ec;
      padding-bottom: 10px;
      margin-bottom: 10px;
      font-weight: bold;
    }
  }
}
</style> 