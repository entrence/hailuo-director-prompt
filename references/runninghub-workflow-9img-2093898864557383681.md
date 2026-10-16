# RunningHub 工作流版本说明

## 已废弃工作流

### ~~新工作流 2098315416350314497~~（已弃用）

2026-09-11 测试。节点结构完全不同：所有参数（prompt/seconds/width/height/mode/prompt_optimizer等）集中在节点197，图片节点为200/333/351（非35/41/42）。需要传中文默认值覆盖（ref_image_size→"original", scene_guide→"none", api_format→"openai"等），且运行不稳定（多次 FAILED errorCode 805 "工作流运行失败"）。

**GK 原话：「就用这个（2094671638389420033），以后不用新的那个了」「还是用原来的工作酒吧那个稳定点」。**

**此工作流永久弃用，不要再用。** 如果未来需要切换工作流，先用 `getJsonApiFormat` 确认节点结构，并在 SKILL.md 记录。

### ~~9图版 2093898864557383681~~（已弃用）

需要占位图+plus实例，浪费积分。已被 None默认版 `2094671638389420033` 完全替代。

## 当前可用工作流

| 工作流 ID | 参考图 | 默认值 | 单价 | 状态 | 说明 |
|-----------|--------|--------|------|------|------|
| **2094671638389420033** | 9 图 | **None** | 最低 | **唯一推荐** | None默认版，用几张传几张，无OOM风险，standard实例 |

## 9图版工作流 2093898864557383681

2026-08-31 实测确认。API Key 存于项目目录 poll_clip.py / submit_clip.py 中。

### 节点映射（getJsonApiFormat 实测）

| 用途 | 节点ID | class_type | fieldName |
|------|--------|-----------|-----------|
| 参考图0 | 35 | LoadImage | image |
| 参考图1 | 41 | LoadImage | image |
| 参考图2 | 42 | LoadImage | image |
| 参考图3 | 43 | LoadImage | image |
| 参考图4 | 44 | LoadImage | image |
| 参考图5 | 36 | LoadImage | image |
| 参考图6 | 37 | LoadImage | image |
| 参考图7 | 38 | LoadImage | image |
| 参考图8 | 39 | LoadImage | image |
| 参考视频 | 31 | VHS_LoadVideo | video |
| 参考音频0 | 28 | LoadAudio | audio |
| 参考音频1 | 29 | LoadAudio | audio |
| 参考音频2 | 30 | LoadAudio | audio |
| 提示词 | 84 | PrimitiveStringMultiline | value |
| 秒数 | 74 | PrimitiveFloat | value |
| 噪声种子 | 63 | RandomNoise | noise_seed |
| (CLIP) | 64 | CLIPLoader | clip_name=qwen3vl_32b_minimax_h3_int8_convrot.safetensors |
| (LoRA) | 118 | Lora Loader Stack (rgthree) | lora_01~04 / strength_01~04 |
| (Sampler) | 58 | KSamplerSelect | sampler_name=euler |
| (Scheduler) | 71 | BasicScheduler | scheduler=simple, steps=4, denoise=1 |
| (分辨率) | 73 | ResolutionSelector | aspect_ratio=16:9, megapixels=0.9, multiple=32 |
| (模型) | 69 | UNETLoader | minimax_h3_ref2va_XUELUO_int8_convrot.safetensors |
| (VAE视频) | 65 | VAELoader | minimax_h3_video_vae_int8_convrot.safetensors |
| (VAE音频) | 66 | VAELoader | minimax_h3_audio_vae_fp32.safetensors |

### 工作流内部参数（getJsonApiFormat 实测 2026-08-31）

| 参数 | 值 | 说明 |
|------|-----|------|
| 噪声种子 | 401628891037980 | **固定种子！** 必须用节点63覆盖为随机值 |
| Sampler | euler | — |
| Scheduler | simple, steps=4 | turbo 4步采样 |
| CFG | 无（BasicGuider, cfg=1） | 纯流匹配，无引导尺度 |
| LoRA | turbo only (str=1) | `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors`，lora_02~04=None，无画风LoRA |
| 分辨率 | 16:9, 0.9MP | ResolutionSelector megapixels=0.9 |
| 噪声节点 | RandomNoise（固定值） | class_type=RandomNoise，但 noise_seed 硬编码，非动态随机 |

### 固定种子问题（关键发现 2026-08-31）

