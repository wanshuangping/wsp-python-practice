from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BLUE="4472C4"; WHITE="FFFFFF"; RED="C00000"; GREEN="1F8B2A"; GREY="808080"
hdr_fill=PatternFill("solid",fgColor=BLUE)
hdr_font=Font(bold=True,color=WHITE,name="微软雅黑",size=10)
title_font=Font(bold=True,size=14,name="微软雅黑",color="1F3864")
sec_font=Font(bold=True,size=11,name="微软雅黑",color="1F3864")
thin=Side(style="thin",color="BFBFBF")
border=Border(left=thin,right=thin,top=thin,bottom=thin)
center=Alignment(horizontal="center",vertical="center",wrap_text=True)
left=Alignment(horizontal="left",vertical="center",wrap_text=True)
wb=Workbook()

def style_header(ws,row,ncol):
    for c in range(1,ncol+1):
        cell=ws.cell(row=row,column=c); cell.fill=hdr_fill; cell.font=hdr_font; cell.alignment=center; cell.border=border

def box(ws,r1,r2,c1,c2):
    for r in range(r1,r2+1):
        for c in range(c1,c2+1):
            ws.cell(row=r,column=c).border=border

# ============ Sheet1 8月核心总结 ============
ws=wb.active; ws.title="8月核心总结"
ws["A1"]="733 运营汇报 · 2026年8月总结"; ws["A1"].font=title_font
ws["A2"]="数据口径：上月=2026.08，去年同期=2025.08；店铺汇总（所有SKU）"; ws["A2"].font=Font(italic=True,size=9,color=GREY,name="微软雅黑")
hdr_row=4
heads=["指标","8月","去年同期","环比/同比","说明"]
for i,h in enumerate(heads,1): ws.cell(row=hdr_row,column=i,value=h)
style_header(ws,hdr_row,5)
rows=[
 ("可售库存(件)",12725,9687,"+33.2%","在库可售较去年增多，周转压力上升"),
 ("在途库存(件)",9687,"—","—","待入仓，需评估是否拦截"),
 ("销量(件)",1777,2068,"-14.07%","同比下滑，需提动销"),
 ("8月毛利润(¥)",24706.7,26260.7,"-5.93%","毛利额略降"),
 ("毛利率",0.1985,0.1268,"+7.17pct","毛利率提升(结构/折扣优化)，但量跌"),
 ("罚款退款(¥)",5686,5263,"+8.04%","退款偏高，关注质量/尺码"),
 ("活动费(¥)",2460,3364,"-26.87%","活动投入收紧"),
 ("销售额/申报价活动价(¥)",124440.38,207167.97,"-39.93%","GMV 同比近乎腰斩"),
 ("广告费(¥)",22624.3,33824.3,"-33.11%","广告收缩"),
]
r=hdr_row+1
for name,a,b,ch,note in rows:
    ws.cell(row=r,column=1,value=name).alignment=left
    ca=ws.cell(row=r,column=2,value=a); ca.alignment=center
    cb=ws.cell(row=r,column=3,value=b); cb.alignment=center
    cc=ws.cell(row=r,column=4,value=ch); cc.alignment=center
    cn=ws.cell(row=r,column=5,value=note); cn.alignment=left
    if name=="毛利率":
        ca.number_format="0.00%"; cb.number_format="0.00%"
    elif "¥" in name or "销售额" in name:
        ca.number_format="#,##0.00"; cb.number_format="#,##0.00"
    else:
        ca.number_format="#,##0"; cb.number_format="#,##0"
    r+=1
box(ws,hdr_row,r-1,1,5)
# key findings
ws.cell(row=r+1,column=1,value="核心结论").font=sec_font
finds=[
 "1. GMV 同比 -39.9%、销量 -14.1%：量价齐跌，8月明显走弱。",
 "2. 毛利率反而 +7.17pct（19.85% vs 12.68%）：靠砍低毛利款/折扣优化，但抵不过量的下滑。",
 "3. 库存亮红灯：可售 1.27万 + 在途 9,687，按 8月卖速约 14 个月才能清完。",
 "4. 退款 5,686 偏高（占销售额 4.6%），睡袍/内裤类需排查尺码与质量。",
 "5. 广告/活动费同比各砍约 1/3，流量获取同步收缩，需重新评估投放效率。",
]
for i,t in enumerate(finds):
    ws.cell(row=r+2+i,column=1,value=t).alignment=left
    ws.merge_cells(start_row=r+2+i,start_column=1,end_row=r+2+i,end_column=5)
widths=[22,14,14,12,46]
for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w
ws.freeze_panes="A5"

# ============ Sheet2 库存预警与清仓优先级 ============
ws2=wb.create_sheet("库存预警与清仓")
ws2["A1"]="库存预警 · 清仓优先级（基于 SPU 在途/可售汇总 + 8月动销）"; ws2["A1"].font=title_font
ws2["A2"]="周转月数 = 可售合计 ÷ 2026-08 销量；0动销记死库。可售合计 12,737 / 在途 9,707。"; ws2["A2"].font=Font(italic=True,size=9,color=GREY,name="微软雅黑")
h2=["动销分级","SPU数","可售件数","处理建议"]
for i,h in enumerate(h2,1): ws2.cell(row=4,column=i,value=h)
style_header(ws2,4,4)
tiers=[
 ("🔴 死库(0动销)",19,3331,"立即清仓：降价/捆绑/退供应商/站外甩"),
 ("🔴 严重滞销(>1年)",9,3626,"优先清：睡袍主力(TERR1624/1988/1916)等，加大活动"),
 ("🟠 滞销(半年~1年)",9,2664,"随卖随清，停止补货"),
 ("🟡 偏慢(3~6月)",4,2171,"降权，观察动销"),
 ("🟢 正常(<3月)",4,945,"保持健康，正常补货"),
]
r=5
for t,n,k,act in tiers:
    ws2.cell(row=r,column=1,value=t).alignment=left
    ws2.cell(row=r,column=2,value=n).alignment=center
    ws2.cell(row=r,column=3,value=k).alignment=center; ws2.cell(row=r,column=3).number_format="#,##0"
    ws2.cell(row=r,column=4,value=act).alignment=left
    r+=1
