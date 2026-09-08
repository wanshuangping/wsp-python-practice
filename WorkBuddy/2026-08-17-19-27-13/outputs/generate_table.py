from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

wb = Workbook()
ws = wb.active
ws.title = "新科目表"

ws.merge_cells('A1:H1')
ws['A1'] = '专业名称：计算机科学与技术(080901)新科目表　|　主考院校：深圳大学　|　广东自考本科'
ws['A1'].font = Font(name='Microsoft YaHei', size=13, bold=True, color='2F75B5')
ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

# Headers
headers = ['类型序号', '课程代码', '课程名称', '学分', '类型', '考试方式', '免考条件/说明', '我的状态']
ws.append(headers)
header_fill = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')
for col in range(1, 9):
    cell = ws.cell(row=2, column=col)
    cell.font = Font(name='Microsoft YaHei', bold=True, size=11)
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal='center', vertical='center')

# 已通过/已免考的课程状态
status_map = {
    '15040': '已过 66分',
    '15043': '待考',
    '15044': '已过 77分',
    '00023': '待考',
    '02324': '待考',
    '13000': '免考(CET-4 428≥425)',
    '13003': '待考',
    '13004': '待考(实践)',
    '13013': '待考',
    '13014': '待考(实践)',
    '13015': '待考',
    '13180': '待考',
    '03344': '待考',
    '03345': '待考(实践)',
    '08074': '待考',
    '08075': '待考(实践)',
    '13005': '待考',
    '13006': '待考(实践)',
    '13009': '待考',
    '13011': '待考',
    '11689': '待考(论文)',
}

data = [
    ['001', '15040', '习近平新时代中国特色社会主义思想概论', 3, '必考', '笔试', '新课，多数前置学历未开设，一般不能免考；原专业修过同名课且合格者方可凭前置学历申请', '已过 66分'],
    ['002', '15043', '中国近现代史纲要', 3, '必考', '笔试', '本科及以上毕业生凭前置学历可免考（大专不可免，须报考）', '待考'],
    ['003', '15044', '马克思主义基本原理', 3, '必考', '笔试', '本科及以上毕业生凭前置学历可免考（大专不可免）', '已过 77分'],
    ['004', '00023', '高等数学(工本)', 10, '必考', '笔试', '前置学历修过同名/等效高数且合格(如理工、数学类专业)可凭前置学历免考', '待考'],
    ['005', '02324', '离散数学', 4, '必考', '笔试', '前置学历有同名且要求相当、成绩合格课程可凭前置学历申请(个案审核)', '待考'],
    ['006', '13000', '英语(专升本)', 7, '必考', '笔试', 'PETS-3及以上证书，或CET-4及以上证书(成绩≥425)可免考', '免考(CET-4 428≥425)'],
    ['007', '13003', '数据结构与算法', 4, '必考', '笔试', '前置学历有同名且要求相当、成绩合格课程可凭前置学历申请(个案审核)', '待考'],
    ['007', '13004', '数据结构与算法', 2, '必考', '实践', '同上，与实践一并凭前置学历申请；须先过13003笔试', '待考(实践)'],
    ['008', '13013', '高级语言程序设计', 4, '必考', '笔试', 'NCRE二级C语言程序设计(笔试+上机)合格证书可免考', '待考'],
    ['008', '13014', '高级语言程序设计', 2, '必考', '实践', '同上，与13013一并免考；须先过13013笔试', '待考(实践)'],
    ['009', '13015', '计算机系统原理', 4, '必考', '笔试', '前置学历有同名且要求相当、成绩合格课程可凭前置学历申请(个案审核)', '待考'],
    ['010', '13180', '操作系统', 4, '必考', '笔试', '前置学历有同名且要求相当、成绩合格课程可凭前置学历申请(个案审核)', '待考'],
    ['011', '03344', '信息与网络安全管理', 3, '必考', '笔试', '前置学历有同名且要求相当、成绩合格课程可凭前置学历申请(个案审核)', '待考'],
    ['011', '03345', '信息与网络安全管理', 2, '必考', '实践', '同上，与实践一并凭前置学历申请；须先过03344笔试', '待考(实践)'],
    ['012', '08074', '计算机高级程序设计', 3, '必考', '笔试', '前置学历有同名且要求相当、成绩合格课程可凭前置学历申请(个案审核)', '待考'],
    ['012', '08075', '计算机高级程序设计', 2, '必考', '实践', '同上，与实践一并凭前置学历申请；须先过08074笔试', '待考(实践)'],
    ['013', '13005', '软件工程', 3, '必考', '笔试', '前置学历有同名且要求相当、成绩合格课程可凭前置学历申请(个案审核)', '待考'],
    ['013', '13006', '软件工程', 2, '必考', '实践', '同上，与实践一并凭前置学历申请；须先过13005笔试', '待考(实践)'],
    ['014', '13009', '数据库原理与技术', 4, '必考', '笔试', '前置学历有同名且要求相当、成绩合格课程可凭前置学历申请(个案审核)', '待考'],
    ['015', '13011', '人工智能与大数据', 6, '必考', '笔试', '前置学历有同名且要求相当、成绩合格课程可凭前置学历申请(个案审核)', '待考'],
    ['016', '11689', '计算机科学与技术(本科)毕业论文', '不计学分', '必考', '实践', '必须完成，无免考', '待考(论文)'],
]

