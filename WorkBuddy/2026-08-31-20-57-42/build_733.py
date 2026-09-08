import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

F26 = "/Users/temu/Downloads/销量统计2026-07-01~2026-08-31-953257282679787520.xlsx"
F25 = "/Users/temu/Downloads/销量统计2025-07-01~2025-08-31-953303947144736768.xlsx"
CODES = ["销量", "订单量", "销售额"]
MONEY = {"销量": False, "订单量": False, "销售额": True}

def to_int(x):
    try:
        s = str(x).replace(",", "").replace("￥", "").strip()
        return int(float(s)) if s not in ("", "nan", "None") else 0
    except Exception:
        return 0

def to_num(x, money):
    if money:
        try:
            s = str(x).replace(",", "").replace("￥", "").strip()
            return float(s) if s not in ("", "nan", "None") else 0.0
        except Exception:
            return 0.0
    return float(to_int(x))

def read_file(f, prefix):
    res = {}; spu_name = {}
    for code in CODES:
        df = pd.read_excel(f, sheet_name=code, dtype=str)
        m = MONEY[code]
        col08 = f"{prefix}-08"; col07 = f"{prefix}-07"
        d = {}
        for _, r in df.iterrows():
            spu = str(r.get("SPU", "")).strip()
            if not spu:
                continue
            d[spu] = {"08": to_num(r.get(col08), m), "07": to_num(r.get(col07), m)}
            if "款名" in df.columns:
                nm = str(r.get("款名", "")).strip()
                if nm:
                    spu_name[spu] = nm
        res[code] = d
    return res, spu_name

d26, name26 = read_file(F26, "2026")
d25, _ = read_file(F25, "2025")
all_sp = sorted(set(d26["销量"]) | set(d25["销量"]))

def yoy(cur, prev):
    if prev is None or prev == 0:
        return None
    return (cur - prev) / prev

details = {}
for code in CODES:
    rows = []
    for spu in all_sp:
        c = d26[code].get(spu); p = d25[code].get(spu)
        c8 = c["08"] if c else 0; p8 = p["08"] if p else 0
        c7 = c["07"] if c else 0; p7 = p["07"] if p else 0
        if c and p:
            status = "存续"
        elif c and not p:
            status = "新品"
        else:
            status = "退市"
        rows.append({"spu": spu, "name": name26.get(spu, ""), "status": status,
                     "c8": c8, "p8": p8, "y8": yoy(c8, p8),
                     "c7": c7, "p7": p7, "y7": yoy(c7, p7)})
    rows.sort(key=lambda r: -r["c8"])
    details[code] = rows

tot = {}
for code in CODES:
    rows = details[code]
    tc8 = sum(r["c8"] for r in rows); tp8 = sum(r["p8"] for r in rows)
    tc7 = sum(r["c7"] for r in rows); tp7 = sum(r["p7"] for r in rows)
    tot[code] = {"c8": tc8, "p8": tp8, "y8": yoy(tc8, tp8),
                 "c7": tc7, "p7": tp7, "y7": yoy(tc7, tp7)}

# ---------- styles ----------
BLUE="4472C4"; WHITE="FFFFFF"; RED="C00000"; GREEN="1F8B2A"
hdr_fill = PatternFill("solid", fgColor=BLUE)
hdr_font = Font(bold=True, color=WHITE, name="微软雅黑", size=10)
tot_fill = PatternFill("solid", fgColor="D9E1F2")
thin = Side(style="thin", color="BFBFBF")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
center = Alignment(horizontal="center", vertical="center")
left = Alignment(horizontal="left", vertical="center")

def pct_cell(ws, row, col, y):
    cell = ws.cell(row=row, column=col)
    if y is None:
        cell.value = "—"; cell.font = Font(name="微软雅黑", color="808080")
    else:
        cell.value = y; cell.number_format = "0.0%;[红色]-0.0%"
        cell.font = Font(name="微软雅黑", color=RED if y >= 0 else GREEN)
    cell.alignment = center

def write_yoy_sheet(ws, code):
    m = MONEY[code]; nf = "￥#,##0.00" if m else "#,##0"
    headers = ["SPU", "款名(2026)", "状态",
               "2026-08", "2025-08", "8月同比",
               "2026-07", "2025-07", "7月同比"]
    ws.append(headers)
    for r in details[code]:
        ws.append([r["spu"], r["name"], r["status"],
                   r["c8"], r["p8"], None, r["c7"], r["p7"], None])
    t = tot[code]
    ws.append(["合计", "", f"{len(details[code])}个SPU",
               t["c8"], t["p8"], None, t["c7"], t["p7"], None])
    for c in range(1, len(headers)+1):
        cell = ws.cell(row=1, column=c)
        cell.fill = hdr_fill; cell.font = hdr_font; cell.alignment = center; cell.border = border
    last = ws.max_row
    for rr in range(2, last+1):
        idx = rr - 2
        for c in range(1, len(headers)+1):
            cell = ws.cell(row=rr, column=c); cell.border = border
            cell.alignment = left if c in (1, 2) else center
            if c in (4, 5, 7, 8):
                cell.number_format = nf
        if rr == last:
            for c in range(1, len(headers)+1):
                ws.cell(row=rr, column=c).fill = tot_fill
                ws.cell(row=rr, column=c).font = Font(bold=True, name="微软雅黑")
        if rr == last:
            pct_cell(ws, rr, 6, t["y8"]); pct_cell(ws, rr, 9, t["y7"])
        else:
            pct_cell(ws, rr, 6, details[code][idx]["y8"])
            pct_cell(ws, rr, 9, details[code][idx]["y7"])
    widths = [14, 24, 8, 12, 12, 10, 12, 12, 10]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"

