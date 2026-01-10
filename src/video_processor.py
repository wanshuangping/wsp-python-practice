import os

def get_data_dir():
    """职业技巧：动态获取 data 文件夹的绝对路径"""
    # 先获取当前文件的目录 (src)，再找它的父目录，最后进入 data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "..", "data")
    return os.path.abspath(data_dir)

def check_file():
    """练习任务：检查 data 文件夹下的文件"""
    path = get_data_dir()
    print(f"---正在检查数据中心:{path} ---")

    if os.path.exists(path):
        os.path.exists(path)
        files = os.listdir(path)
        print(f"已找到{len(files)} 个文件:")
        for i in files:
            print(f"-{i}")
    else:
        print("错误,找不到data目录")

if __name__ == "__main__":
    check_file()
"""
1.2026.1.10作为26年写的第一段代码,通过代码来找文件夹的绝对路径;
2.虽然要大模型辅助了很多,但是通过ai的帮助修理了杂乱无序的文件命名;
3.以及每个文件夹内应该放置哪些文件和重塑文件命名;
4.联动了github在终端的操作下连接了本地服务把代码上传至github;
"""
