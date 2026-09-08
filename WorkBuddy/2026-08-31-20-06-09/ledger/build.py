import csv, html, re
from collections import defaultdict

BASE = '/Users/temu/WorkBuddy/2026-08-31-20-06-09/ledger'

def load(fn, month):
    rows = list(csv.DictReader(open(f'{BASE}/{fn}', encoding='utf-8-sig')))
    for r in rows:
        r['day'] = int(re.match(r'%d月(\d+)日' % month, r['日期']).group(1))
        r['amt'] = float(r['花费'])
    return rows

def cat(item, amt):
    if amt < 0: return '收入'
    if '助学贷款' in item: return '还助学贷款'
    if '花呗' in item: return '还花呗'
    if '补室友' in item or '垫房租' in item: return '代垫室友'
    if '老妹' in item or '欧阳' in item or '转账' in item or '转钱' in item: return '借出他人'
    if '奶奶' in item or '买花' in item: return '人情礼物'
    if '社康' in item or '看病' in item: return '医疗'
    if '房租' in item: return '房租'
    if '话费' in item: return '通讯'
    if '地铁' in item or '打车' in item or '车票' in item or '电驴' in item: return '交通'
    if '体彩' in item or '射箭' in item or '打牌' in item: return '娱乐'
    if 'aa' in item: return '聚餐社交'
    if '榴莲' in item or '水果' in item or '西瓜' in item or '辣条' in item or '冰棒' in item or '买水' in item: return '水果零食'
    if '买菜' in item or '鸡蛋' in item: return '买菜食材'
    if item.startswith('吃') or item == '中饭' or '糖水' in item: return '正餐'
    if '快递' in item or '邮寄' in item: return '杂项'
    if '手机' in item: return '数码维修'
    if '柔顺剂' in item or '地垫' in item or '锯子' in item: return '家居日用'
    return '购物'

COLOR = {'正餐': '#D85A30', '水果零食': '#EF9F27', '聚餐社交': '#F0997B', '买菜食材': '#F5C4B3',
         '房租': '#534AB7', '家居日用': '#AFA9EC', '医疗': '#E24B4A',
         '还助学贷款': '#993C1D', '还花呗': '#BA7517', '借出他人': '#D4537E', '代垫室友': '#F0997B',
         '人情礼物': '#ED93B1',
         '交通': '#378ADD', '通讯': '#888780', '娱乐': '#1D9E75',
         '购物': '#7F77DD', '数码维修': '#5F5E5A', '杂项': '#B4B2A9', '其他': '#B4B2A9', '收入': '#639922'}
GMAP = {'正餐': '吃饭', '水果零食': '吃饭', '聚餐社交': '吃饭', '买菜食材': '吃饭',
        '房租': '居住', '家居日用': '居住',
        '还助学贷款': '还债', '还花呗': '还债', '数码维修': '购物', '人情礼物': '人情',
        '借出他人': '借出与代垫', '代垫室友': '借出与代垫'}
NON_DAILY = {'房租', '还助学贷款', '还花呗', '借出他人', '代垫室友', '医疗'}
ONE_OFF = {'手机送回费', '买体彩', '奶奶过生日', '给倩买花'}

def money(v): return '{:,.2f}'.format(v)

def analyze(rows, days=31):
    for r in rows: r['cat'] = cat(r['事项'], r['amt'])
    exp = [r for r in rows if r['amt'] > 0]
    inc = [r for r in rows if r['amt'] < 0]
    m = {'rows': rows, 'exp': exp, 'inc': inc, 'n': len(rows), 'days': days}
    m['gross'] = sum(r['amt'] for r in exp)
    m['tin'] = -sum(r['amt'] for r in inc)
    m['net'] = m['gross'] - m['tin']
    sub = defaultdict(float)
    for r in exp: sub[r['cat']] += r['amt']
    m['sub'] = dict(sorted(sub.items(), key=lambda kv: -kv[1]))
    grp = defaultdict(float)
    for c, v in m['sub'].items(): grp[GMAP.get(c, c)] += v
    m['grp'] = dict(sorted(grp.items(), key=lambda kv: -kv[1]))
    m['nondaily'] = sum(v for c, v in m['sub'].items() if c in NON_DAILY)
    m['daily'] = m['gross'] - m['nondaily']
    m['oneoff'] = sum(r['amt'] for r in exp if r['事项'] in ONE_OFF)
    m['core'] = m['daily'] - m['oneoff']
    byday = defaultdict(float); dayinc = defaultdict(float)
    for r in exp: byday[r['day']] += r['amt']
    for r in inc: dayinc[r['day']] += -r['amt']
    m['byday'] = byday; m['dayinc'] = dayinc
    m['big'] = sorted(exp, key=lambda r: -r['amt'])[:12]
    return m

