import os
import xml.etree.ElementTree as ET
if not hasattr(ET.ElementTree, 'getiterator'):
    ET.ElementTree.getiterator = lambda self, tag=None: self.iter(tag)

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

FILES = {
    "C_xls": "/Users/temu/Downloads/产品库存(2).xls",
    "A_xlsx": "/Users/temu/Downloads/2026-09-01_bizWarehouseProductInventoryExport6409.xlsx",
    "B_xlsx": "/Users/temu/Downloads/ProductInventory-1788234957397-556059.xlsx",
    "master": "/Users/temu/Downloads/导出产品-按SKU-953261488470130688.xlsx",
}

def norm(s):
    return "".join(ch for ch in str(s).lower() if ch.isalnum())

def num(x):
    try:
        if x is None or (isinstance(x, float) and pd.isna(x)):
            return 0
        s = str(x).strip().replace(",", "")
        return int(float(s)) if s not in ("", "nan", "None") else 0
    except Exception:
        return 0

# ---------- parse warehouse C (.xls) ----------
def parse_whC():
    df = pd.read_excel(FILES["C_xls"], header=2, dtype=str)
    rows = []
    for _, r in df.iterrows():
        sku = str(r.get("产品sku", "")).strip()
        if not sku or not sku.upper().startswith("C3950-"):
            continue
        rows.append({
            "sku": sku,
            "warehouse": str(r.get("仓库", "")).strip(),
            "cust": str(r.get("客户", "")).strip(),
            "pname": str(r.get("产品名称", "")).strip(),
            "在途": num(r.get("在途")),
            "待上架": num(r.get("待上架")),
            "可售": num(r.get("可售")),
            "待出库": num(r.get("待出库")),
            "已出库": num(r.get("已出库")),
            "不良品": num(r.get("不良品")),
        })
    return rows

# ---------- parse warehouse B (fix header detection) ----------
def parse_whB():
    df = pd.read_excel(FILES["B_xlsx"], dtype=str)
    hm = {norm(c): c for c in df.columns}
    def gid(target):
        t = norm(target)
        if t in hm: return hm[t]
        for k, v in hm.items():
            if t in k or k in t: return v
        return None
    sku_c = gid("产品sku") or gid("sku")
    on_c = gid("在途")
    sell_c = gid("可售")
    wh_c = gid("仓库")
    name_c = gid("产品名称")
    rows = []
    for _, r in df.iterrows():
        sku = str(r.get(sku_c, "")).strip() if sku_c else ""
        if not sku or not sku.upper().startswith("C3950-"):
            continue
        rows.append({
            "sku": sku,
            "warehouse": str(r.get(wh_c, "")).strip() if wh_c else "",
            "cust": "C3950",
            "pname": str(r.get(name_c, "")).strip() if name_c else "",
            "在途": num(r.get(on_c)),
            "待上架": num(r.get(gid("待上架"))),
            "可售": num(r.get(sell_c)),
            "待出库": num(r.get(gid("待出库"))),
            "已出库": num(r.get(gid("已出库"))),
            "不良品": num(r.get(gid("不良品"))),
        })
    return rows, (sku_c, on_c, sell_c)

# ---------- parse warehouse A ----------
def parse_whA():
    df = pd.read_excel(FILES["A_xlsx"], dtype=str)
    hm = {norm(c): c for c in df.columns}
    def gid(target):
        t = norm(target)
        if t in hm: return hm[t]
        for k, v in hm.items():
            if t in k or k in t: return v
        return None
    sku_c = gid("产品条码") or gid("sku")
    rows = []
    for _, r in df.iterrows():
        sku = str(r.get(sku_c, "")).strip() if sku_c else ""
        if not sku or not sku.upper().startswith("C3950-"):
            continue
        rows.append({
            "sku": sku,
            "warehouse": str(r.get(gid("仓库"), "")).strip(),
            "cust": "C3950",
            "pname": str(r.get(gid("产品标题")), ""),
            "在途": num(r.get(gid("在途"))),
            "待上架": num(r.get(gid("待上架"))),
            "可售": num(r.get(gid("可售"))),
            "待出库": num(r.get(gid("待出库"))),
            "已出库": num(r.get(gid("已出库"))),
            "不良品": num(r.get(gid("不良品"))),
        })
    return rows

# ---------- product master lookup ----------
def load_master():
    df = pd.read_excel(FILES["master"], sheet_name="产品", dtype=str)
    sku_c = "*SKU" if "*SKU" in df.columns else df.columns[0]
    spu_c = "SPU" if "SPU" in df.columns else None
    name_c = "品名" if "品名" in df.columns else None
    exact = {}
    spu_index = []  # (stripped_spu, spu, name)
    for _, r in df.iterrows():
        sk = str(r.get(sku_c, "")).strip()
        sp = str(r.get(spu_c, "")).strip() if spu_c else ""
        nm = str(r.get(name_c, "")).strip() if name_c else ""
        if sk:
            exact[norm(sk)] = (sk, sp, nm)
        if sp:
            spu_index.append((norm(sp), sp, nm))
    return exact, spu_index

