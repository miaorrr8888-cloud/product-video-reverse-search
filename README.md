# 商品相关视频候选排序

`product-video-reverse-search` · 独立技能仓库 · MIT

适合：找商品内容参考的商家、剪辑师、研究人员

## 解决什么问题

对已经取得的视频候选排出优先查看顺序，说明分数来自哪些字段，减少盲目翻找。

## 快速开始

Python 3.10+，标准库。

在本仓库根目录运行：

```sh
python scripts/extract_and_rank.py examples/candidates.json --as-of 2026-10-15T00:00:00Z
python scripts/extract_and_rank.py examples/candidates.json --as-of 2026-10-15T00:00:00Z --json
```

## 输入与输出

**输入**：product 对象和 candidates 数组，字段及含义见 examples/candidates.json。使用自己有权整理的数据。

**输出**：前五名 Markdown 或完整 JSON，含去重数、权重、各项分数和 SUPPLIED_UNVERIFIED 标记。

## 本次完善

原有缺口：名称容易让人误以为自带搜全网和视觉同款识别；缺去重与可复现评分时间。

已补：补输入校验、跟踪参数去重、固定 --as-of 时间、JSON 分数构成；无效计数和未来日期保留未知；明确输入数据未被独立核实。

## 仍然缺什么

脚本不执行网络反向搜索或图片匹配；confirmed 由输入声明。来源权重是内部假设，分数不等于销量、热度真实性或版权许可。

## 验证与使用注意

```sh
python -m unittest discover -s tests -v
```

测试覆盖被断言的离线行为，不等于真实平台、生产模型或业务效果验证。

示例数据和图片均为合成演示，不是真实客户、交易、销量或模型成绩。不要提交真实凭据和私有输入。

## 来源与工作记录

由 miaorrr8888-cloud 在 AI 辅助下积累和维护，来源与边界见 [PROVENANCE.md](PROVENANCE.md)，许可见 [LICENSE](LICENSE)。

[全部独立技能与阶段性工作记录](https://github.com/miaorrr8888-cloud/agent-skills-worklog)