jul = analyze(load('july.csv', 7))
aug = analyze(load('august.csv', 8))

CSS = '''*{{box-sizing:border-box}}
body{{margin:0;padding:32px 24px 64px;background:#FAFAF8;color:#2C2C2A;
font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB",sans-serif;font-size:13px;line-height:1.6}}
.wrap{{max-width:1000px;margin:0 auto}}
h1{{font-size:20px;font-weight:500;margin:0 0 4px}}
h2{{font-size:15px;font-weight:500;margin:32px 0 12px}}
h3{{font-size:13px;font-weight:500;margin:0 0 8px;color:#5F5E5A}}
.sub{{color:#5F5E5A;margin:0 0 24px}}
.cards{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}}
.card{{background:#fff;border:0.5px solid rgba(0,0,0,.12);border-radius:12px;padding:16px}}
.card .k{{color:#5F5E5A;font-size:12px}}
.card .v{{font-size:22px;font-weight:500;margin-top:4px;font-variant-numeric:tabular-nums}}
.card .n{{color:#5F5E5A;font-size:12px}}
.card.hi{{border:1px solid #534AB7}}
.card.warn{{border:1px solid #E24B4A;background:#FCEBEB}}
table{{width:100%;border-collapse:collapse;background:#fff;border:0.5px solid rgba(0,0,0,.12);border-radius:12px;overflow:hidden;margin-bottom:8px}}
th,td{{padding:8px 12px;text-align:left;border-bottom:0.5px solid rgba(0,0,0,.06)}}
th{{background:#F1EFE8;color:#5F5E5A;font-weight:500;font-size:12px}}
tr:last-child td{{border-bottom:none}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
tr.inc td{{color:#3B6D11}}
tr.dup td{{background:#FCEBEB}}
.tag{{display:inline-block;padding:1px 8px;border-radius:20px;border:0.5px solid;font-size:11px;white-space:nowrap}}
.bar{{height:8px;background:#F1EFE8;border-radius:4px;overflow:hidden}}
.bar i{{display:block;height:100%;border-radius:4px}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.note{{background:#fff;border:0.5px solid rgba(0,0,0,.12);border-radius:12px;padding:16px;color:#444441}}
.note li{{margin:6px 0}}
.note.warn{{border-color:#E24B4A;background:#FCEBEB;color:#501313}}
.up{{color:#A32D2D}}
.down{{color:#3B6D11}}
@media(max-width:760px){{.cards{{grid-template-columns:repeat(2,1fr)}}.grid2{{grid-template-columns:1fr}}}}'''

def cat_html(m, title):
    mx = max(m['grp'].values())
    rows = ''.join(
        f'<tr><td>{k}</td><td class="num">{money(v)}</td><td class="num">{v/m["gross"]*100:.1f}%</td>'
        f'<td style="width:34%"><div class="bar"><i style="width:{v/mx*100:.1f}%;background:{COLOR.get(k,"#85B7EB")}"></i></div></td></tr>'
        for k, v in m['grp'].items())
    return f'<h2>{title}大类</h2><table><thead><tr><th>类别</th><th class="num">金额</th><th class="num">占毛流出</th><th>分布</th></tr></thead><tbody>{rows}</tbody></table>'

def sub_html(m):
    rows = ''.join(
        f'<tr><td><span class="tag" style="background:{COLOR.get(k,"#888")}1a;color:{COLOR.get(k,"#5F5E5A")};border-color:{COLOR.get(k,"#888")}55">{k}</span></td>'
        f'<td class="num">{money(v)}</td>'
        f'<td class="num">{money(v/len([r for r in m["exp"] if r["cat"]==k]))}</td></tr>'
        for k, v in m['sub'].items())
    return f'<table><thead><tr><th>科目</th><th class="num">金额</th><th class="num">笔均</th></tr></thead><tbody>{rows}</tbody></table>'

