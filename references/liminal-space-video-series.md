# 阈限空间视频系列设计参考

记录十二星座避难所系列和电梯按钮系列的设计规律、提示词写法、差异化要求。

## 系列格式

### 十二星座避难所系列

每集结构（15秒，4-5个 Shot）：
1. **门外关门**（2-3秒）：第一视角接近关闭的门，环境建立，回头瞥一眼
2. **解锁+开门**（2-3秒）：交互解锁（密码/指纹/钥匙/手柄），门开，光透出
3. **门内通道**（3-4秒）：跑/走通过走廊，回头门还开着
4. **到达避难所**（4-5秒）：进入内部空间，环视，门密封，安全了
5. **（可选）回望**（1-2秒）：从床上/椅子上回头看已关的门

### 电梯按钮系列

每集结构（15秒，4-5个 Shot）：
1. **发现按钮**（2-3秒）：电梯内发现不该存在的楼层按钮
2. **按下+运行**（2-3秒）：按下后电梯异常运行
3. **门开+异空间**（3-4秒）：第一视角走出电梯，探索异空间
4. **不对劲**（2-3秒）：发现异常细节
5. **门关/回去**（1-2秒）：回头，电梯门关上

## 差异化矩阵（十二星座避难所）

| 星座 | 门外环境 | 锁类型 | 走廊风格 | 避难所风格 | 色调 |
|------|---------|--------|---------|-----------|------|
| 白羊 | 沙漠峡谷 | 现代银色门把手 | 混凝土+红壁灯 | 碉堡军械室 | 赭黄→猩红→暗灰红 |
| 金牛 | 地下停车场 | 电子门禁面板 | 混凝土+橙LED | 霓虹卧室 | 冷灰白→橙红→粉绿 |
| 双子 | 地铁站台 | 电子密码键盘 | 电缆管道+青黄 | 通讯中心 | 蓝灰→青黄 |
| 巨蟹 | 海崖涉水 | 蓝色圆环锁 | 水波光影 | 洞穴卧室 | 灰蓝→银紫→暖黄 |
| 狮子 | 冰封城堡 | 兽首衔环 | 罗曼拱廊+火炬 | 王座室 | 冰蓝灰→金红→冷暖交织 |
| 处女 | 废弃医院 | 金属门闩 | 白色走廊+绿光 | 医疗室 | 暗黄绿→紫粉绿→冷白 |
| 天秤 | 黄昏荒野 | 门把手 | 白砖+花环 | 卧室+抽象画 | 橙红→粉紫→暗紫 |
| 天蝎 | 废弃工厂 | 红色指示按钮 | 铆钉钢板+洋红LED | 监控室 | 灰绿锈→血红→洋红→屏蓝 |
| 射手 | 高空信号塔 | 太阳能电子键盘 | 多彩LED+管道 | 云端卧室 | 冰青白→紫品红→暖米白 |
| 摩羯 | 雪松林 | 蓝色背光键盘 | 极光能量场 | 行军床+星云投影 | 灰白雾→紫品红→星云蓝绿 |
| 水瓶 | 深海沉船 | 量子加密触屏 | 飞船白走廊 | 驾驶舱 | 墨绿蓝→紫粒子→冷白蓝 |
| 双鱼 | 雨林瀑布 | 共振频率音叉 | 霓虹岩缝+积水 | 水淹卧室+鱼群 | 灰绿→紫绿→海蓝 |

## 海螺视频提示词结构模板

每个星座/集使用统一六段格式：

