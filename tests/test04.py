import json
import random
from pathlib import Path


MAX_ATTEMPTS = 7
SCORE_FILE = Path("best_scores.json")

DIFFICULTIES = {
    "1": {"name": "简单", "min": 1, "max": 20},
    "2": {"name": "普通", "min": 1, "max": 50},
    "3": {"name": "困难", "min": 1, "max": 100},
}


def load_best_scores():
    """读取历史最佳成绩。"""
    default_scores = {
        difficulty["name"]: None
        for difficulty in DIFFICULTIES.values()
    }

    if not SCORE_FILE.exists():
        return default_scores

    try:
        with SCORE_FILE.open("r", encoding="utf-8") as file:
            saved_scores = json.load(file)

        for name in default_scores:
            if name in saved_scores:
                default_scores[name] = saved_scores[name]

    except (json.JSONDecodeError, OSError):
        print("成绩文件读取失败，将使用空记录。")

    return default_scores


def save_best_scores(best_scores):
    """保存历史最佳成绩。"""
    try:
        with SCORE_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                best_scores,
                file,
                ensure_ascii=False,
                indent=4
            )
    except OSError:
        print("成绩保存失败。")


def choose_difficulty():
    """让玩家选择游戏难度。"""
    print("\n请选择难度：")
    print("1. 简单：1～20")
    print("2. 普通：1～50")
    print("3. 困难：1～100")

    while True:
        choice = input("请输入 1、2 或 3：").strip()

        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]

        print("输入无效，请重新选择。")


def get_star_rating(attempts):
    """根据猜测次数返回星级评价。"""
    if attempts <= 2:
        return "★★★★★ 天才猜手！"
    elif attempts <= 4:
        return "★★★★☆ 非常厉害！"
    elif attempts <= 6:
        return "★★★☆☆ 表现不错！"
    else:
        return "★★☆☆☆ 惊险过关！"


def show_best_score(difficulty_name, best_scores):
    """显示当前难度的最佳成绩。"""
    best = best_scores[difficulty_name]

    if best is None:
        print("当前难度还没有历史成绩。")
    else:
        print(f"当前难度最佳成绩：{best} 次")


def play_game(best_scores):
    """进行一局游戏。"""
    difficulty = choose_difficulty()

    difficulty_name = difficulty["name"]
    minimum = difficulty["min"]
    maximum = difficulty["max"]

    target = random.randint(minimum, maximum)

    print(f"\n你选择了【{difficulty_name}】难度。")
    print(f"我已经想好了一个 {minimum}～{maximum} 之间的整数。")
    print(f"你最多可以猜 {MAX_ATTEMPTS} 次。")
    show_best_score(difficulty_name, best_scores)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        remaining = MAX_ATTEMPTS - attempt

        while True:
            user_input = input(
                f"\n第 {attempt}/{MAX_ATTEMPTS} 次，请输入数字："
            ).strip()

            try:
                guess = int(user_input)
            except ValueError:
                print("请输入有效的整数。")
                continue

            if not minimum <= guess <= maximum:
                print(f"请输入 {minimum}～{maximum} 之间的数字。")
                continue

            break

        if guess == target:
            print(f"\n恭喜你猜对了！答案是 {target}。")
            print(f"你一共猜了 {attempt} 次。")
            print(f"星级评价：{get_star_rating(attempt)}")

            old_best = best_scores[difficulty_name]

            if old_best is None or attempt < old_best:
                best_scores[difficulty_name] = attempt
                save_best_scores(best_scores)

                if old_best is None:
                    print("这是该难度的第一个历史成绩！")
                else:
                    print(f"新纪录！原纪录是 {old_best} 次。")
            else:
                print(f"该难度的最佳纪录仍然是 {old_best} 次。")

            return

        if guess < target:
            print("猜小了。")
        else:
            print("猜大了。")

        if remaining > 0:
            print(f"还剩 {remaining} 次机会。")

    print("\n很遗憾，7 次机会已经用完。")
    print(f"正确答案是 {target}。")
    print("星级评价：★☆☆☆☆ 继续努力！")


def ask_to_play_again():
    """询问玩家是否再玩一次。"""
    while True:
        choice = input("\n是否再玩一次？(y/n)：").strip().lower()

        if choice in ("y", "yes", "是"):
            return True

        if choice in ("n", "no", "否"):
            return False

        print("请输入 y 或 n。")


def main():
    best_scores = load_best_scores()

    print("=" * 30)
    print("欢迎来到猜数字游戏")
    print("=" * 30)

    while True:
        play_game(best_scores)

        if not ask_to_play_again():
            print("\n游戏结束，欢迎下次再来！")
            break


if __name__ == "__main__":
    main()