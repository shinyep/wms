#!/usr/bin/env python
import os
import sys
import logging
import argparse
from datetime import datetime

# 添加项目根目录到sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

# 导入项目相关模块
from django.apps import apps
from apps.warehouse.views import WarehouseViewSet

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs', 'cron_tasks.log')),
    ]
)
logger = logging.getLogger(__name__)

def create_monthly_reports():
    """
    该功能已禁用：不再自动创建月度报表
    """
    logger.info("每月自动创建月度报表功能已被禁用")
    logger.info("如需手动创建报表，请使用前端界面的'补创建当月报表'功能")
    return {
        'success_count': 0,
        'error_count': 0,
        'message': '自动创建月度报表功能已禁用'
    }
    
def main():
    """主函数，处理命令行参数"""
    parser = argparse.ArgumentParser(description='WMS系统自动化任务脚本')
    parser.add_argument('task', choices=['create_monthly_reports'], help='要执行的任务名称')
    parser.add_argument('--force', action='store_true', help='强制执行任务，忽略时间检查')
    
    args = parser.parse_args()
    
    logger.info(f"准备执行任务: {args.task}")
    
    if args.task == 'create_monthly_reports':
        logger.info("每月自动创建月度报表功能已被禁用")
        logger.info("如需手动创建报表，请使用前端界面的功能")
    
if __name__ == '__main__':
    main() 