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

# -------------------------- 核心优化1：字体适配（兼容Windows/Mac/Linux）
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Zen Hei", "Heiti TC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
plt.rcParams["font.size"] = 10  # 全局字体大小优化，避免过小/过大
plt.rcParams["axes.titlepad"] = 15  # 标题与图表间距，提升美观度

# -------------------------- 核心优化2：完善数据集（新增收入增长数据）
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

# 数据集3：重点区街道级本科占比（不变，新增分组逻辑）
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

# 数据集4：2024 vs 2023 工资&可支配收入增长
income_growth = pd.DataFrame({
    "指标": ["工资增长", "年均可支配收入增长"],
    "增长率(%)": [1.0, 5.47]
})

# -------------------------- 核心优化3：图表布局与样式优化（3行2列，覆盖所有数据）
fig, axes = plt.subplots(3, 2, figsize=(22, 18))
fig.suptitle("深圳各区&街道人口与本科占比可视化（2020普查+2030-2040适龄人口+收入增长）",
             fontsize=20, y=0.98, fontweight="bold")

# 子图1：各区总人口+本科占比（双轴图，优化配色+数值标注）
ax1 = axes[0, 0]
district_total_sorted = district_total.sort_values("总人口(万)", ascending=False)
# 柱状图：总人口（渐变色，优化透明度）
bars1 = ax1.bar(x=district_total_sorted["区域"],
                height=district_total_sorted["总人口(万)"],
                color="#2E86AB", alpha=0.8, label="总人口(万)")
ax1.set_title("各区总人口与本科占比对比", fontsize=14, fontweight="bold")
ax1.set_xlabel("区域", fontsize=12)
ax1.set_ylabel("总人口(万)", fontsize=12, color="#2E86AB")
ax1.tick_params(axis="y", labelcolor="#2E86AB")
ax1.grid(axis="y", alpha=0.3)  # 新增网格线，提升可读性
# 总人口数值标注（优化位置，避免遮挡）
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 5,
             f"{height:.0f}", ha="center", va="bottom", color="#2E86AB", fontweight="bold")
# 折线图：本科占比
ax1_twin = ax1.twinx()
line1 = ax1_twin.plot(district_total_sorted["区域"],
                      district_total_sorted["本科占比(%)"],
                      color="#E63946", marker="o", linewidth=2.5, markersize=6, label="本科占比(%)")
ax1_twin.set_ylabel("本科占比(%)", fontsize=12, color="#E63946")
ax1_twin.tick_params(axis="y", labelcolor="#E63946")
# 本科占比数值标注
for i, val in enumerate(district_total_sorted["本科占比(%)"]):
    ax1_twin.text(i, val + 0.5, f"{val:.1f}%", ha="center", va="bottom", color="#E63946", fontweight="bold")
# 合并图例（优化位置，避免遮挡图表）
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_twin.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", frameon=True, fancybox=True, shadow=True)

# 子图2：2030-2040年各区20-30岁适龄人数（优化配色+数值标注）
ax2 = axes[0, 1]
district_age2030_sorted = district_age2030.sort_values("适龄人数(万)", ascending=False)
bars2 = sns.barplot(x="区域", y="适龄人数(万)", data=district_age2030_sorted, ax=ax2,
                    palette="viridis", alpha=0.8)
ax2.set_title("2030-2040年各区20-30岁适龄人数", fontsize=14, fontweight="bold")
ax2.set_xlabel("区域", fontsize=12)
ax2.set_ylabel("适龄人数(万)", fontsize=12)
ax2.grid(axis="y", alpha=0.3)
# 数值标注（优化大小和颜色）
for container in ax2.containers:
    ax2.bar_label(container, fmt="%.0f", fontsize=10, fontweight="bold", color="#1D3557")

# 子图3：2024 vs 2023 工资&可支配收入增长（新增，突出对比）
ax3 = axes[1, 0]
bars3 = ax3.bar(x=income_growth["指标"], height=income_growth["增长率(%)"],
                color=["#457B9D", "#A8DADC"], alpha=0.8, width=0.6)