工作流节点63 (RandomNoise) 的 `noise_seed` 硬编码为 `401628891037980`。这意味着：
- **每次生成都从相同噪声起点出发** → 相同提示词会产生几乎一样的画面
- **画面显得"死板、不活份"**（GK 原话："画面很死，不活份"）——缺乏扩散模型应有的自然随机变化

**GK 的最终决定（2026-09-01）：固定种子，不传随机种子。** GK 原话："不要随机种子，固定住，以后都固定住"。画面"死"的问题改用 None 默认工作流（方案C）解决——减少白色占位图对注意力的干扰，而非靠随机种子引入变化。

**所有后续提交都不传节点63**，使用工作流默认固定种子。

**注意：工作台默认值全是真实文件**（9图+3wav+1mp4），不传参时全部加载 → OOM。必须用占位文件顶位（见 runninghub-node-management.md 占位规格）。

### ResolutionSelector 节点73 + 节点56 — 画幅比例覆盖（2026-09-08 实测）

节点 73 (ResolutionSelector) 控制输出视频的画幅比例。工作台默认 `16:9 (Widescreen)`。

**方法一：覆盖节点73的aspect_ratio字段 — ❌ 实测全部失败**

尝试了 `"9:16"`、`"9:16 (Vertical)"`、`"9:16 (Portrait)"`、`"1:1"`、`"4:3"`、`"3:4"`、`"2:3"` 等值——全部在运行时报 `Value not in list` (errorCode 805)。提交时不验证（返回 RUNNING），但运行时 ResolutionSelector 节点拒绝。**此方法不可用。**

**方法二：直接传 node 56 的 width/height — ✅ 实测成功**

绕过 ResolutionSelector，直接给 MiniMaxH3ReferenceToVideo 节点（node 56）传分辨率：
```python
{"nodeId": "56", "fieldName": "width", "fieldValue": 720},
{"nodeId": "56", "fieldName": "height", "fieldValue": 1280},
```

实测结果：输出 864×1536（9:16 竖屏），正常生成无报错。

**原理**：node 56 的 width/height 来自 node 73 的输出（width=output[0], height=output[1]）。直接传 node 56 的 width/height 会覆盖 node 73 的输出。node 73 仍执行（使用默认 16:9），只是结果被忽略。

**常用画幅配置**：
| 画幅 | width | height | 实测输出 |
|------|-------|--------|----------|
| 16:9 横屏（默认） | 不传 | 不传 | 1536×880 |
| 9:16 竖屏 | 720 | 1280 | 864×1536 |

### instanceType 选择（OOM 修复 2026-08-31）

`instanceType` 控制分配的 GPU 显存大小。9 图版工作流因加载 9 个 LoadImage 节点，显存需求高。

| instanceType | 显存 | 适用场景 | OOM 风险 |
|---|---|---|---|
| `"default"` | 标准 | 2图版旧工作流、简单任务 | 9图版偶发 OOM |
| `"plus"` | 大显存 | **9图版推荐默认使用** | 几乎不 OOM |

**关键发现**：`instanceType: "default"` 连续 3 次 OOM（固定种子也 OOM，随机种子也 OOM），换 `instanceType: "plus"` 后一次成功。OOM 根因不是种子或缓存，是平台 GPU 资源不足/显存碎片。GK 原话："就是有缓存"——实测确认不是缓存，是 GPU 资源争抢。

**推荐所有 9 图版提交都用 `"instanceType": "plus"`**。payload 模板已更新为 plus。

### poll_clip.py 下载失败 workaround

`poll_clip.py` 在后台模式（`terminal(background=true)`）下偶发不保存文件——进程 exit code=0 但目标文件不存在。原因可能是后台进程 stdout 被截断导致下载逻辑未执行。

**Workaround**：检测到文件不存在时，手动 query + curl 下载：

```bash
# 1. Query task to get result URL
curl -s -X POST 'https://www.runninghub.cn/openapi/v2/query' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"taskId":"TASK_ID"}' | python3 -c "import json,sys; d=json.load(sys.stdin); [print(r.get('url','')) for r in d.get('results',[]) if isinstance(r,dict) and r.get('url')]"

# 2. Download with curl
curl -sL -o output.mp4 'RESULT_URL'
```

### 完整提交 nodeInfoList 模板（16项全传，含随机种子 + plus 实例）

