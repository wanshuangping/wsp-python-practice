import os
import pandas as pd
from moviepy import VideoFileClip  # 适配新版 MoviePy 2.x 导入方式


def run_batch_processing():
    # 1. 路径设置
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "..", "data", "exercise_calories.csv")
    video_input = os.path.join(current_dir, "..", "data", "TERR1708-GY.mp4")
    output_folder = os.path.join(current_dir, "..", "data", "outputs")

    # 自动创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"📁 已创建输出目录: {output_folder}")

    # 2. 读取任务单 (增加 encoding 防止中文乱码)
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except:
        df = pd.read_csv(csv_path, encoding='gbk')

    # 3. 核心循环：一行数据 = 一个短视频
    print("🚀 批量处理启动...")

    with VideoFileClip(video_input) as full_video:
        for index, row in df.iterrows():
            # 获取 CSV 里的数据
            name = row['运动']
            start = row['start_time']
            end = row['end_time']

            # 定义文件名：例如 0_游泳.mp4
            output_filename = f"{index}_{name}.mp4"
            save_path = os.path.join(output_folder, output_filename)

            print(f"🎬 正在处理 ({index + 1}/{len(df)}): {name} [{start}s - {end}s]")

            # 执行裁剪逻辑
            # subclipped 是 MoviePy 2.x 的新方法
            clip = full_video.subclipped(start, end)

            # 自动变竖屏 (9:16)
            w, h = clip.size
            target_w = int(h * 9 / 16)
            final_clip = clip.cropped(x_center=w / 2, y_center=h / 2, width=target_w, height=h)

            # 导出 (去掉 audio_codec 如果视频没声音，或者保留以防万一)
            final_clip.write_videofile(save_path, codec="libx264", audio_codec="aac")
            print(f"✅ 已完成: {output_filename}")


if __name__ == "__main__":
    run_batch_processing()
# 这段代码会像流水线工人一样，读取表格里的每一行，然后去视频里“切”对应的片段。
'''
在 PyCharm 中补全 CSV 数据
请点击 exercise_calories.csv 选项卡，将内容手动修改为如下格式。
我们需要给 Python 两个关键信息：**start_time（开始秒数）**和 end_time（结束秒数）
运动,热量消耗（大卡）,start_time,end_time
游泳,1036,0,5
快跑,700,10,15
体能训练,650,20,25
跳绳,448,30,35
MoviePy 版本差异：如果你运行报错提示没有 subclipped，
请将其改回 subclip（旧版）；如果提示没有 cropped，请改回 crop。
查看 outputs 文件夹：运行成功后，点击左侧项目栏的 data 文件夹，
你会看到多了一个 outputs 目录，里面整齐排列着切好的视频。
Git 提交记录：这是一个巨大的阶段性进步，建议完成运行后执行：
git add .
git commit -m "实现基于CSV的批量视频自动裁剪"
git push
'''
