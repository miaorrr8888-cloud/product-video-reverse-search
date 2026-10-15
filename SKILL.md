---
name: product-video-reverse-search
description: 从商品信息检索相关视频并对用户提供的候选证据做排序，区分同款声明、相似和未知。
license: MIT
---

# 商品相关视频检索与排序

先记录品牌、型号、外观特征和检索关键词。用当前可用的搜索工具或用户提供的链接取得候选；不假设旧接口或第三方免费额度仍可用。

逐项核对型号、外观与原页面；只在证据足够时把 match_level 设为 confirmed，否则为 similar 或 unknown。该字段由调用者判断，排序器不会独立识别同款。

`python scripts/extract_and_rank.py candidates.json` 输出前五名 Markdown。输入为 product 对象与 candidates 数组，字段见脚本文件顶部说明。匹配、关键词、互动、来源和日期是启发式权重，来源权重是内部假设。

计数与时间缺失保留 UNKNOWN，非有限数值不作为已知播放量。脚本不会访问链接、核实计数或判断交易销量。排序得分不是成交、需求或内容质量证明。

输出真实链接、匹配依据、缺失项和可借鉴内容。下载、重用视频和对外发布需符合来源许可与用户授权，不购买服务或绕过访问限制。
