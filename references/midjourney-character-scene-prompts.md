# Midjourney 角色与场景参考图提示词

用 MJ 生成角色立绘和场景图，作为海螺导演台多模态参考生成的输入素材。
本文件记录从实际项目中迭代出的提示词写法规律和用户偏好。

## 角色立绘

### 基本模板

```
/imagine prompt: [年龄] [国籍] [性别], [角色气质描述], [发型], [面部特征], [服装], [姿态/表情], [可选: 年代/地域aesthetic标签], CG character art, hyper-realistic render, PBR textures, [灯光], 8K, Unreal Engine 5 style, clean white background --ar 2:3 --s [250-400] --raw
```

### GK 确认的有效示例

```
a 42-year-old Chinese female teacher, stern and intimidating, straight black hair tied back, gold-rimmed glasses, wearing a black straight-cut suit jacket, large scissors tucked into her belt, arms crossed, fierce eagle-eyed gaze, no-nonsense expression, 2008 Chinese school aesthetic, CG character art, hyper-realistic render, PBR textures, harsh fluorescent lighting, 8K, Unreal Engine 5 style, clean white background

a 18-year-old Chinese teenage girl, quiet and introverted honor student, simple ponytail, neat blue-and-white Chinese school uniform fully buttoned, canvas shoulder bag strap, no makeup, gentle and reserved expression, slight downward gaze, 2008 Chinese county-town school aesthetic, CG character art, hyper-realistic render, PBR textures, soft natural lighting, 8K, Unreal Engine 5 style, clean white background

a 28-year-old Chinese man, cold and aloof, long black hair, slender, youthful boyish face, sharp dark eyes, unfathomable gaze, wearing a black jacket over a dark t-shirt, black pants, arms crossed, calm unreadable expression, CG character art, hyper-realistic render, PBR textures, dramatic rim lighting, 8K, Unreal Engine 5 style, clean white background, --ar 2:3 --s 350 --raw
```

### 短语原则（GK 反复纠正7版后总结）

**每个特征写成一个短语，不写长句。** 这是最重要的规则。

| ✅ 正确 | ❌ 错误 |
|---------|---------|
| `short black hair` | `short black hair with a slight upward sweep at the front` |
| `sharp dark eyes` | `deep-set dark eyes with an icy cold unfathomable gaze` |
| `wearing a black jacket` | `wearing a fitted dark grey tactical jacket with collar popped` |
| `arms crossed` | `standing in a confident relaxed pose with arms crossed` |
| `calm unreadable expression` | `exuding an intimidating aura of quiet danger` |
| `slender` | `lean muscular build` / `broad-shouldered muscular build` |

长句修饰会让 MJ 混淆，生成丑陋粗糙的图。短语让 MJ 精准理解每个特征。

### 风格后缀铁律

**角色图风格后缀固定为：**
```
CG character art, hyper-realistic render, PBR textures, [灯光], 8K, Unreal Engine 5 style, clean white background
```

**确认有效的灯光词：**
- `dramatic rim lighting` — 通用角色
- `harsh fluorescent lighting` — 严厉角色/室内
- `soft beauty lighting` — 女性角色
- `soft natural lighting` — 学生/日常
- `warm front lighting` — 老人/温暖角色
- `dramatic side lighting` — 反派/侧面角色

**禁用的风格后缀（会生成丑图）：**
- ❌ `3D CG animation style, Unreal Engine 5 render quality` — 生成粗糙3D建模脸
- ❌ `CG character art, high detail, sharp focus, [灯光], octane render` — 生成粗糙非CG风
- ❌ `photorealistic, photography, photo` — 真人拍摄风，不是CG
- ❌ 去掉 `clean white background` — 会生成非白底

**场景图风格后缀：**
```
CG environment art, hyper-realistic render, PBR textures, [灯光], 8K, Unreal Engine 5 style
```
场景图不加 `clean white background`。

### aesthetic 标签使用规则

**只有 MJ 训练数据中存在的真实年代/地域/亚文化 aesthetic 标签才可用。** GK 确认的有效示例中都带这种标签：

