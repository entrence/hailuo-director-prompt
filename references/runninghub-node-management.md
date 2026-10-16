# RunningHub 节点管理：禁用参考图与占位文件策略

## 核心问题

H3 工作流有 9 个 LoadImage 节点连到 ref_image_0~8，1 个 LoadVideo 连到 ref_video_0，3 个 LoadAudio 连到 ref_audio_0~2。某个 clip 只需 2 张参考图时，其余 7 个图片节点 + 1 个视频节点 + 3 个音频节点不会自动忽略——它们会使用工作台保存的默认文件参与生成，可能干扰结果甚至导致 OOM。

## API 不支持节点禁用

RunningHub API 的 `nodeInfoList` **只能覆盖节点参数值**（`fieldValue`），不支持：

- 禁用/绕过节点（ComfyUI 前端的 `Ctrl+B`，节点 mode=0→4）
- 修改节点连线拓扑
- 删除或跳过节点

`nodeInfoList` 每个元素只有三个字段：`nodeId`、`fieldName`、`fieldValue`。没有 `mode`、`disabled`、`bypass` 等。

## 跨工作流版本节点 ID 不互通

不同版本的工作流节点 ID **不相同**。旧工作流只有节点 35/41 两个 LoadImage，新工作流有 35/41/42/43/44/36/37/38/39 九个。把新工作流的节点 42 传给旧工作流会返回：

```
803 NODE_INFO_MISMATCH(nodeId=42, fieldName=image, reason=node_not_found_in_workflow)
```

**每次切换工作流版本时，必须重新用 `getJsonApiFormat` 确认实际节点列表。**

## 两个工作流版本对比

| | 旧工作流 (2093776941622059010) | 9图版 (2093898864557383681) | None默认版 (2094671638389420033) |
|--|------|------|------|
| LoadImage 节点 | 35, 41（共2个） | 35, 41, 42, 43, 44, 36, 37, 38, 39（共9个） | 35, 41, 42, 43, 44, 36, 37, 38, 39（共9个） |
| LoadVideo 节点 | 无 | 31 | 无（已移除） |
| LoadAudio 节点 | 无 | 28, 29, 30 | 28, 29, 30 |
| 默认值 | 真实图 | 真实图（OOM风险） | **全部 None**（零风险） |
| 提交方式 | 5-6项 | 15项全量+占位 | 只传真实图（方案C） |
| 费用 | ~106-137 coins | ~134-154 coins | 待测（预计更低） |
| OOM 风险 | 无（只有2张图） | 有（需占位+plus实例） | 无（None不占显存） |
| 参考图上限 | 2张 | 9张+1视频+3音频 | 9张+3音频 |
| 适用场景 | 单角色+单场景 | 全量参数控制 | **推荐默认使用** |

## 网页端断连 = 永久修改

在 RunningHub 网页端断开 LoadImage 连线并保存，会**永久修改工作台**：

- 所有后续 API 调用都受影响，不是只作用于一次请求
- 下一个 clip 如果又需要该图，必须重新连上再保存
- 每个 clip 需要的角色不同 → 反复断开→保存→提交→重连→保存，极繁琐

**结论：不要在网页端操作连线来跳过参考图。**

## 实证："用几张传几张"行不通

### 实验 B：只传 4 节点（提示词+2张图+秒数）

- **假设**：不传的节点会被忽略
- **实际结果**：`OutOfMemoryError`（显存溢出），节点 108 `SamplerCustomAdvanced` 报错
- **原因**：不传的节点使用了工作台保存的默认值（9 张真实角色/场景图全部加载），GPU 显存不够
- **结论**：不传 ≠ 禁用。未传参数的节点仍会使用工作台默认值参与运算

### 实验 A v1：占位视频 2×2 / 1帧

- **结果**：`ValueError: Must specify length when using variable-size data-type`，节点 31 `VHS_LoadVideo` 报错
- **原因**：VHS_LoadVideo 对 2×2 / 1帧视频无法正常解码，numpy fromiter 无法推断数组长度
- **结论**：占位视频必须有足够尺寸和帧数供 VHS_LoadVideo 正常解析

### 实验 A v2：占位视频 16×16 / 24fps / 1秒

- **结果**：SUCCESS，144 coins，716 秒
- **结论**：16×16 / 24fps / 1秒的纯黑视频可被 VHS_LoadVideo 正常解析

### 占位图 1×1 被拒绝事件

- **结果**：`LoadImage` 报 `Invalid image file: openapi/xxx.png`，节点 38 报 `Custom validation failed for node`
- **原因**：1×1 PNG 偶尔能过但不可靠——RunningHub 的 LoadImage 有自定义验证，极小尺寸图片会被判定为无效
- **修复**：升级到 64×64 纯白 PNG（134 字节），稳定通过
- **结论**：占位图最小用 64×64，不要用 1×1

