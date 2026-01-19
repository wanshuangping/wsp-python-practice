import os
import pandas as pd
from moviepy import VideoFileClip
# 批量化
try:
    from moviepy import VideoFileClip
except ImportError:
    from moviepy.editor import VideoFileClip
def run_batch_task():
    # 1. 自动定位路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "..", "data", "exercise_calories.csv")
    video_input = os.path.join(current_dir, "..", "data", "TERR1708-GY.mp4")
    output_dir = os.path.join(current_dir, "..", "data", "outputs")

    # 自动创建输出文件夹
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 2. 读取 CSV 任务表 (如果报错 UnicodeDecodeError，请尝试 encoding='gbk')
    print(f"📖 正在读取任务清单...")
    df = pd.read_csv(csv_path)

    # 3. 循环处理每一行任务
    with VideoFileClip(video_input) as full_video:
        # 假设 CSV 列名是 'start_time' 和 'end_time'
        for index, row in df.iterrows():
            start = row['start_time']
            end = row['end_time']
            output_name = f"clip_{index}.mp4"
            target_path = os.path.join(output_dir, output_name)

            print(f"🎬 正在切割第 {index+1} 段: {start}s -> {end}s")

            # 时间切割 + 9:16 居中裁剪
            clip = full_video.subclip(start, end)
            w, h = clip.size
            target_w = int(h * 9/16)
            final_clip = clip.crop(x_center=w/2, y_center=h/2, width=target_w, height=h)

            # 导出视频
            final_clip.write_videofile(target_path, codec="libx264", audio_codec="aac")
            print(f"✅ 已保存: {output_name}")

if __name__ == "__main__":
    run_batch_task()