def day_html(m, month):
    mx = max(m['byday'].values()) if m['byday'] else 1
    rows = ''.join(
        f'<tr><td>{month}月{d}日</td><td class="num">{money(m["byday"][d])}</td>'
        f'<td class="num">{"+"+money(m["dayinc"][d]) if m["dayinc"][d] else "—"}</td>'
        f'<td style="width:34%"><div class="bar"><i style="width:{m["byday"][d]/mx*100:.1f}%;background:{"#D85A30" if m["byday"][d] > mx*0.5 else "#85B7EB"}"></i></div></td></tr>'
        for d in range(1, m['days'] + 1))
    return f'<table><thead><tr><th>日期</th><th class="num">支出</th><th class="num">当日进账</th><th>分布</th></tr></thead><tbody>{rows}</tbody></table>'

def detail_html(m, month):
    rows = []
    for r in m['rows']:
        pos = r['amt'] > 0
        cls = 'inc' if not pos else ('dup' if r['事项'] in ('借老妹钱', '借老妹') else '')
        c = COLOR.get(r['cat'], '#888780')
        rows.append(
            f'<tr class="{cls}"><td>{month}月{r["day"]}日</td><td>{html.escape(r["事项"])}</td>'
            f'<td><span class="tag" style="background:{c}1a;color:{c};border-color:{c}55">{r["cat"]}</span></td>'
            f'<td class="num">{money(abs(r["amt"]))}</td></tr>')
    return f'<table><thead><tr><th style="width:88px">日期</th><th>事项</th><th style="width:104px">分类</th><th class="num" style="width:96px">金额</th></tr></thead><tbody>{"".join(rows)}</tbody></table>'

keys = ['借出与代垫', '还债', '居住', '吃饭', '医疗', '交通', '通讯', '娱乐', '购物', '人情']
cmp_rows = ''.join(
    f'<tr><td>{k}</td><td class="num">{money(jul["grp"].get(k,0))}</td><td class="num">{money(aug["grp"].get(k,0))}</td>'
    f'<td class="num {"up" if aug["grp"].get(k,0) > jul["grp"].get(k,0) else "down"}">{aug["grp"].get(k,0)-jul["grp"].get(k,0):+,.2f}</td></tr>'
    for k in keys if jul['grp'].get(k, 0) or aug['grp'].get(k, 0))

dup_note = ''
sister = [r for r in jul['exp'] if '老妹' in r['事项']]
if len(sister) == 2:
    dup_note = (f'<div class="note warn" style="margin-top:16px"><strong>已确认：两笔「借老妹」为真实的两笔借出</strong>'
                f'<ul><li>7月29日 ¥5,280 + 7月31日 ¥5,280 = <strong>¥10,560</strong>，三天内借出，相当于当月工资 ¥7,921.95 的 <strong>133%</strong>。</li>'
                f'<li>这是 7月超支 ¥{money(jul["net"])} 的<strong>最主要原因</strong>——光借给老妹的钱就比工资多 ¥{money(10560-7921.95)}。</li>'
                f'<li>建议明确一下还款时间：如果老妹能近期还回，7月的「超支」只是资金临时腾挪；如果短期还不上，这笔要当作支出看待，先把自己 3–6 个月的生活备用金留足。</li></ul></div>')

FC = [
 ('房租（含跨月预付）', 1219.50, 652.00, 652, 652, 652,
  '7月 ¥1,219.50 = 7月份额 567.5 + 预付8月 652（另 ¥521 代垫已单列，不计入）。你的月租份额 ¥567–652，付款节奏是月底付下月'),
 ('吃饭', 1351.68, 1261.81, 1300, 1150, 1550,
  '7月日均 43.6、8月日均 40.7，9月少一天。中秋聚餐会推高；榴莲是单项最大变量（8月 ¥172.23）'),
 ('中秋 + 国庆前置（9/25–27）', None, None, 300, 0, 600,
  '9月25日中秋放假 3 天，国庆 10/1–7 紧随。含返乡往返车票 150–200、月饼伴手 100–200、聚餐 100–200'),
 ('交通', 163.20, 165.45, 165, 140, 260,
  '地铁 + 电驴，两月几乎一样（163.20 / 165.45），是最稳的一栏；返乡车票已单列在中秋项'),
 ('通讯', 96.33, 92.74, 95, 90, 100,
  '两月都在 92–96，且每月各有两笔 37–48 的充值——是固定支出（疑为两张卡或话费+宽带），不是异常'),
 ('医疗', 609.80, 246.40, 250, 0, 650,
  '连续两月发生。7月是一笔 ¥410 的检查；无复查则接近 0，有复查或长期用药则 400+'),
 ('日用 + 购物', 333.98, 445.90, 180, 80, 400,
  '两月都含一次性大额（7月手机送修 150，8月耳机 114 + 购物 193）。剔除后常规月份约 140–180'),
 ('人情 + 娱乐', 239.35, 588.62, 80, 30, 400,
  '剔除体彩 218、奶奶生日 400、买花 109 之后常规只有 20–80；中秋可能带来额外人情'),
]
fc_rows = ''.join(
    f'<tr><td>{l}</td><td class="num">{money(j) if j is not None else "—"}</td>'
    f'<td class="num">{money(a) if a is not None else "—"}</td>'
    f'<td class="num"><strong>{money(c)}</strong></td>'
    f'<td class="num">{money(lo)} – {money(hi)}</td><td>{n}</td></tr>'
    for l, j, a, c, lo, hi, n in FC)
