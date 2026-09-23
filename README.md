# signal

A 股研究记录：每只票在等哪个公告、什么条件算看错、后来发生了什么。
台账页面：https://wwfemg.github.io/signal/
查一只票：https://wwfemg.github.io/signal/stock.html （输入代码看标签、时间轴、机构持仓、龙虎榜）

## 目录

```
index.html      台账页面（脚本生成，别手改）
data/           数据：台账 ledger.json、时间轴 timeline.json、机构持仓池 pool.json
tools/          命令行工具
docs/           投稿规矩 CONTRIBUTING.md、变更记录 CHANGELOG.md
assets/         页面样式
```

## 工具（不用装任何库，下载就能跑）

```
git clone https://github.com/wwfemg/signal.git
cd signal/tools
python3 timeline.py 600520     # 查一只票的时间轴
python3 unlock.py 001391       # 查一只票的解禁时间表
```

`timeline.py`：上面是今后排定的日子（解禁、财报法定截止），中间一条线是今天，
下面是过去两年的关键公告，分成控制权、重组定增、增减持、激励回购、风险五类。

`unlock.py`：列出每一批限售股什么时候解禁、占总股本多少、分别是谁的。
买之前看一眼，未来一年有大比例解禁的票，上面压着一批随时能卖的人。

解禁不等于马上卖。持股 5% 以上的股东要在集中竞价减持前 15 个交易日公告，
每人每 3 个月集中竞价不超过总股本 1%、大宗不超过 2%。真正要盯的是减持预披露公告。

## 台账

`data/ledger.json` 是台账数据，页面由它生成。每只票记五件事：进入视野的时间、触发它的事实
（必须有公告标题和日期）、在等哪个公告、什么条件算看错、后来发生了什么。

想加一只票或者补进展，看 [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)。不会用 Git 也可以开
一个 Issue 提名。

## 记录改过没有，自己可以查

这个仓库的每一次改动都留在 Git 里，谁改的、改了哪一行、什么时候改的，都能翻出来，
改不掉也删不掉。想核对某只票当初写的是什么：

```
git log --follow -p data/ledger.json      # 看台账每一次改动
git tag                              # 看有哪些季度快照
git show 2026Q3:data/ledger.json          # 看某个季度当时的原样
```

每季度打一个标签存档，看错的记录标成"作废"保留，不删。

## 变更记录

见 [docs/CHANGELOG.md](docs/CHANGELOG.md)。

## 说明

数据来自交易所和公司公告原文、十大流通股东名册、基金定期报告。
这里只是把公开信息摆出来，不构成投资建议。

MIT License