# 总览
wb = Workbook()
ws0 = wb.active; ws0.title = "总览"
headers0 = ["指标", "2026-08", "2025-08", "8月同比", "2026-07", "2025-07", "7月同比"]
ws0.append(headers0)
for code in CODES:
    t = tot[code]; m = MONEY[code]; nf = "￥#,##0.00" if m else "#,##0"
    ws0.append([code, t["c8"], t["p8"], None, t["c7"], t["p7"], None])
for c in range(1, len(headers0)+1):
    cell = ws0.cell(row=1, column=c)
    cell.fill = hdr_fill; cell.font = hdr_font; cell.alignment = center; cell.border = border
for rr in range(2, ws0.max_row+1):
    code = CODES[rr-2]; m = MONEY[code]; nf = "￥#,##0.00" if m else "#,##0"
    for c in range(1, len(headers0)+1):
        cell = ws0.cell(row=rr, column=c); cell.border = border
        cell.alignment = left if c == 1 else center
        if c in (2, 3, 5, 6):
            cell.number_format = nf
    pct_cell(ws0, rr, 4, tot[code]["y8"]); pct_cell(ws0, rr, 7, tot[code]["y7"])
widths0 = [10, 13, 13, 10, 13, 13, 10]
for i, w in enumerate(widths0, 1):
    ws0.column_dimensions[get_column_letter(i)].width = w

for code in CODES:
    ws = wb.create_sheet(f"{code}同比(按SPU)")
    write_yoy_sheet(ws, code)

# raw 2026 / 2025 (months only)
def write_raw(f, prefix, sheetname):
    ws = wb.create_sheet(sheetname)
    hdr = ["SPU", "款名", "销量-08", "销量-07", "订单量-08", "订单量-07", "销售额-08", "销售额-07"]
    ws.append(hdr)
    for spu in all_sp:
        row = [spu, name26.get(spu, "")]
        for code in CODES:
            d = (d26 if prefix == "2026" else d25)[code].get(spu, {})
            row += [d.get("08", 0), d.get("07", 0)]
        ws.append(row)
    for c in range(1, len(hdr)+1):
        cell = ws.cell(row=1, column=c)
        cell.fill = hdr_fill; cell.font = hdr_font; cell.alignment = center; cell.border = border
    for rr in range(2, ws.max_row+1):
        for c in range(1, len(hdr)+1):
            cell = ws.cell(row=rr, column=c); cell.border = border
            cell.alignment = left if c in (1, 2) else center
            if c in (3, 4, 5, 6):
                cell.number_format = "#,##0"
            else:
                cell.number_format = "￥#,##0.00"
    widths = [14, 22, 10, 10, 11, 11, 13, 13]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"

write_raw(F26, "2026", "2026明细(8月+7月)")
write_raw(F25, "2025", "2025明细(8月+7月)")

# 说明
wsx = wb.create_sheet("说明")
n_cont = sum(1 for r in details["销量"] if r["status"] == "存续")
n_new = sum(1 for r in details["销量"] if r["status"] == "新品")
n_out = sum(1 for r in details["销量"] if r["status"] == "退市")
notes = [
    "733 同比报表说明（仅 8月 / 7月 单月对比，无 7-8 累计）",
    "",
    "1. 数据源：销量统计2026-07-01~2026-08-31、销量统计2025-07-01~2025-08-31。",
    "2. 口径：仅做单月同比 —— 8月(2026-08 vs 2025-08) 与 7月(2026-07 vs 2025-07)，不含 7-8 累计。",
    f"3. 指标：销量 / 订单量 / 销售额。对比维度 = SPU（款）。共 {len(all_sp)} 个 SPU：存续 {n_cont} / 新品 {n_new} / 退市 {n_out}（按销量判定）。",
    "4. 同比%：红=同比增长(涨)、绿=同比下降(跌)；「—」表示去年同期为0(新品或退市)。",
    f"5. 总览 8月：销量 {tot['销量']['c8']:,.0f} vs {tot['销量']['p8']:,.0f}（{tot['销量']['y8']*100:+.1f}%）；",
    f"   订单量 {tot['订单量']['c8']:,.0f} vs {tot['订单量']['p8']:,.0f}（{tot['订单量']['y8']*100:+.1f}%）；",
    f"   销售额 ￥{tot['销售额']['c8']:,.0f} vs ￥{tot['销售额']['p8']:,.0f}（{tot['销售额']['y8']*100:+.1f}%）。",
    f"6. 总览 7月：销量 {tot['销量']['c7']:,.0f} vs {tot['销量']['p7']:,.0f}（{tot['销量']['y7']*100:+.1f}%）；",
    f"   订单量 {tot['订单量']['c7']:,.0f} vs {tot['订单量']['p7']:,.0f}（{tot['订单量']['y7']*100:+.1f}%）；",
    f"   销售额 ￥{tot['销售额']['c7']:,.0f} vs ￥{tot['销售额']['p7']:,.0f}（{tot['销售额']['y7']*100:+.1f}%）。",
    "7. 2025文件无「款名」列，款名取自2026文件；仅2025出现的SPU款名留空。",
]
for i, t in enumerate(notes, 1):
    wsx.cell(row=i, column=1, value=t)
wsx.column_dimensions["A"].width = 115

out = "/Users/temu/WorkBuddy/2026-08-31-20-57-42/733数据报表.xlsx"
wb.save(out)
print("SAVED:", out)
print("SPU:", len(all_sp), "存续", n_cont, "新品", n_new, "退市", n_out)
for code in CODES:
    t = tot[code]
    print(f"{code}: 8月 {t['c8']} vs {t['p8']} ({t['y8']*100:+.1f}%) | 7月 {t['c7']} vs {t['p7']} ({t['y7']*100:+.1f}%)")
