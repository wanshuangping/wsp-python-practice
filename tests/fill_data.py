import pandas as pd

csv_path = "../data/exercise_calories.csv"
df = pd.read_csv(csv_path)
df['start_time'] = [i * 10 for i in range(len(df))]
df['end_time'] = [(i + 1) * 10 for i in range(len(df))]
df.to_csv(csv_path,index=False,encoding='utf-8')
print("success,fill in")