```
subject_definitions:
<Subject 1> is [门外关门状态] from <Picture 1> top-left panel. [详细特征].
<Subject 2> is [门外开门状态] from <Picture 1> top-right panel. [详细特征].
<Subject 3> is [走廊] from <Picture 1> bottom-left panel. [详细特征].
<Subject 4> is [避难所内部] from <Picture 1> bottom-right panel. [详细特征].
<Picture 1> is a 4-panel reference grid showing: [四格概述].

summary:
[reference generation] A 15-second first-person POV handheld video following the narrative sequence of <Picture 1>. [概述四个Shot]. Handheld shaky camera with dreamcore liminal aesthetic and an urgent sense of escape, as if being chased. No people visible on camera — only hands at the bottom of frame. Uses <Picture 1> as the visual reference for all environments.

retention_analysis:
<Subject 1> (appears in [Shot 1]): partially_preserved - [保留内容].
<Subject 2> (appears in [Shot 2]): partially_preserved - [保留内容].
<Subject 3> (appears in [Shot 3]): partially_preserved - [保留内容].
<Subject 4> (appears in [Shot 4]): partially_preserved - [保留内容].
<Picture 1> (visual reference for all shots): weak_reference - [参考关系].

detailed_description:
[风格行]. Handheld shaky camera at chest height with motion blur, slight chromatic aberration on edges, heavy vignetting, found-footage style. Fast-paced movement, each shot lasting 2-4 seconds with whip-pan transitions.

[Shot 1] ...
[Shot 2] At 00:03.000, ...
[Shot 3] At 00:06.000, ...
[Shot 4] At 00:10.000, ...

overall_soundscape:
[全局环境音概述].

non_diegetic_music:
N/A
```

## 动态效果写法要点

### 自然元素动态（GK 强调）

- **海浪**：waves swell, crest, and break, spray hitting the lens, water streaming down the glass, 涉水有阻力感
- **雾/水汽**：drifting mist, swirling in slow eddies, 两种雾气混合（如白色瀑布雾+紫色能量雾）
- **水波光影 (caustics)**：caustic patterns crawl across every surface in real time — ripples, circles, flowing lines, never static
- **鱼群游动**：fish dart between objects, weaving through plants, flashing silver as they turn, movement natural and fluid
- **雪/冰**：snow crunching underfoot, ice cracking, frost on surfaces
- **火焰/火炬**：flames dancing, flickering, casting shifting shadows

### 门关闭时序（GK 确认规则）

门不应在人刚进门就关闭。正确时序：
1. 进门后门保持开着
2. 跑走廊时回头看门还开着（看到外部光线透入）
3. 到达避难所内部后门才密封（"the person just made it in"）

### 交互解锁动作（GK 确认规则）

不能一句话带过"按完就开"。必须分步骤：
- 手伸出（可加颤抖/僵硬/湿冷等状态）
- 逐位输入/逐个动作
- 可加入失误/犹豫（按错、手滑）
- 等待响应
- 机械响应声
- 门开

### 爬梯/下降过程（GK 确认规则）

不能快切跳过。必须完整展示：跨上梯子→POV朝下→每步横档声→头顶暗门缩小→光线变化→到达底部踏上地面。

## MJ 多格生图提示词写法

### 基本原则

1. **每个面板开头标注位置**：`Panel top-left:` / `Panel top-center:` / `Panel bottom-right:` 等
2. **重复元素逐个描述**：如电梯按钮，不能写"all buttons are silver"，必须逐个 `Button 1 is round silver metal with black text "1". Button 2 is ...` 逐个声明
3. **面板间一致性**：如果多个面板展示同一场景不同状态，开门面板必须写 `the exact same [场景] from the exact same angle as top-left, nothing has changed inside — same [元素1], same [元素2]` 并复述关门面板的元素
4. **叙事连贯**：面板必须是一条连贯叙事链，不能有角度跳跃或逻辑断裂
5. **结尾统一**：`No people, photorealistic, 8k, masterpiece, cinematic lighting, wide angle, liminal space, dreamcore, eerie, uncanny, [主题] atmosphere`

### 网格大小选择

- **四宫格 2×2**：适合4步叙事（关门/开门/走廊/避难所）
- **六宫格 2×3**：适合6步叙事（关门/按钮特写/开门/迈脚/走廊全貌/回头）
- GK 更倾向六宫格——信息更完整，但四宫格也能用

### 按钮面板写法（电梯系列）

3×4 排列按钮必须逐个描述颜色材质：
```
Button 1 is round silver metal with black text "1".
Button 2 is round silver metal with black text "2".
...
Button 13½ is solid black with white text "13½".
Only the 13½ button is black, all other eleven buttons are silver metal.
```