- `2008 Chinese school aesthetic` ✅ — 具体年代+地域+场景，MJ 能理解
- `2008 Chinese county-town school aesthetic` ✅ — 更精确的年代+地域
- `emo scene kid aesthetic` ✅ — 真实存在的亚文化风格，MJ 有训练数据
- `Japanese idol aesthetic` ✅ — 日系美型风格，MJ 有训练数据

**禁止自造 aesthetic 标签。** 以下都是 H 自造的、MJ 不理解的复合标签，会导致丑图：

- ❌ `modern urban apocalypse aesthetic` — GK 明确说"这个是丑的元凶"
- ❌ `cold and aloof loner survivor aesthetic` — 自造角色气质标签
- ❌ `femme fatale aesthetic` — MJ 会过度渲染成卡通风
- ❌ `friendly two-faced traitor aesthetic` — 自造角色气质标签
- ❌ `weary ordinary working man aesthetic` — 自造角色气质标签
- ❌ `post-apocalyptic horror aesthetic` — 自造风格标签

原因：MJ 对 `2008 Chinese school aesthetic` 这类真实场景标签有训练数据，能准确渲染。但对 `modern urban apocalypse aesthetic` 这类自造复合标签，MJ 会猜测性渲染，把角色脸搞脏搞粗糙。

角色气质应该用普通描述词（`cold and aloof`、`beautiful and alluring`、`weary man`）直接写在提示词里，不包装成 aesthetic 标签。

### 禁止的写法

1. **不堆形容词叠罗汉**：`devastatingly handsome, sharp jawline, high cheekbones, deep-set dark eyes with an icy cold unfathomable gaze` — MJ 会懵
2. **不写健美体型词**：`lean muscular build` `broad-shouldered muscular build` `tactical` — 会生成健美写实风
3. **不写战术装备词**：`tactical jacket with collar popped` `cargo pants` — 不是写实军事题材
4. **不写长定语从句**：`wearing a dark blue polo shirt stretched tight across broad shoulders` — 写成 `wearing a dark blue polo shirt` 就够
5. **不自作主张换风格后缀**：GK 确认了 `hyper-realistic render, PBR textures, 8K, Unreal Engine 5 style, clean white background` 这套，不要换成 `octane render` 或其他
6. **不自造 aesthetic 标签**：只用真实年代/地域/亚文化标签，不造复合气质标签

### 三视图

### GK 确认的现代职场版 UE5 模板（2026-09-07 确认）

用户在现代打工人版封神小剧场项目中，反复试验后确认了一套有效的现代职场角色 MJ 提示词结构。关键发现：

1. **风格后缀用 `Unreal Engine 5 style, highly detailed, 8k`** — 不是完整 CG 风格后缀（`CG character art, hyper-realistic render, PBR textures`），也不是写实风后缀。这套 UE5 后缀能稳定出 3D CG 渲染质感，不会偏手绘/漫画
2. **风格关键词放在末尾** — `Unreal Engine 5 style` 放在最后，不要放开头（放开头反而偏手绘）
3. **三视图用 `character three-view reference sheet, front view side view back view`** — 替代 `full body shot`，放在服装描述之后
4. **干净背景用 `plain white background, solid color backdrop, studio lighting, no environment, no props behind, clean composition`** — 这组词比 `clean white background` 更有效，能确保背景纯净不生成多余场景元素
5. **不要用 `--niji`** — 用户明确不要 niji（动漫模型），要纯 v 系列 UE5 渲染风
6. **不要加 `Pixar style` / `3D animated character design` / `smooth rendering, stylized proportions`** — 这些词会导致偏手绘漫画风，不是用户要的 UE5 CG 风
7. **不要加 `character reference sheet`** — 这个词容易触发手绘设定图风格，用 `character three-view reference sheet` 或干脆不加

### 用户确认的有效示例（现代职场版）

```
Modern office worker character design, Chinese man, age 45, medium-length black goatee beard, long black hair tied in a bun, wise tired face, wearing navy blue business suit with loosened tie, holding a clipboard binder, ID badge on chest, reading glasses, calm resigned expression, middle management appearance, character three-view reference sheet, front view side view back view, plain white background, solid color backdrop, studio lighting, no environment, no props behind, clean composition, Unreal Engine 5 style, highly detailed, 8k
```

### 三视图

