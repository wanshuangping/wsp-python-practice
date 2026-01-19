import pandas as pd  # 用这个库存来操作

csv_path = "../data/exercise_calories.csv"  # 告诉需要操作的文件路径
df = pd.read_csv(csv_path)   # 用这个方法读取
df['start_time'] = [i * 10 for i in range(len(df))]  # 需要添加的列名,做个循环
df['end_time'] = [(i + 1) * 10 for i in range(len(df))]
df.to_csv(csv_path,index=False,encoding='utf-8') # 输出
print("success,fill in")