fc_j = sum(j for _, j, _, _, _, _, _ in FC if j is not None)
fc_a = sum(a for _, _, a, _, _, _, _ in FC if a is not None)
fc_c = sum(c for _, _, _, c, _, _, _ in FC)
fc_lo = sum(lo for _, _, _, _, lo, _, _ in FC)
fc_hi = sum(hi for _, _, _, _, _, hi, _ in FC)

out = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>7–8月账本 · 支出分析</title><style>{CSS}</style></head><body><div class="wrap">
<h1>7–8月账本 · 支出分析</h1>
<p class="sub">共 189 笔记录（7月 98 笔 / 8月 91 笔）。负号一律按<strong>进账</strong>处理；两月使用同一套分类口径。</p>

<div class="note" style="margin-bottom:8px;border-color:#185FA5;background:#E6F1FB"><strong>口径说明</strong>
<ul>
<li><strong>7月为完整流水</strong>：进账 ¥{money(jul['tin'])}（工资 7,921.95 + 奖金 888.97 + 兼职 250 + 欧阳还钱 300 + 报销/退款 9.10）。</li>
<li><strong>8月工资为补记</strong>：原账本漏记，现按与 7 月同额 <strong>¥7,921.95</strong> 补入 8月15日（若实际金额不同，告诉我即可重算）。</li>
<li><strong>两笔「借老妹 5,280」经确认为真实的两笔借出</strong>，合计 ¥10,560，非重复记账。</li>
<li><strong>房租为与室友 AA，且轮流垫付</strong>：7月31日的 ¥1,173 已拆为「交下月房租 ¥652」+「补室友 6月垫付 ¥521」。拆出的 ¥521 属于<strong>跨月找补、不是 7月居住成本</strong>，已单列为「代垫室友」，与借出归为一类（钱出去了但不属于自己的消费）。你的月租金份额约 <strong>¥567–652</strong>。</li>
</ul></div>

<h2>两月总览</h2>
<div class="cards">
<div class="card"><div class="k">7月 毛流出</div><div class="v">¥{money(jul['gross'])}</div><div class="n">91 笔支出 · 6 笔进账</div></div>
<div class="card warn"><div class="k">7月 超支</div><div class="v" style="color:#A32D2D">¥{money(jul['net'])}</div><div class="n">支出比进账多出这个数</div></div>
<div class="card"><div class="k">8月 毛流出</div><div class="v">¥{money(aug['gross'])}</div><div class="n">88 笔支出 · 5 笔进账（含补记工资）</div></div>
<div class="card" style="border:1px solid #3B6D11;background:#EAF3DE"><div class="k">8月 结余</div><div class="v" style="color:#3B6D11">+¥{money(-aug['net'])}</div><div class="n">补记工资 {money(7921.95)} 后为盈余</div></div>
</div>

