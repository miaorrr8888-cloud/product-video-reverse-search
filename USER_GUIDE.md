# 相似图片与视频候选整理：用户使用指南

## 它能帮你做什么

在本地图片中按简单形状与颜色特征排序；对视频候选去重并解释分数。宿主有搜索工具时，可先取得真实候选再整理。

## 适合谁

需要查找素材参考的商家、剪辑师、内容研究人员。

## 具体解决什么问题

已有一批图片或视频链接，难以知道先看哪个，也容易把相似商品当成同款。

**不适合这些目标：**互联网像素级反向搜图、自动认定同款、证明播放量真实或证明有权重用视频。

## 下载与准备

- [打开独立仓库](https://github.com/miaorrr8888-cloud/product-video-reverse-search)
- [直接下载源码ZIP](https://github.com/miaorrr8888-cloud/product-video-reverse-search/archive/refs/heads/main.zip)

也可在仓库页面点 Code → Download ZIP。解压后打开包含 SKILL.md、README.md、USER_GUIDE.md 的那层文件夹。不要停在外层目录或只复制一个脚本。

建议使用Windows电脑和Python 3.12；这是本次验证环境。先在该文件夹打开PowerShell，再执行：

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe --version
```

这里直接使用虚拟环境里的Python，不需要运行激活脚本或修改系统执行策略。安装步骤及其他系统说明见[通用安装说明](https://github.com/miaorrr8888-cloud/agent-skills-worklog/blob/main/INSTALLATION.md)。

安装本示例需要的依赖：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-images.txt
```

## 第一次使用：先跑自带示例

用生成的杯子参考图查本地候选，再查看公开检索得到的两个视频链接怎样排序；两条结果都保留未知匹配身份。

```powershell
.\.venv\Scripts\python.exe scripts/search_local_images.py examples/image-search/anchor.png examples/image-search
.\.venv\Scripts\python.exe scripts/extract_and_rank.py examples/live-search-candidates.json --json --as-of 2026-10-15T00:00:00Z
```

## 结果怎么看

图片检索输出排序与 identity_verified=false；视频输出权重、分数构成和 content_verified=false。分数不是成交量、真实性或版权结论。

## 换成自己的资料

一张本地参考图和候选目录，或带 product、candidates 的JSON；候选填真实链接，缺播放量保留null。

先用自己的参考图和有权处理的本地素材做小样。要获取视频，让宿主实际搜索品牌型号并记录返回链接，再交给排序器；不要编造指标。

## 不想手动敲命令：给AI助手的任务

以下任务适用于能读取所选目录、执行本地命令的助手。WorkBuddy需要先确认当前版本的权限与技能启用状态；本项目未完成WorkBuddy实际导入验收。

```text
请先读取我选定文件夹中的 SKILL.md 和 USER_GUIDE.md，只在该项目范围内处理。
运行自带本地图片检索和视频候选排序，用中文解释分数与未知项。如果你有搜索工具，可另行搜索我指定的品牌型号并保留真实URL；没有工具就明确告知。不要声称已完成互联网像素反搜或同款验证。
缺少依赖时先说明用途，优先放进本项目虚拟环境；不要读取其他目录中的密码、密钥或浏览器登录数据。
```

## 常见问题

**同一物体换背景后分数下降**

这是简单相似度工具的已知局限；按型号和关键外观人工确认，不能只凭分数判断。

**没有YouTube API密钥**

先使用本地演示或宿主已有的搜索工具；不要把任何密钥发进聊天或写进公开输入文件。

**找不到文件或脚本**

确认终端当前目录就是包含SKILL.md的技能根目录；路径含空格时加双引号。输出目录已存在时换新名字，不覆盖已有结果。

## 当前能力边界

本地图片排序受背景和颜色影响，不是物体身份识别。官方YouTube API的--live路线需额外权限和额度，当前未进行真实账号测试。

## 验证范围

本指南示例已在Windows独立副本中运行复核，见[命令复核结果](https://github.com/miaorrr8888-cloud/agent-skills-worklog/blob/main/USER_GUIDES_VERIFICATION.md)。已有回归测试只覆盖被测试行为，不证明真实业务结果。WorkBuddy实际运行、手机端使用和所有系统版本均不在本次已验证范围内。

许可证和素材来源分别见 [LICENSE](LICENSE)、[PROVENANCE.md](PROVENANCE.md)。
