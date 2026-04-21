# def reverseWords(input_str):
#     inputWords = input_str.split()
#     inputWords = inputWords[-1::-1]
#     output = ''.join(inputWords)
#     return output
# if __name__ == '__main__':
#     input_str = 'i leke rob'
#     rw = reverseWords(input_str)
#     print(rw)
# tuple = ('abc',123,2.3,'roy',70.1)
# tinytuple = (123,'roy')
# print(tuple)
# print(tuple[0])
# print(tuple[2:])
# print(tinytuple * 2)
# print(tuple + tinytuple)
# tup = (1,2,3,4,5,6,7)
# # tup[0] = 11(不能直接对元祖元素修改会报语法错误)
# print(tup[0])
# tup1 = ()
# tup2 = (20, )
# print(tup1,tup2)
# sets = {'baidu','xiaomi','1688'}
# if '1688' in sets:
#     print('1688 is sets now')
# else:
#     print('1688 not in set')
# a = {'dhajklgvas'}
# b = {'dafghjklufs'}
# print(a)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体（解决matplotlib中文乱码问题）
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# ===================== 1. 构建数据集 =====================
# 数据集1：深圳各区总人口+本科占比（2020普查）
district_total = pd.DataFrame({
    "区域": ["南山", "福田", "罗湖", "盐田", "龙华", "龙岗", "宝安", "坪山", "光明"],
    "总人口(万)": [174, 150, 111, 20, 244, 383, 434, 53, 106],
    "本科占比(%)": [24.7, 20.3, 14.3, 14.0, 12.2, 10.9, 10.3, 8.6, 5.9]
})

# 数据集2：2030-2040年各区20-30岁适龄人数(万)
district_age2030 = pd.DataFrame({
    "区域": ["南山", "福田", "罗湖", "盐田", "龙华", "龙岗", "宝安", "坪山", "光明"],
    "适龄人数(万)": [15, 13, 10, 2, 16, 32, 32, 5, 8]
})

# 数据集3：重点区街道级本科占比
street_data = pd.DataFrame({
    "所属区": ["宝安"]*10 + ["龙岗"]*11 + ["福田"]*10 + ["南山"]*8 + ["龙华"]*6,
    "街道": [
        # 宝安
        "新安", "西乡", "航城", "福永", "福海", "沙井", "新桥", "松岗", "燕罗", "石岩",
        # 龙岗
        "平湖", "坪地", "南湾", "坂田", "布吉", "龙城", "龙岗", "横岗", "吉华", "宝龙", "园山",
        # 福田
        "南园", "园岭", "福田", "沙头", "香蜜湖", "梅林", "莲花", "华富", "福保", "华强北",
        # 南山
        "南头", "南山", "沙河", "蛇口", "招商", "粤海", "桃源", "西丽",
        # 龙华
        "观湖", "民治", "龙华", "大浪", "福城", "观澜"
    ],
    "本科占比(%)": [
        # 宝安
        19.6, 18.2, 9.0, 10.0, 7.0, 4.5, 5.5, 4.8, 3.3, 6.0,
        # 龙岗
        1.8, 3.9, 11.0, 21.0, 14.0, 15.5, 8.0, 11.0, 12.0, 5.3, 3.9,
        # 福田
        7.9, 22.0, 13.3, 21.0, 26.0, 22.0, 27.0, 20.6, 24.0, 14.8,
        # 南山
        23.4, 21.8, 25.0, 20.0, 27.6, 34.7, 27.0, 17.8,
        # 龙华
        8.0, 22.0, 13.5, 8.0, 6.8, 4.3
    ]
})

# ===================== 2. 绘制图表 =====================
fig, axes = plt.subplots(2, 2, figsize=(20, 16))
fig.suptitle("深圳各区&街道人口与本科占比可视化（2020普查+2030-2040适龄人口）", fontsize=18, y=0.98)

# 子图1：各区总人口+本科占比（双轴图）
ax1 = axes[0, 0]
district_total_sorted = district_total.sort_values("总人口(万)", ascending=False)
# 柱状图：总人口
sns.barplot(x="区域", y="总人口(万)", data=district_total_sorted, ax=ax1, color="#4287f5", alpha=0.7, label="总人口(万)")
ax1.set_title("各区总人口与本科占比对比", fontsize=14)
ax1.set_xlabel("区域", fontsize=12)
ax1.set_ylabel("总人口(万)", fontsize=12, color="#4287f5")
ax1.tick_params(axis="y", labelcolor="#4287f5")
# 折线图：本科占比
ax1_twin = ax1.twinx()
sns.lineplot(x="区域", y="本科占比(%)", data=district_total_sorted, ax=ax1_twin, color="#f54242", marker="o", linewidth=2, label="本科占比(%)")
ax1_twin.set_ylabel("本科占比(%)", fontsize=12, color="#f54242")
ax1_twin.tick_params(axis="y", labelcolor="#f54242")
# 合并图例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_twin.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

# 子图2：2030-2040年各区20-30岁适龄人数
ax2 = axes[0, 1]
district_age2030_sorted = district_age2030.sort_values("适龄人数(万)", ascending=False)
sns.barplot(x="区域", y="适龄人数(万)", data=district_age2030_sorted, ax=ax2, palette="viridis")
ax2.set_title("2030-2040年各区20-30岁适龄人数(万)", fontsize=14)
ax2.set_xlabel("区域", fontsize=12)
ax2.set_ylabel("适龄人数(万)", fontsize=12)
# 数值标注
for container in ax2.containers:
    ax2.bar_label(container, fmt="%.0f", fontsize=10)

# 子图3：重点区街道本科占比（横向条形图）
ax3 = axes[1, 0]
# 筛选占比≥15%的街道（突出高学历街道）
high_edu_streets = street_data[street_data["本科占比(%)"] >= 15].sort_values("本科占比(%)", ascending=True)
sns.barplot(x="本科占比(%)", y="街道", hue="所属区", data=high_edu_streets, ax=ax3, palette="Set2")
ax3.set_title("重点区本科占比≥15%的街道排名", fontsize=14)
ax3.set_xlabel("本科占比(%)", fontsize=12)
ax3.set_ylabel("街道", fontsize=12)
ax3.legend(loc="lower right")

# 子图4：各区街道本科占比分布（箱线图）
ax4 = axes[1, 1]
sns.boxplot(x="所属区", y="本科占比(%)", data=street_data, ax=ax4, palette="coolwarm")
ax4.set_title("各区街道本科占比分布差异", fontsize=14)
ax4.set_xlabel("所属区", fontsize=12)
ax4.set_ylabel("本科占比(%)", fontsize=12)

# 调整布局
plt.tight_layout()
# 保存图片（可修改路径）
plt.savefig("深圳人口学历可视化.png", dpi=300, bbox_inches="tight")
plt.show()