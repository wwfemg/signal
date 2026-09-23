#!/usr/bin/env python3
"""查一只 A 股的解禁时间表：哪天解禁、解多少、占总股本多少、是谁的股份。
用法：python3 unlock.py 001391
买之前先看这张表。未来一年有大比例解禁的票，上面压着一批随时能卖的人。"""
import json, sys, urllib.parse, urllib.request
from datetime import date

UA = {"User-Agent": "Mozilla/5.0", "Referer": "https://data.eastmoney.com/"}

def get(rep, code):
    flt = urllib.parse.quote(f'(SECURITY_CODE="{code}")')
    u = (f"https://datacenter-web.eastmoney.com/api/data/v1/get?reportName={rep}"
         f"&columns=ALL&filter={flt}&pageSize=100&sortColumns=FREE_DATE&sortTypes=1")
    with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25) as r:
        d = json.loads(r.read().decode("utf-8", "ignore"))
    return (d.get("result") or {}).get("data") or []

def main():
    if len(sys.argv) < 2:
        print("用法：python3 unlock.py 001391"); sys.exit(1)
    code = sys.argv[1].strip()
    today = str(date.today())
    stages, holders = get("RPT_LIFT_STAGE", code), get("RPT_LIFT_GD", code)
    if not stages:
        print("没查到解禁数据（可能是老股，限售股早已全部解禁）"); return
    by_date = {}
    for h in holders:
        by_date.setdefault((h.get("FREE_DATE") or "")[:10], []).append(
            (h.get("LIMITED_HOLDER_NAME") or "", h.get("ADD_LISTING_SHARES") or 0))
    print(f"\n=== {code} 解禁时间表 ===\n")
    ahead = 0
    for s in stages:
        d = (s.get("FREE_DATE") or "")[:10]
        ratio = round((s.get("TOTAL_RATIO") or 0) * 100, 2)
        past = d < today
        if not past: ahead += ratio
        print(f"{'已解禁' if past else '未解禁'}  {d}  占总股本 {ratio:>5}%  {s.get('FREE_SHARES_TYPE','')}"
              f"  解禁 {round((s.get('ABLE_FREE_SHARES') or 0)/10000, 2)} 亿股")
        for name, sh in sorted(by_date.get(d, []), key=lambda x: -x[1])[:8]:
            print(f"        └ {name}  {round(sh/1e8, 2)} 亿股")
    print(f"\n今后还有 {round(ahead, 2)}% 的股份要解禁。")
    print("提示：解禁不等于马上卖。持股 5% 以上的股东要在集中竞价减持前 15 个交易日公告，")
    print("      每人每 3 个月集中竞价不超过总股本 1%、大宗不超过 2%。盯减持预披露公告。\n")

if __name__ == "__main__":
    main()