# ---------- build ----------
rowsC = parse_whC()
rowsB, bcols = parse_whB()
rowsA = parse_whA()
exact, spu_index = load_master()

print("Warehouse C C3950 rows:", len(rowsC))
print("Warehouse B C3950 rows:", len(rowsB), "cols:", bcols)
print("Warehouse A C3950 rows:", len(rowsA))

allrows = rowsC + rowsB + rowsA
print("TOTAL C3950 inventory rows:", len(allrows))

# cross-reference
def xref(sku):
    n = norm(sku)
    if n in exact:
        return exact[n]
    # substring match on any master SPU stripped
    best = None
    for sspu, spu, nm in spu_index:
        if sspu and sspu in n:
            best = (sku, spu, nm)  # prefer master spu/name
            break
    if best:
        return best
    return (sku, "", "")

for r in allrows:
    sk, sp, nm = xref(r["sku"])
    r["m_sku"] = sk
    r["spu"] = sp
    r["m_name"] = nm

# ---------- write workbook ----------
wb = Workbook()
ws = wb.active
ws.title = "C3950库存汇总"

headers = ["SKU", "SPU(产品表)", "品名(产品表)", "仓库", "产品名称(仓库)",
           "在途", "可售", "待上架", "待出库", "已出库", "不良品"]
ws.append(headers)

# sort by SKU
allrows.sort(key=lambda r: r["sku"])
for r in allrows:
    ws.append([
        r["sku"], r["spu"], r["m_name"], r["warehouse"], r["pname"],
        r["在途"], r["可售"], r["待上架"], r["待出库"], r["已出库"], r["不良品"]
    ])

# totals
tot = {k: sum(r[k] for r in allrows) for k in ["在途","可售","待上架","待出库","已出库","不良品"]}
ws.append(["合计", "", f"{len(allrows)}个SKU", "", "",
           tot["在途"], tot["可售"], tot["待上架"], tot["待出库"], tot["已出库"], tot["不良品"]])

# style
hdr_fill = PatternFill("solid", fgColor="4472C4")
hdr_font = Font(bold=True, color="FFFFFF", name="微软雅黑", size=10)
tot_fill = PatternFill("solid", fgColor="D9E1F2")
thin = Side(style="thin", color="BFBFBF")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
center = Alignment(horizontal="center", vertical="center")
left = Alignment(horizontal="left", vertical="center")

for c in range(1, len(headers)+1):
    cell = ws.cell(row=1, column=c)
    cell.fill = hdr_fill; cell.font = hdr_font; cell.alignment = center; cell.border = border
last = ws.max_row
for c in range(1, len(headers)+1):
    cell = ws.cell(row=last, column=c)
    cell.fill = tot_fill; cell.font = Font(bold=True, name="微软雅黑"); cell.border = border
    cell.alignment = center if c >= 6 else left

# number format for qty cols
for rr in range(2, ws.max_row+1):
    for c in range(6, len(headers)+1):
        ws.cell(row=rr, column=c).number_format = "#,##0"
        ws.cell(row=rr, column=c).alignment = center
    for c in (1,2,3,5):
        ws.cell(row=rr, column=c).alignment = left

widths = [30, 16, 22, 22, 18, 8, 8, 9, 9, 9, 9]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.freeze_panes = "A2"

# ---------- note sheet ----------
ws2 = wb.create_sheet("说明")
notes = [
    "C3950 库存筛选说明",
    "",
    f"1. 数据来源：3个仓库明细表。C3950 系列 SKU 全部来自【仓库C / TX 1 美中休斯顿大牛仓】（客户代码 C3950）。",
    f"2. 仓库A（5775仓）与仓库B（WPLA仓）均未发现 C3950- 前缀 SKU。",
    f"3. 共筛出 C3950- 库存 SKU {len(allrows)} 个。",
    f"4. 在途合计 {tot['在途']:,} ，可售合计 {tot['可售']:,} ，待上架 {tot['待上架']:,} ，不良品 {tot['不良品']:,}。",
    "5. 产品表(导出产品-按SKU)中无 C3950- 开头的精确 SKU，故 SPU/品名 通过「SKU 中的 SPU 片段」匹配产品表 SPU 得到；",
    "   未匹配到产品表的行，SPU/品名 留空（可对照仓库自带的产品名称）。",
    "6. 数量口径：在途=在途(采购/调拨未入库)；可售=可售/在库可销售；其余为辅助列。",
]
for i, t in enumerate(notes, 1):
    ws2.cell(row=i, column=1, value=t)
ws2.column_dimensions["A"].width = 100

out = "/Users/temu/WorkBuddy/2026-08-31-20-57-42/C3950库存汇总.xlsx"
wb.save(out)
print("SAVED:", out)
print("在途合计:", tot["在途"], "可售合计:", tot["可售"])
# matched count
matched = sum(1 for r in allrows if r["spu"])
print("matched SPU:", matched, "/", len(allrows))
