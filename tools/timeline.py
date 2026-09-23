#!/usr/bin/env python3
"""查一只 A 股的时间轴：过去发生过的关键事件，今后已经排定的日子。
用法：python3 timeline.py 600520
数据来自东方财富公开接口，只用标准库，不用装任何东西。抓取间隔 2.5—4 秒，别改快。"""
import json, random, re, sys, time, urllib.parse, urllib.request
from datetime import date

UA = {"User-Agent": "Mozilla/5.0", "Referer": "https://data.eastmoney.com/"}
KINDS = [("控制权", r"控制权|权益变动|收购报告书|股份转让|表决权|实际控制人|要约"),
         ("重组定增", r"重大资产|购买资产|吸收合并|向特定对象发行|非公开发行|重整|审核|注册|问询|上会|摘帽"),
         ("增减持", r"增持|减持|解除限售|上市流通"),
         ("激励回购", r"股权激励|员工持股|限制性股票|股票期权|回购"),
         ("风险", r"冻结|质押|诉讼|仲裁|立案|处罚|关注函|异常波动|风险提示|终止|中止")]
SKIP = r"法律意见|核查意见|独立董事.*(意见|声明)|提名人声明|候选人声明|摘要|英文|更正|持续督导|独立财务顾问|评估报告|审计报告|审阅报告|证券事务代表"

def get(url):
    time.sleep(random.uniform(2.5, 4))
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))

def kind_of(t):
    for k, p in KINDS:
        if re.search(p, t): return k
    return None

def past(code, years=2):
    since = f"{date.today().year - years}{str(date.today())[4:]}"
    out, seen = [], set()
    for page in (1, 2):
        try:
            lst = get(f"https://np-anotice-stock.eastmoney.com/api/security/ann?page_size=100&page_index={page}&ann_type=A&stock_list={code}")["data"]["list"]
        except Exception as e:
            print("公告接口取不到：", e); break
        for a in lst:
            d, t = a["notice_date"][:10], re.sub(r"^[^:：]{2,10}[:：]", "", a["title"])
            if d < since: return out
            if re.search(SKIP, t): continue
            k = kind_of(t)
            if k and (d, k) not in seen:
                seen.add((d, k)); out.append((d, k, t[:50]))
        if len(lst) < 100: break
    return out

def future(code):
    today = str(date.today())
    out = []
    try:
        flt = urllib.parse.quote(f'(SECURITY_CODE="{code}")')
        rows = (get(f"https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_LIFT_STAGE&columns=ALL&filter={flt}&pageSize=50&sortColumns=FREE_DATE&sortTypes=1").get("result") or {}).get("data") or []
        for r in rows:
            d = (r.get("FREE_DATE") or "")[:10]
            if d >= today:
                out.append((d, "解禁", f"{r.get('FREE_SHARES_TYPE','')}，占总股本 {round((r.get('TOTAL_RATIO') or 0)*100, 2)}%"))
    except Exception as e:
        print("解禁接口取不到：", e)
    y, md = int(today[:4]), today[5:]
    for cut, name in (("04-30", "年报法定截止"), ("08-31", "半年报法定截止"), ("10-31", "三季报法定截止")):
        if md <= cut:
            out.append((f"{y}-{cut}", "财报", name)); break
    else:
        out.append((f"{y+1}-04-30", "财报", "年报法定截止"))
    return sorted(out)

def main():
    if len(sys.argv) < 2:
        print("用法：python3 timeline.py 600520"); sys.exit(1)
    code = sys.argv[1].strip()
    print(f"\n=== {code} 时间轴 ===\n")
    f = future(code)
    print("【今后已排定的日子】")
    for d, k, t in f: print(f"  {d}  {k:<5}{t}")
    if not f: print("  （没查到）")
    print(f"\n----------- 今天 {date.today()} -----------\n")
    print("【过去两年的关键事件】")
    p = past(code)
    for d, k, t in p: print(f"  {d}  {k:<5}{t}")
    if not p: print("  （没查到）")
    print(f"\n共 {len(p)} 条过去事件、{len(f)} 条今后日程。公告原文去巨潮或交易所网站按标题搜。\n")

if __name__ == "__main__":
    main()
