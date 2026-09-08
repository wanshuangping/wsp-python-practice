import csv, html, json, re
from collections import defaultdict

BASE = '/Users/temu/WorkBuddy/2026-08-31-20-06-09/ledger'
rows = list(csv.DictReader(open(f'{BASE}/august.csv', encoding='utf-8-sig')))
for r in rows:
    r['day'] = int(re.match(r'8月(\d+)日', r['日期']).group(1))
    r['amt'] = float(r['花费'])

income_items = {'欧阳还钱', '老妹转账', '兼职', '小红包'}

def cat(item):
    if item in income_items: return '收入'
    if '榴莲' in item or '水果' in item: return '水果'
    if '辣条' in item or item == '买水': return '零食饮料'
    if '买菜' in item or '鸡蛋' in item: return '买菜食材'
    if item.startswith('吃') or '糖水' in item: return '正餐外卖'
    if '地铁' in item: return '交通-地铁'
    if '电驴' in item: return '交通-电驴'
    if '话费' in item: return '通讯'
    if '社康' in item: return '医疗'
    if item == '交房租': return '房租'
    if item in ('奶奶过生日', '给倩买花'): return '人情礼物'
    if item in ('射箭', '打牌输钱'): return '娱乐'
    if item in ('四级邮寄费', '蜂巢快递费'): return '杂项'
    if item in ('买地垫', '买锯子'): return '家居日用'
    return '购物'

for r in rows:
    r['cat'] = cat(r['事项'])

COLOR = {'正餐外卖': '#D85A30', '水果': '#EF9F27', '买菜食材': '#F5C4B3', '零食饮料': '#F0997B',
         '房租': '#534AB7', '家居日用': '#AFA9EC', '人情礼物': '#D4537E', '购物': '#BA7517',
         '医疗': '#E24B4A', '交通-地铁': '#378ADD', '交通-电驴': '#85B7EB', '通讯': '#888780',
         '娱乐': '#1D9E75', '杂项': '#B4B2A9', '收入': '#639922'}
GMAP = {'正餐外卖': '吃饭', '买菜食材': '吃饭', '水果': '吃饭', '零食饮料': '吃饭',
        '交通-地铁': '交通', '交通-电驴': '交通', '房租': '居住', '家居日用': '居住'}

exp = [r for r in rows if r['amt'] > 0]
inc = [r for r in rows if r['amt'] < 0]
total = sum(r['amt'] for r in exp)
tin = -sum(r['amt'] for r in inc)

sub = defaultdict(float)
for r in exp: sub[r['cat']] += r['amt']
grp = defaultdict(float)
for c, v in sub.items(): grp[GMAP.get(c, c)] += v
sub = dict(sorted(sub.items(), key=lambda kv: -kv[1]))
grp = dict(sorted(grp.items(), key=lambda kv: -kv[1]))

byday = defaultdict(float); dayinc = defaultdict(float)
for r in exp: byday[r['day']] += r['amt']
for r in inc: dayinc[r['day']] += -r['amt']

def money(v): return '{:,.2f}'.format(v)

rows_html = []
for r in rows:
    pos = r['amt'] > 0
    rows_html.append(
        f'<tr class="{"inc" if not pos else ""}"><td>8月{r["day"]}日</td><td>{html.escape(r["事项"])}</td>'
        f'<td><span class="tag" style="background:{COLOR.get(r["cat"],"#888")}1a;color:{COLOR.get(r["cat"],"#5F5E5A")};border-color:{COLOR.get(r["cat"],"#888")}55">{r["cat"]}</span></td>'
        f'<td class="num">{money(abs(r["amt"]))}</td></tr>')

grp_html = ''.join(
    f'<tr><td>{k}</td><td class="num">{money(v)}</td><td class="num">{v/total*100:.1f}%</td>'
    f'<td><div class="bar"><i style="width:{v/max(grp.values())*100:.1f}%;background:{COLOR.get(k,"#85B7EB")}"></i></div></td></tr>'
    for k, v in grp.items())

sub_html = ''.join(
    f'<tr><td>{k}</td><td class="num">{money(v)}</td><td class="num">{v/total*100:.1f}%</td>'
    f'<td class="num">{money(v/len([r for r in exp if r["cat"]==k]))}</td></tr>'
    for k, v in sub.items())

day_html = ''.join(
    f'<tr><td>8月{d}日</td><td class="num">{money(byday[d])}</td><td class="num">{"+"+money(dayinc[d]) if dayinc[d] else "—"}</td>'
    f'<td><div class="bar sm"><i style="width:{byday[d]/max(byday.values())*100:.1f}%;background:{"#D85A30" if byday[d]>300 else "#85B7EB"}"></i></div></td></tr>'
    for d in range(1, 32))

big = sorted(exp, key=lambda r: -r['amt'])[:10]
big_html = ''.join(f'<tr><td>8月{r["day"]}日</td><td>{html.escape(r["事项"])}</td><td class="num">{money(r["amt"])}</td></tr>' for r in big)

