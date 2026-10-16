# 喜剧快节奏场景 — 教室念情书（第四幕）完整示例

15秒短剧，5张参考图（林屿川、教室、李疏清、林玥、老师），10组镜头，7句对白。
本例展示活泼俏皮基调下的密集硬切、反应镜头链、群白写法，以及画外角色转上画。所有对白用 (Sx) Speaker ID + `<d>[Language] 台词</d>` 格式写入 detailed_description 各 Shot。

## 参考图

| 编号 | 文件 | 用途 |
|------|------|------|
| <Picture 1> | 林屿川.png | 锁定林屿川外观 |
| <Picture 2> | 教室.png | 锁定教室场景 |
| <Picture 3> | 李疏清.png | 锁定李疏清外观 |
| <Picture 4> | 林玥.png | 锁定林玥外观 |
| <Picture 5> | 老师.png | 锁定老师外观（本幕首次上画） |

## subject_definitions

```
<Subject 1> is the young male student in <Picture 1>, with unkempt black hair, a blue-and-white school uniform jacket, and a lean face with dark eyes. Personality: outwardly aloof but soft-hearted, pretends composure when nervous but panic shows in his eyes.
<Subject 2> is the classroom environment in <Picture 2>, featuring a green chalkboard, rows of wooden desks, fluorescent ceiling lights, and large windows on the right wall.
<Subject 3> is the young male student in <Picture 3>, with a round face, short neat hair, and a blue-and-white uniform. Personality: earnest and easily shocked.
<Subject 4> is the young female student in <Picture 4>, with long straight black hair, a pale slender face, and a blue-and-white uniform. Personality: cool and quiet, with a faint melancholic detachment.
<Subject 5> is the middle-aged male teacher in <Picture 5>, with short cropped hair, a receding hairline, a dark jacket over a white shirt. Personality: outwardly stern but loves stirring up drama, grinning slyly when egging students on.
<Audio 1> is the voice-timbre reference for <Subject 1> (S1), containing a young male vocal layer.
<Audio 2> is the voice-timbre reference for <Subject 5> (S2), containing a middle-aged male vocal layer.
```

## 镜头结构与对白路由

| Shot | 时间 | 景别 | 说话人 | Speaker ID | 台词 | 运镜 |
|------|------|------|--------|-----------|------|------|
| 1 | 0-2s | 近景 | 林屿川 | (S1) | "这什么肉麻玩意..." | 固定 |
| 2 | 2-3.5s | 中近景 | 老师 | (S2) | "念不出来是吧，我来替你念" | 固定 |
| 3 | 3.5-4.5s | 近景 | 林屿川 | (S1) | "哎别我自己来" | 固定 |
| 4 | 4.5-6.5s | 近景 | 林屿川 | (S1) | "致————林玥！" | Push In |
| 5 | 6.5-7.5s | 近景 | (李疏清反应) | — | (无声) | 固定 |
| 6 | 7.5-9s | 中景 | (同学们反应) | — | (环境嘈杂) | 横移 |
| 7 | 9-10.5s | 近景 | (林玥反应) | — | (无声) | 固定 |
| 8 | 10.5-11.5s | 特写 | 老师 | (S2) | "你说什么？？？" | 固定 |
| 9 | 11.5-13s | 中景→近景 | 林屿川 | (S1) | "林玥，我写的情书就是给林玥的" | 横移 |
| 10 | 13-15s | 远景 | 同学们(群白) | (S3) | "卧槽？给林玥？林屿川疯了吧！" | 固定 |

## 关键写法要点

### 1. 密集硬切节奏

10组镜头/15秒，平均1.5秒一切。Shot 3仅1秒（抢话节拍），Shot 5仅1秒（反应闪现）。硬切是喜剧节奏的核心工具，不使用软过渡。

### 2. 反应镜头链（Shot 5-7）

关键台词"致——林玥！"落地后，连续切三个反应：
- Shot 5: <Subject 3> — eyes wide, mouth open, a flash of shocked sadness (1 sec)
- Shot 6: classmates — surprised gazes panning across (1.5 sec)
- Shot 7: <Subject 4> — looking at a hand mirror, turns, face flushing red (1.5 sec, interrupted mid-action)

每个反应镜头只拍一个角色/群体，表情具体不笼统。

### 3. 对白交替节奏（Shot 1-3）

A 嘟囔→B 插嘴→A 抢话，三组镜头共3.5秒，语速递增制造喜剧张力。每个说话人独立 Shot。

```
[Shot 1] ... <Subject 1> (S1) mutters under his breath in a low, dismissive young male voice, using the timbre referenced from <Audio 1>, <d>[Chinese] 这什么肉麻玩意...</d>
[Shot 2] ... <Subject 5> (S2) says in a sly, teasing middle-aged male voice with a grin, using the timbre referenced from <Audio 2>, <d>[Chinese] 念不出来是吧，我来替你念</d>
[Shot 3] ... <Subject 1> (S1) blurts out in a quick, urgent young male voice, <d>[Chinese] 哎别我自己来</d>
```

### 4. 群白写法（Shot 10）

全班炸锅的群白写入 Shot 10，用 (S3) 群体 Speaker ID + `<d>` 格式，注明多人嘈杂+动作音效：

```
[Shot 10] ... Classmates' chorus (S3), multiple noisy voices, surprised and gossiping, <d>[Chinese] 卧槽？给林玥？林屿川疯了吧！</d>, accompanied by desk-slapping, chair creaking, and overlapping laughter.
```

### 5. 画外角色转上画

老师在前几幕仅画外声音（无 Subject 定义），第四幕首次上画：
- 新增 <Subject 5>，用 VLM 分析 <Picture 5> 提取外观
- 对白从 off-screen 变为正常直接对白写入老师所属 Shot
- 老师性格气质定义写入 subject_definitions
- 性格贯穿 Shot 2（嬉皮笑脸）和 Shot 8（不可置信），表情反差明确

### 6. 运镜中的画外音（Shot 9）

林屿川中景指着林玥，镜头横移到林玥近景，画外音同期播放：

```
[Shot 9] ... <Subject 1> extends his right arm, index finger pointing toward the upper-right of the frame. The camera begins a slow horizontal pan from <Subject 1>'s medium shot, following the pointing direction toward <Subject 4>'s close-up. <Subject 1> (S1) narrates off-screen in a feigned-calm young male voice with desperate resolve, <d>[Chinese] 林玥，我写的情书就是给林玥的</d>
```

运镜+画外音叠加，声音跟着镜头走，不拆到 overall_soundscape。

### 7. 基调体现

detailed_description 风格行（在 [Shot 1] 之前）标注活泼基调：

```
The tone is livelier and warmer than the previous scenes, with a slightly brighter color palette. Fast pacing with frequent hard cuts, averaging 1-2 seconds per shot, strong comedic rhythm.
```

### 8. 性格气质贯穿

- <Subject 1> 林屿川："外冷内热、嘴硬心软，紧张时会装从容但眼底藏不住慌" — Shot 1嘟囔嫌弃、Shot 3抢话警觉、Shot 4故作正经播音腔、Shot 9破罐破摔坦然
- <Subject 5> 老师："表面严肃但爱起哄看热闹" — Shot 2嬉皮笑脸、Shot 8不可置信，两个表情形成反差
- <Subject 4> 林玥："清冷安静、略带忧郁疏离感" — Shot 7照镜子不是在欣赏而是发呆出神，被点名后脸红
