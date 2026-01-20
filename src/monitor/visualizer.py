import matplotlib.pyplot as plt
import json
import os

def plot_monitor_data():
    # 1. 定位日志文件
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_file = os.path.join(base_dir, "logs", "live_monitor.json")

    # 2. 读取数据
    timestamps = []
    heart_rates = []

    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            timestamps.append(data['timestamp'])
            heart_rates.append(data['heart_rate'])

    # 3. 绘图 (只取最后 20 条数据，防止图表太拥挤)
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps[-20:], heart_rates[-20:], marker='o', color='r', linestyle='-')

    # 4. 美化图表
    plt.title("实时心率监控图 (最近 20 次采样)")
    plt.xlabel("时间")
    plt.ylabel("心率 (bpm)")
    plt.xticks(rotation=45)  # 时间文字旋转 45 度防止重叠
    plt.grid(True)

    # 解决中文显示问题（针对 Mac/Windows 可能需要设置字体）
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 如果报错可以注释掉这行
    plt.rcParams['axes.unicode_minus'] = False

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_monitor_data()