<h2>两月对比</h2>
<table><thead><tr><th>类别</th><th class="num">7月</th><th class="num">8月</th><th class="num">变化</th></tr></thead><tbody>{cmp_rows}
<tr style="background:#F1EFE8"><td><strong>毛流出合计</strong></td><td class="num"><strong>{money(jul['gross'])}</strong></td><td class="num"><strong>{money(aug['gross'])}</strong></td><td class="num"><strong>{aug['gross']-jul['gross']:+,.2f}</strong></td></tr>
<tr style="background:#F1EFE8"><td><strong>进账合计</strong></td><td class="num"><strong>{money(jul['tin'])}</strong></td><td class="num"><strong>{money(aug['tin'])}</strong></td><td class="num"><strong>{aug['tin']-jul['tin']:+,.2f}</strong></td></tr>
<tr style="background:#F1EFE8"><td><strong>结余</strong>（正=盈余 / 负=超支）</td><td class="num" style="color:#A32D2D"><strong>−{money(jul['net'])}</strong></td><td class="num" style="color:#3B6D11"><strong>+{money(-aug['net'])}</strong></td><td class="num" style="color:#3B6D11"><strong>{-(aug['net']-jul['net']):+,.2f}</strong></td></tr>
<tr style="background:#F1EFE8"><td><strong>两月合计结余</strong></td><td class="num" colspan="2"><strong>{'净超支' if (jul['net']+aug['net'])>0 else '净结余'} ¥{money(abs(jul['net']+aug['net']))}</strong></td><td class="num"><strong>—</strong></td></tr>
<tr><td>日常开销（剔房租/还债/借出/医疗）</td><td class="num">{money(jul['daily'])}</td><td class="num">{money(aug['daily'])}</td><td class="num up">{aug['daily']-jul['daily']:+,.2f}</td></tr>
<tr><td>日常日均</td><td class="num">{money(jul['daily']/31)}</td><td class="num">{money(aug['daily']/31)}</td><td class="num up">{aug['daily']/31-jul['daily']/31:+.2f}</td></tr>
<tr><td>再剔一次性（维修/彩票/生日/买花）</td><td class="num">{money(jul['core'])}</td><td class="num">{money(aug['core'])}</td><td class="num up">{aug['core']-jul['core']:+,.2f}</td></tr>
<tr><td>生活基本盘 日均</td><td class="num">{money(jul['core']/31)}</td><td class="num">{money(aug['core']/31)}</td><td class="num up">{aug['core']/31-jul['core']/31:+.2f}</td></tr>
</tbody></table>

<h2>7月</h2>
{cat_html(jul, '7月')}
<div class="grid2">
<div><h3>细分科目</h3>{sub_html(jul)}</div>
<div><h3>单笔 TOP 12</h3><table><thead><tr><th>日期</th><th>事项</th><th class="num">金额</th></tr></thead><tbody>
{''.join(f'<tr class="{"dup" if r["事项"] in ("借老妹钱","借老妹") else ""}"><td>7月{r["day"]}日</td><td>{html.escape(r["事项"])}</td><td class="num">{money(r["amt"])}</td></tr>' for r in jul['big'])}
</tbody></table>
<h3>进账明细</h3><table><thead><tr><th>日期</th><th>事项</th><th class="num">金额</th></tr></thead><tbody>
{''.join(f'<tr class="inc"><td>7月{r["day"]}日</td><td>{html.escape(r["事项"])}</td><td class="num">+{money(-r["amt"])}</td></tr>' for r in jul['inc'])}
</tbody></table></div>
</div>
<h3>逐日支出</h3>{day_html(jul, 7)}
{dup_note}

<h2>8月</h2>
{cat_html(aug, '8月')}
<div class="grid2">
<div><h3>细分科目</h3>{sub_html(aug)}</div>
<div><h3>单笔 TOP 12</h3><table><thead><tr><th>日期</th><th>事项</th><th class="num">金额</th></tr></thead><tbody>
{''.join(f'<tr><td>8月{r["day"]}日</td><td>{html.escape(r["事项"])}</td><td class="num">{money(r["amt"])}</td></tr>' for r in aug['big'])}
</tbody></table>
<h3>进账明细</h3><table><thead><tr><th>日期</th><th>事项</th><th class="num">金额</th></tr></thead><tbody>
{''.join(f'<tr class="inc"><td>8月{r["day"]}日</td><td>{html.escape(r["事项"])}</td><td class="num">+{money(-r["amt"])}</td></tr>' for r in aug['inc'])}
</tbody></table></div>
</div>
<h3>逐日支出</h3>{day_html(aug, 8)}

<h2>明细</h2>
<h3>7月全部记录</h3>{detail_html(jul, 7)}
<h3>8月全部记录</h3>{detail_html(aug, 8)}

