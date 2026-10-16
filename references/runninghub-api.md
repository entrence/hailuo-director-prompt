# RunningHub ComfyUI 工作流 API 调用指南

RunningHub 托管 ComfyUI 工作流，可通过 API 远程调用。适用于 H3 视频生成等场景。

## 基本流程

1. 在 RunningHub 网页端搭好工作流 → 发布为 API → 获取 workflowId
2. 通过 `getJsonApiFormat` 获取工作流 JSON，找到可修改节点的 nodeId 和 fieldName
3. 上传参考图 → 获取 fileName
4. 组装 nodeInfoList → 提交任务 → 轮询查询 → 下载结果
5. ffmpeg 截尾帧 → 供下一 clip 首帧承接

## 关键接口

### 获取工作流 JSON
```
POST https://www.runninghub.cn/api/openapi/getJsonApiFormat
Content-Type: application/json
Body: {"apiKey": "YOUR_API_KEY", "workflowId": "WORKFLOW_ID"}
```
返回 `data.prompt` 是一个 JSON 字符串，解析后即可看到所有节点的 `class_type`、`inputs`、`_meta.title`。

### 上传参考图
```
POST https://www.runninghub.cn/openapi/v2/media/upload/binary
Authorization: Bearer YOUR_API_KEY
Form: file=@/path/to/image.png
```
返回 `data.fileName`（如 `openapi/abc123.png`），用于 nodeInfoList 中的 fieldValue。

⚠️ 上传后的 URL 有效期 1 天，需及时使用。

### 提交任务
```
POST https://www.runninghub.cn/openapi/v2/run/workflow/WORKFLOW_ID
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
Body: {
  "addMetadata": true,
  "nodeInfoList": [
    {"nodeId": "84", "fieldName": "value", "fieldValue": "提示词全文"},
    {"nodeId": "35", "fieldName": "image", "fieldValue": "openapi/xxx.png"},
    {"nodeId": "74", "fieldName": "value", "fieldValue": 15}
  ],
  "instanceType": "default"
}
```

返回 `taskId` 和 `status: "RUNNING"`。

### 查询结果
```
POST https://www.runninghub.cn/openapi/v2/query
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
Body: {"taskId": "TASK_ID"}
```

状态流转：QUEUED → RUNNING → SUCCESS / FAILED。
SUCCESS 时 `results[].url` 是视频下载链接，**有效期 24 小时**。

## ⚠️ 关键 Pitfalls

0a. **所有接口必须带 `Authorization: Bearer` header**：只在 JSON body 里放 `apiKey` 字段不够，会返回 `{"code":1602,"msg":"HEADER_API_KEY_NOT_FOUND"}`。提交、查询、上传三个接口全部需要 `-H "Authorization: Bearer YOUR_API_KEY"`。

0b. **查询结果用 `/openapi/v2/query`，不是 `/openapi/v2/getResults`**：`getResults` 返回 `errorCode: 1001, "Invalid URL"` 且 status 字段为空，轮询脚本会空转数十分钟无输出。正确接口是 `/openapi/v2/query`，body 只需 `{"taskId": "..."}`（不需 apiKey），返回 `status` 字段为 `QUEUED`/`RUNNING`/`SUCCESS`/`FAILED`。2026-09-11 实测踩坑：用错接口白轮询 25 分钟。

0c. **给GK完整的可复制curl命令时用heredoc**：curl命令里JSON payload含单引号会导致bash解析错误。用heredoc包裹JSON避免引号冲突：
```bash
curl -X POST "https://www.runninghub.cn/openapi/v2/run/workflow/WORKFLOW_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer API_KEY" \
  -d @- <<'ENDOFJSON'
{"apiKey":"...","nodeInfoList":[...],"instanceType":"standard"}
ENDOFJSON
```
GK原话："你就不能直接给我一个curl可以直接复制就能请求的？"——写完整命令到单个txt文件用MEDIA发，不在chat贴长命令（太长无法复制）。不截断不placeholder。

0d. **OOM重试不需要升plus**：standard实例偶发OOM（errorCode 805, "VRAM grow failed"），直接重新提交同一参数通常能过。2026-09-11实测：clip4首次OOM，重试即成功。不需要升plus实例。

1. **字段名是 `fieldValue` 不是 `value`**：nodeInfoList 里每个元素用 `{"nodeId": "X", "fieldName": "Y", "fieldValue": "Z"}`。用 `value` 会报 `errorCode: 803, errorMessage: "JsonNull"`。这是最容易犯的错误。

2. **图片传 fileName 不传 URL**：LoadImage 节点的 fieldValue 用上传接口返回的 `fileName`（如 `openapi/abc123.png`），不要传完整 URL。

3. **nodeInfoList 为空也能跑**：如果不传 nodeInfoList 或传空数组 `[]`，工作流会用默认参数执行。这在测试连通性时有用，但会消耗余额。

4. **绝对不要发空请求测试**：空 `{}` 请求会触发工作流用默认参数执行，消耗余额，可能触发平台风控（用户收到违规短信被限制使用）。如果只是测试 API 连通性，用 `getJsonApiFormat` 接口而非 `run/workflow`。

