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
ax1.set_title("各区总人口与本科占比对比", fontsize=1)