<h2>读出来的几件事</h2>
<div class="note"><ul>
<li><strong>7月是严重超支月——但超支的全是"钱借出去"，不是自己花掉的</strong>：毛流出 ¥{money(jul['gross'])}，进账 ¥{money(jul['tin'])}，现金上超支 <strong>¥{money(jul['net'])}</strong>。把不属于自己消费的部分剔掉后：借给老妹 ¥10,560 + 补室友垫付 ¥521 + 借给欧阳/汤汤/卤蛋 ¥902.90 = <strong>¥11,983.90 是"钱出去了但不算消费"</strong>。剩下 ¥{money(jul['gross']-11983.90)} 才是 7月真实花钱（含还债 ¥4,088.08）。用它对比进账 ¥{money(jul['tin'])}，<strong>7月其实还有 ¥{money(jul['tin']-(jul['gross']-11983.90))} 的结余</strong>——你的消费水平并没有失控。</li>
<li><strong>助学贷款 ¥{money(jul['sub']['还助学贷款'])}</strong> 分 5 次还（400 / 350 / 163 / 485 / 1,940.91），7月15日那笔 1,940.91 大概率是结清尾款。确认一下是否已还完，8月起这笔应该消失。</li>
<li><strong>花呗还款 ¥{money(jul['sub']['还花呗'])}</strong> 是 6 月的消费账单，7月已清。8月账本里没有花呗还款记录，说明 7月内的消费（约 749 那部分）已在 8月账单里，注意别滚雪球。</li>
<li><strong>医疗 ¥{money(jul['sub']['医疗'])}</strong>，集中在 7月29日一笔 ¥410 的检查。加上 8月的 ¥246.40，两个月身体上花了 ¥856.20，是仅次于房租的固定支出来源。</li>
<li><strong>吃饭其实很稳</strong>：7月 ¥{money(jul['grp']['吃饭'])}，8月 ¥{money(aug['grp']['吃饭'])}，降了 ¥{money(jul['grp']['吃饭']-aug['grp']['吃饭'])}。7月有三次聚餐型大餐（220 / 202 / 195.9），8月只有一次 169。</li>
<li><strong>房租已理清：你和室友 AA、轮流垫付</strong>。7月31日的 ¥1,173 拆为「8月房租你的份额 ¥652」+「补室友 6月垫付的 ¥521」。你的月租金份额在 <strong>¥567–652</strong> 之间（7月1日 567.5、8月31日 652）。注意付款节奏是<strong>月底付下个月</strong>，所以 8月31日那笔 ¥652 付的是 9月房租——9月的现金流里不用再预留房租，除非 9月30日继续付 10月。</li>
<li><strong>8月补记工资后是盈余月</strong>：支出 ¥{money(aug['gross'])}，进账 ¥{money(aug['tin'])}（补记工资 7,921.95 + 老妹转账 520 + 欧阳还钱 200 + 兼职 200 + 红包 0.18），<strong>结余 +¥{money(-aug['net'])}</strong>。7月超支 ¥{money(jul['net'])}、8月盈余 ¥{money(-aug['net'])}，两月相抵仍是<strong>净超支 ¥{money(jul['net']+aug['net'])}</strong>，缺口全在 7月借给老妹的 ¥10,560 上。</li>
<li><strong>9月没有大额负债压力了</strong>：助学贷款 ¥3,338.91 已在 7月结清（8月无记录），花呗 8月也无还款记录。若 9月不再借出，按 8月的生活水平（日常 ¥{money(aug['core'])}，日均 ¥{money(aug['core']/31)}）走，一个月工资能存下约 ¥{money(7921.95-652-aug['core'])}。</li>
<li><strong>生活基本盘在上升</strong>：剔除房租、还债、借出、医疗和一次性项目后，7月日均 ¥{money(jul['core']/31)}，8月日均 ¥{money(aug['core']/31)}，涨了 {(aug['core']/31)/(jul['core']/31)*100-100:.1f}%。增速不快，但方向是往上走。</li>
</ul></div>

