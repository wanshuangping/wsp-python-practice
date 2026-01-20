import matplotlib.pyplot as plt
import json
import os

# 针对 Mac 系统 (你的设备是 Mac mini) 修复中文
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False # 修复负号显示
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
    # 使用美化风格
    plt.style.use('dark_background')  # 开启酷炫黑夜模式

    plt.figure(figsize=(12, 6))
    # 换成浅蓝色，带阴影填充
    plt.fill_between(timestamps[-30:], heart_rates[-30:], color="skyblue", alpha=0.3)
    plt.plot(timestamps[-30:], heart_rates[-30:], color="Slateblue", marker='o', linewidth=2)

    plt.title("实时心率波形监控 (Real-time Heart Rate)", fontsize=16, pad=20)
    plt.ylabel("BPM", fontsize=12)
    plt.grid(color='gray', linestyle='--', alpha=0.5)

    # 解决中文显示问题（针对 Mac/Windows 可能需要设置字体）
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 如果报错可以注释掉这行
    # plt.rcParams['axes.unicode_minus'] = False
    # 在 plt.show() 之前加入
    ax = plt.gca()
    # 设置每隔 5 个显示一个刻度
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % 5 != 0:
            label.set_visible(False)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_monitor_data()




'''
横轴时间戳堆叠重合的解决办法
1.稀疏显示（最推荐）不要每个点都标时间，每隔 5 个点标一个，画面瞬间清爽
# 在 plt.show() 之前加入
ax = plt.gca()
# 设置每隔 5 个显示一个刻度
for n, label in enumerate(ax.xaxis.get_ticklabels()):
    if n % 5 != 0:
        label.set_visible(False)
2.增大旋转角度 + 缩小字号(现在的旋转角度可能不够，或者字太大)
plt.xticks(rotation=45, fontsize=8)
3.格式化时间（精简字符串）(目前时间戳包含“时:分:秒”，太占位置。如果只显示“分:秒”，空间会多出一倍)
# 处理数据时截取字符串
short_timestamps = [t[3:] for t in timestamps[-30:]] # 只取 "MM:SS"
plt.plot(short_timestamps, heart_rates[-30:], ...)
'''