```
/imagine prompt: character reference sheet, turnaround, [角色描述], multiple views, front view, side view, back view, full body, hyper-realistic CG character render, PBR textures, dramatic studio lighting, 8K, Unreal Engine 5 style, white background --ar 16:9 --s 150 --raw --c 0
```

三视图参数要点：
- `--ar 16:9` 横向构图容纳三角度
- `--s 150`（不要太高，保证三角度一致性）
- `--c 0` 混乱度归零，减少视角间偏差

## 场景图

### 基本模板

```
/imagine prompt: [场景核心元素1-2个], simple and clean, [lighting], CG environment art, hyper-realistic render, PBR textures, [灯光], 8K, Unreal Engine 5 style --ar 16:9 --s 100 --raw
```

### 场景图关键原则

1. **元素要少**：每个场景只写2-3个核心元素，加 `minimal` / `clean` / `simple` 控制元素数量
2. **`--s` 降到 100-150**：降低风格化，减少 MJ 自行添加随机细节
3. **不加年代标签**：不要写 `2008 Chinese` / `rural China` 等——用 `modern Chinese` 替代
4. **去掉所有陈旧词**：`rusty`、`peeling paint`、`faded`、`dusty` 等词让画面变丑
5. **纯净构图**：场景尽量留空
6. **物件密集型场景要强制限定数量**：花店、商店、仓库等本身有大量装饰物件的场景，必须用限定词控制元素数量——`a few simple` / `two buckets` / `minimal` / `uncluttered`。去掉 `colorful flowers` / `flower arrangements` / `buckets of fresh flowers` 等复数堆砌词。GK 原话："花店外观和花店内景里花太多太繁杂了"。改法示例：`large glass windows displaying colorful flowers` → `clean glass windows with a few simple flower arrangements`，`buckets of fresh flowers` → `two buckets of fresh flowers`，加 `uncluttered minimalist space`。

## 风格控制

### 避免中国场景"民国化"问题

MJ 对 "Chinese + 年代/县城/乡村" 的组合经常生成民国或清末风格的破旧建筑。解决方法：
- 用 `modern Chinese` 代替 `2008 Chinese`
- 用 `tiled building facade`（瓷砖楼）等具体现代建筑元素
- 不写 `rural` / `county-town` / `dusty` 等词

## 非主流/杀马特角色写法

GK 项目中使用的杀马特视觉元素（经验总结）：

- `shamate subculture` — 直接使用杀马特英文词
- `layered wolf-cut hairstyle, heavily hairsprayed` — 层次狼尾头+发胶定型
- `45-degree angled side-swept bangs covering one eye` — 遮眼斜刘海
- `voluminous teased spiky hair with one streak of purple highlight` — 爆炸头+挑染紫
- `fake Versace print t-shirt` — 假名牌T恤
- `wide studded belt` — 宽版铆钉腰带
- `squatting pose` — 蹲姿（杀马特经典拍照动作）
- `exaggerated pouty duck-face expression` — 嘟嘴

### MJ 参数

### --raw（GK 确认必用）+ 永远不要加任何 --v 参数

**GK 明确要求所有 MJ 提示词用 `--raw`，且永远不要加任何 `--v` 版本号。** `--raw` 是模式标志，不是版本号。

- `--raw`：高对比、高细节、少后期修饰，CG质感强
- **永远不要写 `--v 6.1`、`--v 8.1` 或任何 `--v` 版本号**——GK 2026-09 明确说"以后永远不要加v6.1这个参数"。用户的 MJ profile 自带版本设置，提示词里加 `--v` 会覆盖 profile 设置或造成冲突
- `--niji 6` 也已过时，动漫/niji 风格需确认最新 niji 版本后再用
- **profile 自带美学风格时不要写风格描述词**：如果用户的 MJ profile 已经自带某种美学（如鱼眼胶片风），提示词里不要写 "fisheye/lomography/film grain/cross-processed/vignette" 等风格词，profile 会自动处理。GK 原话："你不需要强调鱼眼 我这个profile自带这种美学"

GK 原话（2026-09）："以后永远不要加v6.1这个参数"
GK 原话（2026-09）："你不需要强调鱼眼 我这个profile自带这种美学"
GK 原话（早期）："你自己去查查mj的最新参数，你说的v6.1都多老了，现在都8.1了"
GK 原话（早期）："你为什么要用v6.1，用--raw就好了，你昨天不都是用的raw吗？什么变？？？"