html_out = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>8月账本 · 支出分析</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;padding:32px 24px 64px;background:#FAFAF8;color:#2C2C2A;
font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB",sans-serif;font-size:13px;line-height:1.6}}
.wrap{{max-width:960px;margin:0 auto}}
h1{{font-size:20px;font-weight:500;margin:0 0 4px}}
.sub{{color:#5F5E5A;margin:0 0 24px}}
h2{{font-size:15px;font-weight:500;margin:32px 0 12px}}
.cards{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}}
.card{{background:#fff;border:0.5px solid rgba(0,0,0,.12);border-radius:12px;padding:16px}}
.card .k{{color:#5F5E5A;font-size:12px}}
.card .v{{font-size:22px;font-weight:500;margin-top:4px;font-variant-numeric:tabular-nums}}
.card .n{{color:#5F5E5A;font-size:12px}}
table{{width:100%;border-collapse:collapse;background:#fff;border:0.5px solid rgba(0,0,0,.12);border-radius:12px;overflow:hidden}}
th,td{{padding:8px 12px;text-align:left;border-bottom:0.5px solid rgba(0,0,0,.06)}}
th{{background:#F1EFE8;color:#5F5E5A;font-weight:500;font-size:12px}}
tr:last-child td{{border-bottom:none}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
tr.inc td{{color:#3B6D11}}
.tag{{display:inline-block;padding:1px 8px;border-radius:20px;border:0.5px solid;font-size:11px}}
.bar{{height:8px;background:#F1EFE8;border-radius:4px;overflow:hidden}}
.bar i{{display:block;height:100%;border-radius:4px}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.note{{background:#fff;border:0.5px solid rgba(0,0,0,.12);border-radius:12px;padding:16px;color:#444441}}
.note li{{margin:4px 0}}
@media(max-width:700px){{.cards{{grid-template-columns:repeat(2,1fr)}}.grid2{{grid-template-columns:1fr}}}}
</style></head><body><div class="wrap">
<h1>8月账本 · 支出分析</h1>
<p class="sub">共 91 笔记录（支出 87 笔 / 进账 4 笔），覆盖 8月1日 – 8月31日。4 笔带负号的记录均为<strong>进账</strong>：欧阳还钱 200、老妹转账 520、兼职 200、小红包 0.18，已从毛流出中抵充。</p>

<div class="cards">
<div class="card" style="border:1px solid #534AB7"><div class="k">8月实际花掉</div><div class="v">¥{money(total-tin)}</div><div class="n">主口径 · 日均 ¥{(total-tin)/31:.2f}</div></div>
<div class="card"><div class="k">毛流出</div><div class="v">¥{money(total)}</div><div class="n">87 笔 · 日均 ¥{total/31:.2f}</div></div>
<div class="card"><div class="k">进账抵充</div><div class="v">−¥{money(tin)}</div><div class="n">还钱 + 转账 + 兼职 + 红包</div></div>
<div class="card"><div class="k">单笔中位数</div><div class="v">¥12.00</div><div class="n">典型一笔的金额</div></div>
</div>

<p class="sub" style="margin:16px 0 0">下面的占比与明细均基于<strong>毛流出 ¥{money(total)}</strong>统计；若按实际花掉 ¥{money(total-tin)} 计，吃饭占 {1261.81/(total-tin)*100:.1f}%、居住占 {grp["居住"]/(total-tin)*100:.1f}%、人情占 {grp["人情礼物"]/(total-tin)*100:.1f}%。</p>
<div class="card"><div class="k">单笔中位数</div><div class="v">¥12.00</div><div class="n">典型一笔的金额</div></div>
</div>

<h2>大类结构</h2>
<table><thead><tr><th>类别</th><th class="num">金额</th><th class="num">占比</th><th style="width:36%">分布</th></tr></thead><tbody>{grp_html}</tbody></table>

<div class="grid2">
<div>
<h2>细分科目</h2>
<table><thead><tr><th>科目</th><th class="num">金额</th><th class="num">占比</th><th class="num">笔均</th></tr></thead><tbody>{sub_html}</tbody></table>
</div>
<div>
<h2>单笔 TOP 10</h2>
<table><thead><tr><th>日期</th><th>事项</th><th class="num">金额</th></tr></thead><tbody>{big_html}</tbody></table>
</div>
</div>

<h2>逐日支出</h2>
<table><thead><tr><th>日期</th><th class="num">支出</th><th class="num">当日收入</th><th style="width:36%">分布</th></tr></thead><tbody>{day_html}</tbody></table>

<h2>全部明细</h2>
<table><thead><tr><th style="width:90px">日期</th><th>事项</th><th style="width:110px">分类</th><th class="num" style="width:100px">金额</th></tr></thead><tbody>{''.join(rows_html)}</tbody></table>

<h2>读出来的几件事</h2>
<div class="note"><ul>
<li>吃饭 ¥1,261.81（36.5%）是第一大头。其中正餐外卖 36 笔共 ¥918.68，午饭均价 ¥12.10、晚饭均价 ¥26.64——午饭控制得很好，晚饭是午饭的 2.2 倍。</li>
<li>水果 ¥248.46 里，榴莲就占 ¥172.23（3 次）。这一项弹性最大，砍一半能省 ¥86。</li>
<li>剔除一次性大额（房租 652 + 奶奶生日 400 + 社康 246.40 = ¥1,298.40）后，日常开销 ¥2,045.52，日均 ¥65.98——这才是 9 月该拿来当基准的数。</li>
<li>医疗 ¥246.40 集中在 8月25日一笔 ¥185，值得留意身体。</li>
<li>通讯 ¥92.74 中，8月27日一笔 ¥48 占了一半以上，其余都是几毛几块的零头。8月1日那笔 ¥37.47 也偏大。</li>
<li>四笔进账共 ¥920.18（欧阳还钱 200 + 老妹转账 520 + 兼职 200 + 红包 0.18）全部是一次性的，已从毛流出中抵充，得出 8 月实际花掉 ¥2,532.74。<strong>做 9 月预算时不要指望还有这 ¥920</strong>，基准应取日均 ¥65.98 的日常口径。</li>
</ul></div>
</div></body></html>'''

open(f'{BASE}/report.html', 'w', encoding='utf-8').write(html_out)
print('ok', len(html_out))