thin_border = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)

for row_data in data:
    ws.append(row_data)

green_fill = PatternFill(start_color='E2EFDA', end_color='E2EFDA', fill_type='solid')
passed_fill = PatternFill(start_color='FCE4D6', end_color='FCE4D6', fill_type='solid')

for r in range(3, ws.max_row + 1):
    code = ws.cell(row=r, column=2).value
    note = ws.cell(row=r, column=7).value
    status = ws.cell(row=r, column=8).value
    # 已通过/已免考 行：橙色
    if status and ('已过' in status or '免考' in status):
        for c in range(1, 9):
            ws.cell(row=r, column=c).fill = passed_fill
    # 证书/本科前置可免考 行：绿色（未被橙色覆盖时）
    elif note and ('PETS' in note or 'NCRE' in note or '本科及以上毕业生凭前置学历' in note):
        for c in range(1, 9):
            ws.cell(row=r, column=c).fill = green_fill

for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=8):
    for cell in row:
        cell.border = thin_border
        cell.font = Font(name='Microsoft YaHei', size=11)
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

summary_row = ws.max_row + 1
ws.merge_cells(start_row=summary_row, start_column=1, end_row=summary_row, end_column=8)
sc = ws.cell(row=summary_row, column=1)
sc.value = '课程与毕业学分：必考课16门，毕业总学分为75学分。橙底=已通过/已免考；绿底=凭证书或本科前置学历可免考。'
sc.font = Font(name='Microsoft YaHei', size=11)
sc.alignment = Alignment(horizontal='center', vertical='center')
sc.border = thin_border

note_row1 = ws.max_row + 1
ws.merge_cells(start_row=note_row1, start_column=1, end_row=note_row1, end_column=8)
nc1 = ws.cell(row=note_row1, column=1)
nc1.value = '说明：'
nc1.font = Font(name='Microsoft YaHei', size=11, bold=True)
nc1.alignment = Alignment(horizontal='left', vertical='center')

note_row2 = ws.max_row + 1
ws.merge_cells(start_row=note_row2, start_column=1, end_row=note_row2, end_column=8)
nc2 = ws.cell(row=note_row2, column=1)
nc2.value = '申请毕业时须持具有学历教育资格的高等学校、高等教育自学考试机构颁发的专科(或以上)学历证书。免考以广东省自学考试管理系统及主考院校最新公告为准。'
nc2.font = Font(name='Microsoft YaHei', size=11)
nc2.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)

widths = [12, 12, 30, 10, 10, 12, 46, 20]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[chr(64 + i)].width = w

ws.row_dimensions[1].height = 30
for row in range(2, ws.max_row + 1):
    ws.row_dimensions[row].height = 28

# ===== Sheet 2: 毕业与学位要求 =====
ws2 = wb.create_sheet('毕业与学位要求')
ws2.merge_cells('A1:B1')
ws2['A1'] = '深圳大学 自考本科（计算机科学与技术 080901）毕业与学位要求'
ws2['A1'].font = Font(name='Microsoft YaHei', size=13, bold=True, color='2F75B5')
ws2['A1'].alignment = Alignment(horizontal='center', vertical='center')