### 参数速查

| 图类型 | --ar | --s | 其他参数 |
|--------|------|-----|----------|
| 角色立绘 | 2:3 | 250-400 | --raw |
| 三视图 | 16:9 | 150 | --raw --c 0 |
| 场景图 | 16:9 | 100-120 | --raw |
| 道具图 | 2:3 | 250 | --raw |

**注意：角色立绘 `--ar` 是 `2:3`，不是 `3:4`。** 用错比例会影响 MJ 生成的人物构图。

## 3D 动画风格（用户要求"3D漫剧风格"时使用）

当用户明确要求"3D漫剧风格""3D动画风"时，MJ 提示词的风格后缀需要切换到3D动画渲染风。这不同于 CG 角色立绘风（PBR+UE5），也不同于写实风（摄影质感）。

### 3D动画风格替换表

| 图类型 | CG 风格后缀 → 3D动画风格后缀 |
|--------|------------------------------|
| 角色图 | `CG character art, hyper-realistic render, PBR textures, [灯光], 8K, Unreal Engine 5 style, clean white background` → `3D animated character design, Pixar style, smooth rendering, stylized proportions, [灯光], 8K` |
| 场景图 | `CG environment art, hyper-realistic render, PBR textures, [灯光], 8K, Unreal Engine 5 style` → `3D animated environment, Pixar style, smooth rendering, stylized proportions, [灯光], 8K` |

### 3D动画风格关键点

1. **核心关键词**：`3D animated character design, Pixar style, smooth rendering, stylized proportions`
2. **保留 `clean white background`**：角色立绘仍用白底
3. **`--niji` 参数需确认最新版本**：旧版 `--niji 6` 可能已过时，写之前确认当前 niji 版本
4. **`character turnaround sheet`** 替代 `character reference sheet`——更贴合3D角色设计语境
5. **短语原则仍然适用**：3D风不等于可以写长句修饰
6. **`--raw` 仍可用**，但如果用户指定 `--niji` 则以 niji 模式为准
7. **如效果偏日漫不够3D**：加 `Octane render, subsurface scattering` 强化3D质感

### 3D动画风格参数速查

| 图类型 | --ar | --s | 风格后缀 |
|--------|------|-----|----------|
| 角色立绘（3D动画） | 2:3 | 250-350 | 3D animated character design, Pixar style |
| 场景图（3D动画） | 16:9 | 100-150 | 3D animated environment, Pixar style |

### 3D动画风格示例

角色（3D动画）：
```
3D animated character design, Pixar style, elderly Chinese man, age 60, long white beard, wise tired face, wearing navy blue business suit with loosened tie, ID badge on chest, reading glasses, holding clipboard binder, middle management appearance, calm weathered expression, full body shot, plain white background, solid color backdrop, studio lighting, smooth rendering, stylized proportions, 8k, highly detailed, --ar 2:3 --s 300 --raw
```

## 工作流程

1. 用 MJ 生成角色立绘（先出主角，多roll到满意，再出配角）
2. 生成场景图（保持简约，风格和角色图统一）
3. 把生成的角色/场景图作为参考图上传到海螺导演台
4. 按 hailuo-director-prompt skill 格式编写视频提示词，用 `<Subject N>` / `<Picture N>` 标签引用参考图

## 服装细节控制

当用户对服装有精确要求时，用具体描述词而非笼统词：

- 透视装不要写 `sheer black lace top`（MJ 会生成满身花蕾丝），写 `sheer black see-through top with lace trim only at collar and cuffs`（透视为主，蕾丝只做领口袖口装饰）
- 全身照加 `full body shot`
- 厚黑丝写 `thick black opaque tights`（不透肉），不要写 `black tights`（MJ 可能生成薄透肉）
- 日系圆头玛丽珍皮鞋写 `round-toe black Mary Jane leather shoes`
- 服装细节用具体材质词而非笼统词

## 角色腿/姿势控制（GK 确认）

MJ 默认生成的角色经常腿短、半蹲不蹲、扭腰摆拍。GK 原话："角色腿很短，而且都是半跪不跪的，要长腿，站直了别扭腰"。

