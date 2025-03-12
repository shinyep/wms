const getters = {
  sidebar: state => state.app.sidebar,
  size: state => state.app.size,
  device: state => state.app.device,
  token: state => state.user.token,
  avatar: state => state.user.avatar,
  name: state => state.user.name,
  roles: state => state.user.roles,
  permission_routes: state => state.permission.routes,
  user: state => state.user.user,
  userLevel: state => state.user.user ? state.user.user.level : 0,
  permissions: state => state.user.permissions || {},
  // 通用权限
  canView: state => state.user.permissions ? state.user.permissions.can_view : false,
  canAdd: state => state.user.permissions ? state.user.permissions.can_add : false,
  canEdit: state => state.user.permissions ? state.user.permissions.can_edit : false,
  canDelete: state => state.user.permissions ? state.user.permissions.can_delete : false,
  canExport: state => state.user.permissions ? state.user.permissions.can_export : false,
  canImport: state => state.user.permissions ? state.user.permissions.can_import : false,
  // 库存特定权限
  inventoryPermissions: state => state.user.permissions ? state.user.permissions.inventory || {} : {},
  canViewInventory: state => state.user.permissions && state.user.permissions.inventory ? state.user.permissions.inventory.can_view_inventory : false,
  canAddInventory: state => state.user.permissions && state.user.permissions.inventory ? state.user.permissions.inventory.can_add_inventory : false,
  canEditInventory: state => state.user.permissions && state.user.permissions.inventory ? state.user.permissions.inventory.can_edit_inventory : false,
  canDeleteInventory: state => state.user.permissions && state.user.permissions.inventory ? state.user.permissions.inventory.can_delete_inventory : false,
  canExportInventory: state => state.user.permissions && state.user.permissions.inventory ? state.user.permissions.inventory.can_export_inventory : false,
  
  // 仓库特定权限
  warehousePermissions: state => state.user.permissions ? state.user.permissions.warehouse || {} : {},
  canViewWarehouse: state => {
    // 超级管理员拥有所有权限
    if (state.user.roles && state.user.roles.includes('admin')) {
      return true;
    }
    return state.user.permissions && state.user.permissions.warehouse ? state.user.permissions.warehouse.can_view_warehouse : false;
  },
  canAddWarehouse: state => {
    // 超级管理员拥有所有权限
    if (state.user.roles && state.user.roles.includes('admin')) {
      return true;
    }
    return state.user.permissions && state.user.permissions.warehouse ? state.user.permissions.warehouse.can_add_warehouse : false;
  },
  canEditWarehouse: state => {
    // 超级管理员拥有所有权限
    if (state.user.roles && state.user.roles.includes('admin')) {
      return true;
    }
    return state.user.permissions && state.user.permissions.warehouse ? state.user.permissions.warehouse.can_edit_warehouse : false;
  },
  canDeleteWarehouse: state => {
    // 超级管理员拥有所有权限
    if (state.user.roles && state.user.roles.includes('admin')) {
      return true;
    }
    return state.user.permissions && state.user.permissions.warehouse ? state.user.permissions.warehouse.can_delete_warehouse : false;
  },
  canExportWarehouse: state => {
    // 超级管理员拥有所有权限
    if (state.user.roles && state.user.roles.includes('admin')) {
      return true;
    }
    return state.user.permissions && state.user.permissions.warehouse ? state.user.permissions.warehouse.can_export_warehouse : false;
  },
  
  // 超级管理员
  isSuperAdmin: state => {
    // 从权限中判断，如果没有，则从角色判断
    if (state.user.permissions && state.user.permissions.is_super_admin) {
      return state.user.permissions.is_super_admin;
    }
    // 如果角色包含 admin，也视为超级管理员
    return state.user.roles && state.user.roles.includes('admin');
  }
}

export default getters 