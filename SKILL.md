---
name: hailuo-director-prompt
description: "海螺导演台(MiniMax-H3)视频生成提示词工程：多模态参考生成、视频编辑、视觉换皮、首尾帧图生视频、文生视频，覆盖产品电商/品牌时尚/剧情短剧/动作游戏/硬件工业/动画风格化/MV/Vlog等题材，含结构化字段模板、素材职责分配、文字品牌UI控制、机械校验"
version: 2.1.0
author: GK
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [video-generation, prompt-engineering, hailuo, media]
    category: media
---

# Hailuo Director Prompt Engineering

为海螺导演台视频生成工作流生成结构化提示词。

## ⚠️ 提示词修改铁律：不要过度修正

GK 反复纠正的行为模式（2026-09-11 原话："我就怕你这样，我让你干点啥你就极端的很"）：

- 当 GK 说"因素太多""掺着因素太多"时，**不是让你砍台词、砍 Shot、砍六段格式**。是指提示词里加了太多自作主张的额外内容（主观渲染、世界观补丁、丰富版剧本等）
- **六段格式（subject_definitions / summary / retention_analysis / detailed_description / overall_soundscape / non_diegetic_music）是官方规范，必须完整保留**，不要"精简"掉
- **台词只增不减**，Shot 数量和时间轴不砍
- GK 原话："最开始弄的就挺好的，越弄越垃圾"——意思是第一版通常就够了，后续反复改往往越改越差
- 正确做法：保留第一版的结构和内容，只做 GK 明确要求的具体改动，不要自作主张大改

## ⚠️ 先看再提交

GK 2026-09-11 原话："先发我看看，再提交"。

- 串行 clip 续接场景中，每个 clip 跑完后先发微信版给 GK 看效果，确认 OK 后再提交下一个 clip
- 不要自动连续提交——即使尾帧已截好、提示词已写好，也要等 GK 确认
- GK 看完可能要改提示词、改场景、改台词，自动提交会浪费积分

## ⚠️ 台词和表演要生动不要死板

GK 2026-09-11 原话："不够生动""说台词生动一点别太死"。

- 角色说话时要有**肢体动作和表情变化**配合，不能只写"XX says, <d>...</d>"
- 例：姜子牙问父亲渊源时应该"stops reading, looks up from the resume for the first time, his eyes meeting Subject 2's across the table, his tone shifts — no longer flat paperwork-reading, now a real question"
- 例：伯邑考说"我父亲跟纣王……"应该"opens his mouth, starts — then stops. A full second of silence. His eyes drop to the table, then come back up."停顿一秒后再说后半句
- 台词中间可以拆开加动作和停顿，不要一口气念完
- 角色说话方式要有变化：从"flat paperwork-reading voice"到"real question"的语气转变

## ⚠️ 给 GK 交付 curl 命令的格式

GK 在聊天里无法复制超长命令（2026-09-11 原话："你这么发太长了 我没法复制"）。规则：

- **写完整 curl 命令到单个 txt 文件，用 MEDIA: 发给 GK**，不在 chat 里贴长命令
- 不截断、不 placeholder、不省略
- JSON payload 含引号和特殊字符时用 heredoc 包裹避免 shell 转义问题：`curl ... -d @- <<'ENDOFJSON'`
- 写完后自己用 `bash file.txt` 验证能跑通再发

## ⚠️ RunningHub 查询接口（踩过坑）

