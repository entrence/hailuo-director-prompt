# 病房对话 — 直接对白与内心独白路由示例

15秒短剧，2张参考图（青年林屿川、绝症林玥），5组镜头，4个对话节拍。
本例展示同一场景中两种音频的路由：内心独白和直接对白均写入 detailed_description 各 Shot 描述中，用 (Sx) Speaker ID + `<d>` 格式，overall_soundscape 仅保留全局环境音概述。

这是与 [classroom-voiceover-example.md](classroom-voiceover-example.md) 的对照——教室场景只有画外音无直接对白，病房场景两者兼有。另见 [comedy-fast-pace-example.md](comedy-fast-pace-example.md) 了解喜剧快节奏场景中的密集对白交替与群白写法。

## 参考图

| 编号 | 文件 | 用途 |
|------|------|------|
| <Picture 1> | 林屿川-青年.png | 锁定青年林屿川外观 |
| <Picture 2> | 林玥-绝症.png | 锁定绝症林玥外观 |

## subject_definitions

```
<Subject 1> is the young man in <Picture 1>, with short black hair, a pale complexion, a dark-grey jacket, and dark circles under his eyes.
<Subject 2> is the young woman in <Picture 2>, with long black hair spread on the pillow, a pale and thin face, wearing a white hospital gown.
<Audio 1> is the voice-timbre reference for <Subject 1> (S2), containing a low, tired young male vocal layer.
<Audio 2> is the voice-timbre reference for <Subject 2> (S1), containing a weak, breathy female vocal layer.
```

## 镜头结构与音频路由

| Shot | 时间 | 景别 | 说话人 | Speaker ID | 台词 | 语言 |
|------|------|------|--------|-----------|------|------|
| 1 | 0-4s | 大近景 | 林屿川(内心) | (S2) | "后来这个我以为的坏女孩，临死前给我留了一千万，盘活了我的公司。" | [Chinese] |
| 2 | 4-8s | 大近景 | 林玥(直接) | (S1) | "你能来，真是挺好..." | [Chinese] |
| 3 | 8-10.5s | 大近景 | 林屿川(直接) | (S2) | "我该早点来" | [Chinese] |
| 4 | 10.5-13s | 大近景 | 林玥(直接) | (S1) | "不晚..." | [Chinese] |
| 5 | 13-15s | 大特写 | (无人) | — | (无声) | — |

## 字段级写法

### detailed_description 中对白与独白的写法

所有声音（内心独白、直接对白、环境音）均写入对应 Shot 的详细描述中，用 (Sx) Speaker ID + `<d>[Language] 台词</d>` 格式：

```
The target video uses a restrained, intimate drama style with low-key hospital lighting and a muted color palette.
[Shot 1] An extreme close-up of <Subject 1>, his face filling the frame at a slight upward angle. His eyes are red-rimmed, lips pressed together. The camera holds for 4 seconds. The room is nearly silent except for the faint rhythmic beep of a heart monitor and <Subject 1>'s slow breathing. <Subject 1> (S2) narrates off-screen in a low, exhausted voice with restrained grief, using the voice timbre referenced from <Audio 1>, <d>[Chinese] 后来这个我以为的坏女孩，临死前给我留了一千万，盘活了我的公司。</d>

[Shot 2] At 00:04.000, a hard cut to an extreme close-up of <Subject 2>, at eye level. Her lips part slightly as she speaks in a weak, slow, breathy but gentle female voice, using the timbre referenced from <Audio 2>, <d>[Chinese] 你能来，真是挺好...</d> The heart monitor beep continues. The camera holds for 4 seconds. A faint exhale follows the final word.

[Shot 3] At 00:08.000, a hard cut to an extreme close-up of <Subject 1>. He leans slightly forward, brow furrowed with guilt. <Subject 1> (S2) says in the same low young male voice, quieter and more urgent, <d>[Chinese] 我该早点来</d> The camera holds for 2.5 seconds.

[Shot 4] At 00:10.500, a hard cut to an extreme close-up of <Subject 2>. A faint, resigned smile touches her lips. <Subject 2> (S1) replies in the same weak breathy female voice, barely above a whisper, <d>[Chinese] 不晚...</d> The camera holds for 2.5 seconds.

[Shot 5] At 00:13.000, a hard cut to a macro close-up of a handwritten letter resting on the bedside table, its edge curling slightly. No dialogue. The heart monitor beep continues alone.
```

### overall_soundscape 的处理

overall_soundscape 只保留一句全局环境音概述，不逐 Shot 拆分：

```
overall_soundscape:
Hospital room tone throughout the video: faint rhythmic heart-monitor beep, IV pump hum, and distant muffled city noise outside the window.
```

### non_diegetic_music

```
non_diegetic_music:
N/A
```

## 关键写法要点

1. **直接对白写法**：`<Subject N> (Sx) says in a [声音特征] voice, <d>[Language] 台词原文</d>.` — 说话人 ID、声音特征、台词三者绑定，写入该说话人所属 Shot。

2. **内心独白写法**：`<Subject N> (Sx) narrates off-screen in a [语气描述] voice, <d>[Language] 独白原文</d>.` — 同样写入对应 Shot，标注 off-screen。

3. **声音特征必须具体**：声调（low/weak/shaking）、语速（slow/fast）、情感（guilty/relieved/gentle），让导演台渲染正确的口型和面部情绪。

4. **overall_soundscape 不承载逐 Shot 声音**：只保留全局环境音概述。逐 Shot 声音写入 detailed_description 各 Shot 描述。重复到两个字段会导致导演台AI混淆说话人归属（Pitfall #17）。

5. **每个对话节拍给独立 Shot**：说话人切换时硬切到该说话人的大近景，不把两个角色的对白塞进同一个 Shot。

6. **台词原文逐字保留**：省略号、标点都要原样保留，不增删不"优化"（Pitfall #15）。

7. **Speaker ID 全局复用**：林屿川始终是 (S2)，林玥始终是 (S1)，在内心独白和直接对白中复用同一 ID。Audio 定义绑定说话人时也复用同一 (Sx)。

8. **风格行在 [Shot 1] 之前**：用1-2句英文建立整体画风/光影/色调。
