import os
def get_data_dir():
    """职业技巧：动态获取 data 文件夹的绝对路径
    文件目录操作创建os.mkdir(‘’),删除空目录os.rmdir(‘’),删除文件/目录os.remove(‘’)
    ,重命名os.rename(‘’),遍历文件/文件夹os.listdir(‘’)
    """
    # 先获取当前文件的目录 (src)，再找它的父目录，最后进入 data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "..", "data") # 拼接路径,自动适配系统分隔符
    return os.path.abspath(data_dir) #获取绝对路径
def check_file():
    """练习任务：检查 data 文件夹下的文件"""
    path = get_data_dir()
    print(f"---正在检查数据中心:{path} ---")

    if os.path.exists(path):
        os.path.exists(path) # 判断路径是否存在
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
5.使用终端指令上传:git add .
6.git commit -m "对更新的内容做简单的描述"
7.git push(上传)
8.开梯子的设置:
git config --global --unset http.proxy
git config --global --unset https.proxy
git config --global http.postBuffer 524288000(增大缓存)
以上4-8说的是怎么在mac终端把代码上传和更新
9.os库是python程序与操作系统进行交互的内置库
"""