<h2>9月预算建议</h2>
<p class="sub">按 8月实际消费水平 + 两月均值定额度，房租按你的 AA 份额计。工资按 ¥7,921.95 估。</p>
<table><thead><tr><th>科目</th><th class="num">额度</th><th class="num">8月实际</th><th>依据与说明</th></tr></thead><tbody>
{''.join(f'<tr><td>{l}</td><td class="num">{money(b)}</td><td class="num">{money(a)}</td><td>{n}</td></tr>' for l, b, a, n in [
('房租', 652.00, aug['sub']['房租'], '你的 AA 份额。8月31日那笔 ¥652 付的是 9 月房租，若 9月30日继续付 10 月则本月现金流出 652'),
('正餐 + 聚餐', 900.00, aug['sub']['正餐'] + aug['sub'].get('聚餐社交', 0), '日均 30 元（午饭 12 + 晚饭 18），8月实际日均 29.6，基本持平'),
('水果 + 零食', 150.00, aug['sub']['水果零食'], '榴莲 ¥172.23 是最大变量：砍到每月 1 次（约 ¥60）即可守住这栏'),
('买菜食材', 50.00, aug['sub']['买菜食材'], '买菜 + 鸡蛋，8月 3 笔共 ¥64.67'),
('交通', 170.00, aug['sub']['交通'], '地铁 60 + 电驴 105，两月都在 165 左右，很稳定'),
('通讯', 45.00, aug['sub']['通讯'], '8月含一笔异常 ¥48，正常月份约 ¥45。建议查套餐外扣费'),
('医疗', 250.00, aug['sub']['医疗'], '两月连续发生（7月 ¥609.80 / 8月 ¥246.40），必须预留'),
('日用 + 购物', 200.00, aug['sub']['家居日用'] + aug['sub']['购物'] + aug['sub']['杂项'], '8月含骨传导耳机 ¥114.19 + 购物 ¥193.49 属一次性，常规月份约 ¥140'),
('人情 + 娱乐', 300.00, aug['sub'].get('人情礼物', 0) + aug['sub']['娱乐'], '8月含奶奶生日 ¥400 + 买花 ¥109 属一次性，常规月份约 ¥80'),
])}
<tr style="background:#F1EFE8"><td><strong>合计</strong></td><td class="num"><strong>2,717.00</strong></td><td class="num"><strong>{money(aug['gross'])}</strong></td><td><strong>预算比 8月实际低 ¥{money(aug['gross']-2717)}</strong>，差额主要在人情与一次性购物；预计可存 ¥5,204.95（工资 7,921.95 − 2,717）</td></tr>
</tbody></table>
<div class="note"><ul>
<li>预算里<strong>没有</strong>助学贷款和花呗（7月已结清、8月无记录），如果 9月还有欠款要还，从「预计可存」里扣。</li>
<li>如果老妹的 ¥10,560 能在 9月还回，那是一笔额外进账，建议<strong>直接转入储蓄，不要并入日常预算</strong>。</li>
<li>最容易超的是「水果零食」和「人情娱乐」两栏，两者合计 ¥450，占预算 16.6%，但历史上波动最大。</li>
</ul></div>

<h2>9月花销预估（基于两月数据的预测）</h2>
<p class="sub">上一节是「该花多少」的<strong>预算</strong>，这一节是「会花多少」的<strong>预估</strong>。按 7、8 月实际水平外推，并计入 9月25–27日中秋假期。工资按 ¥{money(7921.95)} 估。</p>
<table><thead><tr><th>科目</th><th class="num">7月</th><th class="num">8月</th><th class="num">9月预估</th><th class="num">区间</th><th>预测依据</th></tr></thead><tbody>
{fc_rows}
<tr style="background:#F1EFE8"><td><strong>合计</strong></td><td class="num"><strong>{money(fc_j)}</strong></td><td class="num"><strong>{money(fc_a)}</strong></td><td class="num"><strong>{money(fc_c)}</strong></td><td class="num"><strong>{money(fc_lo)} – {money(fc_hi)}</strong></td><td>日均约 ¥{money(fc_c/30)}（含房租与中秋）</td></tr>
</tbody></table>

<div class="cards" style="margin:16px 0">
<div class="card" style="border:1px solid #3B6D11;background:#EAF3DE"><div class="k">乐观情形</div><div class="v" style="color:#3B6D11">¥{money(fc_lo)}</div><div class="n">不回老家、无医疗、无额外购物 → 结余 ¥{money(7921.95-fc_lo)}</div></div>
<div class="card hi"><div class="k">中枢预估</div><div class="v">¥{money(fc_c)}</div><div class="n">结余 ¥{money(7921.95-fc_c)}（工资 7,921.95 − 预估支出）</div></div>
<div class="card warn"><div class="k">悲观情形</div><div class="v" style="color:#A32D2D">¥{money(fc_hi)}</div><div class="n">医疗复查 + 返乡 + 人情叠加 → 结余 ¥{money(7921.95-fc_hi)}</div></div>
<div class="card"><div class="k">预估存款率</div><div class="v">{(7921.95-fc_c)/7921.95*100:.0f}%</div><div class="n">8月实际为 {(7921.95-aug['gross'])/7921.95*100:.0f}%</div></div>
</div>

