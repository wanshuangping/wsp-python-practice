import pandas as pd
import os
import glob

# ========== 配置区 ==========
# 订单文件所在的文件夹路径（改成你自己的）
folder_path = "/Users/temu/Downloads/订单导出2026730001.xlsx"

# 输出合并后的文件名
output_file = "/Users/temu/Downloads/全部订单合并.xlsx"
# ============================

# 1. 找到文件夹下所有 .xlsx 文件
xlsx_files = glob.glob(os.path.join(folder_path, "*.xlsx"))

if not xlsx_files:
    print("❌ 文件夹里没有找到xlsx文件，请检查路径！")
else:
    print(f"✅ 找到 {len(xlsx_files)} 个订单文件：")
    for f in xlsx_files:
        print(f"  - {os.path.basename(f)}")

    # 2. 逐个读取并合并
    all_data = []
    success_count = 0
    fail_files = []

    for file in xlsx_files:
        try:
            df = pd.read_excel(file, engine="openpyxl")
            # 额外加一列，标记数据来自哪个文件
            df["来源文件"] = os.path.basename(file)
            all_data.append(df)
            success_count += 1
            print(f"  ✅ 读取成功：{os.path.basename(file)}（{len(df)}行）")
        except Exception as e:
            fail_files.append((os.path.basename(file), str(e)))
            print(f"  ❌ 读取失败：{os.path.basename(file)} - {e}")

    # 3. 合并所有数据
    if all_data:
        merged_df = pd.concat(all_data, ignore_index=True)
        print(f"\n🎉 合并完成！共 {success_count} 个文件，总计 {len(merged_df)} 行订单，{len(merged_df.columns)} 个字段")

        # 4. 保存为新的Excel
        merged_df.to_excel(output_file, index=False, engine="openpyxl")
        print(f"💾 已保存到：{output_file}")

        # 5. 快速预览
        print("\n前5行预览：")
        print(merged_df.head())

    if fail_files:
        print(f"\n⚠️ 有 {len(fail_files)} 个文件读取失败：")
        for name, err in fail_files:
            print(f"  - {name}: {err}")