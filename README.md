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

## 当前限制

本地相似度不是物体身份判定，背景变化会影响分数；当前没有上传图片到互联网进行像素反搜。宿主搜索工具须实际可用；独立命令不代替搜索工具。官方 YouTube API 路线的账号与额度仍未实测。

## 验证与使用注意

```sh
python -m unittest discover -s tests -v
```

测试覆盖被断言的离线行为，不等于真实平台、生产模型或业务效果验证。

live-search-candidates.json 记录本次公开网络检索的候选链接，标题取自检索结果，内容与同款未核实；其他示例为合成演示，不代表客户、交易或销量。不要提交真实凭据和私有输入。

## 来源与工作记录

由 miaorrr8888-cloud 在 AI 辅助下积累和维护，来源与边界见 [PROVENANCE.md](PROVENANCE.md)，许可见 [LICENSE](LICENSE)。

[全部独立技能与阶段性工作记录](https://github.com/miaorrr8888-cloud/agent-skills-worklog)

## 第二轮：官方视频检索入口

新增 YouTube 官方检索适配器，输出可直接交给排序器；也支持离线导入 API 响应，无播放量时保持未知。

在仓库根目录运行：

```sh
python scripts/search_youtube.py --query "synthetic product" --response examples/youtube-response.json
# 实时检索会消耗官方额度，先在本机配置 YOUTUBE_API_KEY，再明确加 --live。
# python scripts/search_youtube.py --query "brand model" --live --limit 10
```

新增工具的输入字段见脚本参数与 examples/。快照示例采用固定日期，过期后正常返回 HOLD；需要检查新采集的页面时填写真实带时区的采集时间，不要改日期伪装新证据。

## 接入依据

[YouTube 官方 search.list 文档](https://developers.google.com/youtube/v3/docs/search/list)。实时模式只发一页请求，不自动翻页或重试；账号与额度错误应停止。

## 第三轮：本地以图找图与免密钥检索路线

新增本地图片检索，用形状哈希和颜色分布排序；已用真实生成的参考图找出换场景版本。增加使用宿主搜索工具获取真实公开视频候选的路线，无需为该路线提供 YouTube API 密钥。

```sh
python -m pip install -r requirements-images.txt
python scripts/search_local_images.py examples/image-search/anchor.png examples/image-search
python scripts/extract_and_rank.py examples/live-search-candidates.json --json --as-of 2026-10-15T00:00:00Z
```