```python
import random
seed = random.randint(100000000000000, 999999999999999)

node_info_list = [
    {"nodeId": "35", "fieldName": "image", "fieldValue": f"openapi/{真实图A}.png"},
    {"nodeId": "41", "fieldName": "image", "fieldValue": f"openapi/{真实图B}.png"},
    {"nodeId": "42", "fieldName": "image", "fieldValue": PLACEHOLDER_IMG},  # 占位
    {"nodeId": "43", "fieldName": "image", "fieldValue": PLACEHOLDER_IMG},
    {"nodeId": "44", "fieldName": "image", "fieldValue": PLACEHOLDER_IMG},
    {"nodeId": "36", "fieldName": "image", "fieldValue": PLACEHOLDER_IMG},
    {"nodeId": "37", "fieldName": "image", "fieldValue": PLACEHOLDER_IMG},
    {"nodeId": "38", "fieldName": "image", "fieldValue": PLACEHOLDER_IMG},
    {"nodeId": "39", "fieldName": "image", "fieldValue": PLACEHOLDER_IMG},
    {"nodeId": "31", "fieldName": "video", "fieldValue": PLACEHOLDER_VIDEO},
    {"nodeId": "28", "fieldName": "audio", "fieldValue": PLACEHOLDER_AUDIO},
    {"nodeId": "29", "fieldName": "audio", "fieldValue": PLACEHOLDER_AUDIO},
    {"nodeId": "30", "fieldName": "audio", "fieldValue": PLACEHOLDER_AUDIO},
    {"nodeId": "84", "fieldName": "value", "fieldValue": prompt},
    {"nodeId": "74", "fieldName": "value", "fieldValue": seconds},
    {"nodeId": "63", "fieldName": "noise_seed", "fieldValue": seed},  # 随机种子，覆盖固定种子
]
payload = {"addMetadata": True, "nodeInfoList": node_info_list, "instanceType": "plus"}  # plus 避免OOM
```

⚠️ **GK 要求固定种子，不传随机种子（节点63）。** GK 原话："不要随机种子，固定住，以后都固定住"。工作流默认固定种子 `401628891037980`，不传 node 63 即使用固定种子。

⚠️ **9 图版推荐 `instanceType: "plus"`**。`default` 实例偶发 OOM（errorCode 805, VRAM grow failed），`plus` 实例几乎不 OOM。

### 批量生成模式（batch_generate.py）

当 GK 要求"从1到9重新生成一遍""一块拼接给我一个完整的"时，使用批量生成脚本。模板见 `templates/batch_generate.py`。

**运行方式**：必须用 `delegate_task` 后台子代理运行（`terminal` foreground 有 600s 限制，9 个 clip 约 2 小时）。

脚本自动处理：
1. 逐个 clip 提交（随机种子 + instanceType=plus）
2. 每个 clip 下载后自动提取尾帧 + 上传到 RunningHub
3. 下一个 clip 如需首帧衔接，自动用上一 clip 的尾帧
4. OOM 自动重试（等 60s，换新种子）
5. 全部完成后 ffmpeg concat 拼接成完整 MP4

## None默认版工作流 2094671638389420033

GK 在 2026-09-01 发布的新版本，解决"用几张传几张"的需求。核心改进：所有 LoadImage 默认值设为 None，模型自动跳过未传图的节点。

### 节点映射（getJsonApiFormat 实测 2026-09-01）

| 用途 | 节点ID | class_type | fieldName | 默认值 |
|------|--------|-----------|-----------|--------|
| 参考图0 | 35 | LoadImage | image | **None** |
| 参考图1 | 41 | LoadImage | image | **None** |
| 参考图2 | 42 | LoadImage | image | **None** |
| 参考图3 | 43 | LoadImage | image | **None** |
| 参考图4 | 44 | LoadImage | image | **None** |
| 参考图5 | 36 | LoadImage | image | **None** |
| 参考图6 | 37 | LoadImage | image | **None** |
| 参考图7 | 38 | LoadImage | image | **None** |
| 参考图8 | 39 | LoadImage | image | **None** |
| 参考音频0 | 28 | LoadAudio | audio | 需传占位 |
| 参考音频1 | 29 | LoadAudio | audio | 需传占位 |
| 参考音频2 | 30 | LoadAudio | audio | 需传占位 |
| 提示词 | 84 | PrimitiveStringMultiline | value | — |
| 秒数 | 74 | PrimitiveFloat | value | — |

**与9图版 (2093898864557383681) 的差异**：无 VHS_LoadVideo 节点 31（已移除），其余节点 ID 相同。

