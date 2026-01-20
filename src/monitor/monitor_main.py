import os
import time
import json
from data_fetcher import fetch_realtime_data


def start_monitoring():
    print("🚀 实时运动健康监控系统已启动...")
    print("按 Ctrl+C 可以停止监控\n")

    # 确定日志保存路径 (保存在项目根目录的 logs 文件夹下)
    # 获取当前文件所在目录的上一级的上一级，即项目根目录
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_dir = os.path.join(base_dir, "logs")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "live_monitor.json")

    try:
        while True:
            # 1. 获取数据
            current_data = fetch_realtime_data()

            # 2. 预警逻辑：如果心率超过 150，打印红色警告 (Terminal 里的特殊颜色代码)
            hr = current_data['heart_rate']
            timestamp = current_data['timestamp']

            if hr > 150:
                print(f"[{timestamp}] ⚠️ 预警：当前心率过高！({hr} bpm) 请注意休息！")
            else:
                print(f"[{timestamp}] 状态正常：心率 {hr} bpm, 消耗热量 {current_data['calories']} kcal")

            # 3. 数据持久化：追加写入 JSON 文件
            # 注意：真实的系统通常存入数据库，这里我们用追加模式模拟
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(current_data, ensure_ascii=False) + "\n")

            # 4. 设置采样间隔：每 3 秒获取一次
            time.sleep(3)

    except KeyboardInterrupt:
        print("\n🛑 监控已由用户手动停止。")


if __name__ == "__main__":
    start_monitoring()