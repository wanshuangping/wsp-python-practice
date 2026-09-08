import csv, json, re
from collections import defaultdict, OrderedDict

rows = list(csv.DictReader(open('/Users/temu/WorkBuddy/2026-08-31-20-06-09/ledger/august.csv', encoding='utf-8-sig')))
for r in rows:
    r['day'] = int(re.match(r'8月(\d+)日', r['日期']).group(1))
    r['amt'] = float(r['花费'])

income_items = {'欧阳还钱', '老妹转账', '兼职', '小红包'}

def cat(item, amt):
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
    if item in ('四级邮寄费', '蜂巢快递费'): return '杂项/手续费'
    if item in ('买地垫', '买锯子'): return '家居日用'
    return '购物'

for r in rows:
    r['cat'] = cat(r['事项'], r['花费'])

exp = [r for r in rows if r['amt'] > 0]
inc = [r for r in rows if r['amt'] < 0]
total_exp = sum(r['amt'] for r in exp)
total_inc = -sum(r['amt'] for r in inc)

by_cat = defaultdict(lambda: [0.0, 0])
for r in exp:
    by_cat[r['cat']][0] += r['amt']; by_cat[r['cat']][1] += 1
by_cat = OrderedDict(sorted(by_cat.items(), key=lambda kv: -kv[1][0]))

by_day = defaultdict(float)
for r in exp: by_day[r['day']] += r['amt']

big = sorted(exp, key=lambda r: -r['amt'])[:10]

# 大类合并
group = defaultdict(float)
gmap = {'正餐外卖':'吃饭','买菜食材':'吃饭','水果':'吃饭','零食饮料':'吃饭',
        '交通-地铁':'交通','交通-电驴':'交通','通讯':'通讯','医疗':'医疗','房租':'居住',
        '家居日用':'居住','人情礼物':'人情','娱乐':'娱乐','购物':'购物','杂项/手续费':'杂项'}
for c,(s,n) in by_cat.items(): group[gmap.get(c,c)] += s
group = OrderedDict(sorted(group.items(), key=lambda kv: -kv[1]))

days_with_spend = len(by_day)
print('笔数: %d (支出 %d / 收入 %d)' % (len(rows), len(exp), len(inc)))
print('总支出: %.2f' % total_exp)
print('总收入: %.2f' % total_inc)
print('净额: %.2f' % (total_exp - total_inc))
print('有支出天数: %d, 日均(有支出日): %.2f, 日均(31天): %.2f' % (days_with_spend, total_exp/days_with_spend, total_exp/31))
print()
print('--- 大类 ---')
for k,v in group.items(): print('%-8s %8.2f  %5.1f%%' % (k, v, v/total_exp*100))
print()
print('--- 细分 ---')
for k,(s,n) in by_cat.items(): print('%-12s %8.2f  %5.1f%%  %d笔  均%.2f' % (k, s, s/total_exp*100, n, s/n))
print()
print('--- 单笔 TOP10 ---')
for r in big: print('8月%d日 %-14s %8.2f' % (r['day'], r['事项'], r['amt']))
print()
print('--- 每日 ---')
for d in range(1,32):
    v = by_day.get(d, 0.0)
    inc_d = -sum(r['amt'] for r in inc if r['day']==d)
    print('8月%2d日 %8.2f %s' % (d, v, ('收%.2f'%inc_d) if inc_d else ''))

# 吃饭细分
eat = sum(v[0] for k,v in by_cat.items() if k in ('正餐外卖','买菜食材','水果','零食饮料'))
print()
print('吃饭合计 %.2f 占 %.1f%%' % (eat, eat/total_exp*100))

json.dump({
 'total_exp': round(total_exp,2), 'total_inc': round(total_inc,2),
 'net': round(total_exp-total_inc,2),
 'group': {k: round(v,2) for k,v in group.items()},
 'cat': {k: [round(v[0],2), v[1]] for k,v in by_cat.items()},
 'by_day': {str(d): round(by_day.get(d,0),2) for d in range(1,32)},
 'top': [[r['day'], r['事项'], r['amt']] for r in big],
 'count': len(rows), 'exp_count': len(exp),
}, open('/Users/temu/WorkBuddy/2026-08-31-20-06-09/ledger/summary.json','w'), ensure_ascii=False, indent=1)
