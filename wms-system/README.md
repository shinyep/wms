# WMS仓库管理系统

一个现代化的仓库管理系统，基于Vue 2 + Element UI前端和Django + PostgreSQL后端。

## 功能特点

- 用户权限管理：基于角色的访问控制
- 仓库管理：仓库、库区、库位的层级管理
- 库存管理：实时库存查询、库存预警
- 入库管理：采购入库、退货入库、调拨入库
- 出库管理：销售出库、领料出库、调拨出库
- 库存盘点：定期盘点、动态盘点
- 商品管理：商品信息、分类管理
- 订单管理：订单创建、订单跟踪
- 报表统计：库存报表、出入库报表
- 系统管理：用户、角色、日志管理

## 技术栈

### 前端

- Vue 2.7.14
- Element UI 2.15.14
- Vuex 3.6.2
- Vue Router 3.6.5
- Axios 0.21.1
- ECharts 5.4.3（数据可视化）

### 后端

- Django 4.2.7
- Django REST Framework 3.15.2
- PostgreSQL 数据库
- JWT认证
- Swagger API文档

## 系统架构

- 前后端分离架构
- RESTful API设计
- 响应式布局，支持PC和移动端
- 多角色权限控制

## 开发环境搭建

### 前端

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run serve
```

### 后端

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

## 生产环境部署

### 前端

```bash
# 构建生产版本
npm run build
```

### 后端

推荐使用Gunicorn + Nginx部署Django应用。

## 数据库选择建议

本系统默认使用PostgreSQL数据库，也支持MySQL。对于小型团队：

- **PostgreSQL优势**：更强大的数据完整性、复杂查询支持、地理位置数据支持
- **MySQL优势**：配置简单、资源占用较少、更多托管服务支持

建议：考虑到WMS系统的数据完整性要求和未来可能的扩展性，推荐使用PostgreSQL。

## 许可证

MIT 