import random

# 简单的 猜数字小游戏，可以练习变量、循环、条件判断、函数和异常处理
def play_game():
    target = random.randint(1, 100)
    attempts = 0
    print("我已经想好了一个 1～100 之间的数字。")
    while True:
        user_input = input("请输入你猜的数字，或输入 q 退出：").strip()
        if user_input.lower() == "q":
            print(f"游戏结束，正确答案是 {target}。")
            break
        try:
            guess = int(user_input)
        except ValueError:
            print("请输入有效的整数。")
            continue
        if not 1 <= guess <= 100:
            print("数字必须在 1～100 之间。")
            continue
        attempts += 1
        if guess < target:
            print("猜小了。")
        elif guess > target:
            print("猜大了。")
        else:
            print(f"猜对了！你一共猜了 {attempts} 次。")
            break


play_game()