box(ws2,4,r-1,1,4)
# top red list
ws2.cell(row=r+1,column=1,value="TOP 红色清仓清单（压货最重 / 几乎不卖）").font=sec_font
h3=["SPU","品名","可售","8月销量","周转月数","建议"]
for i,h in enumerate(h3,1): ws2.cell(row=r+2,column=i,value=h)
style_header(ws2,r+2,6)
red=[
 ("TERR1624","女士睡袍 酒红色 4XL/5XL",831,3,"277","降价+捆绑，紧急清"),
 ("TERR1988-M","男士浴袍 黑色",339,156,"2.2","随卖，控制补货"),
 ("TERR1916","女士睡袍 酒红 2XL/3XL",486,36,"13.5","加大活动"),
 ("WAW6096","露趾压缩袜 6XL",483,46,"10.5","捆绑清"),
 ("TEA82341","压缩袜 4XL",453,6,"75.5","清仓价"),
 ("WAW7259","竹纤维点胶松口袜 4双黑 M",362,46,"7.9","随卖"),
 ("TERR1708","女士浴袍 紫色 XL",299,4,"74.8","清仓"),
 ("TE-RR1516","女士浴袍 紫 2XL/3XL",263,1,"263","清仓"),
 ("WAS3380","女士睡袍(在途630)",0,0,"—","在途拦截，勿入仓"),
]
rr=r+3
for spu,name,k,s,cov,act in red:
    ws2.cell(row=rr,column=1,value=spu).alignment=left
    ws2.cell(row=rr,column=2,value=name).alignment=left
    ws2.cell(row=rr,column=3,value=k).alignment=center; ws2.cell(row=rr,column=3).number_format="#,##0"
    ws2.cell(row=rr,column=4,value=s).alignment=center
    ws2.cell(row=rr,column=5,value=cov).alignment=center
    ws2.cell(row=rr,column=6,value=act).alignment=left
    rr+=1
box(ws2,r+2,rr-1,1,6)
ws2.column_dimensions["A"].width=14; ws2.column_dimensions["B"].width=24
ws2.column_dimensions["C"].width=8; ws2.column_dimensions["D"].width=8
ws2.column_dimensions["E"].width=10; ws2.column_dimensions["F"].width=22

# ============ Sheet3 本月运营操作 ============
ws3=wb.create_sheet("本月运营操作")
ws3["A1"]="本月（9月）运营操作"; ws3["A1"].font=title_font
ops=[
 "1. 对热销款链接做重点维护（共6~7款），关注限流/库存/流量；标红 SPU 共12款安排重新作图、上架（库存冗余），预备销售产品维护好链接核价，开启销售模式。",
 "2. 跟踪本周即将入仓的跟踪号入库单，维护热销库存、加大活动销售；重点关注入仓新品链接动销情况（观察 WAW8549/8580/8649/WAN1049/1196/1213 共6款新品期）。",
 "3. 对新品期动销做调整：观察 WAW8681/8659/WAW7398 等3款新品，对活动和广告做优化。",
 "4. 找买手对接 WAN1049/1196/1213 共3款内裤链接（平台要求图片完全非人模展示，目前限流严重），同步沟通情况。",
 "5. 链接优化策略：竞品对标与差异化定价——通过竞品比价/核价，采用阶梯定价/限定价，打造差异化避免价格战内卷；模仿优秀竞品玩法。",
 "6. 持续推进欧区链接上新，关注在售链接动销。",
 "7. 提交第二批旺季睡袍备货单（注：当前睡袍压货 3,126 件、8月仅售约14件，建议先清现有库存再补，详见库存预警表）。",
]
for i,t in enumerate(ops):
    ws3.cell(row=3+i,column=1,value=t).alignment=left
    ws3.merge_cells(start_row=3+i,start_column=1,end_row=3+i,end_column=1)
    ws3.row_dimensions[3+i].height=42
ws3.column_dimensions["A"].width=110

# ============ Sheet4 本周运营计划 ============
ws4=wb.create_sheet("本周运营计划")
ws4["A1"]="本周运营计划"; ws4["A1"].font=title_font
wk=[
 "1. 维护热销款6~7款链接，标红12款重新作图上架。",
 "2. 跟踪在途入库单，维护热销库存、加大活动。",
 "3. 观察6款新品（WAW8549/8580/8649/WAN1049/1196/1213）动销，调整3款新品（WAW8681/8659/WAW7398）活动与广告。",
 "4. 对接买手处理3款内裤（WAN1049/1196/1213）非人模图片限流问题。",
 "5. 下架站内同款互比链接（本周已完成），落实差异化定价策略。",
 "6. 推进欧区上新与在售动销监控。",
 "7. 【新增】盘点红色清仓清单，启动睡袍/死库降价清仓；确认在途 9,687 件拦截方案。",
]
for i,t in enumerate(wk):
    ws4.cell(row=3+i,column=1,value=t).alignment=left
    ws4.merge_cells(start_row=3+i,start_column=1,end_row=3+i,end_column=1)
    ws4.row_dimensions[3+i].height=40
ws4.column_dimensions["A"].width=110

out="/Users/temu/WorkBuddy/2026-08-31-20-57-42/733汇报_8月总结与行动计划.xlsx"
wb.save(out)
print("SAVED:",out)
