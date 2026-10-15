#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商品反查带货视频 · 确定性打分排序脚本

输入: candidates.json
  {
    "product": {"brand":"", "model":"", "product_name":"", "appearance_features":[], "keywords":[]},
    "candidates": [
      {"source":"YouTube", "url":"https://...", "title":"...",
       "published":null, "views":null, "likes":null, "comments":null,
       "match_level":"confirmed|similar|unknown"}
    ]
  }

输出: Markdown 排名报告（stdout）

纪律: 只给真实传入的数据打分; 计数缺失(none)=UNKNOWN, 不编造, 不扣分(权重让渡)。
"""
import json
import sys
import math
from datetime import datetime, timezone


def norm(s):
    return (s or "").lower()


def keyword_overlap(product, title):
    """返回 (重合率, 命中数, 总数)"""
    brand = norm(product.get("brand"))
    model = norm(product.get("model"))
    kws = [norm(k) for k in product.get("keywords", []) if k]
    t = norm(title)
    hits = 0
    total = 0
    if brand:
        total += 1
        if brand in t:
            hits += 1
    if model:
        total += 1
        if model in t:
            hits += 1
    for k in kws:
        if not k:
            continue
        total += 1
        if k in t:
            hits += 1
    return (hits / total) if total else 0.0, hits, total


MATCH_SCORE = {"confirmed": 1.0, "similar": 0.6, "unknown": 0.3}
SOURCE_CRED = {
    "YouTube": 0.90, "TikTok": 0.85, "Douyin": 0.90, "抖音": 0.90,
    "TikTok Shop": 0.80,
}


def recency_score(published):
    if not published:
        return None
    try:
        s = published.replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        days = max(0, (now - dt).days)
        return 0.5 ** (days / 180.0)  # 180 天半衰期
    except Exception:
        return None


def interaction_score(val):
    if val is None:
        return None
    try:
        v = float(val)
    except Exception:
        return None
    if not math.isfinite(v):
        return None
    if v <= 0:
        return 0.0
    return min(1.0, math.log10(v + 1) / 6.0)  # 1e6 播放≈满分


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("usage: extract_and_rank.py candidates.json\n")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)
    product = data.get("product", {})
    cands = data.get("candidates", [])

    results = []
    for c in cands:
        ov, hits, total = keyword_overlap(product, c.get("title", ""))
        match = c.get("match_level") or "unknown"
        mscore = MATCH_SCORE.get(match, 0.3)
        rec = recency_score(c.get("published"))
        inter = interaction_score(c.get("views"))
        cred = SOURCE_CRED.get(c.get("source", ""), 0.70)

        # 动态权重: 缺失项不扣分, 权重让渡给 match
        w = {"match": 0.40, "kw": 0.20, "inter": 0.20, "source": 0.10, "rec": 0.10}
        if inter is None:
            w["match"] += w.pop("inter")
        if rec is None:
            w["match"] += w.pop("rec")
        w_sum = sum(w.values())

        parts = {
            "match": mscore * w["match"],
            "kw": ov * w["kw"],
            "inter": (inter if inter is not None else 0.0) * w.get("inter", 0.0),
            "source": cred * w["source"],
            "rec": (rec if rec is not None else 0.0) * w.get("rec", 0.0),
        }
        total_score = sum(parts.values()) / w_sum if w_sum else 0.0

        results.append({
            "url": c.get("url"),
            "title": c.get("title"),
            "source": c.get("source"),
            "match_level": match,
            "score": round(total_score, 3),
            "keyword_overlap": round(ov, 3),
            "interaction_known": inter is not None,
            "recency_known": rec is not None,
            "views": c.get("views"),
            "likes": c.get("likes"),
            "comments": c.get("comments"),
            "published": c.get("published"),
        })

    results.sort(key=lambda r: r["score"], reverse=True)

    lines = ["# 商品反查带货视频 · 排序报告", ""]
    pname = " ".join(filter(None, [product.get("product_name", ""),
                                    product.get("brand", ""), product.get("model", "")])).strip()
    lines.append(f"商品：{pname or 'UNKNOWN'}")
    lines.append(f"候选数：{len(results)} ｜ 展示 Top {min(5, len(results))}")
    lines.append("")
    for i, r in enumerate(results[:5], 1):
        lines.append(f"## 第 {i} 名 · 得分 {r['score']}")
        lines.append(f"- 来源：{r['source']} ｜ 匹配：{r['match_level']}")
        lines.append(f"- 标题：{r['title']}")
        lines.append(f"- 链接：{r['url']}")
        lines.append(f"- 发布：{r['published'] or 'UNKNOWN'}")
        views = r['views'] if r['views'] is not None else 'UNKNOWN'
        likes = r['likes'] if r['likes'] is not None else 'UNKNOWN'
        comments = r['comments'] if r['comments'] is not None else 'UNKNOWN'
        lines.append(f"- 播放：{views} ｜ 点赞：{likes} ｜ 评论：{comments}")
        lines.append(f"- 关键词重合率：{r['keyword_overlap']} ｜ 互动量已核实：{r['interaction_known']} ｜ 时效已核实：{r['recency_known']}")
        lines.append("")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