## 解决方案（三层，推荐方案 C）

### 方案 A：每次 API 都传 15 节点全量参数

九个 LoadImage + 1 个 LoadVideo + 3 个 LoadAudio 节点全部保持连接，API 调用时需要的传真实文件，不需要的传占位文件。**已验证可行。**

缺点：每次都要组装 15 个节点参数，冗余。仅适用于新工作流 (2093898864557383681)。

### 方案 B：工作台默认值全设为占位文件，API 只传真实文件

1. 在 RunningHub 网页端工作流编辑器中，把 9 个 LoadImage、1 个 LoadVideo、3 个 LoadAudio 的**默认值全换成占位文件**，保存
2. API 调用时只传：提示词（节点84）+ 真实需要的参考图 + 秒数（节点74）
3. 不传的节点自动用工作台里的占位默认值，不占显存，不报错

设好默认值后，nodeInfoList 只需 4 个节点：

```json
"nodeInfoList": [
  {"nodeId": "84", "fieldName": "value", "fieldValue": "提示词全文"},
  {"nodeId": "35", "fieldName": "image", "fieldValue": "openapi/首帧截图.png"},
  {"nodeId": "41", "fieldName": "image", "fieldValue": "openapi/角色图.png"},
  {"nodeId": "74", "fieldName": "value", "fieldValue": 15}
]
```

### 方案 C（推荐）：工作台默认值全设为 None，用几张传几张

**GK 在 2026-09-01 发布的新工作流 `2094671638389420033` 上验证。** 工作流结构：
- 9 个 LoadImage 节点（35/41/42/43/44/36/37/38/39）全部 `image=None`
- **无 VHS_LoadVideo 节点 31**（已移除，不需要传占位视频）
- 3 个 LoadAudio 节点（28/29/30）默认也是 None（GK 2026-09-01 确认："下次音频也是用几个传几个，音频现在也是none"）
- Node 56 (MiniMaxH3ReferenceToVideo) 的 ref_image_0~8 全部连着9个 LoadImage

提交方式：只传真实需要的图 + 提示词 + 秒数，**不传的 LoadImage 和 LoadAudio 自动保持 None，模型跳过**。不需要占位音频。

```json
"nodeInfoList": [
  {"nodeId": "84", "fieldName": "value", "fieldValue": "提示词全文"},
  {"nodeId": "35", "fieldName": "image", "fieldValue": "openapi/陆寒.png"},
  {"nodeId": "41", "fieldName": "image", "fieldValue": "openapi/出租屋.png"},
  {"nodeId": "28", "fieldName": "audio", "fieldValue": "openapi/placeholder.mp3"},
  {"nodeId": "29", "fieldName": "audio", "fieldValue": "openapi/placeholder.mp3"},
  {"nodeId": "30", "fieldName": "audio", "fieldValue": "openapi/placeholder.mp3"},
  {"nodeId": "74", "fieldName": "value", "fieldValue": 15}
]
```

**优势 vs 方案 B**：
- None 比 64×64 白图更干净——零视觉信息量，注意力权重绝对为零
- 不需要预上传占位图，减少维护
- 不需要 LoadVideo 占位（节点31已移除）

**已验证（2026-09-01）**：GK 发布工作流后首次 API 提交只传 2 张图（陆寒+出租屋），不传占位图，taskId=`2094673932144836609`，状态 QUEUED→RUNNING。instanceType 用 `"standard"`（GK 要求省积分）。模型自动跳过 None 的图节点，不影响生成。

**前提**：工作台默认值必须真的是 `None`（不是某个遗留的真实图）。GK 发布工作流前需在网页端确认每个 LoadImage 的 image 字段显示为空/None。

**注意**：旧工作流 `2093898864557383681` 的默认值全是真实角色图，不是 None。方案 C 只适用于 `2094671638389420033` 或后续默认值设为 None 的新工作流。切换工作流时必须用 `getJsonApiFormat` 确认默认值状态。

## 占位文件规格（方案 A/B 需要，方案 C 仅需音频）

GK 明确要求占位文件"要一个极小的，不要影响生成速度"。大占位文件仍需编码传输和模型预处理，拖慢生成。

| 类型 | 尺寸 | 生成命令 | 文件大小 | 备注 |
|------|------|----------|----------|------|
| 图片 | **64×64** 纯白 PNG | `python3 -c "from PIL import Image; Image.new('RGB',(64,64),(255,255,255)).save('p.png')"` | 134 字节 | **不能用 1×1**，LoadImage 会报 Invalid image file |
| 视频 | **16×16** 纯黑 24fps 1秒 | `ffmpeg -y -f lavfi -i color=c=black:s=16x16:r=24:d=1 -c:v libx264 -preset ultrafast -pix_fmt yuv420p -crf 51 p.mp4` | ~1.8 KB | **不能小于 16×16**，VHS_LoadVideo 解析不了 2×2 |
| 音频 | 50ms 静音 mono 8kHz | `ffmpeg -y -f lavfi -i anullsrc=channel_layout=mono:sample_rate=8000:d=0.05 -c:a libmp3lame -b:a 8k p.mp3` | ~477 字节 | 静音即可 |