ws2['A3'] = '一、毕业要求（取得本科毕业证书）'
ws2['A3'].font = Font(name='Microsoft YaHei', size=12, bold=True, color='C00000')
grad = [
    '1. 必考课程全部合格：本计划必考课 16 门，毕业总学分 75 学分（毕业论文不计学分但必须通过）。',
    '2. 实践环节/毕业论文：11689 毕业论文（实践）须通过，且所属专业与主考学校（深圳大学）一致。',
    '3. 前置学历：申请本科毕业时须持专科（或以上）学历证书，并在"广东省自学考试管理系统"完成前置学历信息登记且查验通过。',
    '4. 思想品德鉴定合格（由所在单位或街道填写并加盖公章）。',
    '5. 无未解除的违纪违规记录；未办理过该专业毕业证书。',
    '6. 毕业申请时间：上半年约 6 月、下半年约 12 月（以省考办通知为准）；免考、转考须在申请前办理完成。',
]
r = 4
for line in grad:
    ws2.cell(row=r, column=1, value=line)
    ws2.cell(row=r, column=1).font = Font(name='Microsoft YaHei', size=11)
    ws2.cell(row=r, column=1).alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    r += 1

r += 1
ws2.cell(row=r, column=1, value='二、学士学位要求（依据 深大校发〔2024〕39号《深圳大学学位授予工作细则》）')
ws2.cell(row=r, column=1).font = Font(name='Microsoft YaHei', size=12, bold=True, color='C00000')
r += 1
deg = [
    '1. 已获得本科毕业证书（先毕业、后申学位）。',
    '2. 政治理论课合格，品行端正、恪守学术诚信。',
    '3. 毕业论文（设计）成绩：2024年9月1日后答辩的须达"中等"即 70 分及以上。',
    '4. 学位外语满足之一：',
    '   • 广东省学位办成人学士学位外国语水平全省统考合格；',
    '   • 深圳大学组织或认定的学位外语考试合格；',
    '   • PETS-3 及以上笔试合格（2022年起，非英语类专业）；',
    '   • CET-4 及以上且成绩 ≥425 分（2022年起，非英语类专业）；',
    '   • 全国外语水平考试（外语类专业为第二外语）笔试合格。',
    '5. 申请时限：一般不晚于毕业证书签发日期 6 个月内。',
    '6. 须提交：毕业论文原文、查重报告、开题报告、成绩评定表等过程性材料。',
    '7. 不得授予情形：违反品行/政治要求；在读期间有刑事犯罪记录；论文未达要求；外语未达标；超期等。',
]
for line in deg:
    ws2.cell(row=r, column=1, value=line)
    ws2.cell(row=r, column=1).font = Font(name='Microsoft YaHei', size=11)
    ws2.cell(row=r, column=1).alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    r += 1

r += 1
ws2.cell(row=r, column=1, value='三、毕业论文（设计）报考条件（深大计算机与软件学院自考办）')
ws2.cell(row=r, column=1).font = Font(name='Microsoft YaHei', size=12, bold=True, color='C00000')
r += 1
thesis = [
    '1. 专业计划中除毕业论文（11689）以外的【所有课程】必须已全部通过（笔试≥60分；实践课须在深圳大学考核且合格）。',
    '2. 在"广东省自学考试管理系统"做毕业预测，结果须显示"仅剩毕业论文未通过"方可报考（截图留底上传）。',
    '3. 报考每年两批（约 6 月、12 月），人数限招（如 25–50 人），满额即止，需抢报。',
    '4. 分"普通论文 / 学位论文"两类：欲申请学位须选"学位论文"，成绩须≥70分（中等），并建议于学位申请前一年内完成。',
    '5. 费用参考：报考费 270元/科，论文指导培训费 1500元（培训自选）。',
    '6. 2026年实际报名窗口参考：上半年批=前一年12月24日9:00–27日17:00；下半年批=当年6月1日9:00–5日17:00（每年窗口相近，须盯官网 csse.szu.edu.cn/zk 公告）。',
    '7. 报名须线上线下齐动：系统填报 + 寄纸质材料（报名表、考生信息简表、身份证复印件、毕业预测截图、PETS-3/CET成绩截图等，顺丰寄深大粤海校区），并选定"普通论文/学位论文"（不可改）。',
    '★ 要点：不是"剩几门"就能写，而是须把除论文外的 15 门课（含所有实践课）全考完后才能报论文；论文周期约半年，建议在倒数第二门通过后即关注下一批报考。',
    '★ 抢报提醒：报名窗口仅 3–5 天且限招（计算机约20–50人）、满额即止；须提前备好"毕业预测=仅剩毕业论文未通过"截图等材料，错过再等半年。',
]
for line in thesis:
    ws2.cell(row=r, column=1, value=line)
    ws2.cell(row=r, column=1).font = Font(name='Microsoft YaHei', size=11)
    ws2.cell(row=r, column=1).alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    r += 1

