#!/usr/bin/env python3
"""Validate MiniMax H3 prompt and input counts against bundled official limits.

Usage:
  python3 scripts/validate_h3_prompt.py \
    --input prompt.txt \
    --mode reference-to-video \
    --duration 15 \
    --ratio 16:9 \
    --images 2 \
    --videos 1 \
    --audios 0
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


MODES = (
    "text-to-video",
    "first-last-frame",
    "reference-to-video",
    "video-editing",
)


def parse_durations(raw: str | None, label: str, errors: list[str]) -> list[float]:
    if not raw:
        return []
    values: list[float] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            values.append(float(part))
        except ValueError:
            errors.append(f"{label}包含无效时长：{part}")
    return values


def find_timeline_endpoints(text: str) -> list[float]:
    pattern = re.compile(
        r"(?<!\d)(\d+(?:\.\d+)?)\s*(?:-|–|—|至|到)\s*(\d+(?:\.\d+)?)\s*(?:s|秒)",
        re.IGNORECASE,
    )
    return [float(match.group(2)) for match in pattern.finditer(text)]


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 MiniMax H3 提示词和多模态输入限制")
    parser.add_argument("--input", required=True, help="UTF-8 提示词文本文件")
    parser.add_argument("--mode", choices=MODES, required=True)
    parser.add_argument("--duration", type=int, required=True, help="目标视频时长，整数秒")
    parser.add_argument("--ratio", required=True, help="画幅，如 16:9、9:16 或 adaptive")
    parser.add_argument("--images", type=int, default=0)
    parser.add_argument("--videos", type=int, default=0)
    parser.add_argument("--audios", type=int, default=0)
    parser.add_argument("--video-durations", help="参考视频时长，逗号分隔，如 5,10")
    parser.add_argument("--audio-durations", help="参考音频时长，逗号分隔，如 8,7")
    parser.add_argument("--first-frame", action="store_true")
    parser.add_argument("--last-frame", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    path = Path(args.input)
    if not path.is_file():
        errors.append(f"找不到提示词文件：{path}")
        text = ""
    else:
        text = path.read_text(encoding="utf-8-sig").strip()

    if not text:
        errors.append("提示词为空")
    if len(text) > 7000:
        errors.append(f"提示词共 {len(text)} 字符，超过 7000 字符上限")

    if args.duration < 4 or args.duration > 15:
        errors.append("目标时长必须是 4—15 秒之间的整数")

    if args.images < 0 or args.videos < 0 or args.audios < 0:
        errors.append("素材数量不能为负数")

    ratio = args.ratio.strip().lower()
    if ratio != "adaptive" and not re.fullmatch(r"\d+:\d+", ratio):
        errors.append("画幅必须写成 W:H 或 adaptive")

    if args.mode == "text-to-video":
        if args.images + args.videos + args.audios:
            errors.append("文生视频模式不能同时声明参考图片、视频或音频")
        if ratio == "adaptive":
            errors.append("文生视频必须指定明确画幅，不能使用 adaptive")

    if args.mode == "first-last-frame":
        frame_count = int(args.first_frame) + int(args.last_frame)
        if frame_count == 0:
            warnings.append("未声明首帧或尾帧；该请求实际会退化为文生视频")
        if args.images > 2:
            errors.append("首尾帧图片最多 2 张")
        if args.videos or args.audios:
            errors.append("首尾帧入口不接受参考视频或音频；需要这些素材时改用多模态参考")
        if args.images and args.images != frame_count:
            warnings.append("--images 与 --first-frame/--last-frame 声明数量不一致")

    if args.mode in ("reference-to-video", "video-editing"):
        if args.images > 9:
            errors.append("参考图片最多 9 张")
        if args.videos > 3:
            errors.append("参考视频最多 3 段")
        if args.audios > 3:
            errors.append("参考音频最多 3 段")
        if args.images + args.videos + args.audios > 12:
            errors.append("图片、视频和音频合计最多 12 个文件")
        if args.audios and not (args.images or args.videos):
            errors.append("参考音频不能单独使用，必须同时提供图片或视频")
        if not (args.images or args.videos or args.audios):
            warnings.append("没有参考素材；该请求实际会退化为文生视频")
        if args.mode == "video-editing" and args.videos == 0:
            errors.append("视频编辑模式至少需要 1 段参考视频")

    video_durations = parse_durations(args.video_durations, "参考视频", errors)
    audio_durations = parse_durations(args.audio_durations, "参考音频", errors)

    if video_durations and len(video_durations) != args.videos:
        warnings.append("参考视频时长数量与 --videos 不一致")
    if audio_durations and len(audio_durations) != args.audios:
        warnings.append("参考音频时长数量与 --audios 不一致")

    for value in video_durations:
        if value < 2 or value > 15:
            errors.append(f"单段参考视频时长 {value:g} 秒，必须在 2—15 秒之间")
    if sum(video_durations) > 15:
        errors.append(f"参考视频合计 {sum(video_durations):g} 秒，超过 15 秒")

    for value in audio_durations:
        if value < 2 or value > 15:
            errors.append(f"单段参考音频时长 {value:g} 秒，必须在 2—15 秒之间")
    if sum(audio_durations) > 15:
        errors.append(f"参考音频合计 {sum(audio_durations):g} 秒，超过 15 秒")

    endpoints = find_timeline_endpoints(text)
    if endpoints and max(endpoints) > args.duration:
        errors.append(
            f"提示词时间轴结束于 {max(endpoints):g} 秒，超过目标时长 {args.duration} 秒"
        )

    placeholders = ("非完整prompt", "非完全prompt", "可自行补充", "todo", "待补充")
    lowered = text.lower()
    found = [item for item in placeholders if item in lowered]
    if found:
        warnings.append("提示词仍含占位表述：" + "、".join(found))

    result = {
        "valid": not errors,
        "characters": len(text),
        "errors": errors,
        "warnings": warnings,
    }

    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("PASS" if not errors else "FAIL")
        print(f"字符数：{len(text)}/7000")
        for item in errors:
            print(f"ERROR: {item}")
        for item in warnings:
            print(f"WARN: {item}")

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