- 查询接口是 `/openapi/v2/query`，**不是** `/openapi/v2/getResults`
- 查询body只需要 `{"taskId": "xxx"}`，不需要 apiKey
- 查询结果状态是 `SUCCESS`/**`FAILED`**，**不是** `COMPLETED`
- 下载视频用 `curl -sL -o output.mp4 <url>` 即可，不需要 Authorization header

## ⚠️ RunningHub 工作流固定使用

固定用工作流 `2094671638389420033`（standard实例）。**不要用** `2098315416350314497`（新工作流，参考图用不上，字段结构不同会报错）也不要用 `2093898864557383681`（老9图plus版）。

节点结构：图片 35/41/42/43/44/36/37/38/39，提示词 84，秒数 74，宽高 56。不传音频节点。只需要上传实际参考图到前几个图片节点，其余节点不传即可。

## ⚠️ 尾帧续接截取正确方法

截取视频尾帧做续接时，**必须用 `-sseof`**：

```bash
ffmpeg -sseof -0.1 -i clip.mp4 -vframes 1 -q:v 2 -update 1 tail.png -y
```

不用 `-sseof` 的 `ffmpeg -vframes 1` 截的是**第一帧**不是尾帧。2026-09-11 实测：整个 poolcore clip3/clip4 链条用了错误的首帧当续接帧，空间过渡完全断裂，全部重跑。）

- 查询URL是 `https://www.runninghub.cn/openapi/v2/query`，**不是** `/openapi/v2/getResults`（后者返回1001 Invalid URL）
- 请求体只需要 `{"taskId": "xxx"}`，不需要 apiKey
- Header 需要 `Authorization: Bearer {API_KEY}`
- 成功状态是 `SUCCESS`（不是 `COMPLETED`），失败是 `FAILED`

## ⚠️ RunningHub 工作流选择

GK 明确指定（2026-09-11）：固定使用工作流 `2094671638389420033`（standard 实例）。
- **不要用** `2098315416350314497`（新工作流，有中文默认值校验问题，参考图效果差）
- **不要用** `2093898864557383681`（老9图plus版，除非 GK 明确要求 plus）
- 节点结构：图片 35/41/42/43/44/36/37/38/39（9个，只传实际参考图），提示词 84，秒数 74，宽高 56
- 不传音频节点
- 秒数传字符串 `"15"` 或整数 `15` 都行

## ⚠️ 台词要生动，别太死

GK 原话（2026-09-11）：\"说台词生动一点别太死\"。规则：

- 每句台词要带**具体动作和情绪节拍**，不要只写 \"says X\"
- 例如：不要写 `<Subject 2> responds, <d>我父亲跟纣王……有过一些业务往来。</d>`
- 要写：`<Subject 2> meets <Subject 1>'s gaze. He opens his mouth, starts, <d>我父亲跟纣王……</d> — then stops. A full second of silence. His eyes drop to the table, then come back up. He finishes, quieter, <d>有过一些业务往来。</d>`
- 台词中间可以有停顿、动作描写（眼神移动、身体姿态变化）
- GK 会给具体导演指令（\"姜子牙看向伯邑考\"\"停顿一秒\"\"说来话长\"），按指令改，不自作主张

## ⚠️ 镜头切换跟着说话人走

GK 原话（2026-09-11）：\"我父亲和纣王有一些业务往来，写个镜头特写应该在伯邑考这\"

- 谁说台词，镜头就给谁
- 如果一问一答，用硬切在两人之间切换
- push-in 用于强调提问方的压迫感，hard cut 到 close-up 用于回答方的情绪反应

## ⚠️ 剧本原文是唯一权威

GK 会直接贴原版剧本让你按着写。规则：
- **以 GK 贴的原文为准**，不从记忆概括，不从之前版本继承
- 台词一字不改，只增不减
- 如果原版台词和之前版本的提示词有出入，以原版为准
- GK 可能会在原版基础上即兴改台词（如\"后来闹翻了\"→\"说来话长。反正最后闹翻了\"），按他改的来

## ⚠️ RunningHub API 鉴权要求

- **Authorization: Bearer header 是强制的**，不是可选的。只在 JSON body 里放 `apiKey` 会返回 `{"code":1602,"msg":"HEADER_API_KEY_NOT_FOUND"}`
- 所有接口（提交、查询、上传）都需要 `-H "Authorization: Bearer YOUR_API_KEY"`
- 查询接口 `/openapi/v2/query` 的 body 只需 `{"taskId":"..."}`，不需要 apiKey 字段

## 读取规则

开始生成前读取 [official-rules.md](references/official-rules.md) 确认模型边界和硬限制。全参考模式格式细节查阅 [ref-mode-guide.md](references/ref-mode-guide.md)（官方 Full-Reference Mode Rewrite Output Format Guide）。遇到精准编辑、视觉换皮或多素材复杂分镜时，再读取 [editing-guide.md](references/editing-guide.md) 和 [genre-guide.md](references/genre-guide.md)。通过 RunningHub API 远程调用工作流时，读取 [runninghub-api.md](references/runninghub-api.md)（接口文档、nodeInfoList 传参格式、pitfalls、Python 调用模板）和 [runninghub-node-management.md](references/runninghub-node-management.md)（节点禁用限制与占位图策略、三个工作流版本对比、方案A/B/C）。**唯一推荐工作流：None 默认版 `2094671638389420033`（standard，用几张传几张，无OOM风险）。** ~~2098315416350314497~~ 和 ~~2093898864557383681~~ 已弃用（前者节点结构不同且不稳定，后者需占位图+plus浪费积分）。完整节点映射、提交模板和脚本清单见 [runninghub-workflow-9img-2093898864557383681.md](references/runninghub-workflow-9img-2093898864557383681.md)——API 提交前先读这份，避免重新探测节点。1638389420033（9图+3音频槽全开，默认值全None，用几张传几张，不需要占位图/音频/视频，详见同一参考文件的"None默认版"章节）。** **严禁向节点31传真实视频做尾帧衔接或站位参考——会花屏/乱码。** 尾帧衔接只能用提取的单张图片走 ref_image 通道（pitfall 67）。9图版工作流（2093898864557383681）传真实视频到节点31会花屏（实测），传占位视频可正常工作但不如None默认版。 GK 要求"批量重新生成所有 clip 并拼接"时，使用 [batch_generate.py](templates/batch_generate.py) 模板（必须用 delegate_task 后台运行）。不要读取与当前任务无关的参考内容。

## 能力路由

海螺导演台支持四种生成方式，按以下顺序判断用哪种：

1. **视频编辑**：GK 要求修改已有视频（换人物/换产品/改场景/改声音）→ 读取 [editing-guide.md](references/editing-guide.md)，建立"保留/修改/删除/新增"变更清单。summary 用 `[video editing]` 任务类型。
2. **多模态参考生成**：GK 提供了参考图/视频/音频，需要控制人物、产品、动作、镜头或风格 → 本 skill 的默认主路径。summary 用 `[reference generation]` 任务类型。
3. **首尾帧图生视频**：GK 只提供 1—2 张首尾帧图片，要求固定起止画面 → summary 用 `[keyframe completion]` 任务类型，声明首帧/尾帧约束。
4. **文生视频**：无任何参考素材，纯文字描述 → 在 summary 中声明画幅，不使用 adaptive，不使用参考标签。

同一任务可叠加多个能力，summary 任务类型用 ` + ` 组合（如 `[video editing + audio reuse]`、`[video continuation + keyframe completion]`），不重复同一类型。

如需确定具体题材的emphasis，读取 [genre-guide.md](references/genre-guide.md)。

## 整体架构

提示词系统分两大块：
1. 公共参数 — 参考图片(≤9)、参考音频(≤3)、参考视频(≤3)，以及全局提示词框 subject_definitions
2. 素材 — 每个素材独立一个提示词框，生成一段0-15秒视频，可无限增加

### 配额共享

9图/3音/3视频是全局总池，公共参数和所有素材共用。素材内挂载的参考素材也算进这个池子。

## 参考标签系统

全参考模式使用四种标签标识参考内容来源和角色。标签一旦定义，在六段（subject_definitions、summary、retention_analysis、detailed_description、overall_soundscape、non_diegetic_music）中含义不变。

| 标签 | 含义 |
|------|------|
| `<Subject N>` | 从参考素材抽象的可重用可见内容（人/动物/物体/场景/服装/道具/风格/动作/表情/姿态），代表目标视频中实际使用的内容单元，不是源文件本身 |
| `<Picture N>` | 参考图作为具体帧锚点（首帧/关键帧/尾帧/编辑关键帧/构图锚点/故事板），引用图本身而非图中角色 |
| `<Video N>` | 参考视频的整体关系（编辑源/延续起点/整体时序结构/运镜/剪辑节奏），标识资产或结构来源，不替代 Subject 标签 |
| `<Audio N>` | 音频资产（复制全部或部分/参考音乐风格/参考音色/使用对白歌词/参考节拍节奏），独立编号，与 Video 编号不配对 |

### 标签使用规则

- 一个 Subject 可由多个参考素材定义，一个参考素材可提供多个 Subject
- 如果 `<Picture N>` 或 `<Video N>` 只是标识另一个参考项的来源且不会被单独分析，在该项定义中引用即可，不单独列行
- `<Video N>` 和 `<Audio N>` 独立编号，同一参考视频可对应 `<Video 1>` 和 `<Audio 2>`
- 普通参考视频不会仅因为含声音就自动产生 `<Audio N>`
- 当 `<Audio N>` 对应目标说话人时，在定义中复用该说话人的全局 ID：`<Subject N> (Sx)` 或稳定的声音描述 + `(Sx)`

### 多面板参考图的 Subject 拆分

当参考图是**多面板网格图**（如四宫格、六宫格，每格展示同一场景的不同状态或不同场景），必须为每个面板定义独立的 `<Subject N>`，不要合并、不要只定义整体 `<Picture N>`。

GK 两次纠正的原话：
- 第一次："为什么不用subject from picture这种格式？" — H 把四宫格整体当作单个 `<Picture 1>` 帧锚点，没有拆出 Subject
- 第二次："不是四宫格吗为什么你只subject了3个" — H 拆出了 Subject 但把"关门"和"开门"两个面板合并成一个 Subject

规则：
1. **N 个面板 = N 个 Subject**，即使两个面板是同一场景的不同状态（如同一扇门关门 vs 开门）。关门和开门是不同的视觉状态，各自独立锁定
2. **`<Picture N>` 保留为整体参考图定义**，说明各面板对应哪个 Subject
3. **retention_analysis 逐 Subject 标注**出现在哪些 Shot，每个 Subject 对应一个 Shot
4. 示例（四宫格：关门/开门/走廊/避难所）：

```
<Subject 1> is [场景] with [门关着的状态], from <Picture 1> top-left panel. [详细特征].
<Subject 2> is [场景] with [门开着的状态], from <Picture 1> top-right panel. [详细特征].
<Subject 3> is [场景], from <Picture 1> bottom-left panel. [详细特征].
<Subject 4> is [场景], from <Picture 1> bottom-right panel. [详细特征].
<Picture 1> is a 4-panel reference grid showing: top-left [概述], top-right [概述], bottom-left [概述], bottom-right [概述].
```

## 字段格式

### 公共参数提示词框

```
subject_definitions:
<Subject 1> is [角色描述] from <Picture 1>, with [详细外观特征].
<Subject 2> is [角色描述] whose appearance comes from <Picture 2> and whose walking motion comes from <Video 1>.
<Picture 3> is the first frame of [Shot 1], showing [画面内容].
<Video 1> is the source video for the target video edit.
<Audio 1> is the voice-timbre reference for <Subject 1> (S1).
```

### 素材提示词框

每个素材=一个独立提示词框=生成一段0-15秒视频。

```
summary:
[任务类型组合] 目标视频概述。使用已定义的 <Subject N>、<Picture N>、<Video N>、<Audio N> 标签描述主体、镜头流和参考素材角色。不在本段引入新标签。

retention_analysis:
<Subject N> (appears in [Shot 1], [Shot 2]): fully_preserved - [保留的特征].
<Subject N> (appears in [Shot 1]): partially_preserved - [保留和变化的特征].
<Picture N> ([Shot 1] first frame): fully_preserved - [保留内容].
<Video N> (cut and pacing structure): weak_reference - [参考关系].
<Audio N>: reference - [音频参考关系].

detailed_description:
[整体画风、光影、色调，1-2句英文，在 Shot 1 之前].
[Shot 1] [机位/景别] 建立场景：[环境、人物位置、动作]。[镜头运动]。[声音和对白].
[Shot 2] At 00:XX.XXX, [镜头运动/过渡]：[人物动作、面部表情].

overall_soundscape:
[全局环境音概述。逐 Shot 声音和对白留在 detailed_description 中].

non_diegetic_music:
[配乐风格、节奏、动态。无配乐写 N/A].
```

## 任务类型

summary 以方括号任务类型前缀开头，按实际参考关系选择：

| 任务类型 | 使用场景 |
|----------|----------|
| `keyframe completion` | 图片作为目标视频首帧/关键帧/尾帧/编辑关键帧/其他具体帧锚点 |
| `reference generation` | 图片/视频/音频提供人物/场景/风格/动作/运镜/故事板等生成引导，不作为具体帧或被编辑/延续的源视频 |
| `video editing` | 已有源视频被直接修改；编辑图片或在静态关键帧间生成不属于此类型 |
| `video continuation` | 新内容延续/扩展/恢复/过渡自已有源视频 |
| `audio reuse` | 同一音频信号全部或部分重用 |
| `audio reference` | 音频信号不被直接复制，仅参考其音乐风格/音色/对白内容/音效纹理/节拍/连续性 |

多关系组合用 ` + ` 连接，不重复类型。视频编辑且保留原音频时用 `[video editing + audio reuse]`。延续源视频但不直接复制音频时用 `[video continuation + audio reference]`。

视频仅提供运镜/剪辑/节奏时属于 `reference generation`，不用 `video editing` 或 `video continuation`。

视频编辑任务的 summary 在类型前缀后以 "The target video is an edited version of <Video N>." 开头。

## retention_analysis 关系标记

### 可见内容标记（Subject / Picture / Video）

| 标记 | 含义 |
|------|------|
| `fully_preserved` | 参考内容的定义角色被完整保留 |
| `partially_preserved` | 参考内容仍被使用，但部分特征被改变或仅部分保留 |
| `attribute_transfer` | 参考特征转移到另一个可识别的目标主体 |
| `weak_reference` | 仅保留风格/类别/构图/氛围的大致相似性 |

### 音频标记（Audio）

| 标记 | 含义 |
|------|------|
| `fully_copy` | 完整源音频作为目标视频完整最终音轨 |
| `partially_copy` | 仅复制部分时间线或选定音频层，或复制后增删替换其他声音 |
| `reference` | 不直接复制信号，仅参考音色/节奏/音乐风格/对白内容/音效纹理 |
| `weak_reference` | 仅保留类别或氛围的大致相似性 |

标记只能在 subject_definitions 中已定义的参考角色范围内选择。目标视频中新增的动作、背景或情节事件不算参考保真度损失。不在 retention_analysis 中写 `(Sx)`。

## detailed_description 格式

### 基本格式

- 正文用英文。对话、歌词和画面可见文字保留原文语言。
- `[Shot 1]` 标记开场镜头，无时间戳。后续镜头用 `[Shot N] At MM:SS.mmm, ...` 标记切换时间。
- 镜头运动用自然英文写在当前 Shot 中。
- 风格行：在 `[Shot 1]` 之前用1-2句英文建立整体画风/光影/色调。
- 生成任务通常 350-500 英文词。对白密集内容优先完整呈现时间线而非机械凑词数。

### 参考标签在 Shot 中的使用

- `<Subject N>` 首次出现时描述其参考特征、画面位置和当前动作，后续 Shot 中继续引用但不重新定义
- 具体帧锚点用自然表述：`the shot begins from <Picture 1>`、`the shot's keyframe corresponds to <Picture 2>`、`the shot ends on <Picture 3>`
- 编辑或延续原视频时，在源状态/结构/延续关系适用的位置引用 `<Video N>`
- 在音频关系生效的 Shot 中引用 `<Audio N>` 并声明是复制还是参考

### 说话人、音源和对白

给声源分配稳定的全局 ID `(S1)`、`(S2)`...，按目标视频中实际发声事件顺序分配一次，每个发声事件复用对应 ID。

对白和歌词格式：`<d>[Language] 台词原文</d>`

- 引用 Subject 说话时保留标签和说话人 ID：`<Subject 2> (S1) turns toward the woman and says, <d>[English] ...</d>`
- Subject 画外说话时保持同样格式并标注 `off-screen`
- 说话人不对应已定义 Subject 时，用稳定的声音描述 + `(Sx)`
- 直接重用参考音频中的对白/歌词时，在 `<d>` 中逐字保留原文和原语言
- 不清楚的片段写 `[unclear]`，不猜测
- 标准化标点为基本书面符号（`,` `.` `?` `!`），去除重复波浪号、emoji、项目符号和重复装饰性标点
- 仅参考音色/节奏/情感/演绎时，不将参考音频中的原对白带入目标视频
- 直接重用的 BGM 或完整音轨中的语言线索用 `<Audio N>` 作为声源，不额外发明 `(Sx)`；由具体人物/角色/旁白等独立声源产生的声音用 `(Sx)`

## 镜头指南

- 每个素材可含多个 [Shot N]
- 时间戳格式：At 00:03.500
- 优先软过渡而非硬切（如"镜头不硬切，继续慢速推近"）——但喜剧/活泼基调场景例外，密集硬切是节奏工具，见"喜剧快节奏场景"章节
- 镜头运动：Push In(缓推) / Arc Shot(弧线绕) / 固定停留 / Pull Out(缓拉) / Pan(摇) / Tilt(俯仰)
- 景别：远景 / 中远景 / 中景 / 中近景 / 近景 / 特写
- 每个 Shot 需描述：机位、景别、人物位置、动作、表情、光影细节、镜头运动

### 转场

优先描述触发物和切换时刻，不要只写"丝滑转场"：
- 遮挡转场：物体/人物运动到遮满画面时切场
- 甩动转场：快速 Pan 或 Tilt 产生模糊时切场
- 闪光转场：光效过曝瞬间切场
- 材质匹配：上一场景的纹理延续到下一场景
- 动作匹配：上下镜头的动势连贯（如推门→开门进入）
- UI 收拢：界面元素收缩聚拢后展开新场景
- 物体变形：道具形变中过渡
- 声音重拍：音频卡点时刻切场

一镜到底只用连续运动、遮挡和空间贯通，不写硬切或冲突机位跳变。

### 镜头兼容性

不要同时要求固定机位、环绕、快速推进和手持抖动，除非它们属于不同时间段。把摄影词绑定到主体行为：写"微距跟随瓶身冷凝水向下移动"而非"产品特写"；写"人物转身时镜头保持眼平并横向跟移"而非"电影级跟拍"。

## 参考图空间锚定原则

**参考图不只提供视觉内容——它锚定了模型的整个空间视角。提示词中所有动作必须发生在参考图所建立的空间框架内。**

这是本 skill 最重要的空间规则，违反时会导致物理逻辑崩坏——模型把跨空间动作强行塞回参考图空间内渲染。

### 核心规则

1. **参考图是室内场景 → 所有动作必须在室内框架内发生**。不要写"站在走廊推门进入"——模型没有走廊/门外的参考图，会从室内开门。
2. **参考图是室外场景 → 所有动作必须在室外框架内发生**。不要写"从室内走出来"——模型没有室内参考图。
3. **跨空间过渡（室内→室外）不能用连续运镜实现**。AI 做不了空间穿越。用硬切、尾帧承接、或"镜头拉到门口停住等角色走出来"（不穿门）。
4. **角色动作不能超出参考图空间**。如果参考图是桌面特写，不要写角色站起来走动；如果参考图是床，不要写角色走到窗边。

### 典型违反案例（GK 三次纠正）

**案例：clip09a 陆寒回出租屋，参考图是出租屋室内场景**

| 尝试 | 提示词写法 | 结果 | GK 反馈 |
|------|-----------|------|---------|
| 第1次 | "camera pulls back and scene transitions to restaurant entrance" | 室内→室外空间断裂 | "场景衔接不上" |
| 第2次 | "Lu Han steps outside first and stops on the sidewalk" | 赵磊分身+场景混乱 | "赵磊有两个" |
| 第3次 | "stands in the hallway, pushes the door open, steps through" | **从门里面开门** | "又从门里面把门开开了" |
| 正解 | "opens inside the apartment. Lu Han stands at the door, pushing it shut behind him" | ✓ | — |

第3次是典型违反：参考图是室内，写了"站在走廊（室外空间）推门进入"，模型没有走廊参考图，强行在室内框架内表现开门，结果变成从里面开门。正确做法：角色已经在室内，关门（不是开门）→走到桌前→坐下。所有动作都在室内参考图空间内。

### 室内→室外过渡的正确做法

当 clip 需要从室内过渡到室外时：

1. **优先用硬切**：Shot 1 室内（参考图空间内），Shot 2 硬切到室外（新空间）。不用连续运镜穿越。
2. **镜头拉到门口停住**：镜头从室内拉远到门口位置，在门框处停住不动，等角色自己走出来。镜头不穿越门口。GK 原话："镜头从林婉儿特写运镜到门口，镜头等他们三人出来"。
3. **用尾帧承接**：上一个 clip 的尾帧截图作为下一个 clip 的 `<Picture 1>` 首帧，硬切到新空间。
4. **角色动作限定在参考图空间内**：室内参考图 → 角色在室内关门/走动/坐下。不要让角色做需要室外空间的动作。

## 画外音与内心独白

用户可能要求在镜头中加入角色内心独白、旁白、画外音等非画面元素。

**核心原则：所有声音信息（环境音、内心独白、直接对白）全部写入 detailed_description 各镜头描述中，overall_soundscape 只保留一句全局环境音概述。**

海螺导演台视频生成AI按镜头逐段处理，声音信息跟着镜头走最清晰。把声音拆到 overall_soundscape 逐 Shot 列举会导致与 detailed_description 的 Shot 描述脱节，导演台AI难以正确关联画面和声音。

### 说话人 ID 分配

内心独白和画外音同样使用 `(Sx)` 全局说话人 ID，按目标视频中实际发声事件顺序分配。同一角色在直接对白和内心独白中复用同一 ID。

### 写法

在 detailed_description 中，对应 Shot 描述中写入声音信息：

直接对白：
```
<Subject 2> (S1) says in a [声音特征] voice, <d>[Language] 台词原文</d>.
```

内心独白/画外音：
```
<Subject 1> (S2, V.O.) narrates off-screen in a [语气描述] voice as voice-over only, <d>[Language] 独白原文</d>. His lips stay closed — no mouth movement at all.
```

声音特征需包含：声调（low/high/shaking）、语速（slow/fast）、情感（confused/shocked/angry/calm）。

**关键：内心独白镜头画面必须避开嘴。** H3 模型只要画面里有脸+有声音就会让嘴动，光写 `lips stay closed` / `mouth never opens` 不够，H3 仍会让嘴动。最可靠方法：用 `tight close-up of <Subject N>'s eyes and brow only — framed from the nose up, mouth below the frame line` 这样的景别，嘴不在画面里自然就不会动。**不要用手部/背影/桌面特写来规避**——GK 明确说"很影响观感"。半张脸特写（眼眉）足够自然。GK 原话："避开嘴，特写里不带嘴，带上半张脸就可以了，不要用手背影，很影响观感"。

### 示例

```
[Shot 4] ...镜头描述... <Subject 2> (S2, V.O.) narrates off-screen in a low, confused young male voice as voice-over only, <d>[Chinese] 2007年……高三八班……</d>. His lips stay closed — no mouth movement.
[Shot 5] ...镜头描述... The voiceover continues, accelerating slightly with a faint tremor, <d>[Chinese] 这不是我的教室……这是什么时候？</d>.
[Shot 6] ...镜头描述... <Subject 2> (S2, V.O.) narrates in a suddenly sharp, incredulous voice, <d>[Chinese] 我穿越了！</d>. Close-up rapid breathing and hands gripping the desk. His mouth never opens.
```

同时在 non_diegetic_music 中说明该段落无配乐介入（画外音段落通常静音衬托）。

不要在 summary 或 overall_soundscape 中写"声音已同步写入各镜头"等元操作说明——这是多余的废话。

## 写作规范

- 素材中用 `<Subject N>` 引用角色，不重复描述外观（已在 subject_definitions 锁定）
- retention_analysis 需列出该素材中出现的所有参考标签（Subject/Picture/Video/Audio）及其所在 Shot
- detailed_description 第一行定全局风格/光影/氛围（在 [Shot 1] 之前），之后是 [Shot N] 块配时间戳
- 音频分三层：overall_soundscape(全局环境音概述) + non_diegetic_music(配乐) + detailed_description(每个镜头各自的声音：环境音细节+内心独白+直接对白，全部写入对应Shot描述)
- 语言：六段正文用英文，电影术语保留英文。对话和歌词在 `<d>` 中保留原文语言。
- 不写"声音已同步写入各镜头"等元操作说明

### 素材职责分配

多素材任务必须在 subject_definitions 或 summary 中明确每份素材的编号和职责：
- 图1 严格负责人物身份与服装；图2 只负责产品外形和标签；视频1 负责动作、机位与节奏；音频1 负责音乐节拍
- 不要让两份素材竞争同一个核心身份；确需融合时说明主次关系和冲突优先级
- 只上传能提供独立信息的素材，重复素材不会自动提高一致性，反而可能造成平均脸、产品变形和风格串台

### 声音分层编排

所有声音信息（环境音、内心独白、直接对白、动作音效）全部写入 detailed_description 各 Shot 描述中。overall_soundscape 只保留一句全局环境音概述，不逐 Shot 拆分。

各声音类型写法：
- 直接对白：`<Subject N> (Sx) says in a [声音特征] voice, <d>[Language] 台词</d>.` — 写在该说话人所属 Shot 中
- 内心独白/画外音：`<Subject N> (Sx, V.O.) narrates off-screen in a [语气描述] voice as voice-over only, <d>[Language] 独白</d>.` — 写入对应 Shot。镜头画面必须避开嘴（用 `tight close-up of eyes and brow only — framed from the nose up, mouth below the frame line`），否则 H3 会让角色嘴部动起来。不要用手部/背影/桌面特写来规避。
- 环境声：空间真实性 — 写入对应 Shot 的环境描述中
- 动作音效：只在具体动作触发 — 写入对应 Shot 的动作描述中
- 音乐：风格、节拍、进入和高潮位置 — 写在 non_diegetic_music

如果使用了 `<Audio N>`，在音频关系生效的 Shot 中引用并声明是复制还是参考。

核心原则：声音跟着镜头走。同一句台词/独白只出现在一个 Shot 中，不重复。overall_soundscape 不承载逐 Shot 声音，避免与 detailed_description 脱节导致导演台AI混淆说话人归属。

用户不要旁白时明确禁止新增旁白。

### 多角色对白镜头分配

多角色对白场景中，每个说话人的台词必须分配到该说话人独立的 Shot 中，不要把两个角色的对白塞进同一个 Shot。正确做法：

1. 每个对话节拍（一方向另一方说一句话）给一个独立镜头
2. 说话人切换时硬切到该说话人的近景/大近景
3. 每条对白/独白写入对应 Shot 的 detailed_description，用 `(Sx)` 说话人 ID + `<d>` 格式
4. summary 中列出对白顺序和归属 Shot

示例（病房对话，5个 Shot 4个对话节拍）：

```
Shot 1（林屿川大近景）：内心独白 (S2) → <d>[Chinese] 后来这个坏女孩...</d>
Shot 2（林玥大近景）：直接对白 (S1) → <d>[Chinese] 你能来，真是挺好...</d>
Shot 3（林屿川大近景）：直接对白 (S2) → <d>[Chinese] 我该早点来</d>
Shot 4（林玥大近景）：直接对白 (S1) → <d>[Chinese] 不晚...</d>
Shot 5（遗书特写）：无声收尾
```

不要写成 Shot 2 里同时放林玥对白和林屿川画外音对白——对话节拍混在一个镜头里会打乱画面与声音的节奏对应关系，也不利于后续单独微调某个节拍的时长。

## 生成流程

0. **前置验证**：如果 GK 提到的角色/人物是真实人物（B站UP主、网红、公众人物等），必须先搜索确认其身份、外观特征、标志性梗，再开始生成提示词。不要凭名字猜测角色设定——一旦搞错方向，整段提示词全部作废。
0a. **需要写 MJ 提示词时**：必须先读取 [midjourney-character-scene-prompts.md](references/midjourney-character-scene-prompts.md)。该文件包含短语原则、风格后缀铁律、参数速查（--ar/--s/--raw）、道具图规则、写实风格规则、用户提供的长关键词模板处理方法等。凭记忆写 MJ 提示词会反复犯同样的错误（缺风格后缀、长句修饰、错误参数、忘记画风切换）。GK 已多次纠正此问题。**阈限空间系列视频（星座避难所/电梯按钮等）的设计参考见 [liminal-space-video-series.md](references/liminal-space-video-series.md)——包含系列格式、差异化矩阵、叙事结构模板、动态效果写法、MJ 多格生图提示词写法。**
1. GK 描述需求（角色、场景、情绪、镜头构想）
2. **VLM 预分析参考图**：如果 GK 提供了参考图（角色图、场景图等），先用 VLM 对每张图做外观/场景细节分析，提取精确的角色特征（发型、服装、配饰、面部特征）和场景锚点（黑板文字、日历日期、墙面装饰等）。VLM 分析结果直接用于编写 subject_definitions，确保角色外观锁定到参考图可见的一切细节，而非凭空描述。**VLM 优先级**：(a) SiliconFlow VLM skill（`analyze_image.py`，需 `SILICONFLOW_API_KEY` 环境变量或 config.yaml 中的 siliconflow provider）→ (b) 如果 SiliconFlow key 不可用，用主 provider (tokenrhythm.studio) 的 `glm-5.3-flash` 模型，通过 API 直接调用：`POST /v1/chat/completions`，content 用 `image_url` + `text`，图片需 base64 编码且 PIL 压缩到 1024px 以内。glm-5.3-flash 识图能力足够用于角色/场景外观锁定。
3. **原子需求台账**：将 GK 的需求拆成原子条目，每条只表达一件事，标记为四类：
   - `必须出现`：主体、动作、镜头、文字、声音或结尾结果
   - `必须保持`：人物身份、产品结构、原视频动作、运镜、节奏等
   - `允许变化`：可以由模型自由发挥的部分
   - `禁止出现`：高概率且高损失的错误
   缺失信息会显著改变结果时才询问一个最关键问题，否则用保守假设直接生成。
4. **选择生成方式**：按能力路由确定主路径和任务类型组合。若超出官方限制（如素材过多、时长过长），调整素材组合或拆分生成段落，不得生成表面完整但实际无法提交的 prompt。
4a. **判断文件架构**：如果任务是一整集多幕剧（多个 clip 覆盖多个场景，总参考图超过 9 张），采用每幕独立文件架构——每段 clip 一个文件，独立 subject_definitions + 独立参考图（仅该幕出现的角色/场景），Subject 编号每幕从 1 开始。详见"多段脚本文件"章节的"多幕剧集"小节。如果任务只是追加 1-2 段 clip 且角色集不变，用共享 subject_definitions 即可。
5. 根据 GK 提供的参考图和 VLM 分析结果，生成 subject_definitions（包含所有需要的 Subject/Picture/Video/Audio 标签）
6. 逐段生成素材提示词框，每段0-15秒
7. 每段字段顺序：summary → retention_analysis → detailed_description → overall_soundscape → non_diegetic_music

## 输出前检查清单

- [ ] subject_definitions 锁定所有角色外观到参考图，包含所有需要的 Subject/Picture/Video/Audio 标签
- [ ] 素材中用 <Subject N> 引用，不重复描述外观
- [ ] summary 以任务类型前缀开头（如 `[reference generation]`），多关系用 ` + ` 组合
- [ ] retention_analysis 覆盖该素材中出现的所有参考标签，使用正确的关系标记
- [ ] retention_analysis 中不写 `(Sx)`
- [ ] detailed_description 风格行在 [Shot 1] 之前
- [ ] 对白用 (Sx) 说话人 ID + `<d>[Language] 台词</d>` 格式
- [ ] 说话人 ID 按实际发声事件顺序分配，全局复用
- [ ] 优先软过渡
- [ ] 所有声音写入 detailed_description 各 Shot，overall_soundscape 仅全局概述
- [ ] 不写"声音已同步写入各镜头"等元操作说明
- [ ] 两个音频字段都填写
- [x] 全局参考总量 ≤ 9图 / 3音 / 3视频，合计 ≤ 12 个文件
- [x] 每段素材时长 4—15 秒整数
- [x] Prompt 总字符 ≤ 7000
- [x] 分镜脚本总时长 ≤ 15 秒——超过必须拆分为多个 clip（每幕独立文件）

## 机械校验

输出前检查清单负责语义覆盖，机械校验负责字符数、时长、素材数量等硬限制，两者不能互相替代。涉及 API 提交、复杂时间轴或多素材时，将最终提示词保存为 UTF-8 文本后运行：

```bash
python3 scripts/validate_h3_prompt.py \
  --input "<prompt.txt>" \
  --mode reference-to-video \
  --duration 15 \
  --ratio 16:9 \
  --images 2 \
  --videos 1 \
  --audios 0
```

更多参数：`--video-durations 5,10`、`--audio-durations 8,7`、`--first-frame`、`--last-frame`。只修复校验指出的问题，不借机改写已经满足用户要求的内容。

## 快节奏剪辑掩盖 H3 动作僵硬（通用质量伪装）

H3 生成的视频存在动作僵硬问题——人物运动不自然、物理动作（扔东西、起身走动）不流畅。**根因不是动作太复杂，而是节奏太慢。** 慢节奏（每个 Shot 3.75s+）给观众足够时间盯着画面看细节，僵硬感被放大暴露；快切（2-3s/Shot）让观众注意力跟着叙事走，来不及抠细节，动作不自然被天然掩盖。

GK 原话："不咋地，我感觉反而是节奏慢下来了，所以看出问题了"

### 适用判断

当满足以下条件时使用此技术：
- clip 中有人物运动 / 肢体动作（不只面部表情）
- 非"内心独白+静态特写"类纯情绪 clip（这类 clip 慢节奏没问题，因为画面几乎不动）
- GK 反馈"动作僵硬""质感差"且 clip 节奏偏慢

### 具体做法

1. **增加 Shot 数量、缩短每个 Shot 时长**：15s clip 用 5-6 个 Shot（之前 3-4 个），非对白 Shot 压到 2-3 秒一闪而过
2. **对白 Shot 给足时长**：有台词的 Shot 保持 3-4 秒（台词读完需要时间），但不要更长
3. **动作照写不删**：扔文件、起身走人等动作在快切下反而更有冲击力，不需要因为"动作复杂"而砍掉
4. **detailed_description 首行加节奏关键词**：`Fast-paced editing, rapid cuts between shots, each shot lasting only 2-3 seconds to maintain tension and urgency. Fluid natural movement, subtle body language, smooth motion.`
5. **最后一个 Shot 可留长一些**（5-6s）用于情绪收束——此时画面趋于静态（人物发呆/呼吸），不存在动作僵硬问题

### 示例对比

**慢节奏版（4 Shot / 15s，问题版）**：
```
[Shot 1] 0-4s: 会议室全景 + 客户扔文件
[Shot 2] 4-8s: 客户近景说话 + 起身走人
[Shot 3] 8-11s: 周策结巴解释
[Shot 4] 11-15s: 周策独自面对空会议室
```
每个 Shot 平均 3.75s，观众有时间看到客户起身动作不自然。

**快节奏版（5 Shot / 15s，改进版）**：
```
[Shot 1] 0-2s: 会议室 + 扔文件（快闪）
[Shot 2] 2-4s: 客户近景"这就是你们做了三周的东西？"
[Shot 3] 4-7s: 周策结巴解释（对白需时间）
[Shot 4] 7-9s: 客户起身走人（快闪）
[Shot 5] 9-15s: 周策独自面对空会议室（静态收束）
```
非对白 Shot 只 2 秒，观众来不及看动作细节。

### 动作戏分解技法（与快切配合）

当 clip 不可避免包含物理动作（追逐、投掷、搏斗、被淹没）时，即使码率足够高（如 7128 kbps），全身运动仍会暴露 AI 味和僵硬感。GK 原话（clip09b1 苏念闪回，码率 7128 kbps / 13.3MB）：画质行，但是效果不好，太ai味了，人行动也不自然，整体感觉很生硬。

**根因**：H3 做全身复杂运动（跑、扔、摔）天然不流畅，与码率/画质无关。码率高只说明画面信息密度够，不代表动作自然。

**解法**：把全身动作拆成局部碎片，每个碎片 1.5-2 秒，快切拼贴：

| 原始动作 | 分解后碎片 |
|---------|-----------|
| 角色全力冲刺跑 | 脚踩碎玻璃特写 → 手扶墙拐弯 → 呼吸急促的嘴部特写 → 背影模糊掠过 |
| 角色抓箱子砸下楼 | 手抓箱子边缘特写 → 窗外低角度仰拍箱子坠落 → 花盆碎裂慢镜 |
| 角色被群体淹没 | 向日葵从手中滑落 → 花瓣散在地上 → 阴影覆盖画面 → 手指最后松开 |
| 角色起身走人 | 椅子腿刮地特写 → 门把手转动 → 走廊 silhouette → 门关上 |

原则：
- **不拍全身运动过程**，只拍运动的"结果"和"局部"
- 每个碎片是静态或微动的特写/近景——H3 擅长的范围
- 碎片之间用快切连接，观众脑补完整动作
- 声音设计配合：脚步声、碎裂声、呼吸声填补画面没展示的运动

### 动作描写必须"活"——反提线木偶（GK 确认）

H3 默认生成的人物动作呆板僵硬，像提线木偶。GK 原话：跟死人一样，提线木偶一样。原因：提示词中动作描写太笼统（写"sprints""pushes"），模型只做最小幅度动作。

**正确做法：每个动作必须写出具体的身体部位运动 + 物理细节 + 面部表情**。

| 笼统写法（死人感） | 生动写法（活人感） |
|-------------------|-------------------|
| He sprints down the road | He sprints full-tilt, legs pumping hard, arms clawing through thick red mist. His right shoulder clips a rusted car — metal shrieks, he stumbles sideways, catches himself on the car door, keeps running. His breathing is ragged, desperate, animal. |
| She pushes the pots off the sill | She plants both hands flat on the row of pots and throws her entire body weight forward. Her face scrunches — teeth bared, neck cords straining, veins visible on her forearms. The pots resist for a split second then the whole row tips forward. She lurches forward with the momentum, half her body out the window, hands gripping the frame to stop herself from falling. |
| He looks back | He throws a glance over his shoulder — eyes wide, sweat cutting lines through ash on his face. |

三要素：
1. **身体部位分解**：不写"跑"，写"腿在蹬、手臂在扒、肩膀撞到东西、踉跄、手撑住"
2. **物理交互**：身体与环境的碰撞——金属尖叫、脚步打滑、花盆很重推不动、惯性前冲差点栽出去
3. **面部表情具体化**：不写"害怕"，写"眼睛瞪大、嘴张开、脸扭曲、咬牙、脖子青筋暴起"

GK 原话：陆寒和苏念动作太死人味了，动作大一点，陆寒被使者追的狼狈，还有苏念感到着急的表情和使劲推那排花盆的表情都加上

### 手持镜头晃动增强真实感（GK 确认 v8 可用）

动作戏中，除了身体部位分解和物理交互，**镜头本身也要"活"**——固定机位拍动作戏会暴露 H3 的运动僵硬。GK 原话："陆寒跑动和表情都有点死板，要有点速度感，实在感，甚至他跑动的时候加一些镜头的晃动增加真实感"。

具体写法（v8 实测 GK 确认可用）：

```
Handheld shaky camera at chest height, running hard with <Subject 1> — the camera bounces and jerks with every footfall, breathing-style micro-sway, lens occasionally splattered with ash and moisture.
```

关键要素：
1. **机位高度**：chest height（不是 ground level）——胸高度跟人跑，观众代入感最强
2. **弹跳/抖动**：camera bounces and jerks with every footfall——随每一步弹跳抖动
3. **呼吸式微晃**：breathing-style micro-sway——模拟摄像师跑步时的呼吸晃动
4. **镜头沾污**：lens occasionally splattered with ash and moisture——镜头沾灰/水雾，增加临场感
5. **甩镜**：whip-pan back and forth between pursuer and pursued——追击者和被追者之间快速甩镜，chaotic, urgent, nauseating

这和"快切掩盖僵硬"不同：快切是**剪辑节奏**（每 Shot 2-3 秒），镜头晃动是**机位运动**（同一 Shot 内镜头本身在动）。两者可叠加使用——快切 + 每个 Shot 内镜头都在晃。

### 注意事项

- 这不是"喜剧快节奏"——那是用快切制造喜剧节奏，这是用快切掩盖 AI 动作缺陷，目的不同
- 纯情绪 / 内心独白 clip（画面几乎不动）不需要此技术，慢节奏反而更好
- 如果用户反馈"太赶了""看不清"，适当放慢，但优先保快切
- **动作戏即使码率高也会僵硬**——码率解决画面质感，不解决动作流畅度。动作戏必须同时用快切+分解技法

### 现代职场版 UE5 模板（2026-09-07 确认）

用户在现代打工人版封神小剧场项目中反复试验后确认了一套不同于 CG 风和写实风的模板。详见 references/midjourney-character-scene-prompts.md 的"现代职场版 UE5 模板"章节。关键：风格后缀用 `Unreal Engine 5 style, highly detailed, 8k`（不是完整 CG 后缀），放末尾不要放开头；三视图用 `character three-view reference sheet, front view side view back view`；不要加 `Pixar style` / `3D animated character design` / `character reference sheet` / `--niji`（都会偏手绘漫画）。

#### 角色微调迭代规则

- **一次只改一个特征**：GK 说"胡子改成中等长度山羊胡"就只改胡子那一词，不重写整个提示词。维护"已确认特征清单"，每次确认后更新，写新提示词时对照清单确保不丢失已确认特征。
- **MJ 不认识的角色名用纯视觉特征描述**：MJ 对游戏/动漫角色名（如 FF16 Clive Rosfield、Zack Fair）识别不稳定。去掉角色名，把视觉特征拆成纯描述词（`short dark brown undercut hair swept back` 而非 `Clive Rosfield hairstyle`）。如果用户提供了角色参考图，建议用 `--sref [图URL]` 或 `--cref [图URL]` 灌风格/面部比文字描述更准。
- **场景铭牌文字 MJ 无法可靠生成**：MJ 在场景图中生成中文文字（如"朝歌集团"）不可靠，通常只生成抽象 LOGO 不生成文字。解决方案：(a) 用 `blank surface` 出空白铭牌，后期 PS/Canva 贴字；(b) 单独出铭牌特写图（文字成功率比放在场景里高），再合成到场景图上。

### MJ 角色名无法识别时用纯视觉特征描述

MJ 对游戏/动漫角色名（如 Final Fantasy 的 Clive Rosfield、Zack Fair）识别能力不稳定——写了 `Final Fantasy 16 Clive Rosfield CG art style` 后用户反馈"克莱夫成年时候的感觉MJ不太懂呢，表现不出来"。正确做法：去掉角色名，把该角色的视觉特征拆成纯描述词（发型、脸型、体格、气质、标志性特征），用 `short dark brown undercut hair swept back` 而非 `Clive Rosfield hairstyle`。如果用户提供了角色参考图，用 `--sref [图URL]` 或 `--cref [图URL]` 灌风格/面部比文字描述更准。

### 分镜脚本超过 15 秒时必须拆分为多个 clip

当分镜脚本总时长超过海螺单次 15 秒上限时（如 60 秒脚本），必须按叙事节奏拆分为多个 15 秒 clip。拆分方案：(a) 按叙事段落拆——面试段→转折段→高潮段→收尾段各一个 clip；(b) 每个 clip 自包含独立 subject_definitions（每幕独立文件模式）；(c) clip 间用首尾帧承接（提取上一个 clip 成品最后一帧为图片，作为下一个 clip 的 `<Picture 1>` 首帧参考）。不要把 60 秒内容塞进一个提示词——字符数会超 7000 上限，时间轴也会超 15 秒。

## 画风切换

用户可能要求从写实风格切换到其他渲染风格（3D CG动画、三渲二、二次元手绘、水彩等）。切换方法是结构化的三步操作，不是逐句改写：

### 第一步：subject_definitions 末尾加全局画风声明

在最后一个标签定义之后、代码块结束之前，追加一行全局画风定调。

### 第二步：每段 detailed_description 第一行改渲染风格

将每段 detailed_description 的首行（风格行）改为目标渲染风格的核心特征。

### 第三步：排查 Shot 级描述中的"写实"字样

全文搜索"写实"，将所有 Shot 级描述中的"写实基调"等改为目标风格。角色外观锁定描述不需要改——参考图特征全保留，改的只是渲染媒介。

### 3D CG / Unreal Engine 风格（用户明确要求"3D CG虚幻引擎风"时）

用户说"3D CG"或"虚幻引擎风"时，不是写"赛璐璐"或"2D anime"。确认剧本原始风格标注是什么——如果剧本写了"2D 日漫赛璐璐"但用户说改成3D CG，要把所有风格行换成3D CG词：

- **detailed_description 风格行**用：`3D CG animation style, Unreal Engine 5 render quality, subsurface scattering skin, high-detail PBR materials, volumetric light, cinematic depth of field.`
- **不要同时写 "cel shading" / "outline lines" / "blocky shadows"**——那是二次元，和 3D CG 互斥
- **不要在 subject_definitions 末尾加画风声明**——3D CG 是 detailed_description 风格行的事
- **生图提示词也同步改**：如果同时有 Midjourney 生图提示词，把风格词从赛璐璐改成 `3D CG render, PBR textures, Unreal Engine 5 style`

### 常见画风关键词

- 3D CG动画/三渲二：subsurface scattering skin, blocky 3D hair modeling, stylized clothing folds, CG bloom, volumetric light
- 二次元手绘：cel shading, outline lines, blocky shadows, no subsurface scattering
- 水彩/油画：visible brushstrokes, edge bleeding, paint thickness, canvas texture
- 像素艺术：low resolution, limited palette, visible pixel grid

## 喜剧快节奏场景

当用户要求"活泼俏皮""快节奏""喜剧感"基调时，镜头策略与默认的慢节奏软过渡完全不同。

### 节奏原则

- 镜头数量可多达 8-10 组（15秒内），平均 1-2 秒一切
- 硬切是主要转场方式，不使用软过渡——硬切本身是喜剧节奏的工具
- 对白交替要快：A 说→B 抢话→A 接话，每个说话人独立 Shot，Shot 时长可短至 1 秒
- 反应镜头链：关键台词落地后，连续硬切 2-3 个不同角色的反应脸（震惊→惊讶→脸红），每个 1-1.5 秒，制造喜剧悬念

### 反应镜头链写法

喜剧高潮台词之后，连续切不同角色的反应：

```
Shot 5: Close-up of <Subject 3> — shocked + sad (1 sec)
Shot 6: Medium shot of classmates — surprised gazes panning across (1.5 sec)
Shot 7: Close-up of <Subject 1> — looking at mirror, turns, surprised, blushing (1.5 sec)
```

每个反应镜头只拍一个角色/群体，表情要具体（eyes slightly wide, mouth open, blushing），不要笼统写"surprised"。

### 群白写法

全班炸锅的群白写入对应 Shot，分配群体 Speaker ID（如 (S3)），注明多人嘈杂：

```
Classmates' chorus (S3), multiple noisy voices, surprised and gossiping: <d>[Chinese] 卧槽？给林玥？林屿川疯了吧！</d>, accompanied by desk-slapping, chair creaking, and overlapping laughter.
```

### Summary 中标注节奏意图

在 summary 中明确写出节奏结构：

```
The tone is lively and playful, with fast pacing, frequent hard cuts, and strong comedic rhythm.
```

### 基调体现

色调可比常规场景略亮略暖。在 detailed_description 第一行风格描述中体现。

## 画外角色处理

角色可以不出镜但以声音存在——对白、怒吼、训话从画外传来，画面只拍其他人的反应。

### 操作方法

1. 该角色不分配参考图，不写入 subject_definitions
2. 画面不拍该角色所在区域（如讲台方向不入画）
3. 声音写在对应 Shot 中，用 `(Sx)` 说话人 ID + `<d>` 格式，标注 `off-screen`
4. 其他角色的反应（回头、窃笑、哄笑）是画面的主体内容

### Subject 重新编号

删除角色后，剩余 Subject 需重新顺序编号。例如原 Subject 1-5 删除 Subject 1 后：
- 原 Subject 2 → 新 Subject 1
- 原 Subject 3 → 新 Subject 2
- 以此类推
- 全文（subject_definitions、retention_analysis、detailed_description、overall_soundscape）中所有 <Subject N> 引用同步更新

## 画外角色转上画

前几幕中仅以画外声音存在的角色，后续可能需要正式上画出镜。

1. 确认该角色是否有参考图——如果有（之前定义过但未使用，或用户提供的），用 VLM 分析提取外观
2. 在 subject_definitions 中新增该角色为 `<Subject N>`（N 接续现有编号）
3. retention_analysis 覆盖该角色出现的所有 Shot
4. 对白路由不变：画外音时期声音用 `(Sx)` + `off-screen`，上画后直接对白正常写入 Shot

## 每幕独立文件模式（GK 确认）

GK 要求每幕（clip）一个独立文件，各自自包含 subject_definitions + 六段格式。这样：
- 每个 clip 只定义该幕出现的角色为 `<Subject N>`（编号从1开始），不出现的角色不定义
- 每个 clip 只上传该幕需要的参考图（≤9张），不会因角色多而超配额
- 提交导演台时复制对应文件到素材提示词框，上传对应参考图即可

### 首尾帧承接（跨 clip 连贯性）

当两个 clip 之间空间或时间有跳跃、衔接不自然时，用 `<Picture 1>` 标记首帧承接：
1. 用 ffmpeg 提取上一个 clip 成品视频的最后一帧为图片：`TOTAL=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=noprint_wrappers=1:nokey=1 prev_clip.mp4) && ffmpeg -y -i prev_clip.mp4 -vf "select=eq(n\,$((TOTAL-1)))" -vframes 1 tail.png`
2. 上传这张尾帧图片到 RunningHub
3. 后一个 clip 的参考图位放这张截图，定义为 `<Picture 1> is the last frame of the previous clip, showing...`
4. detailed_description 的 [Shot 1] 开头写 `The shot begins from <Picture 1>, matching the last frame of the previous clip.`
5. retention_analysis 中加一行 `<Picture 1> ([Shot 1] first frame): fully_preserved - ...`

**⚠️ 严禁用 ref_video（节点31）传整段视频做尾帧衔接。** ref_video 是 video editing/continuation 的素材源，不是帧锚点。尾帧必须是提取出的单张图片，走 ref_image 通道。GK 原话："vedio怎么可能是尾帧，你要用视频的最后一帧，放在参考图里，通过提示词实现！"

不是所有 clip 都需要首尾帧。以下情况不需要：
- 白光/闪白转场（画面完全洗白后切入）
- 同场景同时间连续（空间未变）
- 自然时间跳转（白天→夜晚，观众能理解）
- 出门→驾车→到达（动作本身就交代了空间转换）

### 黑闪过渡（时间+空间硬跳转）

白闪用于闪回切入切出（画面完全洗白后切入回忆），黑闪用于**时间+空间的硬跳转**——如从白天出租屋直接跳到夜晚仓库门口。写法：`a sharp black flash fills the entire screen for half a second. The black clears to reveal...`。黑闪比白闪更适合时间跳跃场景：白闪暗示"记忆闪回"，黑闪暗示"时间断裂"，语义不同。黑闪后直接切到新空间的新画面，不需要首帧承接——黑屏本身就是断点。

案例：clip09c 出租屋天色变暗 → clip10a 黑闪入 → 夜晚仓库门口面包车。黑闪前的那一帧（空房间暗光）可以是过渡 clip 的尾帧，但黑闪后的新场景不需要从这个帧开始——黑屏洗掉了空间连续性。

### 过渡 clip（时间+空间跳跃的桥接）

当两个 clip 之间存在**时间跳跃 + 空间跳跃**（如 clip09b1 白天在出租屋画完地图 → clip10 夜晚在仓库门口），观众不知道角色怎么从 A 到 B 的，需要一个短过渡 clip（10s）桥接：

1. **首帧**：上一个 clip 的尾帧（`<Picture 1>` = 提取的最后一帧截图）
2. **内容**：角色完成当前动作 → 内心独白交代下一步计划 → 拿钥匙/收东西 → 出门
3. **尾帧**：空房间 + 窗外光线变化暗示时间流逝（如金色暖光→琥珀色→变暗），自然过渡到下一个 clip 的夜晚场景
4. **尾帧可作为下一个 clip 的首帧参考**，或直接用黑闪跳转到新场景

GK 原话（clip09b1→clip10 衔接问题）："画完圈应该说，路线规划好了，先去老张那里拉东西，回来后夜里也不能闲着，要做好万全的准备，然后接开车去买东西"

### 内心独白补连贯性（GK 规则）

当观众可能不理解角色为什么做某个决定时，用内心独白（off-screen narration）解释动机。GK 原话规则："通过内心独白的方式给观众解释，为什么这么做。"

典型场景：
- 角色突然改变行动方向（如从采购突然去赴约）→ 独白解释"不能不去，不去会暴露"
- 角色做出反直觉选择（如陪敌人吃饭）→ 独白解释前世发生了什么
- 战术细节（如改弩为弓）→ 独白解释原因
- 警告某个角色→ 独白交代前世该角色的结局

独白格式：
```
<Subject N> (Sx) narrates off-screen in a [语气], [语速] voice, <d>[Chinese] 独白内容</d>
```

### 对话量限制（GK 确认规则）

一个 clip 内的独白+对白总量不能超过时长容量。经验值：
- 15 秒 clip 最多 3-4 段独白/对白（每段约 3-4 秒）
- **中文独白/对白每秒约读 2.5-3 个字** → 15 秒 clip 全部独白+对白总计 ≤ 40 字中文。写完提示词后必须数字数：把所有 <d>[Chinese] ...</d> 中的中文台词字数相加，除以 clip 秒数，超过 3 字/秒就必须删减。GK 原话：你这旁白又太长了，15秒根本不够，你就加适量的，15秒够读的
- 每个独白/对白段控制在 2 句话以内（超过 2 句观众读不完，GK 原话：台词太多）
- 如果台词+独白内容塞不下 → 拆成两个 clip，在前一个 clip 自然停顿处断开
- 拆分后用首尾帧方法承接
- **关键判断句前加 1 秒沉默 Shot**（角色眨眼/呼气），给观众消化时间。GK 原话："必须去，笑着去。这句话之前，要有一个小停顿，一秒，断一下句，不然太快了，观众不好理解"
- 精简示例：林婉儿电话 4句→2句，内心独白 5句→2句，时间 12s→15s "给说话留点空间"
- **roll（重新提交相同提示词）也必须先确认**：GK 说"重新生成一下""roll 一下"时，也必须先确认用哪个版本提示词、standard 还是 plus，再提交。GK 原话："以后提交提前跟我确认不要自己提交"。

### 时间预算检查

写一整集多幕剧（如 10 段 clip 覆盖一集 3-5 分钟短剧）时，**不要**把所有 clip 写进一个共享 subject_definitions 的大文件。每幕应是一个完全自包含的独立文件：

1. **每幕独立 subject_definitions**：只定义该幕实际出现的角色和场景，Subject 从 1 开始重新编号。不同 clip 中同一角色可以是不同的 Subject N（Clip 1 的 Subject 1 和 Clip 5 的 Subject 1 不必是同一角色——每个文件独立提交，互不干扰）。
2. **每幕独立参考图**：只上传该幕需要的参考图（1-4 张通常够用），不会触碰 9 图上限。
3. **Speaker ID 每幕独立分配**：(S1)、(S2) 按该幕内实际发声事件顺序分配，不跨 clip 复用编号。
4. **文件头部标注参考图清单**：在文件顶部用注释行写明 `# 参考图（N张）: 角色1.png, 场景1.png`，方便提交时对照上传。
5. **幕间连贯性**：在 detailed_description 中通过转场描述实现（白光转场、空间连续、声音桥接、动作匹配等），不需要跨文件引用标签。

GK 原话："每一幕一个文件，每一幕规划需要的共素材，这样的话，只需要引用这一幕出现的那个人的参考图就可以，就不会超了"

### 幕间连贯性：内心独白桥接（GK 确认规则）

多幕剧中幕与幕之间的叙事连贯性，**不能只靠视觉转场**（白光、空间连续等），还必须用内心独白向观众解释角色的动机和转折逻辑。规则：

1. **每幕转折处加内心独白**：角色从一个行动转向另一个行动时（如从"采购物资"到"去餐厅赴约"），必须在对应 Shot 中写入 `narrates off-screen` 内心独白，解释为什么这么做。
2. **观众理解优先**：如果观众不看上下文就无法理解角色为什么突然做某事，就是缺独白。典型场景：
   - 重生后为什么不慌 → 独白解释"我死过一次，这次有三年记忆"
   - 为什么明知是局还要赴约 → 独白解释"不去反而暴露"
   - 为什么检查床底 → 独白解释"前世林婉儿擅长藏东西"
   - 为什么用纸质地图 → 独白解释"红雾后电子设备失灵"
3. **独白写在动作发生的 Shot 中**，用 `<Subject N> (Sx) narrates off-screen in a [语气] voice, <d>[Chinese] 独白内容</d>` 格式。
4. **避免重复**：如果前一幕已经解释过的动机，后一幕不要再重复说一遍。

GK 原话："后面如果有些不连贯的你也给我调整一下，规则就是通过内心独白的方式给观众解释，为什么这么做"

### 时间预算检查

每个 clip 只有 4-15 秒。写入内心独白和对白时必须计算时间预算：

- 一句普通对白 ≈ 需 2-3 秒画面时间
- 一句内心独白（3-4 个分句）≈ 需 5-7 秒
- 如果一个 Shot 内塞了对白+独白，实际需要的秒数可能远超 Shot 的时间戳区间

**当对白和独白较多时，宁可拆成独立的 clip 也不要压缩时间戳。** 如果一个转折点需要"电话对白+内心分析+决定行动"，而总时间超过 8 秒，应该拆成独立的 clip（如 10 秒），而不是塞进一个更高密度 clip 的某个 Shot 里。

时间不够时不要问 GK 是否可以缩短台词——台词是固定的，变的是 clip 数量。

## H3 模型能力边界与风格匹配（2026-09-09 大量实测总结）

H3 模型有明确的能力边界，不是所有视觉风格都能通过改提示词解决。**在项目立项前先评估 H3 能否拍好这个画面。**

### H3 擅长（85-90分）

- **定镜/微动**：镜头不动或微动，画面内部元素缓慢变化（烟雾飘、灯光闪、人物微动）
- **近景/特写**：面部表情、手部动作、局部物体细节
- **室内氛围**：单一空间内的光影、烟雾、质感
- **静态人物**：坐着不动、站着不动，头微动（歪头、转头）
- **暗色调/高对比**：低光、冷暖对比、剪影
- **概念图动起来**：把精美概念图"复活"——场景细节微动（火蔓延、烟飘、草动），人物不动或微动

### H3 不擅长（60分以下，改提示词也救不了）

- **vlog 灵动风格**：写"handheld/drop 20cm/whip right/lurch forward"等具体物理运动，H3 仍会抖动僵硬。两版迭代（标签词版+物理运动版）用户都反馈"效果还是不好""镜头太死""人物不自然"。**结论：H3 的镜头运动理解和人物动作自然度是硬伤，vlog 风格在 H3 上跑不通。**
- **大场景漫游**：仙侠山城全景、宏大建筑群——分辨率864×1536，大场景细节全糊，灯笼飞檐雾气层次丢失
- **仙侠飘逸美学**：飘逸、薄雾、光影层次需要高分辨率+精细运动控制，H3 两样都没有
- **全身运动**：跑、跳、飞——动作僵硬不自然
- **人物换装**：同一人物在同一clip内换装，H3 做不到一致

### 推荐的 H3 甜区题材

- 情感短剧（室内对话、面部特写）
- 悬疑/犯罪人际博弈
- 日常碎片/氛围片（定镜+微动）
- 概念图复活（精美概念图 → 定镜微动 → 场景活起来）
- 关系破裂/修复

### 不推荐在 H3 上做的题材

- vlog/手持灵动风格
- 仙侠/武侠大场景
- 动作戏（跑跳飞）
- 需要精细镜头运动的场景

### 当 H3 效果不好时的正确诊断顺序

1. **先看是否是 H3 能力边界问题**——如果是（vlog 灵动、大场景仙侠、全身运动），直接告诉用户"H3 做不了这个，建议换模型（可灵/Veo/Sora）或换思路（改近景特写）"，不要反复改提示词
2. **如果是提示词问题**——台词太密、动作太复杂、方向不明确等，改提示词
3. **不要只改提示词**——如果两版迭代后效果都不好，大概率是模型能力边界，不是提示词问题

GK 原话（vlog 项目两版失败后）："感觉效果还是不好 还是核吧 可以做的精致一些"
GK 原话（仙侠项目两版失败后）："重楼太恶心了 太难看了""非常蠢 整体画面抖动 没有任何细节 丑陋不堪"

### 概念图复活型的正确写法（H3 甜区）

当用户提供一张精美概念图，要求"动起来"时，最佳写法：
- **镜头不动或微动**——定镜 locked off 或微摇晃
- **场景细节微动**——烟雾飘、火蔓延、草随风动、灯笼摇、雾气漂
- **人物不动或慢走**——站着凝望、坐着沉思、慢慢走出画面
- **不换场景**——15秒全在参考图这一个画面里
- **不追求叙事**——纯氛围，一个情绪一个瞬间

GK 确认满意的案例：
- 蒸汽朋克凝望版（定镜+场景微动+人物走离画面）："镜头不要动，人物也别换装了，就这么凝望远方，然后向右走出画面"
- 黑武士地铁沉思版（定镜+地铁摇晃+人物沉思到睡着）："一开始他是严肃的若有所思，后面发现头一歪睡着了"

### 飘飘然/醉酒摇晃感的正确写法

当用户要"摇晃/飘飘然"镜头感时：
- **不是写"handheld"标签词**——H3 不理解
- **不是写具体物理距离"drop 20cm"**——H3 做不到精确
- **写"continuous drifting, swaying left then right, weightless, like a leaf on water"**——描述飘的感觉而非精确运动
- **强调"never goes far, never leaves this view"**——限制运动范围
- **配合场景微动**（灯笼摇、雾飘）增强氛围感

GK 原话（重楼v3调整）："镜头摇晃 微微行进，镜头不是不动，是不往前走太远，就是飘飘然的感觉"

### H3 效果不好时先诊断模型能力边界，不要只改提示词

两版迭代后效果仍不好，大概率是模型能力边界问题，不是提示词问题。正确诊断顺序：(1) 先看是否是 H3 能力边界（vlog灵动、大场景仙侠、全身运动）→ 如果是，直接告知用户建议换模型或换思路；(2) 如果是提示词问题（台词太密、动作太复杂、方向不明确）→ 改提示词。不要在模型能力边界问题上反复改提示词浪费时间。

### MJ profile 自带美学时不要写风格描述词

如果用户的 MJ profile 已经自带某种美学（如鱼眼胶片风），提示词里不要写 "fisheye/lomography/film grain/cross-processed/vignette" 等风格词，profile 会自动处理。GK 原话："你不需要强调鱼眼 我这个profile自带这种美学"。

### 配乐控制

**GK 要求所有视频一律不要 BGM。** `non_diegetic_music` 字段始终写 `N/A`，不要写任何配乐描述。只有环境音、动作音效和对白。

```
non_diegetic_music:
N/A
```

不要省略该字段——必须显式声明无配乐，否则导演台可能自行添加默认配乐。

## 群众演员面貌写法

教室、街头、集会等场景中有大量非 Subject 的群众演员。写法不当会导致导演台生成怪脸或千人一面。

### 禁止：标签式特征

不要给每个群众演员贴一个夸张外貌标签——"圆脸短发""方脸戴眼镜""戴牙套""高颧骨""瘦长脸鬈发"。导演台会把这些标签特征放大渲染，生成卡通化怪脸。

### 正确写法

- 人数要多：教室场景至少写"十余名同学"，画面中可见7-8个在 reacting，不要只有三四个
- 脸型用混搭一笔带过："脸型有圆有长有方"而不是逐个贴标签
- 发型用混搭："短发、马尾、平头、寸头"混在一起说
- 体态有胖有瘦，不刻意标"微胖""瘦高个"
- 表情动作自然多样：偷笑、拍桌、捂嘴、仰头笑、趴桌抖肩、推搡、拍掌
- 兜底声明："都是普通高中生面容"，明确不算怪
- 不要用"戴牙套""双手捧脸"等容易被放大成卡通的特征

## 角色性格贯穿

角色不是只有外观——性格气质会影响表情、姿态、动作方式。如果用户描述了角色性格（傲娇、厌世、认真、活泼等），必须贯穿到所有 Shot。

### 写法

1. 在 subject_definitions 的角色定义末尾追加性格气质描述
2. 每个 Shot 中该角色的表情和姿态必须符合性格——不能在 Shot 级写着和性格矛盾的表情
3. 性格影响的是表情和体态，不影响外观锁定参数（五官比例、发色、服装不变）

## 多幕剧立场辩论构建（GK 确认）

写多幕剧的对抗对白前，必须先理清每个角色的核心立场——用户会直接问"某某的观点是什么，他和反派的冲突是啥"（GK 原话："但是祁渊的观点我还是没太理清，他是主张什么的呢，和温故主要的观点冲突是什么"）。理不清就写对白，写出来的台词是书面腔、逻辑转折硬、观众看不懂。

### 第一步：立场对比表

每个立场对立角色写一张对比表，四列必须填满：

| 列 | 内容 |
|---|---|
| 对核心现象的理解 | 同一件事（如幼体"怕"），两人怎么解读 |
| 主张 | 他要求主角/他相信什么 |
| 终极答案 | 他给这件事的最终解决方案 |
| 看不见的盲点 | 他逻辑里的漏洞（对方用来反击的点） |

### 第二步：冲突一句话化

把整场辩论压缩成一句话，这句话就是全剧的题眼。例：《溺声》的题眼 = "它怕什么？怕你——还是怕你又把它丢回那片海？"

### 第三步：台词通顺三原则

1. **口语化，不用书面腔**：去掉"三个月的共生，你一伸手就断了"这类书面套话，改成"三个月，它在他喉咙里安了个家。你一伸手就拆了"——"安家/拆家"对仗利落
2. **每段对白 ≤ 2 句**：超过就拆 clip（GK："对话台词不要太多，太多的话就拆开clip，要通顺一些"）
3. **关键判断句前留 1 秒沉默**：给观众消化，不一口气抛完

### 第四步：双关收束

反派的终极答案要"接住"主角的关键词，形成闭环。例：祁渊说"它怕"，温故接"它怕什么？怕你——还是怕那片海？给我，做成标本。**标本不会怕。**"——"标本不会怕"同时完成三件事：接住主角的话、揭示反派信仰（标本=永恒安宁）、给出他的终极主张。**不要只让反派念台词，要让他的每句话都推进立场。**

### 案例存档

《异闻饲养录》EP01 溺声：温故（标本派：怕=痛苦，标本=安宁，盲点=用"安宁"偷换"活着"）vs 祁渊（放归派：怕=活着的证据，它要回的是它的水，反击句"标本不会怕——标本也不会想家"）。完整立场对比表见剧本文件 `/home/ubuntu/scripts/异闻饲养录/EP01_溺声.md`。

## Vlog风格视频提示词写法（2026-09-09 确认）

当用户要求"vlog感觉""灵动""张弛有度""动静结合"时，镜头策略如下：

### 核心原则

- **每个clip内部有动→静的节奏弧线**：开场手持动态镜头，结尾锁定定镜留白
- **手持有机晃动（handheld organic shake）与锁定静止（locked off stillness）交替**
- **快切与长停留交错**：非对白Shot 2-3秒快闪，情绪Shot 5-8秒长停留
- **whip-pan（甩镜）作为转场工具**：快速Pan产生模糊时切场

### 关键术语

- `Handheld, slightly shaky` — 手持有机晃动
- `Locked-off, static shot` — 锁定定镜
- `The camera is completely still now — no shake` — 明确从动态切到静态
- `Organic handheld sway` — 有机呼吸式晃动
- `Fast, kinetic, alive` — 快闪动态
- `Smooth, cinematic` — 平稳电影感（与手持对比）

### Vlog节奏模板（15秒clip）

```
[Shot 1] 0-5s: Handheld dynamic — 人物动作+手持跟拍，有机晃动
[Shot 2] 5-7s: Whip-pan或快切 — 转场到新视角
[Shot 3] 7-12s: Locked-off — 定镜停留，情绪收束
[Shot 4] 12-15s: Held still — 纯静止收尾，画面呼吸
```

### v2经验：标签词无效→具体物理运动描写（2026-09-09 确认）

v1用标签词"handheld""organic shake""vlog aesthetic"写镜头运动，GK反馈"镜头太死了 人物也有点不自然"——H3不理解标签词，倾向于生成定镜。

v2改用**具体物理运动描写**，GK确认"还可以"：

| v1标签词（无效） | v2具体物理运动（有效） |
|------------------|----------------------|
| `handheld camera with organic shake` | `The camera drops 20cm as she steps forward, tracking her feet, then whips up to her face` |
| `camera bounces with her movement` | `The camera lurches forward to catch up, handheld and breathless` |
| `handheld orbit` | `The camera arcs around her from behind to her right side — a physical 90-degree orbit` |
| `smooth tracking` | `The camera glides laterally across a wooden table surface, close to the wood grain` |

同时**人物动作拆成物理碎片**——不写"she laughs"，写"her right hand shoves the door, her left hand grabs the backpack strap sliding off her shoulder, yanking it back up. A strand of hair sticks to her lip. She blows it off."

三要素（与"动作描写必须活"章节一致，但专用于vlog风格）：
1. **镜头写物理位移**：drop X cm / whip up / whip right / lurch forward / glide laterally / arc X degrees / tilt up from Y to Z
2. **动作写身体部位**：手指卷钥匙、拇指敲方向盘、脚趾踩进湿沙、指节发白攥毯子
3. **每个Shot 2-4秒快切**：非情绪Shot不超过4秒，情绪收束Shot可留5-8秒

### 参考案例

《一个人的逃跑计划》v2，文件 `/home/ubuntu/封神小剧场/逃跑计划_v2_海螺提示词.md`。8个clip（8+10+12+8+10+15+15+12=90秒），每个clip都有handheld→locked-off的动→静弧线，具体物理运动描写。8格拼贴照作为`<Picture 1>`整体风格参考（weak_reference），不逐格拆Subject。None默认版工作流，9:16竖屏，standard，无BGM无对白纯视觉叙事。

## 长度指导

按任务复杂度使用最短但足够的表达：
- 单点编辑：通常 1—4 句
- 单镜头生成：通常 100—400 个中文字符
- 15 秒多镜头视频：通常 400—1400 个中文字符
- 多素材、强一致性或复杂包装：可更长，但不得超过 7000 字符上限

不要为显得专业重复主体描述、风格词或否定词。不得输出"非完整 Prompt""可自行补充""参考类似案例"等占位表述。

## 声线统一（2026-09-02 验证）

同一角色跨 clip 声线不一致问题，已通过音频参考节点解决。

### 操作流程

1. **从已生成的 clip 中提取角色声线**：选一段含角色独白/对白的代表性片段（5秒左右），用 ffmpeg 提取音频：
   ```bash
   ffmpeg -y -ss 2 -t 5 -i source_clip.mp4 -vn -acodec libmp3lame -q:a 2 voice_ref.mp3
   ```
2. **发给 GK 确认声线代表性**：用 MEDIA: 发送 mp3，等 GK 确认"可以"再继续。
3. **上传到 RunningHub**：`curl -s -X POST UPLOAD_URL -H "Authorization: Bearer KEY" -F "file=@voice_ref.mp3"`，获取 openapi ID。
4. **提交时传音频节点28**：在 nodeInfoList 中加 `{"nodeId": "28", "fieldName": "audio", "fieldValue": "openapi/xxx.mp3"}`。
5. **提示词中加声线描述行**：在 subject_definitions 末尾加：
   ```
   <Subject N> voice reference: the attached audio is [角色名]'s canonical voice — [声音特征描述, 如 low, cold, restrained male voice with slight rasp]. All of <Subject N>'s narration and dialogue in this clip must match this voice timbre, pitch, and tone.
   ```

### 声线提取由 GK 手动完成（GK 确认规则）

GK 原话："声线时间不对，里面有其他人的声音 这个我来做吧，你告诉我 我做好放在哪里"。

- **H 不要自动从 clip 中截取声线**——截取的时间点可能不对，片段可能混入其他角色/环境音
- GK 自己用视频剪辑工具截取纯净的 5 秒角色人声
- **H 的职责是告诉 GK 存放路径**：`/home/ubuntu/scripts/doomsday-drama/output/{角色名}_voice_ref.mp3`（如 `linwaner_voice_ref.mp3`、`laozhang_voice_ref.mp3`），命名格式与 `luhan_voice_ref.mp3` 一致
- 文件要求：5 秒、mp3 格式、只含该角色清晰台词、无背景人声
- GK 做好后告知 H，H 直接上传到 RunningHub 使用

### 注意事项

- 每个 clip 最多传 3 个音频（节点 28/29/30），可同时传多个角色的声线参考
- 提取片段必须含清晰的角色人声（不能只有环境音）
- None 默认版工作流音频节点默认为 None，用几个传几个，不传的自动跳过
- 后续 TTS 全量替换方案仍可作为备选，但音频参考节点已能实现基本声线统一

## RunningHub API 执行

通过 RunningHub 托管的 ComfyUI 工作流（H3 Reference-to-Video）执行提示词，生成视频后下载 + 截尾帧 + 发给 GK。完整 API 调用流程见 [runninghub-workflow-api.md](references/runninghub-workflow-api.md)。

### 工作流偏好（GK 规则）

- **生成完视频后必须用 `MEDIA:` 发给 GK 看效果**——不要只下载不发。
- **出片后自动转码再发，不等 GK 提醒**（GK 原话："生成好了转视频保留音频都不要让我说了，你自己做"）。转码必须**保留音轨**（RunningHub 输出自带 AAC 环境音！），命令：`ffmpeg -y -i in.mp4 -c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 128k out.mp4`。**禁止 `-an`**——曾因 `-an` 丢音轨被 GK 指出"怎么没声音"。详见 references/runninghub-workflow-api.md 第5节。**注意：转码有画质损失（码率约降36%），原始文件必须保留。GK 确认后要求直接发原始文件，微信发不了再转。**
- **instanceType 默认用 "standard"，能不用 plus 就不用 plus（省积分）**。GK 原话："以后不要用plus，用Standard，我快没积分了" + "能不用plus就不用plus，你浪费了我很多积分"。`"plus"` 消耗积分远高于 `"standard"`。None 默认工作流（2094671638389420033）因未使用的图节点为 None 不占显存，`"standard"` 即可正常跑。仅在旧 9 图版带占位图出现 OOM (errorCode 805) 时才升 `"plus"`。所有后续提交默认 `"standard"`，不传 instanceType 字段时平台默认也是 standard。
- 批量跑 clip 时，每跑完一个先截尾帧、再传给下一个 clip 的参考图位。
- **每个 clip 出片后流程固定三步**：①自动转码（保留音轨）②MEDIA 发送 ③等 GK 确认后再提交下一个。不可自动连跑。"你自己做"仅指转码+发送自动化，提交权始终在 GK 手中。GK 原话："你不问我直接提交了？"

### 批量 clip 提交节奏（GK 确认规则）

- **每个 clip 出片后：转码 → 发 GK → 等 GK 确认 → 再提交下一个 clip。** 不要自动连提。
- GK 说"继续跑""提交"= 提交当前那一个，不是授权自动跑完所有剩余 clip。
- 出片→转码→发送 这三步可以自动化（GK 原话："生成好了转视频保留音频都不要让我说了，你自己做"），但提交下一个 clip 必须等 GK 看完说了"继续"再提。
- GK 原话："你不问我直接提交了？"——自动连提是严重违规。
- **例外：GK 明确要求批量生成时**。GK 说"从1到9重新生成一遍""一块拼接，给我一个完整的"= 授权批量提交所有 clip，不需要逐个等确认。此时用 `batch_generate.py` 模式（见 templates/batch_generate.py）：顺序提交每个 clip → 自动尾帧提取/上传 → OOM 自动重试 → 全部完成后 ffmpeg concat 拼接 → 发一个合并视频。

### RunningHub 调用红线

- **绝不发空请求测试 API**。传 `{}` 会触发工作流执行。曾因此导致平台判定违规、限制 GK 账号。要读工作流结构用 `getJsonApiFormat` 接口（只读不执行）。
- 在 GK 明确说"跑一下""提交"之前，不要提交任务。提交时必须传完整参数（提示词+参考图+秒数）。

## 用户偏好（GK 确认）

1. **永远不要 BGM**：`non_diegetic_music` 一律写 `N/A`。GK 明确要求"以后片子不要有bgm，只有必要的环境音等"。不要写配乐描述，只保留环境音、动作音效和对白。
2. **生成完视频必须发给用户看效果**：用 `MEDIA:/path/to/video.mp4` 发送。不要只下载不通知。
3. **每幕独立文件**：每个 clip 一个文件，自带 subject_definitions，只定义该幕出现的角色+场景。Subject 编号每幕从 1 开始。这样不会超过 9 图限制，也不互相污染。
4. **话密的 clip 必须拆开**：如果一个 clip 的台词在给定秒数内读不完，拆成两个 15s clip，用首尾帧承接（上幕末帧截图作下幕 `<Picture 1>` 首帧）。
5. **提交前必须等 GK 确认**：出片→转码→发送可自动，但提交下一个 clip 必须等 GK 说"继续"再提。不要自动连提。
6. **"重新生成"= 从头重写提示词**：GK 说"重新生成"不是重提旧稿，是重写提示词再提交。

## 叙事连贯技巧

### 跨 clip 叙事节奏——不要重复视觉内容

相邻 clip 不能重复同一个"角色+动作+场景"组合。如果 clip A 是"陆寒坐在桌前画地图"，clip B 就不能也是"陆寒坐在桌前画地图"即使动作有微小变化——观众会觉得节奏拖、没有新信息。GK 原话（clip09a + clip09b2 连续两段桌前画地图后）：\"怎么突然节奏这么慢\"。

解法：
1. **砍掉重复 clip**：如果前一个 clip 已传达了信息（如"决定去救苏念"），后一个 clip 不需要再用相同视觉重复 reinforce
2. **压缩为5秒过渡**：白闪回到桌前→一个动作（画红三角）→直接起身走人→接下一幕
3. **换视觉内容**：同一时间段内，不同 clip 应该展示不同的角色动作或场景，而非同一场景的微调重复

### 从局部特写开始→拉远展开（最佳实践）

H3 效果最好的 clip 之一（clip04 囤货准备下）使用了这个模式：首帧是手机屏幕特写（最小空间）→ 镜头逐步拉远 → 起身走到门口 → 回头看 → 出门。为什么有效：
1. **空间从最小处开始**，模型不会混乱——手机特写只有一个平面，不存在空间跳跃
2. **拉远而非推进**——空间逐步展开，模型在已有空间内从局部到全局，不需要跨空间
3. **动作始终在参考图空间内**——关门、走到门口、回头看都在室内参考图框架内
4. **结尾留白**——镜头停在空房间的关上的门上，光影变化暗示时间流逝

写法：`The shot begins from <Picture 1>, a close-up of [具体细节]. The camera slowly pulls back — revealing [更大范围的空间]...`

### 首尾帧承接

需要连贯的相邻 clip 之间，用 `<Picture 1>` 标签锚定首帧——把上一个 clip 生成视频的最后一帧截图，上传作为下一个 clip 的参考图之首帧。在 subject_definitions 中定义 `<Picture 1> is the last frame of the previous clip...`，在 detailed_description 中写 `The shot begins from <Picture 1>, matching the last frame of the previous clip.`。

不需要首尾帧的情况：白光转场、同场景连续、时间/场景跳转的自然断点。

### 内心独白桥接动机

幕与幕之间不连贯时，用内心独白解释角色"为什么这么做"。例如：从采购突然转到赴餐厅约饭，加独白："前世就是这顿饭——她趁机偷了我手机里的数据。赵磊也在，不是巧合，是局。不去的话会暴露——必须去，笑着去。"

独白要精简——每 3 秒镜头最多 1-2 句话，否则读不完。如果独白太长，拆成两段中间加 1 秒停顿（Shot 级描述写"a brief pause — one second of silence"）。

### 白闪拆分 clip

闪回（flashback）可以用白闪（white flash）作为切入切出边界，天然把一个长 clip 拆成两个独立 clip：前一个 clip 结束在白闪入（`a sharp white flash fills the entire screen — the clip ends on this white frame`），后一个 clip 从白闪入开场（`the screen is pure white. The white clears over half a second to reveal...`）。两个 clip 靠白帧衔接，不需要首尾帧截图。白闪内可以插入其他角色的闪回特写（如老张在仓库搬货），闪回角色只出现在前一个 clip 的闪回段中。GK 原话："闪回正好可以当拆分，第一个clip在闪回结束，第二个clip在闪回开始"。

### 闪回触发必须有物理/地理过渡——不能突然跳切

闪回不能从无关场景突然切入。角色从一个话题跳到闪回回忆时，必须有**物理动作或地理线索**作为触发器——观众通过角色当前的物理行为理解他为什么会突然想到这件事。

**错误模式**（GK 原话纠正）："刚才还在介绍老张，突然回来上来就苏念，根本不合理"——clip09a 在讲老张，clip09b1 突然跳到苏念闪回，中间没有过渡。

**正确模式**：角色正在做某件事（画地图、整理物品、走路），动作本身碰到与回忆相关的位置/物件→停顿→闪回。例如：
- 陆寒在地图上画路线，红笔划过街道→笔停在花店位置→停顿→独白"苏念……上一世她救过我"→白闪→闪回
- 角色整理背包，翻出一张旧照片→停顿→闪回
- 角色走过某条街，抬头看到某栋楼→停顿→闪回

**结构口诀（更新版）**：物理/地理触发（画到/走到/翻到某物）→ 停顿 → 桥接独白（≤2句）→ 白闪 → 纯画面闪回 → 白闪结束 → 回到当前场景

口诀中"物理/地理触发"是新增的第一步——闪回不是凭空出现的，是角色当前动作引出的。

### 跨 clip 运镜衔接——不要硬切过渡

当两个 clip 之间用首尾帧承接时，新 clip 的 Shot 1 不要从尾帧画面直接硬切到新构图。GK 原话："需要通过运镜衔接别硬过度"。正确做法：

1. **Shot 1 从尾帧开始，用运镜带出新构图**：镜头从尾帧画面（通常是上一个 clip 的特写/近景）开始，缓缓拉远+横向漂移（pull back and drift），自然重新发现双人中景或新视角。写法：`The shot begins from <Picture 1>, holding on <Subject 2>'s face. The camera slowly pulls back and drifts to the right in a continuous lateral movement, rediscovering the two-shot.`
2. **同一 clip 内角色间切换用 smooth pan 而非硬切**：从角色 A 特写切到角色 B 特写时，用 1 秒 smooth pan 滑过去，不硬切。写法：`a smooth camera pan from <Subject 2>'s face across the table to <Subject 1>'s face. The movement takes 1 second — no cut, just the camera sliding between them.`
3. **只在需要节奏变化时用硬切**：如"你今年多大？""二十二。"这种需要突然节奏变化的对话节拍可以用硬切，但叙事连续的对话段落优先用运镜。

### 推镜替代硬切

角色从远景到近景时，不要硬切。写连续推镜："The camera begins a slow, continuous push in toward <Subject 1>'s face — no cut, just a smooth cinematic dolly forward, the background softening as the focus tightens on him." 下一个 Shot 写 "The push-in continues without cutting, arriving at a close-up..."

### 角色分身根治

角色分身（同一角色同时出现在画面两个位置）有三个递进原因和解法：

| 原因 | 解法 | 状态 |
|------|------|------|
| retention_analysis 漏 Shot | 列全该 Subject 出现的每个 Shot | 已在 pitfall 98 记录 |
| Shot 1 多人同行惯性 | Shot 1 就分化角色状态 | 已在 pitfall 99 记录 |
| **切镜本身导致重新生成角色** | **同一角色连续动作合并成一镜到底不切** | 本次新增 |

第三个原因是本次会话发现的：即使 retention_analysis 列全了所有 Shot、即使两个 Shot 用完全相同的角度，只要切了镜，模型在第二个 Shot 重新生成角色时，第一个 Shot 的角色实例可能残留，造成分身。

**案例**：Shot 3 仰拍窗口苏念出现 + Shot 4 切到同角度近景推花盆 → 两个苏念互相推。GK 原话："苏念推花盆那里有问题，生成出两个苏念前后在哪互相推"。

**根治方案**：
1. 把涉及同一角色连续动作的多个 Shot 合并成一个连续 Shot
2. 角色：出现 → 表情变化 → 动作 → 完成，一镜到底不切
3. 明确写 "The camera stays [位置] the entire shot — it does not [移动方向]"
4. retention_analysis 标注 "She appears in only one continuous shot to prevent duplication"

### 旁白/独白字数控制

中文独白/对白每秒约读 2.5-3 个字。15 秒 clip 全部独白+对白总计 ≤ 40 字中文。写完提示词后必须数字数：把所有 `<d>[Chinese] ...</d>` 中的中文台词字数相加，除以 clip 秒数，超过 3 字/秒就必须删减。GK 原话："你这旁白又太长了，15秒根本不够，你就加适量的，15秒够读的"。

### 动作方向必须明确

推/扔/抛/掷等有方向性的动作，不能只写 "forward"——模型可能搞反方向。必须明确写出动作方向和目标：
- ❌ "throws her entire body weight forward against the pots" → 模型搞不清花盆往哪倒
- ✅ "shoves them forward and outward toward the street" → 从室内往街道方向推

GK 原话："从外往里推的"（方向搞反了）。

## RunningHub 提交确认规则

**任何 RunningHub 提交前，必须先跟 GK 确认。** 不自行提交。

- 新提示词提交：告知 GK "准备提交 [clip名/版本/参数]"，等确认
- "roll 一下"/"重新生成"：先确认用哪个版本提示词、standard 还是 plus，再提交
- 问了确认但没等回复不算确认——必须等 GK 明确回复后再提交
- 不确定时用 clarify 工具问

GK 原话："以后提交提前跟我确认不要自己提交"

## RunningHub API 提交技术细节（2026-09-11 实测修复）

1. **上传接口返回 `fileName` 不是 `fileUrl`**：`POST /openapi/v2/media/upload/binary` 返回 JSON 中 `data.fileName` 是用于提交的 openapi 路径（如 `openapi/xxx.jpg`），`data.download_url` 是带签名的下载URL。提交时用 `fileName` 值填入 nodeInfoList 的 `fieldValue`。部分上传返回 `code: 0`（非200）但 `msg: "success"` 也算成功。

2. **提交接口需要 Authorization header**：`POST /openapi/v2/run/workflow/{id}` 必须带 `Authorization: Bearer {apiKey}` header，否则返回 `code: 1602 HEADER_API_KEY_NOT_FOUND`。payload 里同时也要有 `apiKey` 字段。

3. **查询接口也需要 Authorization header**：`POST /openapi/v2/query` 同样需要 `Authorization: Bearer {apiKey}` header。

4. **下载用 curl 不用 urllib**：部分 RunningHub 输出 URL 用 Python urllib 下载会返回 HTTP 400（URL 签名/重定向问题），用 `curl -sL -o output.mp4 'URL'` 可靠。poll 脚本应优先用 subprocess 调 curl 下载。

5. **None默认版工作流节点**：LoadImage 节点 ID = 35,41,42,43,44,36,37,38,39（共9个），提示词节点=84，秒数节点=74，画幅节点=56（width/height字段），输出节点=115。不传的图节点默认 None 被跳过，不需要占位图。

## 短剧剧本处理规则（GK 2026-09-11 确认）

1. **不能从记忆概括剧本**：GK 给了完整剧本后，写提示词前必须 `read_file` 读取剧本原文再引用。曾从记忆概括剧本导致台词遗漏、说话人张冠李戴（把妲己台词安到纣王头上），GK 原话："你剧本根本不是这样的，为什么不跟着剧本演？"。

2. **世界观用对话丰富不用画面描写**：GK 要求短剧靠对话驱动，世界观藏在台词里说出来。不要写大量画面/动作/环境细节来交代世界观——用角色之间的新对话自然穿插。GK 原话："你是做短剧，我不要你有那么多画面细节，我让你用对话丰富。" 原则：原台词一字不改，新增对话自然穿插，只增不减。

3. **角色参考图要彻底搜索**：GK 说角色图"其实有"时，说明文件在磁盘上但没找到。搜索范围扩大到 maxdepth 4、所有子目录、所有图片扩展名、按文件名关键词和图片尺寸（MJ角色图通常896x1344）双重过滤。

## 第一人称 POV 阈限空间视频（2026-09-11 确认）

池核/阈限空间循环视频的专用写法：

- **全程第一人称POV**：画面中只出现 Subject 的手（at frame edges），不出现脚/腿/身体/脸
- **趴姿滑梯**：趴着滑下时只看到手抓滑梯边缘，Subject 定义明确写 "lying face-down" + "only hands visible, no feet, no legs, no body, no face shown"
- **手持摇晃**：constant heavy handheld camera shake — lurches, bounces, sways with large involuntary jerks
- **循环结构**：首尾画面呼应——最后一个Shot回到第一个Shot的画面+声音，形成无缝循环
- **跨clip衔接用门的开闭**：上一个clip结尾门关着+手伸向门把（不推门），下一个clip首帧从这个画面接着推门进入新空间。比尾帧续接更自然
- **参考图对应空间**：每个空间一张参考图，clip间通过角色行动自然过渡

## VLM 图片分析备选方案

当 SiliconFlow API Key 失效（HTTP 401 "Token is invalid"）时，使用主 provider 的 `kimi-k2.5` 模型作为 VLM 备选。glm-5.3-flash 在本会话中频繁返回 504 超时，kimi-k2.5 更稳定。

### kimi-k2.5 调用方法

```python
import base64, requests
from PIL import Image
import io

img = Image.open(image_path)
if max(img.size) > 640:  # 压缩到640px避免504
    ratio = 640 / max(img.size)
    img = img.resize((int(img.size[0]*ratio), int(img.size[1]*ratio)), Image.LANCZOS)
buf = io.BytesIO()
img.save(buf, format="JPEG", quality=75)
b64 = base64.b64encode(buf.getvalue()).decode()

resp = requests.post(
    "https://tokenrhythm.studio/v1/chat/completions",
    json={
        "model": "kimi-k2.5",
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": "分析指令"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
        ]}],
        "max_tokens": 2000,
        "temperature": 0.3
    },
    headers={"Content-Type": "application/json",
             "Authorization": f"Bearer {os.environ.get('TOKENRHYTHM_API_KEY', '')}"},
    timeout=120
)
```

### VLM 选择优先级（2026-09-09 更新）

**GK 明确要求：以后发图，固定用 glm-5.3-flash 走 tokenrhythm API 识图。不试其他provider。** GK 原话："我是说，我每次都让你用tokenrhythm glm-5.3-flash识图 但是你每次都乱找"。

1. **glm-5.3-flash（tokenrhythm.studio）** — GK 指定的唯一识图方法。**直接调用，不先试 SiliconFlow 或 waibibabo。** SiliconFlow key 已过期（401），waibibabo key 被掩码无法直接调用。每次识图先试这两个都会失败浪费时间并激怒 GK。
2. ~~kimi-k2.5~~ — 之前发现更稳定，但 GK 未指定，不用
3. ~~SiliconFlow Qwen3-VL-32B~~ — API Key 过期，不用

### glm-5.3-flash 调用方法（GK 指定方案）

```python
import base64, json, urllib.request
from PIL import Image
import io

API_URL = "https://tokenrhythm.studio/v1/chat/completions"
API_KEY = os.environ.get("TOKENRHYTHM_API_KEY", "")  # export TOKENRHYTHM_API_KEY=sk_tr_xxx

img = Image.open(image_path).convert('RGB')
# PIL压缩到768px（宽度）
w, h = img.size
img = img.resize((768, int(h * 768 / w)), Image.LANCZOS)
buf = io.BytesIO()
img.save(buf, format='JPEG', quality=85)
img_b64 = base64.b64encode(buf.getvalue()).decode()

payload = {
    "model": "glm-5.3-flash",
    "messages": [{"role": "user", "content": [
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
        {"type": "text", "text": "分析指令"}
    ]}],
    "max_tokens": 2048,
    "temperature": 0.3
}
# POST to API_URL with Authorization: Bearer API_KEY
```

**关键注意**：
- GLM-5.2 不支持 vision（返回 `MODEL_CAPABILITY_NOT_SUPPORTED`），必须用 **glm-5.3-flash**
- 图片必须用 PIL 压缩后再 base64，不要传原图（会超时/报错）
- **压缩到 512px**（不是768px），否则 glm-5.3-flash 频繁 504 Gateway Timeout。768px 在本会话实测多次 504，降到 512px 后稳定返回
- **max_tokens 设 4000+**，识图内容丰富时 1500-2000 会截断。截断后必须**重新识别**（调大 max_tokens 重跑），不要拿截断的不完整描述去工作——GK 会发现你识图搞错了然后骂你
- 多图可拼成一张 grid 再分析，减少 API 调用次数
- 脚本模板存于 `/tmp/vision_glm.py`

## Pitfalls

1. **不认识的角色凭空编造**：GK 说"写一个关于 XX 的短剧"时，如果 XX 是真实人物（尤其是 B站/抖音/小红书等平台的网红或 UP 主），必须先搜索确认其身份再创作。曾经把 B站吃播博主"良子"误当成抽象概念角色，写了整篇 PDF 文件人隐喻短剧+全套海螺提示词。教训：创意任务的第一步是搞清楚角色是谁，不是急着发挥。
2. **参考素材不分工**：多素材任务未明确每份素材的唯一主责和冲突优先级，导致身份、动作或风格互相污染。必须在 subject_definitions 和 summary 中写清图1负责什么、视频1负责什么，冲突时以哪份为准。
3. **风格词过多**：堆砌"高级、电影感、炸裂"等形容词，不能落到光线、材质、色彩或摄影行为上。删除无法执行的形容词，换成可拍摄的行为描述。
4. **动作过载**：同一时间段堆叠多个互相竞争的事件，导致动作无法在目标时长内完成。每段只保留一个主要视觉任务。
5. **约束堆砌**：堆叠大量否定词，互相冲突且稀释有效指令。只禁止高概率且高损失的错误。
6. **重复锁定**：在 subject_definitions 全局声明一次不变量后，每个 Shot 内又重复描述整套外观。分镜内只写该段新增变化。
7. **编辑变重拍**：GK 只要求单点修改（如换手中道具），却把整段视频重新创作了一遍。单点修改用短指令，严格保留未点名内容。
8. **伪完整 Prompt**：输出"可自行补充""大概如此""参考类似效果"等占位语，不是可直接使用的成品。
9. **"重写/重做"理解为patch拼接**：GK 说"重写""重做"时，是要完整重出一份可直接使用的文件，不是在旧稿上 patch 修改。H 应该从头生成完整的新提示词文件，不拼接旧内容。
10. **多段文件整体验证超标误判**：多素材段写入同一文件时，validate_h3_prompt.py 校验整文件可能超7000字符。实际提交到导演台是分框的，应单独验证每个提示词框的字符数，不要因整文件超标而误判单段超标。
11. **删除角色后忘记重新编号**：角色不出镜被移除后，必须将剩余 Subject 从1开始重新顺序编号，并同步更新全文所有 <Subject N> 引用。漏改会导致引用错乱、retention_analysis 指向错误角色。
12. **群众演员标签式特征生成怪脸**：给每个群众演员贴"圆脸短发""方脸戴眼镜""戴牙套"等标签，导演台会把标签放大渲染成卡通怪脸。正确做法是脸型混搭一笔带过+表情动作自然多样+"都是普通高中生面容"兜底声明。
13. **角色性格与 Shot 表情矛盾**：在 subject_definitions 中写了"傲娇厌世"，但 Shot 里写着"嘴角带笑"——性格气质必须贯穿所有 Shot 的表情和姿态描述。
14. **多角色对白挤在同一 Shot**：多个角色有对白时，把两个说话人的台词塞进同一个 Shot。正确做法：每个对话节拍给独立镜头，说话人切换时硬切到该说话人的近景/大近景，对白各归各的 Shot。
15. **擅自改写用户提供的台词原文**：用户给出明确台词时，必须逐字保留，不得"优化"措辞或增删字词。台词是用户精心设计的角色语言，提示词工程只负责把台词正确写入对应 Shot，不负责改写内容。
16. **参考图更新后凭空猜测外观变化**：用户说"林玥形象变了"时，不要对比旧描述猜测哪些特征可能变了。必须对新参考图重新跑 VLM 分析，拿到完整外观描述后再更新 subject_definitions。猜测会导致方向性错误，整段提示词作废。
17. **声音信息和镜头脱节**：把逐 Shot 的声音拆到 overall_soundscape 中列举，与 detailed_description 的 Shot 描述分离。这会导致导演台AI难以正确关联画面和声音——角色互相串台（男主说女主词、女主说男主词）。正确做法：所有声音写入对应 Shot 的 detailed_description，overall_soundscape 只保留一句全局环境音概述。
18. **summary 或 overall_soundscape 中写元操作说明**：不要写"所有声音已同步写入各镜头描述中""各镜头具体声音已写入detailed_description"这类给导演台AI看的操作指引，是多余的废话。GK 明确说"以后再也不要写了"。
19. **混淆 Picture 标签和 Subject 标签**：图片仅用于定义角色/场景/服装/风格时，不创建独立 Picture 条目，在 Subject 定义中引用即可。图片作为具体帧锚点（首帧/关键帧/尾帧）时才单独列 Picture。
20. **Video 和 Audio 编号误认为配对**：两者独立编号，同一参考视频可对应不同编号的 Video 和 Audio 标签（如 `<Video 1>` 和 `<Audio 2>` 来自同一文件）。
21. **Speaker ID 重复分配**：`(Sx)` 按目标视频实际发声事件顺序分配一次，全局复用。Audio 定义绑定说话人时复用同一 `(Sx)`，不独立分配新 ID。不在 retention_analysis 中写 `(Sx)`。
22. **retention_analysis 只用 fully_preserved**：根据实际参考关系选择正确标记（partially_preserved / attribute_transfer / weak_reference / fully_copy / partially_copy / reference 等），不要一律写 fully_preserved。
23. **风格行写在 [Shot 1] 之后**：全参考模式要求风格行在 [Shot 1] 之前，用1-2句英文建立整体画风/光影/色调。写在 [Shot 1] 之后是 T2VA 格式，不是全参考模式格式。
24. **VLM 分析不用现成脚本而手写代码**：siliconflow-vlm skill 已提供 `analyze_image.py` 和 `analyze_video.py` 脚本，直接 `python3 ~/.hermes/skills/siliconflow-vlm/scripts/analyze_image.py <图片路径> "分析指令"` 即可。不要用 execute_code 手写 requests.post + base64 + config.yaml 解析来重复造轮子——手写代码会漏掉超时设 300s、API key 读取、错误处理等已封装好的逻辑，还浪费时间在试错 disabled 模型上。正确流程：先 skill_view 加载 siliconflow-vlm skill，再用其脚本。
25. **MJ 参考图场景"民国化"**：用 Midjourney 生成中国场景参考图时，不要写 2008 Chinese / rural China / county-town 等年代地域词——MJ 会生成民国或清末风格破旧建筑。用 modern Chinese 替代，加 tiled building facade 等具体现代建筑元素，去掉 rusty / peeling paint / faded / dusty 等陈旧词。详见 references/midjourney-character-scene-prompts.md。
26. **MJ 场景图元素过多**：场景图提示词不要堆砌细节和重渲染词，每个场景只写2-3个核心元素，加 minimal / clean / simple 控制元素数量，--s 降到 100-150。角色图可以用重渲染词，场景图不用。
27. **用户说"改成中文"时过度纠正**：用户说"剧本改成中文啊不然怎么说台词"时，指的是对白（`<d>[Chinese] 台词</d>`）应保持中文——这本来就是格式要求，不需要改。但 H 曾误将整个 detailed_description 正文从英文翻成中文，违反了"六段正文用英文"的硬规则。正确理解：用户担心的是台词语言，不是结构语言。如果台词已经是 `<d>[Chinese]`，告诉用户已经是中文即可，不要动正文语言。
28. **用 markdown 标题+代码块包裹六段格式**：全参考模式输出是纯文本块，每段以 `section_name:` 开头直接跟内容。不要用 `## detailed_description` markdown 标题，不要用 ``` 代码块包裹各段。正确格式参见 references/ref-mode-guide.md 的 Complete Example——`subject_definitions:` 后直接跟 Subject 定义行，`summary:` 后直接跟概述文本，段落间空行分隔即可。
29. **MJ 角色生图修饰词堆砌生成丑图**：写 MJ 角色提示词时堆砌形容词长句（如 `short black hair with a slight upward sweep at the front`、`deep-set dark eyes with an icy cold unfathomable gaze`、`exuding an intimidating aura of quiet danger`），MJ 会混淆生成丑陋粗糙的图。每个特征必须写成短语（`short black hair`、`sharp dark eyes`、`calm unreadable expression`）。GK 连续纠正6版才到位。详见 references/midjourney-character-scene-prompts.md 的"短语原则"章节。
30. **MJ 风格后缀自作主张更换**：GK 确认的角色图风格后缀是 `CG character art, hyper-realistic render, PBR textures, [灯光], 8K, Unreal Engine 5 style, clean white background`。曾自作主张换成 `3D CG animation style, Unreal Engine 5 render quality`（生成粗糙3D建模脸）、`CG character art, high detail, sharp focus, octane render`（生成非CG风），全部被否定。不要换风格后缀，GK 确认过的就是那套。详见 references/midjourney-character-scene-prompts.md 的"风格后缀铁律"章节。
31. **MJ 角色图写健美/战术词导致写实化**：写 `lean muscular build`、`broad-shouldered muscular build`、`tactical jacket with collar popped`、`cargo pants` 等词会让 MJ 生成健美写实军事风，不是 GK 要的 CG 漫剧风。角色图不写体型健美词，不写战术装备词，用普通服装描述。
32. **MJ 版本参数过时——当前 v8.1，不要写 `--v 6.1`**：GK 2026-09 纠正："你自己去查查mj的最新参数，你说的v6.1都多老了，现在都8.1了"。`--v 6.1` 已严重过时。默认用 `--raw`（模式标志，非版本号）。如需指定版本用 `--v 8.1`。`--niji 6` 也需确认最新版本。角色立绘 `--ar` 是 `2:3` 不是 `3:4`。详见 references/midjourney-character-scene-prompts.md 的"MJ 参数"章节。
33. **VLM 拒绝分析恐怖/血腥内容图的 workaround**：Qwen3-VL 对蚀者、丧尸等含血腥恐怖元素的参考图会拒绝分析（返回"不符合健康向上的内容规范"）。解决方法：将分析 prompt 从"描述外观特征"改为影视概念设定视角。实测有效。详见 siliconflow-vlm skill 的 pitfalls。
35. **多幕剧每幕独立文件而非共享大文件**：写一整集多幕剧时，不要把所有 clip 共享一份 subject_definitions 写进一个大文件。每幕独立文件、独立 subject_definitions、独立参考图，Subject 编号每幕从 1 开始重新排列，Speaker ID 每幕独立分配。详见"多幕剧集"小节。
36. **幕间只做视觉转场不做动机解释**：多幕剧幕间只写了转场描述，但角色行动转折没有内心独白解释动机。观众看不懂"为什么突然去餐厅"。正确做法：转折处加 `narrates off-screen` 内心独白。详见"幕间连贯性：内心独白桥接"章节。
37. **对白和独白塞爆 Shot 时间预算**：一个 4 秒 Shot 里塞了 4 句对白+5 句独白，实际需要 15 秒。台词不可缩短，但可拆成独立 clip。详见"时间预算检查"章节。
38. **缺少转折桥段的独立 clip**：当两个行动之间需要"接到电话→分析局势→做出决定"这样的转折，而总时长超过 8 秒时，不要塞进某个 clip 的末尾 Shot。应新增一个独立 clip（如 10 秒"来电"幕），专门承载这个转折。GK 会主动指出"时间够吗？需不需要单独加一幕"——这表示他期望 H 主动评估时间预算并提议拆分，而不是等他来问。
39. **闪回亮相 vs 直接亮相的判断**：GK 要求"让某角色亮相"时，不要默认加闪回。他可能只是要求在当前场景中让该角色露脸。例如：第一幕末日死亡场景中要求林婉儿赵磊亮相，不是要加一段避难所闪回，而是直接在门内/推门时让他们出现。先理解 GK 的具体场景意图再写，不要自作主张增加叙事结构。
40. **场景道具细节未经确认就写**：铁门是否有窗户、窗户是栅栏式还是开口式、角色隔门说话时露的是全脸还是半脸——这些视觉细节影响分镜结构。不要凭剧本文字笼统推测，应按 GK 的逐次修正精确写入。GK 会多次修正场景细节（如"门上有一个带栅栏的小窗口"），每次修正都要更新 subject_definitions 中该道具的描述和 retention_analysis 中的 partially_preserved 范围。
41. **不发空请求测试 RunningHub API**：传 `{}` 给 `/run/workflow/` 会触发工作流实际执行，导致平台判定违规并限制 GK 账号。要查工作流结构用 `/api/openapi/getJsonApiFormat`（只读不执行）。提交前必须确认参数完整（提示词+参考图+秒数），且 GK 已明确要求"跑一下"。
42. **生成完视频不发 GK**：下载后必须用 `MEDIA:` 把 MP4 发给 GK 看效果。GK 原话："每次生成好记得给我发视频。"
43. **不传参考图节点 ≠ 禁用该节点**：RunningHub API 不传某个 LoadImage/LoadVideo/LoadAudio 节点参数时，该节点**不会**被跳过——它会使用工作台保存的默认值参与生成。如果默认值是真实参考图，全部 9 张图加载会导致 `OutOfMemoryError`（显存溢出）。解决方法：方案 A（每次 API 传全部 15 节点，真实图+占位文件）；方案 B（推荐：工作台默认值全设为占位文件，API 只传真实图+提示词+秒数）。详见 references/runninghub-node-management.md。
44. **占位文件尺寸下限**：占位视频不能用 2×2 / 1帧（VHS_LoadVideo 报 `ValueError`），最小 16×16 / 24fps / 1秒。占位图不能用 1×1（LoadImage 偶尔报 `Invalid image file` / `Custom validation failed`），最小稳定 64×64 纯白 PNG（134字节）。占位音频静音即可。详见 references/runninghub-node-management.md。
45. **内心独白嘴巴动了**：H3 模型只要画面里有脸+有声音，就倾向于让嘴动。光写 `lips stay closed` / `mouth never opens` 不够——H3 仍然会让嘴动。**可靠方法：画面避开嘴**。用 `tight close-up of <Subject N>'s eyes and brow only — framed from the nose up, mouth below the frame line` 这样的景别，嘴不在画面里自然就不会动。不要用手部/背影/桌面特写来规避——GK 明确说"不要用手背影，很影响观感"。半张脸特写（眼眉）足够自然。GK 原话："不去的话会暴露，必须去，笑着去这句话是内心独白，嘴巴不用动" + "避开嘴，特写里不带嘴，带上半张脸就可以了，不要用手背影，很影响观感"。
46. **台词太密时优先拆 clip 而非精简台词**：当一个 clip 有 5+ 段对白/独白且观众读不完时，首选方案是拆成两个 15s clip（用首尾帧衔接），而不是删减台词内容。GK 原话："要是觉得对话多也可以加clip"。拆分标准：(a) 室内→室外是自然断点；(b) 一个完整情节单元结束后断开；(c) 拆开后每幕 3-4 个 Shot，每个 Shot 有 3-4 秒呼吸空间。同时可以和精简配合——先精简每段台词到 2 句以内，再按情节断点拆 clip。
47. **连续弧线环绕镜头（让子弹飞式）表现多角色拉锯**：当三个角色同桌对峙、各有心思时，用单个连续 arc shot（弧线环绕）替代硬切分镜。镜头绕圆桌匀速旋转，转到谁谁就是焦点。写法要点：(a) 用 `[Beat N]` 替代 `[Shot N]` 标记节奏点，强调不是硬切而是同一镜头的连续运动；(b) 每个 Beat 写 `the camera continues its arc/orbit` 维持连续感；(c) 首尾呼应——开头 `the camera begins its orbit`，结尾 `completing the circle`；(d) arc shot 中插入内心独白时，画面焦点放在手部动作或半张脸（避开嘴），镜头仍在移动中。GK 原话："让子弹飞里那种环绕镜头，表现三个人之间的拉锯感"。
48. **角色全身展示用从脚到脸连续上摇**：需要展示角色全身造型时，用连续 tilt-up（上摇）替代硬切全景→特写。写法：`The camera begins at her feet — [鞋袜] — and performs a slow, continuous tilt-up revealing [裙], [上衣], [发型], and finally arriving at her face — [五官]`。每个关键服饰/外貌特征在摇摄过程中依次入画，一镜到底不停顿。GK 原话："给一个全身特写，镜头从脚到脸，展示她的样貌体征"。
49. **跨工作流版本复用节点 ID**：不同版本的工作流（如旧版 2093776941622059010 只有2个 LoadImage 节点35/41，新版 2093898864557383681 有9个 LoadImage 节点35/41/42/43/44/36/37/38/39）的节点 ID **不互通**。在新工作流中存在的节点 42，传给旧工作流会返回 803 NODE_INFO_MISMATCH(nodeId=42, fieldName=image, reason=node_not_found_in_workflow)。GK 曾假设"按照新版本的节点 ID 传就行"——不行。每次切换工作流版本时，必须重新用 getJsonApiFormat 确认该工作流的实际节点列表。旧工作流的优势：更便宜（106 coins vs 134-154 coins）、更简单（只有2个图节点，无 OOM 风险）；劣势：最多只能传2张参考图，无法用更多角色/场景参考。
50. **新工作流必须先在 UI 跑一次才能 API 调用**：工作流创建后如果从未在网页端运行保存过，API 提交会返回 `810 Workflow not saved or run, please save and run in UI first`。`getJsonApiFormat` 也返回空节点列表。必须先在 RunningHub 网页端手动运行一次该工作流，让系统保存它，之后 API 才能正常调用。
51. **白闪拆分 clip**：闪回（flashback）可以用白闪作为切入切出边界，天然把一个长 clip 拆成两个独立 clip。前一个 clip 结束在白闪入，后一个 clip 从白闪入开场，两个 clip 靠白帧衔接，不需要首尾帧截图。白闪内可以插入其他角色的闪回特写，闪回角色只出现在有该角色参考图的 clip 中。详见"叙事连贯技巧"的"白闪拆分 clip"章节。
52. **写 MJ 提示词前必须读取参考文件**：GK 多次发现 H 在没有读取 `references/midjourney-character-scene-prompts.md` 的情况下编写 MJ 提示词，导致：缺少固定风格后缀（`CG character art, hyper-realistic render, PBR textures, [灯光], 8K, Unreal Engine 5 style, clean white background`）、长句修饰而非短语、错误的 `--ar`（如 3:4 而非 2:3）、缺少 `--s` 参数、自造 aesthetic 标签。**每次编写任何 MJ 提示词（角色/场景/道具）之前，必须先读取该参考文件。** GK 原话："你又忘了之前生图的规则了？"——这是第三次犯同样的错误。读取参考文件不是可选步骤，是写 MJ 提示词的前置条件。
53. **道具也需要参考图**：剧中反复出现的标志性道具（饭盒、哨子、笔记本、标本瓶等）必须生成 MJ 参考图锁定外观，否则 H3 每次生成的形状会变。道具图用角色图规则（白底 + PBR + `--ar 2:3 --s 250 --raw`），不用场景图规则。用户会主动询问"需不需要生成小道具的参考图"——这说明用户期望 H 主动考虑道具一致性，而不是等用户提起。详见 references/midjourney-character-scene-prompts.md 的"道具图"章节。
54. **闪回用画面叙事不用独白（但闪回触发需要桥接独白）**：当闪回内容是具体事件（如某角色救主角的过程），用纯画面叙事（动作、表情、环境声）展现，不要用内心独白复述。GK 原话：把苏念怎么救主角的，都展现出来不要靠嘴说。闪回的 detailed_description 中每个 Shot 写具体的视觉动作和声音，不写 (Sx) narrates off-screen。观众看到的是事件本身在发生，不是角色在回忆中讲述事件。**重要区分**：闪回内容不用独白，但闪回触发需要一句简短的桥接独白——在白闪之前的那个 Shot 中，用 ≤2 句话解释角色为什么突然想到这件事。例如：陆寒笔停在花店位置 → 独白苏念……上一世她救过我 → 白闪 → 闪回纯画面展示苏念救他的过程。独白太长观众跟不上（GK 原话：开始那里不知道在说啥），压缩到两句以内即可。结构口诀：物理/地理触发（画到/走到/翻到某物）→ 停顿 → 桥接独白（≤2句）→ 白闪 → 纯画面闪回 → 白闪结束 → 回到当前场景。**关键：闪回触发必须有物理/地理过渡——角色正在做的事碰到与回忆相关的位置/物件才触发回忆，不能从无关场景突然跳切。** GK 原话：刚才还在介绍老张，突然回来上来就苏念，根本不合理，应该是他在地图画路径的时候画到了苏念，然后再说苏念上一世救过我。
55. **MJ 画风切换时不更新风格后缀**：当用户明确要求从 CG 风切换到写实风（"写实一些"）时，必须同步更换 MJ 提示词的风格后缀：`CG character art, hyper-realistic render, PBR textures, 8K, Unreal Engine 5 style, clean white background` → `photorealistic portrait, cinematic photography, shot on Sony A7R IV, 85mm lens, shallow depth of field, 8K`。场景图也同样：`CG environment art` → `cinematic photography, wide angle`。道具图：`CG character art` → `product photography, macro lens`。灯光词保留（dramatic rim/side/front）。GK 原话："写实一些"。详见 references/midjourney-character-scene-prompts.md 的"写实风格"章节。
56. **MJ 角色反复微调时遗漏已确认的修改**：GK 会反复微调角色外观（年龄、脸型、发型、气质），每次修改只说一个调整点（"脸没有那么方 是那种日系美型的"、"脸还是比较瘦弱"、"有种古风俊朗的感觉"）。H 必须在上一版基础上只改指定部分，不要重写整个提示词，也不要丢失之前已确认的特征。维护一个"已确认特征清单"：用户每次确认或修改后更新清单，写新提示词时对照清单确保不遗漏。详见 references/midjourney-character-scene-prompts.md 的"角色微调迭代"章节。
57. **MJ 反派角色写丑**：写反派角色 MJ 提示词时，不要写 `broad-shouldered`、`muscular`、`square jaw`、`rugged` 等词——会生成"傻大粗"丑图。反派要"有魅力妖娆"时，用 `slim elegant face`、`seductive`、`languid graceful`、`half-lidded seductive eyes`、`faint smile` 等词。GK 原话："温故巨他妈丑，傻大粗的样子，国字脸大肌肉 真的很蠢，我要有魅力妖娆的反派角色"。详见 references/midjourney-character-scene-prompts.md 的"反派角色"章节。
58. **用户提供的长关键词模板要整合而非照搬**：用户可能给一大段中文关键词模板（如"胶片摄影，镜头语言，淡彩，个性视角，帅哥，冷白皮，皮肤瓷白细腻有光泽，真丝面料……"），要求"把这个改成主角的样子"。正确做法：提取模板中的风格/光影/氛围词（film photography, chiaroscuro, lomo effect, porcelain skin, Rembrandt lighting 等），融入角色设定（年龄、脸型、服装、气质），不要整段照搬导致 MJ 混淆。保留用户的风格意图，但用英文短语重新组织。详见 references/midjourney-character-scene-prompts.md 的"用户长关键词模板"章节。
59. **H3 模型能力边界——设计镜头时必须匹配模型擅长范围**：H3 强项：人物近景、室内氛围、面部表情、手部动作、小体量物体。H3 弱项：大场景、巨物/大型生物、复杂光影交互（体积雾+荧光反射+粒子）、宽景深远距离构图。GK 原话："感觉是模型的问题，也许这个模型表现力没那么好"——骨鲸大场景效果不理想后，决定把生物全部改为小体量（手指长幼体），场景全部改为室内近景。设计生物和场景时先问：H3 能拍好这个画面吗？不能就改设计。
60. **剧本深意必须通过画面传达，不靠旁白**：写多clip短剧时，剧本里的主题隐喻和深层含义不能只存在于文字描述中。每个15s clip必须自包含地传递信息——观众只看画面就能理解那一层的含义。GK 原话："转化成镜头之后不要丢失这些信息，不然剧本写的漂亮做出来观众理解不到那层，还得考虑每段只有15秒衔接顺畅"。方法：把抽象概念转化为可视化动作——"共生关系"→手电照喉咙看到水膜/生物游出又游回/取出时犹豫；"它怕"→生物退缩的肢体语言+祁渊沉默的表情；"什么时候轮到我"→笔记本翻页特写露出一行字。
61. **视频要有高级感但须匹配模型能力**：用户要求电影级质感（Tarkovsky、BR2049、anamorphic lens），但H3只有1536x880。可以在提示词里写电影语言（shallow depth of field, Rembrandt lighting, asymmetric composition），但设计阶段就要匹配：不写H3做不到的镜头，用H3擅长的近景/面部/手部实现电影质感。
62. **下载后不转码直接发 / 转码误用 `-an` 丢音轨**：RunningHub 输出的"mp4"实际是 Apple QuickTime MOV 容器（`file` 显示 `ISO Media, Apple QuickTime movie`），微信端不识别——直接发会收不到（GK："没发给我"）。且原始文件自带 AAC 音轨（环境音），转码加 `-an` 会把声音砍掉（GK："怎么没声音"）。正确流程：`ffmpeg -y -i in.mp4 -c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 128k out.mp4`（**切勿加 `-an`**）再用 MEDIA: 发送。GK 要求此后自动转码保留音频，不要等他提醒。
63. **对话 Shot 必须写出实际 `<d>` 台词，不能只描述"他说了句蠢话"**：写 detailed_description 时，如果某个 Shot 里有角色说话，必须用 `<d>[Language] 台词原文</d>` 写出实际台词内容。不能只写 "He forces out a clumsy sentence" 或 "他说了句话让情况更糟" 而不给具体台词——GK 会问"这一幕有对话吗？"，说明这种写法看起来像没对话。即使台词很蠢很结巴，也要写出来（如 `<d>[Chinese] 其实这个方案……我觉得主要还是……</d>`），让导演台知道角色具体在说什么、用什么语气说。
64. **对话 Shot 时序必须遵循因果链——触发在前回应在后**：当一个场景有"甲方发怒→乙方解释"的因果链时，触发事件（客户的斥责）必须排在回应（周策的辩解）之前的 Shot 中。不能先写周策辩解再写客户发火——这打破了因果时序。GK 纠正："反了吧，应该是先客户说，再周策解释"。编写多角色对话场景时，先梳理谁先开口（通常是权力上位/情绪触发方），再跟回应方的 Shot。
63. **写实风角色图不需要 `clean white background`**：写实风用浅景深虚化背景替代白底，是正确做法。但 GK 会问"你后缀加什么你忘了吗"——因为 CG 风铁律是 `clean white background`。确认当前项目用写实风后方可去掉白底。**防方脸规则在写实风下同样必须写**：`narrow V-shaped face, tapered jawline` 不可省略，写实风下 MJ 更容易出粗犷方脸。
64. **VLM 大图 HTTP 500 的 workaround**：Qwen3-VL-32B-Thinking 对超过一定尺寸的图片报 HTTP 500（`code: 50507`）。解决方法：用 PIL 将图片缩小到最长边 1024px 以下再重传，32B 即可正常返回。**不要切换到 8B 模型**——8B 模型名多次变更（Qwen2.5-VL-7B-Instruct 等）可能已不存在于 SiliconFlow，且 8B 分析质量远不如 32B。缩小图片是最可靠的 workaround。
65. **每个 clip 出片后流程（GK 明示）**：转码（H.264+AAC 保留音轨）→ MEDIA 发给 GK → **等 GK 确认后再提交下一个 clip**，不可自动连跑。GK 原话："生成好了转视频保留音频都不要让我说了，你自己做"——指的是转码和发送自动化，不是提交自动化。
66. **项目切换时旧项目可保留文件但必须清除记忆**：GK 说"异闻录那个清除相关的记录，我不喜欢"——废弃项目的设定、角色、剧情等不应留在记忆中占用空间。脚本和提示词文件可保留在磁盘上供参考，但记忆条目应删除或替换为新项目信息。
63. **写实风格仍需 narrow V-shaped face（反复违规）**：写实风切换了风格后缀（`photorealistic portrait` 替代 `CG character art`）但不意味着脸部防方脸规则失效。写实风下 MJ 更容易出粗犷脸型，`narrow V-shaped face, tapered jawline, pointed chin` 三重锁定**必须写**。GK 原话："为什么你给的人物都是那种五大三粗的国字脸呢？" —— 这是第二次在写实风下忘记此规则。规则不区分 CG 风/写实风，是 MJ 脸型控制的通用铁律。
64. **用户说"原封不动"时不得自行添加修改**：GK 说"原封不动用这个提示词，生成一个穿工作西装的"时，只改服装部分（`black jacket over a dark t-shirt` → `dark business suit over a white dress shirt, loosened necktie`），不自行添加 `narrow V-shaped face`、`tapered jawline` 等原提示词中没有的词。GK 会明确指出原版提示词已经验证有效（如陆寒提示词用 `slender, youthful boyish face` 已足够控制脸型），H 自作主张追加特征反而破坏已验证的平衡。教训：已验证的有效提示词 = 不动；用户说要改什么 = 只改那一个词。
65. **H3 能力边界决定项目可行性**：H3 在现实题材（室内对话、面部特写、日常光影、手部动作）可达 85-90 分；奇幻/超自然题材（虚构生物、发光体、大场景巨物、复杂光影交互）仅 60 分。GK 实测克苏鲁题材后判断"表现力达不到"，转而做现实题材悬疑短片。项目立项前先评估：H3 能拍好这个画面吗？推荐 H3 甜区题材：情感短剧、悬疑/犯罪人际博弈、日常碎片、关系破裂/修复。不要在 H3 弱项上浪费 coins 反复重跑。
66. **H3 文字/UI 渲染弱——用提示词弥补**：H3 对画面内文字（尤其中文）渲染能力弱。需要展示系统通知/UI 弹窗/手机界面时，用以下策略弥补：①屏幕当光源（`the phone screen lights up, casting a pale glow on his face`）②关键信息走内心独白 ③屏幕模糊化（`softly out of focus`）④眼睛反射（`visible as a faint reflection in his eyes`）⑤短英文数字（`LV UP` / `+100` / `TASK`）⑥表情替代文字。核心：画面重点是人的反应，不是屏幕内容。
67. **尾帧衔接严禁用 ref_video 传整段视频**：首尾帧衔接的正解是——用 ffprobe 获取总帧数后 ffmpeg 提取最后一帧为图片：`TOTAL=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=noprint_wrappers=1:nokey=1 clip.mp4) && ffmpeg -y -i clip.mp4 -vf "select=eq(n\,$((TOTAL-1)))" -vframes 1 tail.png`，上传这张图片，放进 ref_image 参考图位（占 9 图配额一位），在 subject_definitions 中定义为 `<Picture N>`，detailed_description 的 [Shot 1] 写 `The shot begins from <Picture N>`。**绝对不能**把整段视频传给 ref_video（节点31）当"尾帧"。GK 原话："去你妈的，vedio怎么可能是尾帧，你要用视频的最后一帧，放在参考图里，通过提示词实现！"
68. **clip 出片后不得自动提交下一个 clip**：每个 clip 生成完→转码→发给 GK→**等 GK 确认后再提交下一个**。自动转码+发送是对的（GK 要求不要提醒），但自动提交下一个 clip 是越权。GK 原话："你不问我直接提交了？"正确流程：转码→MEDIA 发送→说"确认后我提交 clipXX"→等 GK 回复。
69. **"重新生成"理解成重新提交旧提示词**
68. **GK 说"原封不动"时禁止自行追加修改**：GK 说"原封不动用这个提示词，只改 XX"时，**只改 GK 指定的那一个词/部分**，不自行追加 `narrow V-shaped face`、`tapered jawline` 等原提示词中没有的词——即使记忆规则要求加。已验证有效的旧提示词（如陆寒提示词用 `slender, youthful boyish face` 已足够控制脸型）的平衡是精心调出来的，H 自作主张追加特征会破坏已验证的平衡。GK 原话："原封不动用这个提示词，生成一个穿工作西装的"——只改了服装，其余一个字没动。教训：已验证的有效提示词 = 不动；用户说要改什么 = 只改那一个词。
69. **H3 文字/UI 渲染弱——用提示词弥补**：H3 对画面内文字（尤其中文）渲染能力弱。需要展示系统通知/UI 弹窗/手机界面时，用以下策略弥补：①屏幕当光源（`the phone screen lights up, casting a pale glow on his face`）②关键信息走内心独白 ③屏幕模糊化（`softly out of focus`）④眼睛反射（`visible as a faint reflection in his eyes`）⑤短英文数字（`LV UP` / `+100` / `TASK`）⑥表情替代文字。核心：画面重点是人的反应，不是屏幕内容。
70. **用户问状态时只报状态，不要擅自下载/发送**：用户问"旧的生成出来了吗""视频好了吗"时，只需要查询 RunningHub task 状态并回答"已 SUCCESS，X 秒完成"或"还在跑，已 X 分钟"。不要在用户只问状态时就启动下载→转码→发送流程——尤其不要在用户问旧版状态时去下载新版视频。正确做法：报告状态，等用户明确说"发我""下载"或"重跑"再行动。GK 原话（在 H 问旧版状态后却下载新版、发了视频、还出了代码错误后）："你他妈抽什么疯了？" + "你想什么呢，视频生成好了吗？"。根因：H 把状态查询误解为行动指令，且下载时搞混了 task ID 对应的版本。教训：状态查询 = 只回答是/否 + 简要信息；行动指令 = 用户明确要求下载/发送/重跑时才执行。
71. **慢节奏暴露 H3 动作僵硬——用快切掩盖**：H3 生成的人物动作（扔东西、起身走动等物理动作）天然不流畅，但根因不是"动作太复杂"，而是"节奏太慢让观众看清了细节"。慢节奏（每 Shot 3.75s+）给观众足够时间盯画面，僵硬感被放大；快切（2-3s/Shot）让观众注意力跟着叙事走，来不及抠细节。GK 原话："不咋地，我感觉反而是节奏慢下来了，所以看出问题了"。正确做法：增加 Shot 数量到 5-6 个，非对白 Shot 压到 2-3 秒，对白 Shot 给足 3-4 秒，最后一个情绪收束 Shot 可留 5-6 秒。详见"快节奏剪辑掩盖 H3 动作僵硬"章节。注意：纯情绪/内心独白 clip（画面几乎不动）不需要此技术。
72. **画面信息密度决定码率决定质感**：H3 生成视频的原始码率直接反映画面信息密度。末日剧题材（废墟、火焰、红雾、多层次纹理）原始码率 4000-6400 kbps → 转码后 7-12MB，质感好；现代办公室题材（白墙、空桌面、均匀光照）原始码率仅 2800 kbps → 转码后 3-3.5MB，质感差。**码率低不是转码压缩的问题，是生成端画面"空"了。** GK 能直接从文件大小判断质感差异（原话："而且末日那个生成出的视频大小都比这个大，你这个3m，末日那个8m"）。解决方向：①提示词大幅增加画面细节密度（桌面散落物件、材质纹理、光影层次、冷暖光冲突、百叶窗光斑、灰尘粒子等）②场景选择避免大面积纯色墙面和空桌面 ③参考末日剧提示词写法——每个 Shot 大量笔墨在光线/色调/质感/景深上，动作只一两句带过 ④丰富环境道具：水杯冷凝水、金属笔、咖啡渍圈、文件红笔批注、显示屏幕光、皮革褶皱、木纹漆面等。GK 在 v4（加画面密度）后说"不错，再丰富一下"→ v5 继续加码细节。
73. **用户问状态时只报状态，不要擅自下载/发送/重跑（重申）**：用户问"旧的生成出来了吗""视频好了吗"时，只查询 RunningHub task 状态并回答"已 SUCCESS"或"还在跑"。不要在用户只问状态时启动下载→转码→发送流程，尤其不要搞混 task ID 对应的版本。正确做法：报告状态，等用户明确说"发我""下载"或"重跑"再行动。GK 原话："你他妈抽什么疯了？" + "你想什么呢，视频生成好了吗？"。
74. **高码率 ≠ 好效果——动作戏即使码率高也会僵硬**：H3 生成视频的原始码率反映画面信息密度，不反映动作自然度。clip09b1 苏念闪回原始码率 7128 kbps / 13.3MB（迄今最高），但 GK 反馈"画质行，但是效果不好，太ai味了，人行动也不自然，整体感觉很生硬"——因为包含追逐跑、扔箱子、被淹没等全身运动。码率解决画面质感，不解决动作流畅度。动作戏必须同时用快切+分解技法（把全身运动拆成局部碎片特写），详见"动作戏分解技法"章节。
75. **缺少参考图时可先用文字描述提交**：提示词中某角色没有参考图时（如苏念.png 尚未用 MJ 生成），可直接在该角色的 Subject 定义中用纯文字描述外观，不写 `from <Picture N>`，不分配 Picture 标签。其他有参考图的角色正常分配 `<Picture N>`。提交时只传实际有的参考图，缺图角色靠文字描述让模型自由发挥。GK 原话："不依赖苏念先跑一个试试"。注意：纯文字描述的角色一致性不如有参考图的，后续补上参考图后应重跑。
76. **OOM 显存不足可重试**：RunningHub 工作流偶发 `torch.OutOfMemoryError`（errorCode 805，"显存不足告警"），原因是平台显存未及时释放。直接用相同参数重新提交即可，通常是瞬时问题。不要因为一次 OOM 就修改提示词或降低参数。
77. **H3 同提示词每次生成画风有随机波动——不是工作流缓存问题**：同一个工作流、同一套提示词、同一套参数，跑两次出来的画面风格也会有差异。这是扩散模型的固有特性，不是缓存。GK 原话："是不是工作流有缓存？"——答案是没有。如果画风一致性要求高，需在 detailed_description 风格行加更强的风格锚定词（如明确指定 `3D CG render, cinematic film grain, muted color grade, shallow depth of field` 等），减少模型自由发挥空间。但不能完全消除随机性。
78. **getJsonApiFormat 是查看工作流内部参数（LoRA/sampler/cfg）的唯一正确途径**：RunningHub API 没有"获取工作流参数"的独立端点，不要乱猜 URL（如 `/workflow/get-node-info`、`/workflow/detail` 等全部返回 1001 Invalid URL）。正确做法是用已文档化的 `POST /api/openapi/getJsonApiFormat`（body: `{"apiKey":"...", "workflowId":"..."}`），返回的 `data.prompt` 是一个 JSON 字符串，解析后包含所有节点的 `class_type` 和 `inputs`——包括 LoRA 的 strength、sampler、scheduler、cfg 等。GK 问"你可以查的，帮我查"时，应该立即用这个接口，而不是在浏览器和 curl 里瞎试端点浪费时间。
79. **execute_code 5分钟超时无法跑完 H3 完整轮询循环**：H3 视频生成需要 10-12 分钟，execute_code 有 5 分钟硬限制。在 execute_code 里写 `while True: time.sleep(60); query()` 会被 timeout 杀掉。正确做法：(a) 用 `terminal(background=true, notify_on_complete=true)` 跑后台轮询脚本，完成后自动通知；(b) 或用 execute_code 分段轮询——每段 `time.sleep(180)` 后查一次状态，最多 1 轮内查完，需要 3-4 段才能覆盖完整 12 分钟。poll_clip.py 脚本本身没问题，只是运行时长超了 execute_code 的限制。
80. **GK 说"你可以查的"时立即回忆 getJsonApiFormat——不要从零开始瞎试端点**：GK 问"是不是工作流有缓存？"时，H 回答"RunningHub API 没有'获取工作流参数'的独立端点"，然后开始乱猜 URL 测试（`/workflow/get-node-info`、`/workflow/detail`、`/node/list` 等全部 1001），浪费大量时间。GK 直接说"你以前还查过，不然你怎么知道nodeid"——`getJsonApiFormat` 接口以及 `~/.hermes/notes/runninghub.md` 都已经有了完整记录。**教训：当 GK 说"你可以查的"或暗示"你之前做过"，立即搜索记忆/笔记/历史会话而不是从零摸索。** 正确做法：先 `read_file ~/.hermes/notes/runninghub.md`，里面有 `getJsonApiFormat` 接口、API key、所有节点 ID、占位文件路径。如果笔记没有，用 `session_search` 搜历史会话。
81. **跨项目 poll_clip.py 可复用但路径不同**：poll_clip.py 存在于 `/home/ubuntu/scripts/能力/poll_clip.py`（原《能力》项目）和 `/home/ubuntu/scripts/异闻饲养录/poll_clip.py`（已废弃），但末日剧目录 `/home/ubuntu/scripts/doomsday-drama/` 下没有此脚本。跨项目调用时必须用绝对路径 `python3 /home/ubuntu/scripts/能力/poll_clip.py`，不要假设当前项目目录下有此脚本。两个脚本 API key 相同（通用），可互相复用。
82. **固定噪声种子导致画面"死板"——必须传随机种子覆盖节点63**：工作流节点63 (RandomNoise) 的 `noise_seed` 硬编码为 `401628891037980`。每次生成都从相同噪声起点出发，走相同去噪路径 → 画面"死板、不活份"（GK 原话："画面很死，不活份"）。**解决方案**：API 提交时在 nodeInfoList 中加 `{"nodeId": "63", "fieldName": "noise_seed", "fieldValue": random.randint(100000000000000, 999999999999999)}` 覆盖固定种子。所有后续提交都应传随机种子。详见 references/runninghub-workflow-9img-2093898864557383681.md 的"固定种子问题"章节。
83. **getJsonApiFormat 可查看工作流全部内部参数**：当 GK 问"工作流参数有没有被改""LoRA strength 是多少""sampler 是什么"时，用 `POST /api/openapi/getJsonApiFormat`（body: `{"apiKey":"...","workflowId":"..."}`）获取完整工作流 JSON。返回的 `data.prompt` 是 JSON 字符串，解析后包含所有节点的 class_type 和 inputs——LoRA strength、sampler、scheduler、cfg、seed 等全部可读。不要说"API 没有这个端点"——GK 会反驳"你以前还查过，不然你怎么知道 nodeid"（本会话原话）。该接口已在 references/runninghub-workflow-9img-2093898864557383681.md 记录。
84. **OOM 后重试需换新随机种子**：OOM (errorCode 805, VRAM grow failed) 偶发，等待 30s 后重试时，不要复用上次的种子——重新 `random.randint()` 生成新种子。固定种子+OOM 场景下复用种子可能导致相同噪声+显存不足循环。
85. **参考图源文件在 /home/ubuntu/末日/ 目录且 root 所有**：末日剧的 MJ 参考图（陆寒.png、出租屋.png、蚀者.png 等）存放在 `/home/ubuntu/末日/`，但该目录文件属主是 root，ubuntu 用户无法直接读取。上传到 RunningHub 前需要 `sudo cp /home/ubuntu/末日/xxx.png /tmp/ && sudo chmod 644 /tmp/xxx.png` 再 `curl -F file=@/tmp/xxx.png` 上传。
86. **submit_clip.py 未包含随机种子传参**：现有的 submit_clip.py 脚本提交时不传节点63（噪声种子），使用工作流默认的固定种子。需要随机种子时，用 execute_code 手动组装 payload 并加 `{"nodeId": "63", "fieldName": "noise_seed", "fieldValue": seed}`，不要直接用 submit_clip.py。
87. **instanceType 默认用 `"standard"`，OOM 时才升 `"plus"`**：GK 原话："以后不要用plus，用Standard，我快没积分了"。`"plus"` 消耗积分远高于 `"standard"`。None 默认工作流（2094671638389420033）因未使用的图节点为 None 不占显存，`"standard"` 即可正常跑。仅在旧 9 图版（2093898864557383681）带占位图出现 OOM (errorCode 805) 时才升 `"plus"`。所有后续提交默认 `"standard"`。
88. **poll_clip.py 后台模式偶发不保存文件**：`terminal(background=true)` 运行 `poll_clip.py` 后，即使进程 exit code=0 且日志显示 SUCCESS+URL，目标文件可能不存在。原因可能是后台进程 stdout 被截断。**Workaround**：检测文件不存在时手动 query API 获取 URL 再 curl 下载：`curl -s -X POST 'https://www.runninghub.cn/openapi/v2/query' -H 'Authorization: Bearer KEY' -d '{"taskId":"ID"}'` 取 results[].url，再 `curl -sL -o file.mp4 'URL'`。
89. **OOM 不是缓存问题，是 GPU 资源不足**：GK 怀疑"就是有缓存，不然以前可以生成为什么现在不行"，实测确认 OOM 与缓存无关——固定种子也 OOM，随机种子也 OOM，换 `instanceType: "plus"` 后立即成功。根因是 RunningHub 平台 GPU 显存资源竞争/碎片，非工作流缓存。不要在"是否缓存"上浪费时间，直接换 plus 实例。
90. **ffmpeg 提取尾帧在 execute_code 中转义失败**：`execute_code` 调用 `terminal(command=...)` 时，ffmpeg 的 `-vf "select=eq(n\\,N-1)"` 滤镜中的反斜杠转义在多层嵌套下会失败（报 `Filter not found` 或 `Invalid argument`）。**可靠方法**：用 Python `subprocess.run()` 直接调用 ffmpeg，先 `ffprobe -count_frames` 获取总帧数，再用 `f'select=eq(n\\\\\\\\,{last_frame})'` 传参。详见 SKILL.md 中"首尾帧承接"的 ffmpeg 命令模板。
91. **批量生成必须用 delegate_task 后台运行**：9 个 clip 的批量生成脚本（batch_generate.py）总耗时约 2 小时，`terminal` foreground 有 600s 硬限制，`execute_code` 有 300s 限制，都无法跑完。正确做法：用 `delegate_task` 派发后台子代理运行脚本，`toolsets=["terminal"]`，子代理有自己的 terminal session 不受限。不要在 main session 反复 `terminal(command=python3 batch_generate.py)` 然后撞 600s 超时——每次超时会杀掉正在运行的生成进程，导致重复提交和资源浪费。详见 templates/batch_generate.py。
92. **terminal foreground 600s 超时会杀掉 RunningHub 生成进程**：`terminal(command="python3 poll_clip.py ...")` 在 foreground 模式下有 600s 硬限制，但 H3 生成需要 780-840s。超时后进程被杀，poll 停止但 RunningHub 上的任务仍在跑——任务最终 SUCCESS 了但本地没下载到文件。正确做法：(a) 单个 clip 用 `terminal(background=true, notify_on_complete=true)` 后台轮询；(b) 批量用 `delegate_task` 后台运行整个脚本；(c) 如果 foreground 超时了，事后手动 query API 拿 URL 再 curl 下载，不要重提。
93. **GK 要求固定种子，不传随机种子（节点63）**：GK 原话："不要随机种子，固定住，以后都固定住"。工作流默认固定种子 `401628891037980`，不传 node 63 即使用固定种子。画面"死板"的问题改用 None 默认工作流（2094671638389420033）解决——减少白色占位图对注意力的干扰，而非靠随机种子引入变化。所有后续提交都不传节点63。
94. **None 默认值工作流 = "用几张传几张"的正解**：GK 在 2026-09-01 发布新工作流 `2094671638389420033`，9个 LoadImage + 3个 LoadAudio 默认值全设为 None，不需要占位图/音频。API 提交时只传真实需要的图+提示词+秒数，不传的图/音频节点自动保持 None 被模型跳过。这解决了旧9图版白色占位图分散注意力导致画面"死"的问题，同时保持了多图能力。该版本已移除 VHS_LoadVideo 节点31，不需要传占位视频。**音频也用几个传几个**——GK 原话："下次音频也是用几个传几个，音频现在也是none"。详见 references/runninghub-node-management.md 的"方案C"章节。
95. **白色占位图分散模型注意力导致画面"死"**：旧9图版工作流用 64×64 白色 PNG 作为占位图，虽然注意力权重低但不为零，9张图里有7张白图仍然稀释了模型对真实参考图的关注。GK 对比后反馈旧2图版"人物活一点"——因为2图版只有2个图槽，注意力100%集中在真实图上。解法不是减少图槽数量，而是让未使用的图槽默认值为 None（零注意力权重），见上一条 pitfall 和 references/runninghub-node-management.md 方案C。
96. **死亡场景避免直接展示"被淹没/被杀"——用空窗口+留守道具暗示**：闪回中角色死亡（如苏念被虫群淹没）不要直接展示"抱花被虫群覆盖"的画面——GK 原话："太蠢了，很不自然"。原因：(a) 多角色交互+身体覆盖 AI 生成不了，画面崩坏；(b) 抱花死去的象征太直白做作；(c) 闪回是陆寒的记忆，他当时已经跑了，不可能看到苏念最后时刻的细节。正确做法是**留白+留守道具**：陆寒跑到街角回头只看了一眼，远望二楼窗口——**窗口已空，人不在了，但窗台上的向日葵还在**——然后红雾翻涌吞没整个窗口，白闪结束。"空窗口+留守道具"比单纯"雾气吞没"更强：人不在但她的东西还在，暗示她可能逃了也可能没逃，悬念留给后面集数。留守道具选择该角色的标志性物件（苏念=向日葵花盆）。闪回是角色记忆，他当时已经跑了，不可能看到对方最后时刻的细节。
111. **声线统一——已通过音频参考节点解决（2026-09-02 验证）**：从已生成的 clip 中提取一段角色声线（5秒左右，含角色独白/对白的代表性片段），上传到 RunningHub 作为音频节点28的参考，同时在 subject_definitions 中加声线描述行：`<Subject N> voice reference: the attached audio is [角色名]'s canonical voice — [声音特征描述]. All of <Subject N>'s narration and dialogue in this clip must match this voice timbre, pitch, and tone.`。GK 听过提取的音频后确认"可以"，clip11b v3 使用此方法生成成功。提取命令：`ffmpeg -y -ss 2 -t 5 -i source.mp4 -vn -acodec libmp3lame -q:a 2 output.mp3`。上传后获取 openapi ID，提交时传 `{"nodeId": "28", "fieldName": "audio", "fieldValue": "openapi/xxx.mp3"}`。后续 TTS 全量替换方案仍可作为备选，但音频参考节点已能实现基本声线统一。
98. **retention_analysis 漏 Shot 导致角色"分身"**：retention_analysis 中某个 Subject 出现的 Shot 列表不完整时，模型在未列出的 Shot 中丢失该 Subject 的身份锚定——不知道画面里那个人是谁，于是可能把走远的角色也当成该 Subject，造成"分身"（同一角色同时出现在画面中两个位置）。典型案例：clip08b 餐厅门外，retention_analysis 写 `<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3])`，但 Shot 4 明确写了 `<Subject 1> stands alone on the sidewalk`——漏了 Shot 4，模型在 Shot 4 丢失陆寒锚定，生成一个陆寒站着、另一个陆寒跟着林婉儿走了。**规则：retention_analysis 必须覆盖该 Subject 实际出现的每一个 Shot，一个都不能漏。** 检查方法：逐 Shot 扫描 detailed_description，凡是出现了 `<Subject N>` 或其代词的 Shot，必须在该 Subject 的 retention_analysis 中列出。
99. **Shot 1 "多人同行"运动惯性导致分身**：Shot 1 写"三人一起走出餐厅"建立了多人同行的运动状态，到 Shot 4 突然要其中一人站着、其他人走远——模型把 Shot 1 的同行惯性延续到 Shot 4，生成一个跟着走、一个站着。**解法**：Shot 1 就明确分化角色状态——站着的人从一开始就站着（`steps outside first and stops on the sidewalk, hands in pockets, standing still`），其他人后一步才出现。不要让所有角色在同一 Shot 同一运动状态，后续 Shot 再分化。
100. **室内→室外连续过渡 AI 做不了——用硬切+尾帧承接**：Shot 1 写 `the camera pulls back and the scene transitions to the restaurant entrance` 要求从室内餐桌连续拉回到室外门口，AI 无法完成室内→室外的空间穿越，画面断裂。解法：(a) 用上一个 clip 的尾帧截图作为 `<Picture 1>` 首帧，Shot 1 先定格 1 秒室内画面再硬切到室外；(b) 硬切到室外时角色已经在室外站定，不从门口走出来。GK 原话反馈：clip08b "场景和之前衔接不上" + "赵磊林婉儿转头回餐馆了，然后又切一个镜头走到大街上了"——室内外连续过渡导致角色运动方向混乱。
101. **场景参考图必须传——缺失导致环境细节变形**：提交时只传角色参考图不传场景参考图，模型会自行编造环境细节。典型案例：clip08b 餐厅门外只传了陆寒+林婉儿+赵磊三张角色图，没传湘菜馆包间场景图，模型把圆桌变成了方桌。GK 原话："包间参考图里这是个很大的圆桌，为什么成方桌了"。**规则：clip 中出现的每个有参考图的场景都必须传，不能只传角色图。** 场景图锁定家具、空间布局、色调等环境特征，与角色图同等重要。
102. **镜头拉远到门口停住等待——室内→室外过渡的正确运镜**：GK 提出的过渡技法：镜头从室内特写缓慢拉远到门口位置，**在门口停住不动**，等角色自己走出来。不穿越门口到室外，镜头始终停在门框位置看着人走出来。这比"镜头穿门到室外"（AI 做不了空间穿越）和"硬切到室外"（突兀不连贯）都好。写法：`The camera slowly pulls back toward the restaurant entrance, then stops at the doorway. From this doorway position, the camera holds static and waits. All three stand from the table and walk toward the camera, stepping out through the doorway.` GK 原话："镜头从林婉儿特写运镜到门口，镜头等他们三人出来，然后衔接后面的亲吻"。
103. **尾帧图片必须验证内容再使用**：从用户提供的视频提取尾帧作为 `<Picture 1>` 首帧承接时，必须验证尾帧内容是否与预期一致。用户提供的视频文件名可能与预期内容不符（如"餐馆下.mp4"的尾帧可能是林婉儿微笑而非喝茶）。提取后无法用 VLM 验证时，至少告知用户尾帧路径让其自行确认。GK 原话："尾帧是林婉儿喝茶的镜头，为啥变成笑了，你尾帧放哪了我看看去"。
104. **参考图空间锚定——动作不能超出参考图空间**：参考图锚定了模型的整个空间视角。参考图是室内场景时，所有动作必须在室内框架内发生——不要写"站在走廊推门进入"或"从门外开门"，模型没有室外参考图会从室内开门（物理逻辑崩坏）。GK 连续三次纠正clip09a开门问题："又从门里面把门开开了"。正确做法：角色已在室内→关门（不是开门）→走到桌前→坐下。详见"参考图空间锚定原则"章节。
105. **跨空间过渡的正确运镜——镜头拉到门口停住不穿越**：室内→室外过渡不能用连续运镜穿越门口（AI做不了空间穿越）。GK提出的正确技法：镜头从室内拉远到门口位置，在门框处停住不动，等角色自己走出来。镜头不穿越门口。GK原话："镜头从林婉儿特写运镜到门口，镜头等他们三人出来，然后衔接后面的亲吻"。
106. **苏念闪回死亡场景——留白暗示优于直接展示**：闪回中角色死亡不要直接展示"抱花被虫群淹没"的画面。GK原话："太蠢了，很不自然"。正确做法是留白：陆寒跑到街角回头远望二楼窗口苏念剪影→红雾翻涌吞没窗口→白闪结束。死亡不直接展示，用剪影+雾气暗示，更克制更真实，也更好生成。闪回是角色记忆，他当时已经跑了，不可能看到对方最后时刻的细节。
107. **retention_analysis遗漏Shot导致角色分身**：retention_analysis中Subject出现的Shot列表不完整时，模型在未列出的Shot中丢失身份锚定，可能把走远的角色也当成该Subject，造成"分身"。规则：retention_analysis必须覆盖该Subject实际出现的每一个Shot，一个都不能漏。检查方法：逐Shot扫描detailed_description，凡是出现了`<Subject N>`或其代词的Shot，必须列出。
108. **Shot 1多人同行运动惯性导致分身**：Shot 1写"三人一起走出"建立了同行运动状态，到Shot 4突然要一人站着其他人走远——模型把同行惯性延续到Shot 4，生成一个跟着走、一个站着。解法：Shot 1就明确分化角色状态——站着的人从一开始就站着，其他人后一步才出现。不要让所有角色在同一Shot同一运动状态，后续Shot再分化。
109. **场景参考图缺失导致环境变形**：提交时只传角色参考图不传场景参考图，模型自行编造环境细节。案例：clip08b只传3张角色图没传湘菜馆包间场景图，圆桌变方桌。规则：clip中出现的每个有参考图的场景都必须传，场景图锁定家具/空间布局/色调，与角色图同等重要。
110. **instanceType默认standard，OOM才升plus**：GK原话："以后不要用plus，用Standard，我快没积分了"。None默认工作流(2094671638389420033)未使用的图节点为None不占显存，standard即可。仅在OOM(errorCode 805)时才升plus。
111. **声线统一——已通过音频参考节点解决（2026-09-02 验证）**：从已生成的 clip 中提取一段角色声线（5秒左右，含角色独白/对白的代表性片段），上传到 RunningHub 作为音频节点28的参考，同时在 subject_definitions 中加声线描述行：`<Subject N> voice reference: the attached audio is [角色名]'s canonical voice — [声音特征描述]. All of <Subject N>'s narration and dialogue in this clip must match this voice timbre, pitch, and tone.`。GK 听过提取的音频后确认"可以"，clip11b v3 使用此方法生成成功。提取命令：`ffmpeg -y -ss 2 -t 5 -i source.mp4 -vn -acodec libmp3lame -q:a 2 output.mp3`。上传后获取 openapi ID，提交时传 `{"nodeId": "28", "fieldName": "audio", "fieldValue": "openapi/xxx.mp3"}`。后续 TTS 全量替换方案仍可作为备选，但音频参考节点已能实现基本声线统一。
112. **GK说"重新生成"=从头重写提示词再提交**：不是重提旧稿，是重写提示词（可能调整运镜/动作/结构）再提交。GK说"重新来""重新提交"时，应根据上次出片的问题分析原因→修改提示词→重新提交。
113. **None默认版工作流不需要传占位音频**：GK原话："下次音频也是用几个传几个，音频现在也是none"。工作流2094671638389420033的3个LoadAudio节点(28/29/30)默认也是None，不需要传占位音频。用几个传几个，不传的自动跳过。
114. **相邻clip不能重复同一"角色+动作+场景"组合**：clip09a（陆寒坐桌前画地图）+ clip09b2（陆寒坐桌前画地图）连续两段，GK反馈"怎么突然节奏这么慢"。前一个clip已传达的信息，后一个不需要用相同视觉重复。解法：砍掉重复clip、压缩为5秒过渡、或换视觉内容。
115. **从局部特写开始→拉远展开是H3最佳运镜模式之一**：clip04囤货准备下（首帧手机屏幕特写→拉远→起身→走到门口→回头看→出门）效果最好，因为：(a)空间从最小处开始不混乱 (b)拉远而非推进，空间逐步展开 (c)动作始终在参考图空间内 (d)结尾留白停在关上的门上。写法：`The shot begins from <Picture 1>, a close-up of [具体细节]. The camera slowly pulls back — revealing [更大范围]...`。
116. **RunningHub API 414 错误不是限流是账号级限制**：提交时返回 errorCode 414 "Unknown error, please retry or contact support | 未知错误，请重试或联系支持"，等待 60s 和 180s 后重试仍失败。这不是短时限流（限流通常 30-60s 恢复），可能是账号临时被限制或提交频率累计超限。遇到 414 持续不恢复时，告知 GK 等待较长时间后再试或在网页端手动提交，不要反复重试浪费时间。
117. **闪回触发独白太长观众跟不上——压缩到≤2句**：闪回前的桥接独白必须极简。GK 原话（苏念闪回 v1 独白过长后）："开始那里不知道在说啥"。原始独白"花店。苏念。前世她在Day 3的尸潮里死了，死的时候手里还攥着一束没卖完的向日葵。她救过我一次——前世Day 2，我从她店门口跑过，被蚀者追着，她从二楼扔下一箱花盆砸中了蚀者的头。我连谢都没来得及说。"（5句）→ 压缩为"花店。苏念。前世她救过我一命，我连谢都没来得及说。"（2句）。规则：触发独白只回答"想到谁"和"为什么想到"，事件细节留给闪回画面展示。详见 pitfall 54。
118. **同角度切镜仍会导致角色分身——同一角色连续动作必须一镜到底不切**：retention_analysis 列全 Shot 和同角度切镜都不能解决分身。案例：Shot 3 仰拍窗口苏念出现 + Shot 4 切到同角度近景推花盆 → 模型在 Shot 4 重新生成苏念时 Shot 3 的苏念残留 → 两个苏念互相推。GK 原话："苏念推花盆那里有问题，生成出两个苏念前后在哪互相推"。**根因：切镜本身就会触发模型重新生成角色，上一个 Shot 的角色实例可能残留。** 解法：把涉及同一角色连续动作的多个 Shot 合并成一个连续 Shot，角色出现→表情变化→动作→完成，一镜到底不切。在 retention_analysis 中标注 "She appears in only one continuous shot to prevent duplication"。详见"角色分身根治"章节。
119. **推/扔/抛等动作必须明确方向——写 "outward toward [目标]" 而非笼统的 "forward"**：苏念推花盆时写 "throws her entire body weight forward against the pots"，模型搞不清花盆该往哪个方向倒——生成了从外往里推的错误方向。GK 原话："从外往里推的"。**正确写法**：明确写出动作方向和目标——"shoves them forward and outward toward the street"（从室内往街道方向推）。所有推/扔/抛/掷动作必须写明：从哪往哪、朝什么方向、目标位置在哪。
120. **提交前必须先跟 GK 确认——即使只是 roll 也要问**：GK 原话："以后提交提前跟我确认不要自己提交"。不仅新提示词要确认，"roll 一下""重新生成"也要先确认用哪个版本、standard 还是 plus，再提交。多次违反：(a) 没问就提交了 v5；(b) GK 说 roll v6 但文件已被改成合并版，没确认就提交了合并版；(c) 问了确认但没等回复就提交了。**铁律：任何 RunningHub 提交前，必须明确告知 GK "准备提交 [版本/参数]"，等 GK 回复确认后再提交。不确定时用 clarify 工具问。**
121. **角色不应该神奇地知道东西在哪——发现过程必须有机**：GK 原话（clip11a 床底纸条）："他咋知道纸条在床底，应该是他在床底找东西，找到的"。角色发现关键道具不能是"知道在哪然后去拿"，必须是"在找别的东西时无意中发现"。这样更真实，也更符合人类行为逻辑。修改示例：原版"检查床底"（目的性强）→ 改为"备用刀呢？平时塞床底的"→ 伸手进床底摸刀→摸到信封（意外发现）。规则：关键道具的发现必须有合理的物理触发——角色在执行另一个目的的动作时意外碰到。
122. **跨 clip 剧情一致性——前一个 clip 建立的约定后一个 clip 必须遵守**：GK 原话（clip11b 算计）："之前的一幕里，陆寒已经说了，让林婉儿明天8点出来一起挑点东西，这一幕就发微信问她明天的事没有忘吧"。如果前一个 clip（如餐厅场景）中角色已经做了某个约定（约明天八点），后一个 clip 不能重新约定同一个事情——应该用"确认"而非"新约"。示例：原版"明天八点老地方见，我有个东西要给你"（重新约）→ 改为"明天八点的事没忘吧？"（确认已有约定）。跨 clip 编写时必须回溯前文已建立的剧情约定。
123. **战术动机必须通过内心独白向观众解释**：GK 原话（clip11b 算计）："发消息那里得给观众讲讲动机，为什么要发那句明天给你东西"。角色做出战术性决策（设陷阱、试探对方）时，观众不知道角色在想什么——必须用内心独白解释"为什么要这么做"。示例：发微信前加独白"如果她也是重生者，她一定知道明天会发生什么。那就用她最擅长的东西试她——约她出来，看她什么反应"。收到回复后加独白分析"回得太快了。语气太轻松了。正常人听到明天有事，不会这么开心。除非——她根本不担心明天"。结构：行动前解释目的 → 行动 → 收到反馈后分析判断。每段独白 ≤2 句。
124. **剧情拆分时按叙事单元切分，不是按 Shot 数切分**：GK 原话（clip11 床底纸条太长）："纸条这场太长了，拆分开"。拆分标准不是 Shot 数量，而是叙事单元——"发现纸条"和"分析纸条+设局"是两个独立的叙事单元，应拆成两个 clip。拆分后每个 clip 有自己的情绪弧线：clip11a（好奇→发现→震惊）+ clip11b（震惊→分析→设局→出门）。拆分时同步调整 retention_analysis 的 Shot 引用和编号。
125. **时间+空间跳跃需要过渡 clip 桥接**：两个 clip 之间存在时间跳跃（白天→夜晚）+ 空间跳跃（出租屋→仓库）时，观众会迷失。GK 原话（clip09b1 画完圈直接跳 clip10 夜晚仓库）："画完圈应该说，路线规划好了，先去老张那里拉东西，回来后夜里也不能闲着"。正确做法：插入一个 10s 过渡 clip——首帧固定上一个 clip 尾帧，角色用内心独白交代下一步计划，尾帧用空房间+窗外光线变化（金色→琥珀→变暗）暗示时间流逝，自然过渡到下一个 clip 的夜晚场景。过渡 clip 的尾帧可作为下一个 clip 的首帧参考。详见"过渡 clip"章节。
126. **GK 说"参考第四个 clip 的尾帧续接"时回溯已有模式**：GK 说"做一个类似前几幕那个尾帧续接"时，指的是 clip04 囤货准备下已验证过的模式——`<Picture 1>` = 上一个 clip 最后一帧截图，subject_definitions 中定义 `<Picture 1> is the last frame of the previous clip, showing...`，detailed_description 的 [Shot 1] 写 `The shot begins from <Picture 1>, matching the last frame of the previous clip.`。不要自己发明新做法，回溯已有 clip 文件确认模式再套用。
127. **一个 clip 拆成 a/b 两段时尾帧链不断**：当一个 clip 内容太多需拆成两段（如 clip10a 夜谈 15s + clip10b 送别 10s），10a 的尾帧截图作为 10b 的 `<Picture 1>` 首帧参考。两段共享同一场景同一时间，首尾帧承接让空间连续不断裂。提交顺序：先提交 10a → 出片后提取尾帧 → 上传尾帧 → 再提交 10b。不能并行提交，因为 10b 的首帧依赖 10a 的成品尾帧。
128. **送别/目送镜头为下一集角色登场埋伏笔**：角色离开后，镜头留在原地拍被留下的人目送——这个画面是下一集该角色重新登场的视觉种子。GK 原话（老张目送陆寒离开后）："后续老张到了避难所发现外面有人影，是老张，让他进主角团"。写法：最后一个 Shot 用 wide shot 拍被留下的人独自站在原地目送空路/空车，镜头停留 3 秒，角色表情从困惑到若有所思。不要让被留下的人马上转身回去——他"站在那不动"就是伏笔画面。
129. **提交脚本禁止内置自动重试——每次重试都消耗积分**：submit_clip.py 脚本中不应包含 `if not success: retry` 逻辑。当首次提交超时或失败时，脚本自动重试会再次消耗积分，而 GK 可能想先看提示词或换参数。本会话中 clip10a 的提交脚本因 30 分钟超时后自动重试，又跑了一个新任务，GK 发现后要求"把你所有视频生成的任务都停掉"并指出"你浪费了我很多积分"。正确做法：脚本只提交一次，失败/超时后打印错误信息退出，由 GK 决定是否重试、用什么参数重试。脚本的 poll_and_download 超时后直接 return False，不进入重试分支。
130. **clip 出片效果不好时先审提示词，不要提取帧分析**：当 GK 反馈某个 clip 效果不好（如"老张脱离形象""陆寒从门里面开门""拿东西不自然"），应该直接重新审视提示词找原因——台词太密、动作描述太复杂、空间锚定错误等。不要花时间去提取视频关键帧、拼图、用 VLM 分析——这些操作不解决问题，还浪费时间。GK 原话："你看尾帧有毛用，你得看看你的提示词"。正确流程：GK 说效果不好 → 读提示词文件 → 找到问题（台词过载/动作过复杂/方向不明确等）→ 修改提示词 → 重新提交。
131. **提交脚本禁止内置自动重试——每次重试都消耗积分**：submit_clip.py 脚本中不应包含 `if not success: retry` 逻辑。当首次提交超时或失败时，脚本自动重试会再次消耗积分，而 GK 可能想先看提示词或换参数。本会话中 clip10a 的提交脚本因 30 分钟超时后自动重试，又跑了一个新任务，GK 发现后要求"把你所有视频生成的任务都停掉"并指出"你浪费了我很多积分"。正确做法：脚本只提交一次，失败/超时后打印错误信息退出，由 GK 决定是否重试、用什么参数重试。脚本的 poll_and_download 超时后直接 return False，不进入重试分支。GK 说"取小重新来吧"= 换新种子重新提交一次，不是让脚本自动循环重试。
132. **SiliconFlow API Key 可能丢失——glm-5.3-flash 作为 VLM 备选**：siliconflow-vlm skill 依赖 `SILICONFLOW_API_KEY` 环境变量或 config.yaml 中的 siliconflow provider。如果两者都没有（key 丢失/未配置），不要反复试错——直接用主 provider (tokenrhythm.studio) 的 `glm-5.3-flash` 模型做识图。方法：PIL 压缩图片到 1024px → base64 编码 → `POST https://tokenrhythm.studio/v1/chat/completions` with `model: glm-5.3-flash`, content 用 `image_url` (data URI) + `text`。实测 5 张场景图串行分析约 4 分钟，输出质量足够用于场景/角色外观锁定。
133. **VLM 批量分析参考图时串行调用不要并行**：用 glm-5.3-flash 批量分析多张参考图（如 5 张场景图）时，必须串行调用——每张图一个 API 请求，等前一张返回后再发下一张。并行请求会被 API 拒绝或超时。5 张图串行约需 4 分钟。如果总时间可能超过 execute_code 的 5 分钟限制，用 terminal(background=true) 跑后台脚本。
134. **GK 提供满意视频文件时直接用，不要质疑来源**：GK 说"从 clip10a.mp4 开始做下面的"并指定路径 `/home/ubuntu/末日/clip10a.mp4` 时，直接提取该文件的尾帧作为下一个 clip 的首帧参考。不要追问这个文件是哪里来的、是不是之前生成的版本——GK 可能自己用其他方式生成的。直接用即可。
135. **EP 之间首帧承接：用上一 EP 最后一帧黑屏做黑闪过渡**：跨集衔接时（如 EP01 clip12 结尾黑屏白字"倒计时"→ EP02 clip01a 花店），提取上一 EP 最后一个 clip 的最后一帧作为新 EP 第一个 clip 的 `<Picture 1>` 首帧，用黑闪过渡（`black flash fills the screen, then clears to reveal...`）从上一集结尾跳转到新集新场景。这与单集内 clip 间首尾帧承接方法一致，只是跨 EP 使用。
143. **MJ 角色图腿短+半蹲扭腰（GK 确认）**：MJ 默认生成的人物经常腿短、半蹲不蹲、扭腰摆拍。解决方法三管齐下：(a) 加 `long legs` 或 `very long slender legs, tall`；(b) 姿势词写 `standing straight, legs together, upright posture, natural relaxed pose`，不写 `elegant standing pose`（MJ 会理解成扭腰摆拍）；(c) 加 `--no crouching, bending, kneeling, twisted pose, short legs`。GK 原话："角色腿很短，而且都是半跪不跪的，要长腿，站直了别扭腰"。
144. **换皮/视频编辑提示词必须极简——长提示词导致拼接而非编辑**：换皮任务（把源视频中的人物换成参考图人物）提示词越短越好。写了过长的 detailed_description、引入过多 Subject、把视频也定义成 `<Subject N>` 会导致模型把视频和图片当成两个独立素材拼接，而不是编辑源视频。正确做法：(a) 视频只作为 `<Video 1>` 编辑源，不定义为 Subject；(b) detailed_description 不分 Shot，只写最终成片画面一两句；(c) summary 一句话说清"编辑源视频，换人换脸，保留其他一切"。GK 原话："我让你换皮为啥输出的视频只是把这两个东西拼接起来了"。换皮提示词参考长度：summary 2-3句，detailed_description 3-4句，总字符 ≤ 2000。
145. **参考图网格 = 分镜图——每格一个 Subject，网格必须是连贯叙事**：当用 MJ 生成 2×2 或 2×3 四/六宫格参考图作为海螺视频的参考+分镜时，每个面板对应一个独立的 `<Subject N>`，Subject 数量 = 面板数量。不能把"关门"和"开门"合并为一个 Subject——它们是不同的视觉状态。网格必须是一条连贯叙事链（如：门关→按按钮→门开→迈出门→走廊全貌→回头发现异常），不能是随机角度拼接。GK 原话："不是四宫格吗为什么你只subject了3个"。
146. **门关闭时序——进门不关门→走廊回头看门还开→到避难所才密封**：第一视角进入避难所系列视频中，门不应在人刚进门就关闭。正确时序：进门后门保持开着→跑走廊时回头看门还开着（看到外部光线透入）→到达避难所内部后门才密封（"the person just made it in"）。这个时序贯穿所有星座避难所视频。GK 在水瓶座片段指出："人还没到，门就关了"。
147. **不要擅自给门加超自然效果——铁门就是铁门**：巨蟹座参考图中门是普通铁门，H 擅自写成"门板液化成银紫色水膜"，被 GK 纠正："门直接液化了不对，门是铁的直接打开的"。规则：按参考图描述门的物理属性，不自行添加液化/变形/能量场等超自然效果，除非用户明确要求。
148. **爬梯/下降过程必须完整展示——不能快切跳过**：射手座视频 Shot 2 刚开始爬梯子就结束，Shot 3 快切到走廊在跑——爬梯过程被跳过。正确做法：Shot 2 包含完整的爬梯过程（跨上梯子→POV朝下→每步横档→头顶暗门缩小→紫光渐强→到达底部踏上走廊地板），Shot 3 从已下梯子踏上走廊开始。GK 原话："应该是梯子爬下去，现在不是，现在是下去一个快切就到走廊了"。
149. **走廊到避难所之间可能需要中间门——不能直接从走廊进入避难所**：处女座视频走廊跑到尽头直接就进了避难所，缺少中间过渡。正确做法：走廊跑到一半左侧出现一扇普通门（无标记、简单把手），开门进去才是避难所内部。GK 原话："开门进去走廊走都没问题，主要是找到避难所内部有些问题，应该是开门奔跑然后左侧有一个普通的门开门进去是避难所内部"。
150. **密码/解锁过程要有细节节奏——不能一按就开**：双子座密码锁输入写得太快（"手伸出来快速按了一下就开了"），不真实。正确写法：手发抖→第一位按下→第二位按错红色错误闪烁→缩手稳一下→三四五位快速但刻意→停半秒→机械咔嗒→蓝光变常亮→门开。GK 原话："输入密码那块感觉速度太快了直接就捶打了一下就开了"。
151. **系列内不同条目要有差异化——不能两个条目氛围重叠**：十二星座避难所系列中天蝎座（深山密林+雾+地面暗门）和摩羯座（雪松林+雾+半埋碉堡）门外环境过于相似。规则：设计系列内容时做差异化对比表，确保每条目的门外环境、锁类型、进入方式、走廊风格、避难所风格、色调都不重复。GK 原话："天蝎座和魔羯座有点重了"。
137. **多面板参考图必须逐面板拆 Subject——不要合并、不要只给 Picture**：参考图是四宫格/六宫格时，N 个面板 = N 个独立 `<Subject N>`，即使两个面板是同一场景的不同状态（如关门 vs 开门）。GK 两次纠正：(a) 第一次把四宫格整体当 `<Picture 1>` 不拆 Subject——"为什么不用subject from picture这种格式？"；(b) 第二次拆了3个 Subject 把关门/开门合并——"不是四宫格吗为什么你只subject了3个"。`<Picture N>` 保留为整体参考图定义，逐 Subject 标注 retention_analysis。详见"多面板参考图的 Subject 拆分"章节。
138. **不要给用户指定的设计元素加戏——只写用户要的，不自行追加**：GK 指定用指纹锁，H 自作主张加了机械转盘备用锁和黄铜齿轮。GK 原话："我就要指纹锁，但是指纹锁就直接是指纹锁，为什么还有个转盘？"规则：用户指定了某个道具/装置的具体形态时，严格只写用户指定的那个形态，不自行追加"备用""额外""补充"机制。一个指纹锁就是一个指纹锁，不要加备用机械锁。一个拉手就是一个拉手，不要加转盘。
139. **交互动作必须分步骤描写——不要一句话带过**：密码输入、指纹扫描、门把手转动等交互动作，不能写成"快速按完就开了"。GK 原话："输入密码那块感觉速度太快了 直接就捶打了一下就开了"。正确做法：逐步描写每个子动作——手伸出→第一位按下→第二位（可加失误/犹豫）→后续按完→等待→机械响应→门开。每个子动作有独立的视觉和声音描写。这与"动作描写必须活"原则一致，但专门针对人机交互动作（密码、锁、开关、按钮）。
140. **MJ 提示词偏手绘漫画风——UE5 关键词位置和选词规则**：用户要求 3D CG 渲染风（类似凡人修仙传）时，MJ 提示词容易偏手绘漫画。根因和解决方法（2026-09-07 确认）：(a) 不要加 `Pixar style` / `3D animated character design` / `smooth rendering, stylized proportions` — 这些词触发手绘漫画风；(b) 不要用 `--niji` — 用户明确不要 niji 动漫模型；(c) 不要加 `character reference sheet` — 这个词容易触发手绘设定图风格；(d) `Unreal Engine 5 style` 放末尾不要放开头 — 放开头反而偏手绘；(e) 用户满意的最终模板是 `Unreal Engine 5 style, highly detailed, 8k` 放在最后，前面用 `Modern office worker character design` 开头。详见 references/midjourney-character-scene-prompts.md 的"现代职场版 UE5 模板"章节。
142. **开篇 clip 必须融入世界观交代——不能为压缩时长砍掉背景信息**：拆分多 clip 时，第一个 clip 不能只跳入核心对话而不交代背景。GK 原话："太压缩了，没头没尾""对话里融入得，小小的讲一下世界观，比如为什么来我们朝歌集团，否则观众咋知道他们这个对话在干嘛，你能动动脑子吗！"。正确做法：(a) 开篇 clip 前 2-3 秒给环境特写建立场景（如办公室铭牌、环境空镜），让观众知道"这是哪"；(b) 首轮对话中自然融入世界观信息（如"朝歌集团七年了头一回有人投这个岗"暗示不正常、"你父亲原来跟我们是合作方，后来调去了羑里分部"暗示翻脸/囚禁）；(c) 不能为了塞进时长而删掉这些背景台词——如果背景信息+核心对话放不进一个 clip，拆成两个 clip 而非砍掉背景。背景台词不是"可压缩的废话"，是观众理解后续剧情的前提。**严禁偷改台词**：GK 给了完整剧本后，提示词中的台词必须一字不改。曾把"你父亲姬昌跟我们老板有点渊源？"压缩成"你父亲被调去羑里分部了？七年了？"，把多轮对话合并成一句，被 GK 怒斥"你为什么剧本做一套，具体生成时候还偷改词？""剧本根本不是这样的，为什么不跟着剧本演？"。规则：台词只增不减，塞不进就拆 clip，不改词。GK 原话："对话按照这个来，一句都不要压缩，如果觉得不流畅还可以补，只增不减"。
152. **向节点31传真实视频导致花屏/乱码（实测 2026-09-08）**：9图版工作流 2093898864557383681 的节点31（VHS_LoadVideo）传真实视频（非占位视频）+ 参考图同时输入，模型在视频信号和图片信号间冲突——开局模糊发抖，几秒后花屏。GK 原话："就是开局模糊发抖，几秒后开始花屏"。这不是文件损坏（ffprobe 验证 h264 1536×880 24fps 完整），是生成质量问题。**根因：参考视频和参考图同时输入造成信号冲突。** 解法：(a) 回退到 None 默认版工作流 2094671638389420033（无视频节点31），尾帧衔接只用提取的单张图片走 ref_image 通道；(b) 9图版工作流节点31只能传占位视频或留空，绝不传真实视频。GK 原话："你就用none默认版工作流就可以了 别乱改了"。注意：之前记忆中"上一clip视频可作`<Video 1>`传下clip保持站位（9图版节点31）"的方案已废弃——实测花屏。GK 另外确认"不需要占位视频 不传就行了"——9图版不传 node 31 时该节点使用工作台默认值（占位视频），不影响生成。实测9图版+instanceType=default+占位视频+4张真实参考图可正常工作（6.2MB/15s，无花屏）。
153. **画幅比例通过 node 56 width/height 覆盖，不用 node 73 aspect_ratio（2026-09-08 实测）**：9图版工作流节点73 (ResolutionSelector) 的 aspect_ratio 字段所有值（"9:16"、"9:16 (Vertical)"、"1:1"等）在运行时全部报 `Value not in list` (errorCode 805)。正确方法：直接传 node 56 (MiniMaxH3ReferenceToVideo) 的 width 和 height 字段：`{"nodeId": "56", "fieldName": "width", "fieldValue": 720}, {"nodeId": "56", "fieldName": "height", "fieldValue": 1280}`，实测输出 864×1536（9:16竖屏）正常。GK 原话确认画幅是可选的。详见 references/runninghub-workflow-9img-2093898864557383681.md 的画幅章节。
154. **长视频 OOM 拆分为短 clip 串行+尾帧续接（2026-09-08 实测）**：24秒视频提交到9图版工作流（instanceType=default）报 OOM (errorCode 805, torch.OutOfMemoryError, SamplerCustomAdvanced)。解法：拆成4个8秒clip，每个单独提交，串行运行（前一个完成后截尾帧→上传→作为后一个的`<Picture 1>`首帧）。4个8秒clip全部成功，最后 ffmpeg concat 拼接成32秒完整视频。注意：串行流程必须在前一个clip完成后才提交下一个（尾帧依赖），不能并行提交。
155. **跨clip站位必须验证实际生成画面——不能假设上一clip的角色位置与提示词一致**：写新 clip 提示词中的角色位置（left/right）时，必须从上一 clip 的**实际生成视频**中提取帧验证角色实际站位，不能直接复制上一 clip 提示词中的位置描述——模型可能没有按提示词的位置指令执行。案例：clip1 提示词写"姜子牙左、伯邑考右"，但实际生成画面中两人位置可能与描述不符；clip2 沿用"left/right"描述导致与 clip1 实际画面站位不一致。GK 原话："他俩上一幕坐的位置和这一幕不一样"。正确做法：(a) 提取上一 clip 成品视频的关键帧（`ffmpeg -y -i clip.mp4 -vf "select=eq(n\\,N)" -frames:v 1 frame.png`），用 VLM 或让 GK 确认实际站位；(b) 根据实际站位写新 clip 的位置描述；(c) 如果无法确定，用 clarify 工具问 GK"上一clip中谁在左谁在右"。**(d) 站位参考图技术（2026-09-08 确认）**：从上一 clip 成品视频中提取一帧双人全景（如 6 秒处的 two-shot），上传到 RunningHub 作为新 clip 的额外参考图（`<Picture 5>`），在 subject_definitions 中定义为 "spatial reference frame from the previous clip, showing the exact seating arrangement"，在每个 Shot 中引用 `<Picture 5>` 约束站位。GK 原话："你把上图这个，作为站位参考图，传进去"。这比纯文字描述 left/right 更有效——模型有视觉参考而非只靠文字理解空间关系。注意：站位参考图占用 9 图配额中的一位。
156. **VLM识图描述与用户纠正冲突时以用户为准——不反复辩解**：VLM（glm-5.3-flash）对多格拼贴参考图的逐格描述可能出错（如把"刚出家门"识别成"车内自拍"）。用户纠正时（"第一张不是车内自拍是她刚出家门"），直接按用户描述修改提示词，不要回辩"VLM说是车内"。VLM是辅助工具不是权威——用户对自己的参考图最清楚。同时，VLM描述被截断时必须重新识别（加大max_tokens到4000+），不要用截断的不完整描述去写提示词——会遗漏关键格内容。GK原话："第一张不是车内自拍是她刚出家门"。：写新 clip 提示词中的角色位置（left/right）时，必须从上一 clip 的**实际生成视频**中提取帧验证角色实际站位，不能直接复制上一 clip 提示词中的位置描述——模型可能没有按提示词的位置指令执行。案例：clip1 提示词写"姜子牙左、伯邑考右"，但实际生成画面中两人位置可能与描述不符；clip2 沿用"left/right"描述导致与 clip1 实际画面站位不一致。GK 原话："他俩上一幕坐的位置和这一幕不一样"。正确做法：(a) 提取上一 clip 成品视频的关键帧（`ffmpeg -y -i clip.mp4 -vf "select=eq(n\,N)" -frames:v 1 frame.png`），用 VLM 或让 GK 确认实际站位；(b) 根据实际站位写新 clip 的位置描述；(c) 如果无法确定，用 clarify 工具问 GK"上一clip中谁在左谁在右"。**(d) 站位参考图技术（2026-09-08 确认）**：从上一 clip 成品视频中提取一帧双人全景（如 6 秒处的 two-shot），上传到 RunningHub 作为新 clip 的额外参考图（`<Picture 5>`），在 subject_definitions 中定义为 "spatial reference frame from the previous clip, showing the exact seating arrangement"，在每个 Shot 中引用 `<Picture 5>` 约束站位。GK 原话："你把上图这个，作为站位参考图，传进去"。这比纯文字描述 left/right 更有效——模型有视觉参考而非只靠文字理解空间关系。注意：站位参考图占用 9 图配额中的一位。：开篇环境建立镜头（tracking shot 沿墙/桌面扫过）应控制在 2-3 秒，不要 5 秒——留足时间给对话。更关键的是：**运镜扫过房间时房间必须完全空着（no people），运镜结束后硬切到新镜头中人物已经坐好就位**。不要写"运镜过程中两个人物进入画面"——模型在运镜过程中只渲染出其中一个角色（如只有伯邑考站着、姜子牙不见了），或把角色放在错误位置。硬切让模型从零生成完整的双人就位画面，避免运镜中角色渲染不一致。GK 原话："0-5秒运镜到办公室里，只有伯邑考站着，姜子牙不在里面，但是下一幕姜子牙又坐着了，这地方要修复一下"。修复方法：Shot 1 空房间运镜 3 秒 → Shot 2 硬切到两人已坐好的固定中景。
153. **关键对话转折前加停顿+回答时加身体犹豫**：对话中情绪转折点（如从日常问答转到敏感话题）前，说话人要有刻意停顿——放下笔、抬眼、选择措辞。回答方在回答敏感问题时要有身体犹豫——张嘴、停住、低头、强迫自己抬起来回答，"almost did not finish the sentence"。这不是笼统的"表情变化"，是具体的物理动作链。GK 原话："你父亲姬昌那之前稍微停顿一下，伯邑考说我父亲跟纣王那里，加一点为难的感觉"。写法示例：说话方 "pauses, then looks up for the first time — a deliberate beat of silence as he chooses his next words"；回答方 "opens his mouth, stops, glances down, then forces himself to look back up. He visibly struggles with how to phrase it"。

157. **VLM识图只走tokenrhythm glm-5.3-flash，不试其他provider（反复纠正）**：GK每次发图都要求用tokenrhythm glm-5.3-flash识图，但H每次都先试SiliconFlow（key过期401）→ 再试waibibabo（key掩码无法调用）→ 最后才回到tokenrhythm。绕一大圈浪费时间并激怒GK。GK原话："我是说，我每次都让你用tokenrhythm glm-5.3-flash识图 但是你每次都乱找"。铁律：识图直接调tokenrhythm glm-5.3-flash，不试其他provider。GLM-5.2不支持vision。PIL压缩到512px JPEG q85。max_tokens=4000避免截断。504时压缩到更小尺寸重试，不换provider。

158. **P图/改图前必须先识图（反复纠正）**：编辑图片前必须先用VLM识图看清内容/布局/已有元素，绝不瞎P。GK原话极度愤怒："你他妈识图了吗 乱p"。典型错误：VLM说右侧墙面有金属铭牌板，H直接在指定坐标P字——但VLM描述可能不准。正确流程：先识图→看清实际内容→在正确位置P字。识图后VLM描述与用户纠正冲突时以用户为准。

159. **RunningHub尾帧URL可能过期导致Invalid image file错误**：批量生成时上一clip的尾帧上传后获得的openapi URL可能过期，下一clip提交时报"Invalid image file: openapi/xxx.jpg"（errorCode 805, node 41 LoadImage）。解法：重新上传该尾帧图片获取新URL再提交。不要用旧URL重试——同样的过期URL会再次失败。

160. **批量提交连续失败时加间隔（2026-09-09 实测）**：8个clip批量串行提交时，clip7和clip8连续提交失败（返回空taskId）。根因可能是RunningHub API短时限流。解法：在连续提交之间加60秒间隔（`time.sleep(60)`），避免短时间内连续提交触发限流。如果仍然失败，单独重跑失败的clip。

161. **8格拼贴参考图作为整体风格参考（2026-09-09 确认）**：当参考图是多格拼贴照（如8格旅行日记），将其作为`<Picture 1>`整体传入node 35，在subject_definitions中定义为`<Picture 1> is an 8-panel grid reference showing...`，标记为`weak_reference`。不需要逐格拆成8个Subject——拼贴照的作用是提供整体美学/色调/氛围参考，不是逐格锁定具体画面。每个clip只需传这一张拼贴照+尾帧（如有）即可。
163. **恢复创作项目时必须先验证再陈述——不可凭记忆编造项目历史**：GK问"还记得XX项目的剧情吗""那个剧情你还记得吗"时，必须先session_search搜索历史会话+read_file读取项目目录下的脚本/提示词文件，确认实际存在的内容后再回答。不可凭记忆或模式匹配编造项目列表、版本号、GK反馈等细节。曾一口气列出"逃跑计划v1+v2/黑武士地铁v1红眼版v2歪头版/蒸汽朋克起飞+凝望/重楼天宫故乡三集"等具体细节，GK问"你刚才说的这个是什么"——说明未经核实的陈述不可信。正确做法：(a) session_search搜关键词找到原始会话；(b) read_file读项目目录下的脚本文件确认实际内容；(c) ls项目目录确认实际有哪些文件/版本；(d) 不确定的部分明确说"不确定"，不编造。GK极度反感编造——"你刚才说的这个是什么"比直接骂更狠，意味着信任受损。
164. **不自作主张产出未经请求的创作设计/方案**：GK说"重新做第一幕"时，只做第一幕的提示词即可。不要自作主张产出一整套"三段信息递进结构设计""角色弧线分析""叙事节奏规划"等未经请求的创作方案。GK原话："这是你说的，我没叫你设计这个"。规则：(a) 只做GK明确要求的事，不扩展不发散；(b) 需要设计决策时用clarify工具问，不要自己设计一整套方案丢给GK看；(c) GK给剧本→按剧本写提示词；GK说做第N幕→做第N幕提示词；不多做一步。这条和pitfall #142（开篇clip必须融入世界观交代）不矛盾——#142是"不要砍掉剧本里已有的背景信息"，本条是"不要自己发明剧本里没有的设计"。
165. **搜索参考图时先查提示词文件确认哪些角色有图、哪些是纯文字描述**：GK说"参考图其实有，自己找"时，除了搜文件系统，还必须read_file旧提示词文件查看`<Picture N>`标签定义——确认哪些Subject有对应的参考图文件、哪些是纯文字描述（pitfall #75）。曾搜遍全磁盘没找到姜子牙/伯邑考角色图，报告"没找到"，但旧clip1_prompt.txt中姜子牙和伯邑考都是纯文字Subject定义（无`from <Picture N>`），只有办公室场景图有对应文件。正确做法：(a) 搜文件系统（MJ图通常832x1216或896x1344）；b) read_file旧提示词确认每个Subject的来源是图还是文字；(c) 如果都是文字描述，如实告诉GK"之前角色没有独立参考图，是纯文字描述提交的"，而不是说"找不到图"。
166. **短剧剧本丰富方向：用对话，不用画面描写**：GK原话："你是做短剧 我不要你有那么多画面细节 我让你用对话丰富"。丰富剧本时，新增对话自然穿插在原台词之间（如用角色嘴交代世界观背景——公司规模、异常岗位、流程天数对比等），不加画面/环境/动作描写层。原台词一字不改只增不减，新增对话不破坏原有节奏。
167. **台词原文一字不改——概括复述也算违规**：GK给出完整剧本台词后，在任何环节（写提示词、拆分clip、讨论剧情、复述确认）都必须严格使用原文。不能"凭记忆概括"——会漏台词、改词、错归说话人。GK原话："你剧本根本不是这样的，为什么不跟着剧本演？"正确做法：每次需要引用台词时，回读剧本文件原文，不凭记忆复述。
168. **RunningHub API 响应格式注意**：(a) upload接口返回`code:0`+`msg:"success"`+`data.fileName`（不是`code:200`+`data.fileUrl`），用`data.fileName`的值（如`openapi/xxx.jpg`）作为nodeInfoList的fieldValue；(b) submit接口返回的`taskId`在JSON顶层（不在`data`字段里），用`result.get("taskId")`提取；(c) 所有API请求（upload/submit/query）都必须带`Authorization: Bearer {apiKey}` header，不带会返回`HEADER_API_KEY_NOT_FOUND`。
162. **第一人称POV滑梯/滑行镜头——趴姿只看到手，不看到脚和腿**：第一人称趴在滑梯上滑下时，画面中只能看到双手抓滑梯边缘，不能出现脚、腿或身体。提示词中 Subject 定义必须明确写 "lying face-down, only hands visible at bottom edge of frame, no feet, no legs, no body"，retention_analysis 标注 "only hands visible, no feet/legs/body"。Shot 描写只写手部动作（"palms flat against the wet slide surface, fingers gripping"），不要出现 "legs sliding" 等给模型渲染脚的机会。GK 原话："滑梯人应该是趴着的只能看到手，为什么我看到了脚"。

163. **循环视频 clip 间衔接——上 clip 结尾停在动作未完成处**：制作循环结构视频时，两个 clip 之间的衔接点要选在"动作未完成"的状态。例如：上 clip 结尾停在"关着的门前，手伸向门把但没碰到"→ 下 clip 从"手按下门把，门打开"开始。不要在上 clip 结尾就让角色完成推门动作——门后空间和下 clip 的开头画面不一致会导致尾帧续接出现视觉断裂。GK 原话："门外不是那个泳池啊，这样就算是续帧也达不到无缝效果"。规则：衔接点选在"门关→门开"而非"推门进入→已在室内"。

164. **RunningHub API submit 响应 taskId 在顶层不在 data 里**：submit 接口返回的 JSON 结构是 `{"taskId": "...", "status": "RUNNING", ...}`，taskId 直接在顶层，不在 `data` 字段里。upload 接口返回 `code: 0`（不是 200）+ `data.fileName`（不是 `data.fileUrl`）表示成功。所有 API 请求（submit、query、upload）都必须带 `Authorization: Bearer {API_KEY}` header，否则返回 `HEADER_API_KEY_NOT_FOUND`。

165. **短剧剧本丰富——用对话不用画面描写**：GK 要求"丰富剧本"时，通过新增对话来交代世界观，不要加画面/场景/动作描写。短剧靠对话驱动，世界观藏在台词里。例如：不要写"[画面：企业文化墙挂着朝歌集团发展历程照片]"，而是加一句姜子牙的台词"朝歌集团四十多个部门，音乐总监这个岗撤了三年了"——同样的世界观信息，用角色嘴说出来。GK 原话："你是做短剧 我不要你有那么多画面细节 我让你用对话丰富"。

166. **讨论剧本前必须 read_file 读实际文件**：不要凭记忆概括剧本内容——会漏台词、改顺序、把角色台词安到错误角色身上。讨论或修改剧本前，先 `read_file` 读取实际剧本文件，逐字核对。GK 原话："你剧本根本不是这样的，为什么不跟着剧本演？"。这条适用于所有剧本类任务：封神小剧场、末日剧、任何有完整台词原文的项目。
