import logging
import os

# 配置日志输出格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("task_log.txt"), # 同时保存到文件
        logging.StreamHandler()              # 同时输出到控制台
    ]
)

# 使用示例
logging.info("🚀 批量剪辑任务启动...")
logging.error("❌ 处理第 5 行时出错：结束时间超过视频总长")