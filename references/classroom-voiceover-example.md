# 教室情书事件 — 含画外音的完整示例

13秒短剧，3张参考图（老师、学生、教室），6组镜头，含内心独白画外音与震惊画外音。
本例展示纯画外音场景的对白路由：所有画外音用 (Sx) Speaker ID + `<d>` 格式写入 detailed_description 各 Shot，overall_soundscape 仅保留全局环境音概述。

这是与 [dialogue-routing-example.md](dialogue-routing-example.md) 的对照——病房场景内心独白和直接对白兼有，教室场景只有画外音无直接对白。另见 [comedy-fast-pace-example.md](comedy-fast-pace-example.md) 了解喜剧快节奏场景。

## 参考图

| 编号 | 文件 | 用途 |
|------|------|------|
| <Picture 1> | 老师.png | 锁定老师外观 |
| <Picture 2> | 林屿川.png | 锁定学生外观 |
| <Picture 3> | 教室.png | 锁定教室场景 |

## subject_definitions

```
<Subject 1> is the middle-aged male teacher in <Picture 1>, with short cropped hair, a receding hairline, a dark jacket over a white shirt, and a stern expression.
<Subject 2> is the young male student in <Picture 2>, with unkempt black hair, a blue-and-white school uniform jacket, and a lean face with dark eyes.
<Subject 3> is the classroom environment in <Picture 3>, featuring a green chalkboard with "高三(8)班" written in the lower-left corner, rows of wooden desks, and a wall calendar on the left showing "2007年10月16日".
<Audio 1> is the voice-timbre reference for <Subject 2> (S1), containing a young male vocal layer suitable for inner monologue.
```

## 镜头结构

| Shot | 时间 | 景别 | 运动 | 内容 | 画外音 | Speaker ID |
|------|------|------|------|------|--------|-----------|
| 1 | 0-3s | 中景 | 固定 | 老师拍A4纸在讲台上 | 无 | — |
| 2 | 3-6s | 近景 | 硬切固定 | 老师正面指镜头说话 | 无 | — |
| 3 | 6-9s | 中景 | 硬切固定 | 林屿川正面，背后同学哄笑 | 无 | — |
| 4 | 9-10.5s | 特写 | 硬切固定 | 日历"2007年10月16日" | 内心独白 | (S1) |
| 5 | 10.5-12s | 特写 | Pan横摇 | 黑板左下角"高三(8)班" | 画外音继续 | (S1) |
| 6 | 12-13s | POV | 下摇 | 林屿川第一视角双手放课桌 | 震惊画外音 | (S1) |

## 字段级写法

### detailed_description 中画外音的写法

所有画外音写入对应 Shot，用 (Sx) Speaker ID + `<d>[Language] 独白</d>` 格式：

```
The target video uses a realistic drama style with flat fluorescent classroom lighting and a slightly desaturated color palette.
[Shot 1] A medium shot establishes <Subject 3>, the classroom with its green chalkboard, rows of wooden desks, and wall calendar. <Subject 1>, the teacher with short cropped hair and a dark jacket, stands at the podium slapping an A4 sheet onto the desk. The camera holds for 3 seconds. The slap of paper on wood echoes sharply.

[Shot 2] At 00:03.000, a hard cut to a close-up of <Subject 1> facing the camera. He points directly at the lens, mouth open mid-shout, brow furrowed. The camera holds for 3 seconds. His voice booms across the classroom but no subtitle text is shown — his shout is diegetic sound only.

[Shot 3] At 00:06.000, a hard cut to a medium shot of <Subject 2>, the young student with unkempt black hair and a blue-and-white uniform, sitting upright with a bewildered expression. Behind him, a dozen classmates in identical uniforms turn to look — some covering their mouths, one slapping his desk, others nudging each other. Their faces vary naturally in shape and hairstyle, all ordinary high-school faces. The camera holds for 3 seconds. Overlapping laughter and desk-thumping fill the room.

[Shot 4] At 00:09.000, a hard cut to a close-up of the wall calendar on the left, clearly showing "2007年10月16日" in black print. The camera holds for 1.5 seconds. The classroom noise fades to near-silence. <Subject 2> (S1) narrates off-screen in a low, confused young male voice, using the timbre referenced from <Audio 1>, <d>[Chinese] 2007年……高三八班……</d>

[Shot 5] At 00:10.500, a slow Pan across the chalkboard surface, settling on the lower-left corner where "高三(8)班" is written in chalk. The camera moves over 1.5 seconds. <Subject 2> (S1) continues off-screen, the voiceover accelerating slightly with a faint tremor, <d>[Chinese] 这不是我的教室……这是什么时候？</d>

[Shot 6] At 00:12.000, a tilt-down to a POV shot of hands resting on a wooden desk — <Subject 2>'s hands in blue-and-white uniform sleeves. The camera holds for 1 second. Close-up rapid breathing. <Subject 2> (S1) narrates off-screen in a suddenly sharp, incredulous voice, <d>[Chinese] 我穿越了！</d>
```

### overall_soundscape

```
overall_soundscape:
Classroom ambience throughout: fluorescent-light hum, distant hallway noise, and overlapping student chatter that peaks in Shot 3 and fades to near-silence from Shot 4 onward.
```

### non_diegetic_music

```
non_diegetic_music:
N/A
```

## 关键写法要点

1. **画外音写法**：`<Subject N> (Sx) narrates off-screen in a [语气描述] voice, <d>[Language] 独白原文</d>.` — 写入对应 Shot，标注 off-screen，语气描述包含声调/语速/情感。

2. **Speaker ID 全局复用**：林屿川的内心独白和震惊画外音始终用 (S1)，Audio 1 定义绑定 (S1) 也复用同一 ID。

3. **overall_soundscape 不承载画外音**：只保留全局环境音概述。画外音写入 detailed_description 各 Shot 描述。

4. **non_diegetic_music 显式声明 N/A**：画外音段落通常不配乐，用静音衬托独白。不省略该字段。

5. **retention_analysis 覆盖 Shot 6 的双手**：POV 镜头只出现手部时注明"仅出现双手手部及袖口"。

6. **风格行在 [Shot 1] 之前**：用1-2句英文建立整体画风/光影/色调。

7. **VLM 预分析参考图**：本例中先用 siliconflow-vlm 的 analyze_image.py 分析了三张参考图，提取到关键场景锚点（黑板左下角确实有"高三(8)班"粉笔字、左侧确有日历显示"2007年10月16日"），这些锚点直接写入 <Subject 3> 的场景定义和 Shot 4/5 的画面描述。