r += 1
ws2.cell(row=r, column=1, value='★ 关键提示：深大自考本科不要求课程平均分，各科 60 分及格即可；真正门槛是"论文70分 + 学位外语"。')
ws2.cell(row=r, column=1).font = Font(name='Microsoft YaHei', size=11, bold=True, color='2F75B5')
r += 1
ws2.cell(row=r, column=1, value='★ CET-4(428/2023) 仅在"注册深大考籍前"考的，不能抵学位外语，只能免 13000 英语课程；学位外语须在读期间另考 PETS-3（2027.03 场）。')
ws2.cell(row=r, column=1).font = Font(name='Microsoft YaHei', size=11, bold=True, color='C00000')
r += 1
ws2.cell(row=r, column=1, value='★ 策略：用 PETS-3 / CET-4(≥425) 免考 13000 英语，可"一证两用"——既免必考课，又满足学位外语条件（但仅限在读期间考的 CET-4）。')
ws2.cell(row=r, column=1).font = Font(name='Microsoft YaHei', size=11, bold=True, color='2F75B5')

ws2.column_dimensions['A'].width = 115
ws2.row_dimensions[1].height = 28

# ===== Sheet 3: 我的规划时间线 =====
ws3 = wb.create_sheet('我的规划时间线')
ws3.merge_cells('A1:C1')
ws3['A1'] = '个人规划时间线（已通过 3 门：15040 / 15044 / 13000免考）'
ws3['A1'].font = Font(name='Microsoft YaHei', size=13, bold=True, color='2F75B5')
ws3['A1'].alignment = Alignment(horizontal='center', vertical='center')

ws3['A3'] = '一、剩余课程清单（除已过的3门外，共 12 笔试 + 5 实践 + 1 论文）'
ws3['A3'].font = Font(name='Microsoft YaHei', size=12, bold=True, color='C00000')
remain = [
    '【政治/公共】15043 近现代史(3)｜00023 高等数学(工本,10学分)｜02324 离散数学(4)',
    '【专业笔试】13003 数据结构(4)｜13013 高级语言(4)｜13015 计算机系统原理(4)｜13180 操作系统(4)｜03344 信息与网络(3)｜08074 计算机高级程序(3)｜13005 软件工程(3)｜13009 数据库(4)｜13011 人工智能(6)',
    '【实践-须先过对应笔试】13004←13003｜13014←13013｜03345←03344｜08075←08074｜13006←13005',
    '【论文】11689 毕业论文（不计学分）',
    '★ 12 门笔试 ÷ 3 期(10月/1月/4月)×4门 = 名额刚好用满，无冗余；实践课会突破此排期。',
]
r = 4
for line in remain:
    ws3.cell(row=r, column=1, value=line)
    ws3.cell(row=r, column=1).font = Font(name='Microsoft YaHei', size=11)
    ws3.cell(row=r, column=1).alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    r += 1