### 提交模板（方案C：用几张传几张）

```python
# 只传2张图的示例
node_info_list = [
    {"nodeId": "84", "fieldName": "value", "fieldValue": prompt},
    {"nodeId": "35", "fieldName": "image", "fieldValue": "openapi/陆寒.png"},
    {"nodeId": "41", "fieldName": "image", "fieldValue": "openapi/出租屋.png"},
    {"nodeId": "28", "fieldName": "audio", "fieldValue": PLACEHOLDER_AUDIO},
    {"nodeId": "29", "fieldName": "audio", "fieldValue": PLACEHOLDER_AUDIO},
    {"nodeId": "30", "fieldName": "audio", "fieldValue": PLACEHOLDER_AUDIO},
    {"nodeId": "74", "fieldName": "value", "fieldValue": 15},
]
# 不传的 LoadImage 自动 None，模型跳过
# 不需要占位图！不需要占位视频！
# GK 要求：standard 优先（省积分），OOM 才升 plus
payload = {"addMetadata": True, "nodeInfoList": node_info_list, "instanceType": "standard"}
```

### 背景：为什么需要这个版本

GK 发现旧2图工作流（2093776941622059010）生成的视频"人物活一点"，但只有2个图槽不够用。9图版（2093898864557383681）虽然支持9张图，但白色占位图在注意力机制里分散了模型对真实参考图的关注，导致画面"死、不活份"。

None 默认版解决了这个矛盾：9个图槽都在，但未使用的默认为 None（零注意力权重），模型只关注实际传入的图——既有多图能力，又有2图版的注意力集中优势。

**注意：None默认版工作流音频节点（28/29/30）默认值不是 None，提交时仍需传占位音频。** 2026-09-09 实测：不传音频节点会报错。

### None默认版 OOM 风险（2026-09-09 实测）

None默认版工作流（2094671638389420033）在画面信息密度高的场景下（蒸汽朋克：飞船+工业区+火+烟雾+9:16竖屏）`instanceType: "standard"` 仍会 OOM（errorCode 805）。OOM 后换 `instanceType: "plus"` 重跑。

### RunningHub API 500 错误（2026-09-09 实测）

连续批量提交后 API 可能返回 errorCode 500。不是限流（限流是414），是服务器临时故障。等待 5-10 分钟后重试。批量脚本应包含重试机制（失败后等 180s 再试，最多 3 次）。

### 批量提交间隔

连续提交多个 clip 时，clip 之间留 60s 间隔避免服务器压力。

### 测试状态

- 2026-09-01 首次提交测试：只传2张图（陆寒+出租屋），taskId=`2094673932144836609`，等待结果确认效果
- 待确认：None 默认值的图节点是否真正被模型跳过，还是仍参与计算但输出空张量

## 2图版旧工作流 2093937520844304386

GK 在《能力》项目中指示"用老版本，正常传多个参考图试试可不可以"。

### 已知信息
- 工作流 URL: https://www.runninghub.cn/workflow/2093937520844304386
- 只有 2 个 LoadImage 节点（35 和 41），无 OOM 风险
- 更便宜（~106 coins vs 134-154 coins）
- GK 原话只开了两个参考图位

### 使用前必须 getJsonApiFormat
切换到旧工作流前，必须先用 `getJsonApiFormat` 确认节点列表——旧工作流节点 ID 与 9 图版**不互通**，传 9 图版的节点 42 会报 `803 NODE_INFO_MISMATCH`。

```bash
curl -s -X POST "https://www.runninghub.cn/api/openapi/getJsonApiFormat" \
  -H "Content-Type: application/json" \
  -d '{"apiKey": "YOUR_KEY", "workflowId": "2093937520844304386"}'
```

### 提交差异
2图版只需传 5-6 项 nodeInfoList（2 图 + 视频占位 + 音频占位 + 提示词 + 秒数 + 种子），不需要占位文件顶位（因为只有 2 个图节点）。`instanceType` 用 `"default"` 即可（2 图版不 OOM）。

## 占位文件

