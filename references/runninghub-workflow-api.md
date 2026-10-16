# RunningHub ComfyUI 工作流 API 调用指南

通过 RunningHub API 调用托管的 ComfyUI 工作流（如 MiniMax H3 Reference-to-Video），实现提示词→视频生成的自动化流水线。

## 前置条件

- RunningHub 账号 + 充值余额（消费级会员需基础版以上）
- API Key（32位，在 RunningHub API 管理页面生成）
- 已发布的工作流（workflowId）

## API 端点总览

| 操作 | 方法 | 端点 |
|------|------|------|
| 提交任务 | POST | `/openapi/v2/run/workflow/{workflowId}` |
| 查询结果 | POST | `/openapi/v2/query` |
| 获取工作流JSON | POST | `/api/openapi/getJsonApiFormat` |
| 上传图片 | POST | `/openapi/v2/media/upload/binary` |

所有请求需 Header: `Authorization: Bearer {apiKey}` + `Content-Type: application/json`

## 1. 获取工作流节点结构

提交任务前，先获取工作流的 API-format JSON，查看哪些节点可修改：

```bash
curl -s -X POST "https://www.runninghub.cn/api/openapi/getJsonApiFormat" \
  -H "Content-Type: application/json" \
  -d '{"apiKey": "YOUR_API_KEY", "workflowId": "WORKFLOW_ID"}'
```

返回 `data.prompt` 是一个 JSON 字符串，解析后按 `class_type` 找关键节点：

| 常见 class_type | 作用 |fieldName |
|----------------|------|----------|
| `PrimitiveStringMultiline` | 提示词输入框 | `value` |
| `LoadImage` | 参考图加载 | `image` |
| `VHS_LoadVideo` | 参考视频加载 | `video` |
| `PrimitiveFloat` | 数值参数（秒数等）| `value` |
| `PrimitiveInt` | 整数参数 | `value` |
| `ResolutionSelector` | 画幅选择 | `aspect_ratio` |

### 两个工作流版本的节点差异

不同版本的工作流节点 ID **不相同**。旧工作流 (2093776941622059010) 只有节点 35/41 两个 LoadImage，新工作流 (2093898864557383681) 有 35/41/42/43/44/36/37/38/39 九个。把新工作流的节点 42 传给旧工作流会返回 `803 NODE_INFO_MISMATCH(nodeId=42, reason=node_not_found_in_workflow)`。**每次切换工作流版本必须重新获取节点列表。**

## 2. 提交任务

```bash
curl -s -X POST "https://www.runninghub.cn/openapi/v2/run/workflow/{workflowId}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {apiKey}" \
  -d '{
    "addMetadata": true,
    "nodeInfoList": [
      {"nodeId": "84", "fieldName": "value", "fieldValue": "提示词全文"},
      {"nodeId": "35", "fieldName": "image", "fieldValue": "openapi/xxxx.png"},
      {"nodeId": "41", "fieldName": "image", "fieldValue": "openapi/yyyy.png"},
      {"nodeId": "74", "fieldName": "value", "fieldValue": 15}
    ],
    "instanceType": "default"
  }'
```

### nodeInfoList 说明

- `nodeInfoList` 是**必填**字段，即使为空数组 `[]` 也要传（工作流用默认值跑）
- 每个元素指定一个节点的某个字段值：**字段名是 `fieldValue`，不是 `value`**
  - 正确：`{"nodeId": "84", "fieldName": "value", "fieldValue": "提示词"}`
  - 错误：`{"nodeId": "84", "fieldName": "value", "value": "提示词"}` → 返回 errorCode 803 JsonNull
- 图片参数传 **fileName**（上传接口返回的 `data.fileName`，格式如 `openapi/xxxx.png`），不是完整 URL
- 如果工作流已在网页端配置好参数，传空 `nodeInfoList: []` 即可用当前配置跑
- 传入不存在于该工作流的 nodeId 会返回 `803 NODE_INFO_MISMATCH(nodeId=X, reason=node_not_found_in_workflow)`