r += 1
ws3.cell(row=r, column=1, value='二、关键前提与提醒（★ = 影响毕业时间的硬约束）')
ws3.cell(row=r, column=1).font = Font(name='Microsoft YaHei', size=12, bold=True, color='C00000')
r += 1
notes = [
    '1. ★ Oct 2026 报名紧急：考生报考 2026.9.1 14:00–9.4 17:00；缴费 9.2 10:00–9.5 17:00；考试 10.24–25；成绩约 11 月下旬。每期最多 4 门。',
    '2. ★ 5 门实践前置笔试（13003/13013/03344/08074/13005）须最晚在 2027.1 实践报名前通过，否则对应实践推迟到 2027.6 批。',
    '3. ★【已用官方原件二次核对】来源=粤考办〔2025〕20号《2026年4、10月开考课程安排表》(用户提供的4833814.pdf)。080901 在 2026.10 开 13 门：15044/15040/15043/13000/02324/00023/13180/13005/03344/13003/13009/13015/13013（与Web查得一致，无误）。4月表(同PDF第7页)对照：08074、13011 仅在4月+1月开→不在10月；03344、13009 仅在10月+1月开→不在4月。1月(附件.pdf)恰好开这4门交替课：03344/08074/13009/13011。',
    '4. ★ 【硬结论】08074 不在10月（4月/1月开，但2026.4已过→最早2027.1）；同理13011不在10月。08074 最早 2027.1 考、3月出分 → 实践 08075 最早 2027.6 批 → 故 2027.12 毕业在数学上不可能，锁定 2028.6 毕业。NCRE 9月场(6.25–7.3报名)已错过，无法补救。',
    '5. Oct 2026 名额只有 4 个，须放 13003/13013/13005/15043（4门全在10月开考，已核对）。03344 虽在10月开考，但塞进10月会导致 15043/00023/02324/13015/13180 中一门无处可考（Apr仅4名额）→ 故 03344 留 1 月考，对应实践 03345 顺延 2027.6。',
    '6. 学位外语：在读期间另考 PETS-3（2027 上半年 3 月场，约 1 月报名），5 月出分；CET-4(428/注册考籍前) 仅免 13000 课程，不能抵学位。',
    '7. 前置学历免考：大专·大数据(计算机类) 凭成绩单申请，但 2026 新规大专→本科仅免"加考课"，核心必考课大概率免不掉；15043/15044 须本科及以上前置方可免(大专不可)。仍建议提交系统判定，有免则赚。',
    '8. 实践课在深大粤海校区考（本人签到），报名约每年 1 月、6 月两批，限招满额即止，不走省系统，须盯计算机与软件学院自考办(csse.szu.edu.cn/zk)。',
    '9. 毕业预测须在"仅剩毕业论文未通过"时才能报论文；所有实践课通过是前提。论文周期约半年。',
    '10. ★【2026.8.17 晚最终定论】用户已自查大专(大数据技术与应用)全部专业课，均不满足前置学历免考"要求相当"条件 → 专业课免考希望归零，规划按"零免考"执行。仅 13000 凭 CET-4(428) 确认免考；15043/15044 须本科及以上前置(大专不可)。剩余 12 笔试 + 5 实践 + 1 论文全部要考，2028.6 为唯一确定毕业时间（无减压阀）。仍建议把大专成绩单提交系统走一次终审形式，但以 2028.6 为基准规划，不赌免考。',
    '11. ★【2026.8.18 排法澄清】最终笔试排法=10月4门(13003/13005/15043/13013) + 1月4门(03344/08074/13009/13011) + 4月4门(02324/13180/00023/13015)，共12门。注意：4月是"4门"不是"3门"——用户曾误以为10月能同时报离散+操作系统，但 02324/00023/13180/13005 全在 10/24 下午四选一撞车，离散(02324)与操作系统(13180)报不成→必须挪到4月。NCRE-2 免 13013 因 2026.9 场已错过、2027.3 场出成绩(约5月)赶不上4月报名，故 13013 直接在 2026.10 考，不靠 NCRE。',
]
for line in notes:
    ws3.cell(row=r, column=1, value=line)
    ws3.cell(row=r, column=1).font = Font(name='Microsoft YaHei', size=11)
    ws3.cell(row=r, column=1).alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    r += 1

r += 1
ws3.cell(row=r, column=1, value='三、Oct 2026 报名建议（4 门优先级）')
ws3.cell(row=r, column=1).font = Font(name='Microsoft YaHei', size=12, bold=True, color='C00000')
r += 1
oct_plan = [
    '第1门：13003 数据结构与算法（实践前置，10月开考，必抢）',
    '第2门：13013 高级语言程序设计（实践前置，10月开考，必抢）',
    '第3门：13005 软件工程（实践前置，10月开考，必抢）',
    '第4门：15043 近现代史（10月开考；若想先清高数可换 00023，但15043更该早过）',
    '（03344/13009 虽10月也开，但留1月保4/4/4平衡；08074/13011 不在10月只能1月或4月→锁1月）',
]
for line in oct_plan:
    ws3.cell(row=r, column=1, value=line)
    ws3.cell(row=r, column=1).font = Font(name='Microsoft YaHei', size=11)
    ws3.cell(row=r, column=1).alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    r += 1

