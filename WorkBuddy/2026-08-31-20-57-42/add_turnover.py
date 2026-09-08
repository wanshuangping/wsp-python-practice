import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

F = "/Users/temu/WorkBuddy/2026-08-31-20-57-42/在途可售SPU汇总.xlsx"
df = pd.read_excel(F, sheet_name="SPU汇总", dtype=str)
df["可售"] = pd.to_numeric(df["可售合计"], errors="coerce").fillna(0).astype(int)
df["销量8"] = pd.to_numeric(df["2026-08销量"], errors="coerce").fillna(0).astype(int)

def cover(r):
    if r["销量8"] > 0:
        return round(r["可售"] / r["销量8"], 1)
    return 999.0

df["周转月数"] = df.apply(cover, axis=1)

def tier(c):
    if c >= 999: return "死库(0动销)"
    if c >= 12:  return "严重滞销(>1年)"
    if c >= 6:   return "滞销(半年~1年)"
    if c >= 3:   return "偏慢(3~6月)"
    return "正常(<3月)"

df["动销分级"] = df["周转月数"].apply(tier)

# reorder: original cols + 周转月数 + 动销分级
base_cols = list(df.columns)
base_cols = [c for c in base_cols if c not in ("可售","销量8","周转月数","动销分级")]
new_order = base_cols + ["周转月数", "动销分级"]
df = df[new_order]

# tier color
tier_color = {
    "死库(0动销)": "C00000",
    "严重滞销(>1年)": "E06C00",
    "滞销(半年~1年)": "BF8F00",
    "偏慢(3~6月)": "548235",
    "正常(<3月)": "1F8B2A",
}

BLUE="4472C4"; WHITE="FFFFFF"
hdr_fill=PatternFill("solid",fgColor=BLUE); hdr_font=Font(bold=True,color=WHITE,name="微软雅黑",size=10)
thin=Side(style="thin",color="BFBFBF"); border=Border(left=thin,right=thin,top=thin,bottom=thin)
center=Alignment(horizontal="center",vertical="center"); left=Alignment(horizontal="left",vertical="center")

wb=Workbook(); ws=wb.active; ws.title="SPU汇总"
ws.append(list(df.columns))
for _,r in df.iterrows():
    row=[]
    for c in df.columns:
        if c=="周转月数":
            row.append("死库" if r[c]>=999 else r[c])
        else:
            row.append(r[c])
    ws.append(row)

headers=list(df.columns)
for c in range(1,len(headers)+1):
    cell=ws.cell(row=1,column=c); cell.fill=hdr_fill; cell.font=hdr_font; cell.alignment=center; cell.border=border
for rr in range(2,ws.max_row+1):
    for c in range(1,len(headers)+1):
        cell=ws.cell(row=rr,column=c); cell.border=border
        cell.alignment=left if c in (1,2) else center
        if c in (4,5,6,7,8,9,10,11,12,13):
            cell.number_format="#,##0"
        if c==14: cell.number_format="￥#,##0.00"
    # 动销分级 color (last col)
    tc=ws.cell(row=rr,column=len(headers))
    tval=tc.value
    if tval in tier_color:
        tc.font=Font(name="微软雅黑",bold=True,color=tier_color[tval])
widths=[15,28,8,13,13,13,13,15,15,10,10,12,12,14,11,16]
for i,w in enumerate(widths,1):
    ws.column_dimensions[get_column_letter(i)].width=w
ws.freeze_panes="A2"

# 说明
ws2=wb.create_sheet("说明")
tiers=df.groupby("动销分级").agg(SPU数=("SPU(产品表)","count"),可售件数=("可售合计","sum"))
lines=["在途/可售 + 2026-08 销量 + 周转月数/动销分级（SPU 汇总）","",
       f"周转月数 = 可售合计 ÷ 2026-08 销量（按8月卖速估算清仓月数；0动销记死库）。",
       f"可售合计 12,737 件 / 在途合计 9,707 件 / 8月销量 1,425 件。",""]
for t in ["死库(0动销)","严重滞销(>1年)","滞销(半年~1年)","偏慢(3~6月)","正常(<3月)"]:
    if t in tiers.index:
        lines.append(f"  {t}：{int(tiers.loc[t,'SPU数'])}个SPU / {int(tiers.loc[t,'可售件数']):,}件")
lines.append("")
lines.append("重点：3,126件睡袍(TERR1624/TERR1988/TERR1916等)多属死库/严重滞销，8月仅售约14件，应优先清仓而非当健康库存。")
lines.append("在途9,707件建议先拦停采购单，避免库存进一步恶化。")
for i,t in enumerate(lines,1):
    ws2.cell(row=i,column=1,value=t)
ws2.column_dimensions["A"].width=120

wb.save(F)
print("SAVED:",F)
print(tiers.to_string())
dead=int(df[df['动销分级']=='死库(0动销)']['可售合计'].sum())
sev=int(df[df['动销分级']=='严重滞销(>1年)']['可售合计'].sum())
print(f"\n硬死库(0动销)={dead}件 + 严重滞销(>1年)={sev}件 = 真实死重 {dead+sev}件")