### 不传节点 ≠ 禁用节点（重要）

不传某个节点的参数，该节点**不会被跳过**——它会使用工作台保存的默认值参与生成。如果默认值是真实参考图，全部 9 张图加载会导致显存溢出（OOM）。

解决方法取决于工作台默认值设置：

- **工作台默认值 = 占位文件**（推荐）：API 只传提示词+真实图+秒数（4节点即可）
- **工作台默认值 = 真实图**：API 必须传全部 15 节点（真实图+占位文件顶位）

详见 references/runninghub-node-management.md。

### 返回

```json
{"taskId": "2093889686992027649", "status": "RUNNING", ...}
```

保存 `taskId` 用于查询。

## 3. 查询结果

H3 模型生成约需 5-12 分钟（taskCostTime 实测 526~716 秒）。

```bash
curl -s -X POST "https://www.runninghub.cn/openapi/v2/query" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {apiKey}" \
  -d '{"taskId": "TASK_ID"}'
```

### 状态值

| status | 含义 |
|--------|------|
| QUEUED | 排队中 |
| RUNNING | 运行中 |
| SUCCESS | 成功 |
| FAILED | 失败 |

### 成功返回

```json
{
  "status": "SUCCESS",
  "results": [{
    "url": "https://rh-images-xxx.cos.ap-beijing.myqcloud.com/.../Video_00001.mp4",
    "nodeId": "115",
    "outputType": "mp4"
  }],
  "usage": {"consumeCoins": "106", "taskCostTime": "526"}
}
```

### 失败诊断

失败时 `failedReason` 包含详细的 traceback。关键看：

- `node_name` / `node_id`：哪个节点出错
- `exception_type`：错误类型
  - `ValueError` + node `VHS_LoadVideo`：占位视频太小，改用 16×16 / 24fps / 1秒
  - `torch.OutOfMemoryError` + node `SamplerCustomAdvanced`：显存不够，检查是否有不必要的真实图被加载
- `exception_message`：具体错误信息

**结果 URL 有效期仅 24 小时**，必须及时下载。

**任务不存在 (`errorCode: 1004`)**：空请求被平台拒绝，未实际执行，不扣 coins。

## 4. 上传参考图

本地图片需先上传获取 URL：

```bash
curl -s -X POST "https://www.runninghub.cn/openapi/v2/media/upload/binary" \
  -H "Authorization: Bearer {apiKey}" \
  -F "file=@/path/to/image.png"
```

返回 `data.download_url` 是带签名的临时 URL（有效期 1 天），可直接用于 `nodeInfoList` 的图片参数。

## 5. 下载结果 + 转码 + 截尾帧

**注意：RunningHub 输出的"mp4"实际是 Apple QuickTime MOV 容器**（`file` 显示 `ISO Media, Apple QuickTime movie`）。微信端不识别 MOV 容器——直接发会收不到（GK 实测反馈："没发给我"）。必须先转码为标准 H.264+AAC MP4，且**必须保留音轨**：原始文件自带 AAC 音轨（环境音/对白），转码加 `-an` 会把声音砍掉（GK 实测反馈："怎么没声音"）。

```bash
# 下载视频
curl -sL -o output.mp4 "RESULT_URL"

# 转码为微信兼容 H.264+AAC MP4（保留音轨！禁止 -an）
ffmpeg -y -i output.mp4 -c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p \
  -movflags +faststart -c:a aac -b:a 128k output_weixin.mp4

# 截取最后一帧（用于下一个 clip 的首帧承接）
TOTAL_FRAMES=$(ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of csv=p=0 output.mp4)
ffmpeg -y -i output.mp4 -vf "select=eq(n\,$((TOTAL_FRAMES-1)))" -frames:v 1 -update 1 last_frame.png
```