### 解决方法三件套（缺一不可）

1. **加腿长词**：`very long slender legs, tall`
2. **姿势词用直站**：`standing straight, legs together, upright posture, natural relaxed pose`
   - 禁用 `elegant standing pose`（MJ 会理解成扭腰摆拍）
   - 禁用 `confident pose`（可能生成叉腰扭胯）
3. **负面提示词**：`--no crouching, bending, kneeling, twisted pose, short legs`

### 写实风触发词

GK 说"真人的"或"写实一些"时，风格后缀切换：
- CG 风 → `photorealistic portrait, cinematic photography, shot on Sony A7R IV, 85mm lens, shallow depth of field`
- 去掉 `CG character art, hyper-realistic render, PBR textures, Unreal Engine 5 style, clean white background`
- `--s` 降到 200
- `--raw` 保留

## 道具图（反复出现的标志性物品）

剧中反复出现的道具（如旧铁皮饭盒、哨子、笔记本、标本瓶）需要生成参考图锁定外观，否则 H3 每次生成形状会变。

### 基本模板

```
/imagine prompt: [a/an] [形容词] [物品名], [材质/纹理描述], [1-2个特征], simple, CG character art, hyper-realistic render, PBR textures, [灯光], 8K, Unreal Engine 5 style, clean white background --ar 2:3 --s 250 --raw
```

### 道具图关键原则

1. **用角色图规则，不用场景图规则**：白底 + clean white background + PBR + 风格后缀
2. **短语原则同样适用**：`dented metal surface` 而非 `slightly dented dark greenish-grey metal surface with rusted edges and worn texture`
3. **元素要少**：2-3个核心特征 + `simple`，不要堆砌细节
4. **`--ar 2:3 --s 250 --raw`**：和角色图一致
5. **灯光词**：`soft front lighting`（通用道具）、`dramatic blue lighting`（发光/特殊道具）、`warm front lighting`（旧物/温暖道具）

### 道具图 vs 场景图

| | 道具图 | 场景图 |
|--|--------|--------|
| 背景 | clean white background | 无白底 |
| --ar | 2:3 | 16:9 |
| --s | 250 | 100-120 |
| 风格后缀 | CG character art | CG environment art |
| 角色 | 物品居中、纯净 | 场景留空、氛围 |

道具图本质上是"物品的角色立绘"——用角色图的所有规则，只是把人换成物品。

## 写实风格（用户要求"写实一些"时切换）

当用户明确要求写实风格时，MJ 提示词的风格后缀需要从 CG 风切换到摄影质感风。GK 原话："写实一些"。

### 写实风格替换表

| 图类型 | CG 风格后缀 → 写实风格后缀 |
|--------|---------------------------|
| 角色图 | `CG character art, hyper-realistic render, PBR textures, [灯光], 8K, Unreal Engine 5 style, clean white background` → `photorealistic portrait, cinematic photography, shot on Sony A7R IV, 85mm lens, shallow depth of field, [灯光], 8K` |
| 场景图 | `CG environment art, hyper-realistic render, PBR textures, [灯光], 8K, Unreal Engine 5 style` → `cinematic photography, wide angle, [灯光], 8K` |
| 道具图 | `CG character art, hyper-realistic render, PBR textures, [灯光], 8K, Unreal Engine 5 style, clean white background` → `product photography, macro lens, shallow depth of field, [灯光], 8K` |

### 写实风格关键点

1. **灯光词保留不变**：`dramatic rim lighting` / `dramatic side lighting` / `soft front lighting` 等灯光词在写实风下同样有效，不需要换
2. **去掉 `clean white background`**：写实风角色图用浅景深虚化背景替代白底。道具图可保留浅景深，特殊道具可用暗背景
3. **`--s` 可适当降低**：写实风 `--s` 200 左右，场景图降到 80-100
4. **短语原则仍然适用**：写实风不等于可以写长句修饰
5. **`--raw` 仍然必用**：写实风也是 `--raw`，不用旧版 `--v 6.1`（已过时，当前 MJ 版本 v8.1）

### 写实风格参数速查

