# 仓库管理系统 (WMS)
本系统为公司内部定制系统，未经许可请勿使用，严禁二次开发和商用。

仓库管理系统是一个用于管理仓库物资入库、出库和库存的Web应用程序。系统支持多仓库管理、物资库存管理、月度报表生成等功能。

## 功能特点

- 仓库基本信息管理
- 物资入库和出库管理
- 库存管理和盘点
- 月度报表生成和导出
- 数据备份和恢复

## 系统要求

- Python 3.8+
- Node.js 14+
- SQLite3或PostgreSQL数据库

## 安装指南

### 后端安装

1. 进入后端目录：

```bash
cd wms-system/backend
```

2. 创建并激活虚拟环境：

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# 或
source .venv/bin/activate  # Linux/Mac
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

4. 配置环境变量：
   - 复制`.env.example`文件为`.env`
   - 修改`.env`文件中的配置信息

5. 初始化数据库：

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 前端安装

1. 进入前端目录：

```bash
cd wms-system/frontend
```

2. 安装依赖：

```bash
npm install
```

## 运行应用

### 运行后端

```bash
cd wms-system/backend
python manage.py runserver 8000
```

### 运行前端

```bash
cd wms-system/frontend
npm run dev
```

## 使用说明

1. 访问管理后台：`http://localhost:8000/admin`
2. 访问前端应用：`http://localhost:3000`

## 数据备份和恢复

系统支持数据备份和恢复功能：

1. 在仓库详情页面点击"备份数据"按钮
2. 备份文件会自动下载到本地
3. 通过"恢复备份"按钮可以上传备份文件恢复数据


## 许可证

本项目使用MIT许可证 - 详情见 [LICENSE](LICENSE) 文件