转码后 `MEDIA:` 发送用 `output_weixin.mp4`。出片后**自动**完成"下载→转码→发送"，GK 明确要求不要等他提醒（原话："生成好了转视频保留音频都不要让我说了，你自己做"）。

## 完整流水线：clip 提示词 → 视频 → 尾帧

1. 读取 clip 的 .txt 提示词文件（六段格式）
2. 上传该 clip 需要的参考图（角色图 + 首帧截图）→ 获取 URL
3. 用 `getJsonApiFormat` 查看工作流节点 ID（首次确认后后续可跳过）
4. 提交任务：`nodeInfoList` 传入提示词 + 图片 URL + 秒数
5. 等待 5-12 分钟
6. 查询结果，下载 MP4
7. 截尾帧，存为 `clip{N}_尾帧.png`，供下一个 clip 使用
8. **转码为 H.264+AAC MP4（保留音轨，勿用 `-an`）后用 MEDIA: 发送给 GK 看效果**——出片后自动执行，不等 GK 提醒

## Pitfalls

1. **绝不发空请求测试 API**：传 `{}` 会触发工作流实际执行。曾因空请求导致平台判定违规、限制账号。如果要测试连通性，用 `getJsonApiFormat` 接口（只读取不执行）。
2. **结果 URL 24 小时过期**：生成后立即下载，不要隔天再取。
3. **上传的图片 URL 1 天过期**：上传后尽快提交任务使用。
4. **nodeInfoList 必填**：即使不修改任何参数也要传 `[]`，不能省略。
5. **H3 生成耗时不可控**：实测 526~716 秒（9~12 分钟），不要设太短的 polling 间隔。建议 10 分钟后查询。
6. **不传节点参数 ≠ 禁用节点**：未传参的节点使用工作台默认值。如果默认值是真实大图，9张全加载导致 OOM。解决方案见 references/runninghub-node-management.md。
7. **占位视频不能小于 16×16**：2×2 / 1帧视频会导致 VHS_LoadVideo 报 ValueError。最小有效尺寸 16×16 / 24fps / 1秒。
8. **占位图不能用 1×1**：1×1 PNG 偶尔能过但不可靠——RunningHub LoadImage 有自定义验证，极小尺寸图片会被判定为 `Invalid image file`。最小稳定尺寸为 64×64 纯白 PNG（134 字节）。
9. **OOM 重试模式**：`torch.OutOfMemoryError` / `RuntimeError: VRAM grow failed` 如果参数正确（占位文件已顶位、非全量大图），通常不是参数问题而是 RunningHub GPU 资源波动。直接用相同参数重新提交即可，不需要改参数。重试通常成功。区分：秒级报错（taskCostTime=0）= 参数/资源问题；持续 RUNNING 后失败 = 资源波动。
10. **跨工作流版本复用节点 ID**：不同版本工作流的节点 ID 不互通。旧工作流只有35/41两个LoadImage，新工作流有35/41/42/43/44/36/37/38/39九个。传不存在的节点会返回 `803 NODE_INFO_MISMATCH`。每次切换工作流版本必须重新用 `getJsonApiFormat` 确认节点列表。旧工作流更便宜（106-137 coins vs 134-154 coins）但只能传2张参考图。
11. **新工作流必须先在 UI 跑一次**：如果工作流创建后从未在网页端运行保存过，API 提交会返回 `810 Workflow not saved or run`。先用 UI 跑一次让系统保存工作流。
12. **输出是 MOV 容器 + 转码丢音轨**：RunningHub 输出的"mp4"实际是 Apple QuickTime MOV 容器（`file` 显示 `ISO Media, Apple QuickTime movie`），微信不识别——直接发会收不到（GK："没发给我"）。转码必须用 `-c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 128k`，**绝对不能加 `-an`**——原始文件自带 AAC 音轨（环境音），`-an` 会砍掉（GK："怎么没声音"）。出片后自动"下载→转码→发送"，不要等 GK 提醒。