5. **H3 视频生成耗时 5-10 分钟**：15 秒视频约 500-730 秒生成时间。用后台 sleep+curl 轮询，notify_on_complete 通知。

6. **输出 URL 24 小时过期**：生成后立即下载，不要隔天再取。

7. **提交脚本禁止内置自动重试**：poll_and_download 超时或失败后直接 return False 退出，不要写 `if not success: retry` 分支。自动重试会再次消耗积分，而 GK 可能想先看提示词或换参数。GK 说"取小重新来吧"= 换新种子手动重新提交一次，不是让脚本自动循环重试。正确做法：脚本只提交一次 → 失败打印错误退出 → GK 决定是否重试。

8. **instanceType 不要用 plus**：默认用 `"standard"` 或 `"default"`，能不用 plus 就不用 plus（省积分）。GK 原话："能不用plus就不用plus，你浪费了我很多积分"。仅在 OOM (errorCode 805) 时才升 plus。提交脚本中不要写 `"instanceType": "plus"`。

## H3 工作流节点参考

### 旧工作流（workflowId: 2093776941622059010，仅 2 张参考图）

| 节点ID | class_type | fieldName | 作用 |
|--------|-----------|-----------|------|
| 84 | PrimitiveStringMultiline | value | 提示词（六段格式全文） |
| 35 | LoadImage | image | 参考图1（ref_image_0，通常首帧截图） |
| 41 | LoadImage | image | 参考图2（ref_image_1，通常角色图） |
| 74 | PrimitiveFloat | value | 视频秒数（如 15） |
| 73 | ResolutionSelector | aspect_ratio | 画幅（16:9 等） |
| 63 | RandomNoise | noise_seed | 随机种子 |
| 56 | MiniMaxH3ReferenceToVideo | ref_images.ref_image_N | H3 核心节点，支持 9 张参考图 |

### 新工作流（workflowId: 2093898864557383681，9图+1视频+3音频）

用户在网页端已添加全部 LoadImage(9)、LoadVideo(1)、LoadAudio(3) 节点。

| 节点ID | class_type | fieldName | 作用 |
|--------|-----------|-----------|------|
| 84 | PrimitiveStringMultiline | value | 提示词 |
| 74 | PrimitiveFloat | value | 视频秒数 |
| 35 | LoadImage | image | ref_image_0 |
| 41 | LoadImage | image | ref_image_1 |
| 42 | LoadImage | image | ref_image_2 |
| 43 | LoadImage | image | ref_image_3 |
| 44 | LoadImage | image | ref_image_4 |
| 36 | LoadImage | image | ref_image_5 |
| 37 | LoadImage | image | ref_image_6 |
| 38 | LoadImage | image | ref_image_7 |
| 39 | LoadImage | image | ref_image_8 |
| 31 | LoadVideo | video | ref_video_0 |
| 28 | LoadAudio | audio | ref_audio_0 |
| 29 | LoadAudio | audio | ref_audio_1 |
| 30 | LoadAudio | audio | ref_audio_2 |

### 节点禁用与占位图策略

RunningHub API **不支持节点级禁用**（ComfyUI 的 Ctrl+B bypass 在 API 层没有对应接口）。`nodeInfoList` 只能覆盖参数值，不能改连线拓扑或节点模式。不需要的参考图位置传**纯白占位图**（1024×1024 RGB(255,255,255)）。H3 是 attention-based 模型，纯色图几乎无信息量，不影响生成质量。工作台 9 个节点保持连接永不改动。详见 [runninghub-node-management.md](references/runninghub-node-management.md)。

## ffmpeg 截尾帧

⚠️ **必须用 `-sseof`，不能用裸 `-vframes 1`**：不带 `-sseof` 的 `ffmpeg -vframes 1` 截的是**第一帧**不是尾帧！2026-09-11 实测：poolcore clip3/clip4 全部用了错误的首帧当续接帧，空间过渡完全断裂，全部重跑。

```bash
# 正确的尾帧截取
ffmpeg -sseof -0.1 -i input.mp4 -vframes 1 -q:v 2 -update 1 output.png -y
```

轮询脚本模板见 liminal-core-prompts skill 的 [scripts/poll_h3_video.py](../../liminal-core-prompts/scripts/poll_h3_video.py)，已内置正确的 `-sseof` 截帧命令。

## Python 调用模板

```python
import json, urllib.request

def submit_workflow(api_key, workflow_id, node_info_list):
    url = f"https://www.runninghub.cn/openapi/v2/run/workflow/{workflow_id}"
    payload = {
        "addMetadata": True,
        "nodeInfoList": node_info_list,
        "instanceType": "default"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def query_result(api_key, task_id):
    url = "https://www.runninghub.cn/openapi/v2/query"
    payload = {"taskId": task_id}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def upload_image(api_key, image_path):
    import subprocess
    result = subprocess.run([
        "curl", "-s", "-X", "POST",
        "https://www.runninghub.cn/openapi/v2/media/upload/binary",
        "-H", f"Authorization: Bearer {api_key}",
        "-F", f"file=@{image_path}"
    ], capture_output=True, text=True)
    return json.loads(result.stdout)
```