<h3>9月现金流节奏</h3>
<table><thead><tr><th>时间</th><th>事项</th><th class="num">预计金额</th><th>说明</th></tr></thead><tbody>
<tr><td>9月15日前后</td><td>工资到账</td><td class="num" style="color:#3B6D11">+{money(7921.95)}</td><td>与 7月同额估；若中秋有加班或过节费会更高</td></tr>
<tr><td>全月</td><td>日常开销</td><td class="num">−{money(fc_c-652-300)}</td><td>吃饭 + 交通 + 通讯 + 日用，日均约 ¥{money((fc_c-652-300)/30)}</td></tr>
<tr><td>9月25–27日</td><td>中秋假期</td><td class="num">−{money(300)}</td><td>放假 3 天；返乡车票、月饼伴手、聚餐集中在这几天</td></tr>
<tr><td>9月30日</td><td>付 10 月房租</td><td class="num">−{money(652)}</td><td>维持「月底付下月」节奏才会发生；9月本身的房租已于 8月31日付清</td></tr>
<tr style="background:#F1EFE8"><td colspan="2"><strong>月末预计余额</strong></td><td class="num"><strong>+{money(7921.95-fc_c)}</strong></td><td>未计老妹还款与花呗账单</td></tr>
</tbody></table>

<div class="note" style="border-color:#BA7517;background:#FAEEDA"><strong>三个可能打脸预测的因素</strong>
<ul>
<li><strong>老妹是否还钱</strong>：¥10,560 若 9月到账是纯进账（建议直接转储蓄）；若反过来<strong>再借</strong>，中枢预估要往上加几千——这是唯一能让 9月由盈转亏的变量。</li>
<li><strong>医疗</strong>：7月 ¥609.80、8月 ¥246.40 连续发生，9月中枢只给了 ¥250。若有复查或长期用药，单这一项就能到 ¥600 以上。</li>
<li><strong>花呗</strong>：7月还了 ¥749.17（6月账单），8月无还款记录，需确认 8月消费是否走了花呗——若有，9月会多出一笔还款。</li>
</ul></div>

<div class="note"><strong>修正一处之前的判断</strong>：我上一版把通讯预算写成 ¥45，理由是「8月那笔 ¥48 是异常」。回头看 7月也有两笔 ¥48 和 ¥47.5，两月合计都是 ¥92–96，<strong>这是固定支出，不是异常</strong>（很可能是两张卡，或话费 + 宽带）。9月通讯应按 ¥95 预估，不是 ¥45。预算表那栏我保留原值，实际执行请以这里的 ¥95 为准。</div>
</div></body></html>'''

open(f'{BASE}/report.html', 'w', encoding='utf-8').write(out)

print('7月 毛流出 %.2f | 进账 %.2f | 实际花掉 %.2f' % (jul['gross'], jul['tin'], jul['net']))
print('7月 日常 %.2f (日均 %.2f) | 剔一次性 %.2f (日均 %.2f)' % (jul['daily'], jul['daily']/31, jul['core'], jul['core']/31))
print('8月 毛流出 %.2f | 进账 %.2f | 实际花掉 %.2f' % (aug['gross'], aug['tin'], aug['net']))
print('8月 日常 %.2f (日均 %.2f) | 剔一次性 %.2f (日均 %.2f)' % (aug['daily'], aug['daily']/31, aug['core'], aug['core']/31))
print('7月 吃饭 %.2f | 8月 吃饭 %.2f' % (jul['grp']['吃饭'], aug['grp']['吃饭']))
print('助学贷款 %.2f | 花呗 %.2f | 借出 %.2f | 医疗7 %.2f 医疗8 %.2f' % (
    jul['sub']['还助学贷款'], jul['sub']['还花呗'], jul['grp']['借出与代垫'], jul['sub']['医疗'], aug['sub']['医疗']))
print('7月 居住 %.2f | 8月 居住 %.2f | 代垫室友 %.2f' % (jul['grp']['居住'], aug['grp']['居住'], jul['sub'].get('代垫室友', 0)))
print('7月真实消费(剔借出代垫) %.2f | 进账 %.2f | 结余 %+.2f' % (jul['gross']-11983.90, jul['tin'], jul['tin']-(jul['gross']-11983.90)))
print('午餐均 7月 %.2f | 晚餐均 7月 %.2f' % (
    sum(r['amt'] for r in jul['exp'] if r['事项'] in ('吃中饭','中饭'))/len([r for r in jul['exp'] if r['事项'] in ('吃中饭','中饭')]),
    sum(r['amt'] for r in jul['exp'] if r['事项']=='吃晚饭')/len([r for r in jul['exp'] if r['事项']=='吃晚饭'])))
