import datetime
import time

exam_date = datetime.datetime(2026, 12, 20)
while True:
    now = datetime.datetime.now()
    delta = exam_date - now
    days_left = delta.days
    if days_left < 0:
        print("考试已经结束了！")
        break
    print(f"距离2026年考研还有 {days_left} 天")
    time.sleep(86400) # 24小时