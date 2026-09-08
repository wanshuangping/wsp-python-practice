import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

SPU_FILE = "/Users/temu/WorkBuddy/2026-08-31-20-57-42/在途可售SPU汇总.xlsx"
SALES_FILE = "/Users/temu/WorkBuddy/2026-08-31-20-57-42/733数据报表.xlsx"
OUT = "/Users/temu/WorkBuddy/2026-08-31-20-57-42/在途可售SPU汇总.xlsx"

# ---------- read current SPU inventory table (first 11 cols only, keep user rows) ----------
df_spu = pd.read_excel(SPU_FILE, sheet_name="SPU汇总", dtype=str, usecols=range(0, 11))
# rename any polluted headers back to clean
colmap = {}
for c in df_spu.columns:
    s = str(c).strip()
    if "在途" in s and "合计" in s:
        colmap[c] = "在途合计"
    elif "可售" in s and "合计" in s:
        colmap[c] = "可售合计"
df_spu = df_spu.rename(columns=colmap)
print("SPU rows:", len(df_spu), "cols:", list(df_spu.columns))

# ---------- read 8月 sales from 733 report ----------
sales = {}
for metric, sheet in [("2026-08销量", "销量同比(按SPU)"),
                        ("2026-08订单量", "订单量同比(按SPU)"),
                        ("2026-08销售额", "销售额同比(按SPU)")]:
    df = pd.read_excel(SALES_FILE, sheet_name=sheet, dtype=str)
    df = df[df["SPU"] != "合计"]
    for _, r in df.iterrows():
        spu = str(r["SPU"]).strip()
        v = r["2026-08"]
        if metric == "2026-08销售额":
            try:
                sales.setdefault(spu, {})[metric] = float(str(v).replace(",", "").replace("￥", "").strip())
            except Exception:
                sales.setdefault(spu, {})[metric] = 0.0
        else:
            try:
                sales.setdefault(spu, {})[metric] = int(float(str(v).replace(",", "").strip()))
            except Exception:
                sales.setdefault(spu, {})[metric] = 0

# ---------- merge ----------
for metric in ["2026-08销量", "2026-08订单量", "2026-08销售额"]:
    df_spu[metric] = df_spu["SPU(产品表)"].map(lambda x: sales.get(str(x).strip(), {}).get(metric, 0))

# ---------- write ----------
wb = Workbook()
ws = wb.active
ws.title = "SPU汇总"
headers = ["SPU(产品表)", "品名(产品表)", "SKU数",
           "在途-仓库A(5775)", "可售-仓库A(5775)",
           "在途-仓库B(WPLA)", "可售-仓库B(WPLA)",
           "在途-仓库C(休斯顿)", "可售-仓库C(休斯顿)",
           "在途合计", "可售合计", "2026-08销量", "2026-08订单量", "2026-08销售额"]
ws.append(headers)
for _, r in df_spu.iterrows():
    ws.append([r[c] for c in headers])

# style
BLUE = "4472C4"; WHITE = "FFFFFF"
hdr_fill = PatternFill("solid", fgColor=BLUE)
hdr_font = Font(bold=True, color=WHITE, name="微软雅黑", size=10)
thin = Side(style="thin", color="BFBFBF")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
center = Alignment(horizontal="center", vertical="center")
left = Alignment(horizontal="left", vertical="center")

for c in range(1, len(headers)+1):
    cell = ws.cell(row=1, column=c)
    cell.fill = hdr_fill; cell.font = hdr_font; cell.alignment = center; cell.border = border
for rr in range(2, ws.max_row+1):
    for c in range(1, len(headers)+1):
        cell = ws.cell(row=rr, column=c)
        cell.border = border
        cell.alignment = left if c in (1, 2) else center
        if c in (4, 5, 6, 7, 8, 9, 10, 11, 12, 13):
            cell.number_format = "#,##0"
        if c == 14:
            cell.number_format = "￥#,##0.00"

widths = [15, 28, 8, 13, 13, 13, 13, 15, 15, 10, 10, 12, 12, 14]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.freeze_panes = "A2"

# 说明
ws2 = wb.create_sheet("说明")
matched = (df_spu["2026-08销量"] != 0).sum()
notes = [
    "在途/可售 + 2026-08 销售 SPU 汇总",
    "",
    f"1. 在途/可售 数据来自 3 仓库汇总（仓库A=5775 / 仓库B=WPLA / 仓库C=休斯顿）。",
    f"2. 共 {len(df_spu)} 个 SPU，保留原表中被筛选后的 45 行数据，未做增减。",
    f"3. 新增列：2026-08 销量 / 2026-08 订单量 / 2026-08 销售额，来自 733 数据报表(2026-08 vs 2025-08 的 8月数据)。",
    f"4. 其中 {matched} 个 SPU 在 2026-08 有销量记录；其余为 0（可能是库存备货款或当月无动销）。",
    "5. 仓库C 无可售列，故可售合计未含仓库C。",
]
for i, t in enumerate(notes, 1):
    ws2.cell(row=i, column=1, value=t)
ws2.column_dimensions["A"].width = 110

wb.save(OUT)
print("SAVED:", OUT)
print("matched SPU with 2026-08 sales:", matched)