已在 doomsday-drama/output/ 上传过，可复用 fileName：
- 占位图 `placeholder_64x64.png` (134B) — `openapi/003e10e75c7e682c5e870640abfe7f2ff6ced25835f9c966e13a76c499bc5fa8.png`
- 占位白图 `placeholder_white.png` (5334B) — `openapi/d9bd147ced77bca4a875af12714949cd17ddd3c11cc47218b4de30185bc0b4e9.png`
- 占位视频 `placeholder_video_fixed.mp4` (1.8KB) — `openapi/c5114f4ec154a523dc5439396b11cf2f33d1b34d57c6ad1ea146251f91f5c1aa.mp4`
- 占位音频 `placeholder_tiny.mp3` (477B) — `openapi/1c8e34af202f94d0d741c12e4a90fe865bb4c771362102d5a730562c47655bc6.mp3`

## 已上传参考图 fileName 映射

| 本地文件 | RunningHub fileName | 上传时间 |
|----------|-------------------|----------|
| 陆寒.png | `openapi/371403c97f259b783a8ac5ec211963fde82d0e86ada112cade0b5ad8acfe66e2.png` | 2026-08-30 |
| 出租屋.png | `openapi/3831fb42a0026765e4ec2a7aaeb24bc37786d2f5aaf5c9636c3bc5b2e3078d01.png` | 2026-08-31 |
| 蚀者.png | `openapi/d1c53b85cdd1475510e82e3ac3b9e25e9209ff9a09a8bc4d22cbe41e73c295a7.png` | 2026-08-31 |
| 红雾废墟城市.png | `openapi/d4e8fea64f10320c19c223a100287d2de545cfbedb4daf9436cc74d883e8fbc2.png` | 2026-08-31 |
| 林婉儿.png | `openapi/86335879e879b1579bd10fe8c407c8a9ef1a56c663ceae02548b17853d8ae9c7.png` | 2026-08-31 |
| 赵磊.png | `openapi/b38289c3026a7e61547134ee86754dd597db89faa159527921e540188052b5a7.png` | 2026-08-31 |
| 湘菜馆包间.png | `openapi/e6769119c4c943b8ebf735d412e49c3d762a2bda66f94fc15be89206314f252b.png` | 2026-08-31 |
| 苏念.png | `openapi/9257298b901f2db70c3ae52f21900dceb36f44dd20f2c10547ff8d7346b84bbf.png` | 2026-09-02 |
| clip05尾帧 | `openapi/4c0e1b5ee4c28a28d79affb538b0a17414b198b5f7d4ad23edbad612d9ee1ba4.png` | 2026-08-30 |

参考图源文件在 `/home/ubuntu/末日/` 目录（root 所有，需 sudo cp 到 /tmp/ 再上传）。

## 脚本

各项目目录下的标准三件套：
- `upload_refs.py` — 批量上传真实图+占位文件，输出 fileName 映射
- `submit_clip.py <提示词txt> <秒数> <任务名> [图A fileName] [图B fileName]` — 组装参数提交，taskId 追加到 task_ids.txt
- `poll_clip.py <taskId> <输出文件名>` — 轮询至完成，下载到 output/

注意：submit_clip.py 中的 API_KEY 和 WORKFLOW_ID 是硬编码的，切换工作流版本时需修改脚本中的 WORKFLOW_ID。
**注意：submit_clip.py 尚未包含随机种子（节点63）和 instanceType=plus 的传参**，手动提交或用 execute_code 组装 payload 时需加上 `{"nodeId": "63", "fieldName": "noise_seed", "fieldValue": seed}` 和 `"instanceType": "plus"`。

批量生成时用 `batch_generate.py`（模板见 `templates/batch_generate.py`），必须通过 `delegate_task` 后台运行。

## 实测行为

- 提交返回 `{"taskId": "...", "status": "RUNNING"}` 即成功，不需等队列确认
- H3 生成约 600-840s（10-14分钟），后台轮询 + notify_on_complete 模式
- 结果 URL 24h 过期，立即下载
- query endpoint 是 `/openapi/v2/query`（不是 `/task/outputs` 也不是 `/taskOutputs`）
- query 返回的 results 是数组，每个元素有 `url` 字段（不是 `value`）
- Authorization header 用 `Bearer {apiKey}` 格式
- OOM (errorCode 805, VRAM grow failed) 在 `instanceType: "default"` 下偶发。解法：换 `instanceType: "plus"`，不要只等 30s 重试 default
- **poll_clip.py 后台模式偶发不保存文件**：进程 exit code=0 但文件不存在。检测到后手动 query + curl 下载
- **terminal foreground 600s 超时会杀掉轮询进程**：H3 生成需 780-840s，foreground 600s 不够。用 background 模式或 delegate_task