ax3.set_title("2024年对比2023年增长情况", fontsize=14, fontweight="bold")
ax3.set_xlabel("增长指标", fontsize=12)
ax3.set_ylabel("增长率(%)", fontsize=12)
ax3.grid(axis="y", alpha=0.3)
# 数值标注（保留两位小数，突出收入增长）
for bar in bars3:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f"{height:.2f}%", ha="center", va="bottom", fontweight="bold", color="#1D3557")

# 子图4：高学历街道排名（优化筛选，新增分区配色）
ax4 = axes[1, 1]
# 筛选占比≥15%的街道（突出高学历街道，优化排序）
high_edu_streets = street_data[street_data["本科占比(%)"] >= 15].sort_values("本科占比(%)", ascending=True)
# 按所属区分色，提升辨识度
sns.barplot(x="本科占比(%)", y="街道", hue="所属区", data=high_edu_streets, ax=ax4,
            palette={"南山":"#2E86AB", "福田":"#457B9D", "宝安":"#A8DADC", "龙岗":"#F1FAEE", "龙华":"#E63946"},
            edgecolor="#1D3557", linewidth=0.5)
ax4.set_title("重点区本科占比≥15%的街道排名", fontsize=14, fontweight="bold")
ax4.set_xlabel("本科占比(%)", fontsize=12)
ax4.set_ylabel("街道", fontsize=12)
ax4.grid(axis="x", alpha=0.3)
ax4.legend(loc="lower right", frameon=True, fancybox=True, shadow=True)
# 数值标注
for i, val in enumerate(high_edu_streets["本科占比(%)"]):
    ax4.text(val + 0.5, i, f"{val:.1f}%", ha="left", va="center", fontweight="bold", color="#1D3557")

# 子图5：各区街道本科占比分布（优化箱线图样式，突出异常值）
ax5 = axes[2, 0]
sns.boxplot(x="所属区", y="本科占比(%)", data=street_data, ax=ax5,
            palette="coolwarm", linewidth=1.5, flierprops={"marker":"o", "markerfacecolor":"red", "markersize":6})
ax5.set_title("各区街道本科占比分布差异", fontsize=14, fontweight="bold")
ax5.set_xlabel("所属区", fontsize=12)
ax5.set_ylabel("本科占比(%)", fontsize=12)
ax5.grid(axis="y", alpha=0.3)
# 标注区域均值
for i, district in enumerate(street_data["所属区"].unique()):
    mean_val = street_data[street_data["所属区"] == district]["本科占比(%)"].mean()
    ax5.text(i, mean_val + 0.5, f"均值:{mean_val:.1f}%", ha="center", va="bottom", fontweight="bold", color="#1D3557")

# 子图6：重点区街道本科占比热力图（新增，直观展示分布）
ax6 = axes[2, 1]
# 按所属区分组，整理成透视表（便于热力图展示）
street_pivot = street_data.pivot_table(index="街道", columns="所属区", values="本科占比(%)")
# 热力图（优化配色，突出高低差异）
sns.heatmap(street_pivot, ax=ax6, cmap="RdYlBu_r", annot=True, fmt=".1f", cbar_kws={"label":"本科占比(%)"},
            linewidths=0.5, linecolor="white")
ax6.set_title("重点区各街道本科占比热力图", fontsize=14, fontweight="bold")
ax6.set_xlabel("所属区", fontsize=12)
ax6.set_ylabel("街道", fontsize=12)
# 旋转x轴标签，避免遮挡
ax6.tick_params(axis="x", rotation=45)

# 核心优化4：调整布局，避免拥挤（优化子图间距）
plt.tight_layout(rect=[0, 0.02, 1, 0.96])  # 预留标题空间
# 保存图片（优化分辨率，支持高清导出）
plt.savefig("深圳人口学历可视化_优化版.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()

# -------------------------- 核心优化5：新增代码注释与复用提示
print("可视化图表已保存为：深圳人口学历可视化_优化版.png")
print("代码可直接复用，如需调整：")
print("1. 如需修改图表尺寸，调整figsize参数（当前22,18）")
print("2. 如需修改配色，替换color/palette参数")
print("3. 如需筛选不同占比的街道，修改high_edu_streets中的筛选条件")