#!/bin/bash
# 1. 进入你的项目根目录
cd /Users/temu/PycharmProjects/pythonProject

# 2. 使用项目自带的虚拟环境运行数据库同步脚本
# 这样可以确保所有依赖包（如 akshare, sqlite3）都能被正确加载
./.venv/bin/python src/crawler/data_storage.py >> logs/auto_update.log 2>&1