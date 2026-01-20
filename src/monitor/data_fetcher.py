import random
import time


def fetch_realtime_data():
    """
    模拟从云端接口获取当前的运动热量消耗
    """
    # 模拟网络延迟
    time.sleep(0.5)

    # 模拟返回的 JSON 数据
    data = {
        "timestamp": time.strftime("%H:%M:%S"),
        "calories": random.randint(300, 800),
        "heart_rate": random.randint(60, 160),
        "status": "online"
    }
    return data