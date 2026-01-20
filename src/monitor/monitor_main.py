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


'''
目的:
处理已经生成好的 4000 多行的 JSON 文件，核心需求是保留文件中的 200 条数据、删除其余所有数据
如果一直不停止监控的话,程序一直跑会生成大量json文件,绘制图表无法展示完全;

import json
import os

def keep_200_items_in_json(file_path, keep_new_file=False):
    """
    保留JSON文件中的前200条数据，删除其余数据
    :param file_path: JSON文件的路径（相对/绝对路径）
    :param keep_new_file: 是否保留原文件，True则写入新文件（xxx_keep200.json），False则覆盖原文件
    """
    # 1. 安全校验：检查文件是否存在且是JSON文件
    if not os.path.exists(file_path):
        print(f"❌ 错误：文件不存在 - {file_path}")
        return
    if not file_path.endswith(".json"):
        print(f"⚠️  警告：文件不是JSON格式（后缀非.json） - {file_path}")

    try:
        # 2. 读取并解析JSON文件（支持大文件，避免内存溢出）
        with open(file_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        
        # 3. 校验JSON根结构是否为数组（只有数组才能按条数筛选）
        if not isinstance(json_data, list):
            print(f"❌ 错误：JSON文件根结构不是数组，无法按条数保留数据")
            return
        
        # 4. 保留前200条数据（如果数据不足200条，就保留全部）
        original_count = len(json_data)
        keep_count = min(200, original_count)  # 避免数据不足200条时报错
        kept_data = json_data[:keep_count]     # 取前200条
        
        # 5. 写入数据（可选覆盖原文件/写入新文件）
        if keep_new_file:
            # 写入新文件，原文件保留（推荐新手使用，防止误删）
            new_file_path = file_path.replace(".json", "_keep200.json")
            with open(new_file_path, "w", encoding="utf-8") as f:
                json.dump(kept_data, f, ensure_ascii=False, indent=2)
            print(f"✅ 处理完成！原文件保留，新文件已生成：")
            print(f"   原数据条数：{original_count} | 保留条数：{keep_count}")
            print(f"   新文件路径：{new_file_path}")
        else:
            # 覆盖原文件（谨慎使用！）
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(kept_data, f, ensure_ascii=False, indent=2)
            print(f"✅ 处理完成！原文件已覆盖：")
            print(f"   原数据条数：{original_count} | 保留条数：{keep_count}")
    
    except json.JSONDecodeError:
        print(f"❌ 错误：JSON文件格式错误，无法解析 - {file_path}")
    except PermissionError:
        print(f"❌ 错误：没有权限读写文件 - {file_path}")
    except Exception as e:
        print(f"❌ 处理失败，未知错误：{str(e)}")

# ==================== 主程序（修改这里的文件路径即可） ====================
# 替换成你的JSON文件路径（比如 "data.json" 或 "D:/files/big_json.json"）
JSON_FILE_PATH = "your_4000_lines_json_file.json"

# 推荐新手先设置为 True（保留原文件，生成新文件），确认无误后再改为 False
keep_200_items_in_json(JSON_FILE_PATH, keep_new_file=True)
'''