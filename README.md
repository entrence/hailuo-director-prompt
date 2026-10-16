# Hailuo Director Prompt Engineering

海螺导演台(MiniMax-H3)视频生成提示词工程：多模态参考生成、视频编辑、视觉换皮、首尾帧图生视频、文生视频。

覆盖产品电商/品牌时尚/剧情短剧/动作游戏/硬件工业/动画风格化/MV/Vlog等题材，含结构化字段模板、素材职责分配、文字品牌UI控制、机械校验。

## Features

- 结构化六段式提示词生成（subject_definitions / summary / retention_analysis / detailed_description / overall_soundscape / non_diegetic_music）
- 多模态参考生成：首帧+尾帧+参考图+文字描述
- 视频编辑：换皮、续接、风格迁移
- 14种题材模板（产品电商、品牌时尚、剧情短剧、动作游戏、硬件工业、动画风格化、MV、Vlog等）
- RunningHub 工作流 API 集成（9图拼接、节点管理、API提交）
- Midjourney 角色/场景提示词生成
- 提示词机械校验脚本（字段完整性、格式合规性）
- 批量生成模板

## Install

```bash
hermes skills install https://raw.githubusercontent.com/entrence/hailuo-director-prompt/main/SKILL.md
```

## Prerequisites

### Python packages
```bash
pip install requests
```

### External services
- 海螺导演台账号 (MiniMax H3)
- RunningHub 账号 (API key + workflow IDs)
- Midjourney (可选，用于角色立绘/场景图生成)

### Environment variables
- `RUNNINGHUB_API_KEY` — RunningHub API 密钥
- 海螺导演台通过浏览器操作，无需 API key

## Usage

Say any of these to trigger the skill:
- "帮我写个海螺视频提示词"
- "生成一个产品展示的视频提示词"
- "封神小剧场第X场提示词"
- "换皮视频提示词"
- "RunningHub提交工作流"

## Repository Structure

```
hailuo-director-prompt/
├── SKILL.md                                    # Main skill definition (v2.1.0)
├── README.md                                   # This file
├── references/
│   ├── official-rules.md                       # 海螺官方规则和字段规范
│   ├── genre-guide.md                          # 14种题材指南
│   ├── editing-guide.md                        # 视频编辑/换皮/续接指南
│   ├── ref-mode-guide.md                       # 多模态参考模式指南
│   ├── live-action-vs-animation-pitfall.md     # 真人实拍vs动画避坑
│   ├── comedy-fast-pace-example.md             # 喜剧快节奏示例
│   ├── classroom-voiceover-example.md           # 课堂旁白示例
│   ├── dialogue-routing-example.md             # 对话路由示例
│   ├── liminal-space-video-series.md           # Liminal space系列示例
│   ├── midjourney-character-scene-prompts.md    # MJ角色场景提示词
│   ├── runninghub-api.md                       # RunningHub API 参考
│   ├── runninghub-workflow-api.md              # RunningHub 工作流API
│   ├── runninghub-node-management.md           # RunningHub 节点管理
│   └── runninghub-workflow-9img-2093898864557383681.md  # 9图拼接工作流
├── templates/
│   └── batch_generate.py                       # 批量生成模板脚本
└── scripts/
    └── validate_h3_prompt.py                   # 提示词校验脚本
```

## Notes

- 提示词修改铁律：不要过度修正，第一版通常就够了
- 六段格式是官方规范，必须完整保留
- 台词只增不减，Shot数量和时间轴不砍
- 串行clip续接：先发GK看效果，确认OK后再提交下一个
- 提交前必须机械校验（validate_h3_prompt.py）
- RunningHub: standard实例OOM时切plus模式，不要降低分辨率
- 海螺视频可生成语音台词，写进clip不省略

## License

MIT