### 占位图尺寸陷阱

**1×1 PNG 会被 LoadImage 拒绝**：报 `Invalid image file` + `Custom validation failed for node`。1×1 偶尔能过（取决于节点验证的随机性），但不可靠。**最小稳定尺寸为 64×64**。

### 占位视频尺寸陷阱

**2×2 / 1帧的视频会导致 VHS_LoadVideo 报错**：`ValueError: Must specify length when using variable-size data-type`。

VHS_LoadVideo 用 `np.fromiter` 加载视频帧，帧分辨率过小时 numpy 无法推断数组长度。**最小有效尺寸为 16×16 / 24fps / 1秒（24帧）**。文件仅 1.8KB，对生成速度几乎零影响。

### 上传到 RunningHub

```bash
# 上传所有占位文件
curl -s -X POST "https://www.runninghub.cn/openapi/v2/media/upload/binary" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@placeholder.png"
# 记录返回的 fileName，API 调用时填充空位
```

### 占位文件 fileName 记录

上传后将三个 fileName 存为 JSON 供脚本读取：

```json
{
  "placeholder_image": "openapi/xxxx.png",
  "placeholder_video": "openapi/xxxx.mp4",
  "placeholder_audio": "openapi/xxxx.mp3"
}
```

### 原理

H3 是 attention-based 模型，64×64 纯白图几乎没有视觉信息量，注意力权重极低，实测基本不影响生成质量。16×16 黑屏视频和静音音频同理。极小文件避免传输和预处理开销，不影响生成速度。

## 新工作流节点映射（workflowId: 2093898864557383681）

用户在 RunningHub 网页端添加了全部 LoadImage/LoadVideo/LoadAudio 节点：

### 参考图（9张）

| ref_image | 节点ID | class_type | fieldName |
|-----------|--------|------------|-----------|
| ref_image_0 | 35 | LoadImage | image |
| ref_image_1 | 41 | LoadImage | image |
| ref_image_2 | 42 | LoadImage | image |
| ref_image_3 | 43 | LoadImage | image |
| ref_image_4 | 44 | LoadImage | image |
| ref_image_5 | 36 | LoadImage | image |
| ref_image_6 | 37 | LoadImage | image |
| ref_image_7 | 38 | LoadImage | image |
| ref_image_8 | 39 | LoadImage | image |

### 参考视频（1个）

| ref_video | 节点ID | class_type | fieldName |
|-----------|--------|------------|-----------|
| ref_video_0 | 31 | VHS_LoadVideo | video |

### 参考音频（3个）

| ref_audio | 节点ID | class_type | fieldName |
|-----------|--------|------------|-----------|
| ref_audio_0 | 28 | LoadAudio | audio |
| ref_audio_1 | 29 | LoadAudio | audio |
| ref_audio_2 | 30 | LoadAudio | audio |

### 其他参数

| 节点ID | class_type | fieldName | 作用 |
|--------|------------|-----------|------|
| 84 | PrimitiveStringMultiline | value | 提示词 |
| 74 | PrimitiveFloat | value | 视频秒数 |

## 旧工作流节点映射（workflowId: 2093776941622059010）

旧工作流只有 2 个 LoadImage 节点，不支持参考视频和音频。

| 节点ID | class_type | fieldName | 作用 |
|--------|------------|-----------|------|
| 35 | LoadImage | image | ref_image_0 |
| 41 | LoadImage | image | ref_image_1 |
| 84 | PrimitiveStringMultiline | value | 提示词 |
| 74 | PrimitiveFloat | value | 视频秒数 |

旧工作流传空 `nodeInfoList: []` 可用默认值跑，不会 OOM（只有2张图）。传不存在于该工作流的节点 ID 会返回 `803 NODE_INFO_MISMATCH`。

## 工作流版本选择建议

- **唯一推荐用 None 默认版 `2094671638389420033`**：9 图槽全开，默认值全 None，用几张传几张，无 OOM 风险，不需要占位图/视频。instanceType 用 "standard"（GK 要求省积分，OOM 才升 plus）
- **~~2098315416350314497~~（已弃用）**：节点结构完全不同（参数集中在197，图片节点200/333/351），运行不稳定，GK 2026-09-11 明确弃用
- **~~2093898864557383681~~（已弃用）**：需要占位图+plus实例，浪费积分，已被 None 默认版完全替代
- **~~2093776941622059010~~（已弃用）**：只有2个图槽，不够用
- **每次切换工作流版本**：必须重新用 `getJsonApiFormat` 确认节点列表和默认值，不能复用旧版本的节点 ID