| 图类型 | --ar | --s | 风格后缀 |
|--------|------|-----|----------|
| 角色立绘（写实） | 2:3 | 200-250 | photorealistic portrait, cinematic photography |
| 场景图（写实） | 16:9 | 80-100 | cinematic photography, wide angle |
| 道具图（写实） | 2:3 | 150 | product photography, macro lens |

### 写实风格示例

角色（写实）：
```
an 18-year-old Chinese young man, handsome, elegant classical Chinese facial features, slim narrow face, delicate thin features, medium length black hair neatly styled, dark calm eyes, fair skin, wearing a dark trench coat over a grey fisherman sweater, holding an old tin lunchbox, relaxed posture, quiet confident expression, photorealistic portrait, cinematic photography, shot on Sony A7R IV, 85mm lens, shallow depth of field, dramatic rim lighting, 8K --ar 2:3 --s 200 --raw
```

场景（写实）：
```
a vast underground hall, large dark water tanks along walls, concrete surfaces, faint blue bioluminescent glow, a wooden desk with notebooks, minimal, clean, photorealistic, cinematic interior photography, wide angle, cool ambient lighting, 8K --ar 16:9 --s 80 --raw
```

道具（写实）：
```
an old tin lunchbox, dented metal surface, simple latch, worn greenish-grey paint, scratches, photorealistic product photography, macro lens, soft front lighting, shallow depth of field, 8K --ar 2:3 --s 150 --raw
```

## 反派角色写法

反派角色"妖娆有魅力"时的写法规律。GK 原话："温故巨他妈丑，傻大粗的样子，国字脸大肌肉 真的很蠢，我要有魅力妖娆的反派角色"。

### 禁用词（生成"傻大粗"丑图）

- ❌ `broad-shouldered` / `muscular` / `rugged` — 健美壮汉
- ❌ `square jaw` / `strong jawline` — 国字脸
- ❌ `intimidating` — 配合大肌肉会变成"蠢壮"
- ❌ `commanding presence` / `dominating aura` — MJ 渲染成压迫感壮汉

### 推荐词（妖娆有魅力）

- ✅ `slim elegant face` / `slim narrow face` — 瘦窄脸
- ✅ `seductive` / `dangerously charming` — 魅惑
- ✅ `half-lidded seductive eyes` — 半垂眼
- ✅ `faint smile` / `faint smirk` — 似笑非笑
- ✅ `languid graceful posture` — 慵懒优雅
- ✅ `cold alluring gaze` — 冷艳
- ✅ `long black hair loosely tied` — 长发微拢
- ✅ `dramatic side lighting` — 侧面光增加神秘感

### 反派角色示例

```
a 30-year-old Chinese man, dangerously charming, seductive villain, slim elegant face, sharp narrow features, long black hair loosely tied, porcelain skin, ruby red lips, half-lidded seductive eyes, faint smile, wearing a fitted white silk shirt with sleeves rolled up, silver rings, languid graceful posture, cold alluring gaze, photorealistic portrait, cinematic photography, shot on Sony A7R IV, 85mm lens, shallow depth of field, dramatic side lighting, 8K --ar 2:3 --s 250 --raw
```

## 游戏角色名识别问题（2026-09-07 确认）

MJ 对游戏/动漫角色名（如 Final Fantasy 的 Clive Rosfield、Zack Fair）识别能力不稳定。写了 `Final Fantasy 16 Clive Rosfield CG art style` 后用户反馈"克莱夫成年时候的感觉MJ不太懂呢，表现不出来"。

### 解决方法

1. **去掉角色名，用纯视觉特征描述**：把该角色的视觉特征拆成 MJ 能理解的短语——发型（`short dark brown undercut hair swept back`）、脸型（`rugged handsome face`）、体格（`lean athletic muscular build`）、气质（`calm stoic expression with quiet authority`）、标志性特征（`light stubble`、`broad shoulders`）
2. **用户有角色参考图时用 `--sref` 或 `--cref`**：比文字描述更准确。`--cref [图URL]` 锁角色面部，`--sref [图URL]` 灌风格，`--cw 0` 只保脸不保服装
3. **不要反复试不同角色名**：如果 `Final Fantasy Zack Fair` 不行，换 `Final Fantasy 16 Clive Rosfield` 也不行——MJ 对这类角色名的训练数据覆盖不稳定。直接转纯描述词方案

## 角色微调迭代

