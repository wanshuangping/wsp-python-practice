import os

# 1. 定位项目根目录 (相对于 src/config.py 往上走一级)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. 定义统一路径
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_PATH = os.path.join(DATA_DIR, "exercise_calories.csv")
VIDEO_INPUT = os.path.join(DATA_DIR, "TERR1708-GY.mp4")
OUTPUT_DIR = os.path.join(DATA_DIR, "outputs")

# 自动检查并创建输出文件夹
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)