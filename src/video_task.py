import os
from moviepy import VideoFileClip

# 【关键修正】新版 MoviePy 2.x 的导入方式
try:
    from moviepy import VideoFileClip
except ImportError:
    from moviepy.editor import VideoFileClip


def run_task():
    # 1. 路径获取
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 确保路径跳出 src 进入 data
    input_path = os.path.abspath(os.path.join(current_dir, "..", "data", "TERR1708-GY.mp4"))
    output_path = os.path.abspath(os.path.join(current_dir, "..", "data", "result_vertical.mp4"))

    print(f"🔍 检查文件路径: {input_path}")

    # 2. 检查文件
    if not os.path.exists(input_path):
        print(f"❌ 没找到视频文件！请确保文件在: {input_path}")
        return

    try:
        print("🎬 正在处理，请稍候...")
        # 3. 裁剪逻辑
        with VideoFileClip(input_path) as clip:
            w, h = clip.size
            target_w = int(h * 9 / 16)

            # 居中裁剪
            final_clip = clip.cropped(x1=(w - target_w) // 2, y1=0, x2=(w + target_w) // 2, y2=h)

            print("💾 正在导出视频渲染中...")
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
            print(f"✨ 成功！新视频已生成：{output_path}")

    except Exception as e:
        print(f"💥 运行崩溃了: {e}")


if __name__ == "__main__":
    run_task()