GK 会反复微调角色外观，每次只说一个调整点。H 必须在上一版基础上只改指定部分，不重写整个提示词，也不丢失已确认的特征。

### 微调流程

1. 用户说一个调整（如"脸没有那么方 是那种日系美型的"）
2. H 只改对应部分（如把 `slim narrow face` 改成 `Japanese idol aesthetic, slim narrow face`）
3. 其他已确认的特征保持不变
4. 输出新版提示词时保留所有之前确认过的修改

### 维护"已确认特征清单"

每次用户确认或修改后，更新该角色的特征清单：

**示例（祁渊的迭代过程）：**
| 版本 | 用户指示 | 修改内容 |
|------|---------|---------|
| v1 | 初始 | 27岁，dark circles，lazy confidence |
| v2 | "更帅更年轻" | 23岁，加 strikingly handsome, sharp jawline |
| v3 | "18岁，没有分明下颌线，头发中等长度不凌乱" | 18岁，去掉 sharp jawline，改 soft youthful face，medium length neatly styled |
| v4 | "脸没那么方，日系美型" | 加 Japanese idol aesthetic, soft narrow face |
| v5 | "脸还是比较瘦弱" | 改 slim narrow face, delicate thin features, slender build |
| v6 | "古风俊朗的感觉" | 加 elegant classical Chinese facial features |

### 常见微调方向

| 用户指示 | 修改词 |
|---------|--------|
| "更帅" | 加 `strikingly handsome` 或 `dangerously handsome` |
| "更年轻" | 减年龄数字 |
| "不要方脸" | `sharp jawline` → `soft narrow face` / `slim narrow face` |
| "日系美型" | 加 `Japanese idol aesthetic` |
| "古风俊朗" | 加 `elegant classical Chinese facial features` |
| "瘦弱" | 加 `slim` / `delicate thin features` / `slender build` |
| "不要凌乱" | 发型词加 `neatly styled` |
| "妖娆反派" | 见"反派角色写法"章节 |

## 用户长关键词模板处理

用户可能提供一大段中文关键词模板（通常从 AI 绘画工具社区抄来），要求"把这个改成主角的样子"。

### 处理方法

1. **不整段照搬**：中文关键词直接翻译成英文塞入 MJ 会导致 MJ 混淆（太多无序描述词互相竞争）
2. **提取风格/光影/氛围词**：从模板中筛选出有用的风格词（film photography, chiaroscuro, lomo effect, porcelain skin, Rembrandt lighting, hazy dreamy atmosphere 等）
3. **融入角色设定**：将提取的风格词融入角色的基本设定（年龄、脸型、服装、气质），用英文短语重新组织
4. **保留用户风格意图**：用户提供的模板代表他们的审美偏好，不能忽略。但要用 MJ 能理解的方式表达
5. **角色特征优先**：角色识别特征（年龄、发型、服装、道具）排在前面，风格氛围词排在后面

### 常见用户模板词汇 → MJ 可用英文对照

| 中文模板词 | MJ 可用英文 |
|-----------|------------|
| 胶片摄影 | film photography |
| 镜头语言 | cinematic photography |
| 淡彩 | muted pastel tones |
| 个性视角 | personal perspective |
| 冷白皮 | cold white skin |
| 皮肤瓷白细腻有光泽 | porcelain smooth skin with natural glow |
| 光线明暗交接 | chiaroscuro lighting |
| 高对比度 | high contrast |
| lomo效果 | lomo effect |
| 高级感 | luxurious |
| 杰作 | masterpiece |
| 神秘感 | mysterious |
| 近距离肖像画 | close-up portrait |
| 动态视角 | dynamic angle |
| 禁欲系 | celibate aesthetic |
| 明暗对比强烈 | strong chiaroscuro |
| 伦勃朗光 | Rembrandt lighting |
| 碎发随风摆动 | fine loose strands swaying in wind |
| 狭长凤眼 | narrow phoenix eyes |
| 瓷白如玉的肌肤 | porcelain jade skin |
| 柔焦 | soft focus |
| 32K | 32K |
| 大师级光影 | masterful lighting |
| 暗冷色调 | dark cool tones |
| 朦胧且梦幻 | hazy dreamy atmosphere |
| 东方风格 | oriental aesthetic |
