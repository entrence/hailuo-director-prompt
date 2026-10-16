# 真人短剧 vs 动画——风格描述词陷阱

## 问题

GK 2026-09-11 原话："怎么变成动画了"。

封神小剧场分镜脚本中写有"国风2D动画，线条偏写意"等字样。如果直接把这个风格描述搬进提示词，模型会生成2D动画而非真人实拍。

## 根因

分镜脚本的"风格定调"段落描述的是**创作意图和视觉参考**，不等于**视频生成的实际风格指令**。封神小剧场实际要的是真人实拍短剧（realistic live-action short drama），分镜脚本里的"国风2D动画"只是角色立绘的美术风格参考。

## 正确做法

1. 写提示词前先确认 GK 要的是真人实拍还是动画——**默认真人实拍**，除非 GK 明确说要动画
2. 提示词风格行写：`Realistic live-action short drama.`
3. **绝对不要**在提示词中写以下词汇（除非 GK 明确要求动画）：
   - `Chinese 2D animation style`
   - `ink-wash influenced linework`
   - `anime style`
   - `cel-shaded`
   - `cartoon`
4. 如果分镜脚本提到"国风""2D""动画"等词，这些只是美术参考，不搬进提示词的风格描述

## 喜剧节奏陷阱

GK 2026-09-11 原话："节奏太慢了，这是个喜剧，弄的那么严肃"。

### 问题表现

把喜剧写成了悬疑片的节奏：
- 台词之间留长沉默（`a half-beat of silence` / `deliberate silence`）
- 用"the room breathes"等文学性描述拖慢节奏
- 运镜描述用"underlying tension""subconscious unease"等悬疑词汇

### 正确写法

喜剧的"冷"来自**情境荒诞性**和**deadpan表演**，不来自慢节奏：

```
No pause between lines. Crisp back-and-back, like reading a checklist.
```

```
The humor is dry and deadpan — the comedy comes from the absurdity of the situation, not from exaggerated expressions. Keep it deadpan and brisk.
```

### 喜剧 vs 正剧/悬疑节奏对比

| 维度 | 喜剧 | 悬疑/正剧 |
|------|------|----------|
| 台词间隔 | 不停顿，快速来回 | 半拍停顿，留白 |
| 沉默 | 不用 | 刻意留沉默 |
| 运镜描述 | brisk, crisp | underlying tension, unease |
| 基调词 | deadpan, brisk, absurd | heavy, ominous, foreboding |
| 声音描述 | minimal pauses | the room breathes, deliberate silence |

### 参考已有示例

`references/comedy-fast-pace-example.md` — 15秒10个镜头的喜剧示例，平均1.5秒一切，台词密集硬切。