r += 1
ws3.cell(row=r, column=1, value='四、倒推时间线（按"干净排法"：10月放3门前置+1门，1月放4门含03344/08074，4月放剩余 → 现实毕业 2028.6）')
ws3.cell(row=r, column=1).font = Font(name='Microsoft YaHei', size=12, bold=True, color='C00000')
r += 1
# header
for c, h in enumerate(['时间', '动作', '备注'], 1):
    cell = ws3.cell(row=r, column=c, value=h)
    cell.font = Font(name='Microsoft YaHei', bold=True, size=11)
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal='center', vertical='center')
r += 1
timeline = [
    ('现在–尽快', '提交 CET-4 免 13000（已办跳过）；提交前置学历免考（大专成绩单）', '审核约30工作日；决定剩余量，须赶在毕业预测前录完'),
    ('2026.9.1–4', '抢报 Oct 2026：13003、13013、13005、15043（08074不在10月，第4门锁定15043）', '报考窗口仅4天；缴费 9.2–9.5'),
    ('2026.9', 'NCRE 二级C（9月场）报名已结束(6.25–7.3)，未报上；下场2027.3已无意义', '13013 改在 2026.10 正常考'),
    ('2026.10.24–25', '参加 Oct 2026 考试', '成绩约 2026.11 下旬'),
    ('2026.12', '若过13003/13013/13005，备 2027.1 实践报名材料', '须毕业预测="仅剩毕业论文未通过"截图'),
    ('2027.1上旬', '实践报名：13004、13014、13006（对应已过3门前置）；03344/08074若10月已过则连03345、08075一起报', '限额抢报；深大粤海校区'),
    ('2027.1', '笔试报考：03344、08074、13009、13011（若未在10月考）', '按你的1月截图仅这4门计科课'),
    ('2027.3', '实践考试（深大粤海校区，本人签到）', '上半年批实践；成绩约4–5月上传'),
    ('2027.4', '最后笔试4门：02324 离散、13180 操作系统、00023 高数、13015 系统原理', '其中 离散/操作系统 因 10/24 下午撞车(02324/00023/13180/13005 四选一)报不成→挪至4月；等当次官表核对时段后一把报掉'),
    ('2027.5', '4月成绩公布 → 做"毕业预测"', '确认显示"仅剩毕业论文未通过"'),
    ('2027.6.1–5', '抢报下半年批毕业论文（选"学位论文"）', '限招满额即止；前提：所有非论文课已过(含实践)'),
    ('2027下半年', '若03344/08074在1月考，则其实践03345/08075报2027.6批，9–10月考试', '成绩11–12月上传，卡毕业边'),
    ('2028.6（唯一确定）', '本科毕业（领毕业证）', '前置学历免考已排除→零免考，08075实践最早2027.6批→论文2027底启动→2028.6毕业'),
    ('学位外语', '2027上半年(3月)考 PETS-3（约1月报名）', '深圳有考点；深大仅看笔试≥60；须在读期间考。若CET-4(2023/注册考籍前)被认定不可抵，则此证必考'),
    ('2028.6 起6个月内', '提交学士学位申请', '前提：论文≥70(须选"学位论文")+学位外语达标+查重/开题/成绩评定表等过程材料；截止约2028.12'),
    ('约2028.12–2029初', '领取学士学位证书', '审核通过后发放；逾期视为放弃。两证：毕业证2028.6、学位证约2028底–2029初，均非2027'),
]
for t, act, remark in timeline:
    ws3.cell(row=r, column=1, value=t)
    ws3.cell(row=r, column=2, value=act)
    ws3.cell(row=r, column=3, value=remark)
    for c in range(1, 4):
        ws3.cell(row=r, column=c).font = Font(name='Microsoft YaHei', size=11)
        ws3.cell(row=r, column=c).alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
        ws3.cell(row=r, column=c).border = thin_border
    r += 1

ws3.column_dimensions['A'].width = 20
ws3.column_dimensions['B'].width = 52
ws3.column_dimensions['C'].width = 44
ws3.row_dimensions[1].height = 28

wb.save('/Users/temu/WorkBuddy/2026-08-17-19-27-13/outputs/计算机科学与技术_新科目表.xlsx')
print('done')
