# product-video-reverse-search

> Packaged by the WorkBuddy History Audit (2026-10-14). Source copied verbatim from the
> original location; **no modifications made to the original project**.

## 功能介绍
商品反查带货视频。输入商品图片或 1688 链接，自动提取商品属性，跨抖音/TikTok/YouTube 搜索相关带货视频，区分「确认同款/相似参考」，筛选最优 2-5 条并给出匹配依据、可借鉴开头、展示场景、卖点与不足。免费、无需付费 API Key、不编造数据（缺失标 UNKNOWN）。

## 起源与许可
- 类型: 用户原创 Skill (agent_created)
- 许可: MIT (见 LICENSE)
- 是否含密钥/Token: 否 (已通过审计扫描)

## 目录内容
- `SKILL.md` / `README.md` — 技能定义与使用说明
- 脚本与测试 — 见各子目录
- `LICENSE` — MIT

## 发布前检查清单
- [x] 无硬编码密钥 / Cookie / Token
- [x] 依赖清楚 (stdlib-only 或显式声明)
- [x] 含使用说明
- [ ] 作者补充中文/英文双语 README
- [ ] 补充 CI 测试 (如适用)

## Verified scope
This package does not establish current platform availability, demand, sales or permission to contact people.
Ranking is a heuristic applied to supplied evidence, not independent verification.
Use authorized sources; live platform access and outreach were not tested.

## 独立仓库

本仓库只包含 product-video-reverse-search 一个技能。
源码目录、SKILL.md、许可和相关测试均可独立取得，不依赖其他技能仓库。
工作记录与其他技能入口：[agent-skills-worklog](https://github.com/miaorrr8888-cloud/agent-skills-worklog)。

离线验证：`python -m unittest discover -s tests -v`。
