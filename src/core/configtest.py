import pandas as pd
import os
from moviepy import VideoFileClip
# 关键：从上层目录的 config 模块导入路径变量
from src.config import CSV_PATH, VIDEO_INPUT, OUTPUT_DIR


def run_batch_processing():
    df = pd.read_csv(CSV_PATH)

    with VideoFileClip(VIDEO_INPUT) as full_video:
        for index, row in df.iterrows():
            # --- 【防护网：try 开始】 ---
            try:
                start = row['start_time']
                end = row['end_time']
                name = row['运动']

                # 逻辑验证：防御性编程
                if start >= end:
                    raise ValueError(f"时间范围无效: {start}s -> {end}s")

                print(f"🎬 正在处理第 {index + 1} 个: {name}...")

                # 执行剪辑 (使用你之前掌握的逻辑)
                target_path = os.path.join(OUTPUT_DIR, f"{name}.mp4")
                clip = full_video.subclipped(start, end)
                # ... 裁剪比例代码 ...
                clip.write_videofile(target_path, codec="libx264")

            except Exception as e:
                # 即使出错了，也只打印错误并跳过，不会导致整个程序崩溃
                print(f"⚠️ 跳过任务 '{row.get('运动', '未知')}': {e}")
                continue
                # --- 【防护网：except 结束】 ---