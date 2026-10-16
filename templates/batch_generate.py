#!/usr/bin/env python3
"""批量生成多段 clip（clip01~clipN），自动处理尾帧衔接，最后拼接成一个完整视频。

使用场景：GK 说"从1到9重新生成一遍""一块拼接，给我一个完整的"——批量授权。

核心流程：
1. 逐个 clip 提交 → 轮询 → 下载
2. 每个 clip 下载后自动提取尾帧 → 上传到 RunningHub
3. 下一 clip 如果 needs_prev_tail=True，用上一个 clip 的尾帧做首帧参考图
4. 全部完成后 ffmpeg concat 拼接 → 输出一个完整 MP4

关键配置：
- instanceType: "plus"（9图版必须用 plus 避免 OOM）
- 随机种子：每个 clip 用 random.randint(100000000000000, 999999999999999)
- OOM 自动重试：失败后等 60s，换新种子重新提交
- 参考图占位：不用的图节点传 placeholder，不要留空（否则用工作台默认值导致 OOM）

前置条件：
- 所有参考图已上传到 RunningHub，fileName 记录在 REFS 字典中
- 各 clip 提示词文件在 EP_DIR 中，文件头注释行标注参考图清单
- poll 超时设 1200s（每 clip 约 10-14 分钟生成时间）

运行方式：
  cd /home/ubuntu/scripts/<project> && python3 batch_generate.py

注意：此脚本耗时很长（9 个 clip 约 2 小时），必须用 delegate_task 后台运行，
不要用 terminal foreground（600s 超时不够）或 execute_code（300s 限制不够）。
"""
import json, random, subprocess, time, urllib.request, os

API_KEY = "YOUR_API_KEY"
WORKFLOW_ID = "2093898864557383681"
SUBMIT_URL = f"https://www.runninghub.cn/openapi/v2/run/workflow/{WORKFLOW_ID}"
QUERY_URL = "https://www.runninghub.cn/openapi/v2/query"
UPLOAD_URL = "https://www.runninghub.cn/openapi/v2/media/upload/binary"
EP_DIR = "/home/ubuntu/scripts/<project>/ep01"
OUT_DIR = "/home/ubuntu/scripts/<project>/output"

# 已上传的参考图 fileName 映射
REFS = {
    "角色A": "openapi/xxxx.png",
    "角色B": "openapi/xxxx.png",
    "场景A": "openapi/xxxx.png",
}

PLACEHOLDER_IMG = "openapi/d9bd147ced77bca4a875af12714949cd17ddd3c11cc47218b4de30185bc0b4e9.png"
PLACEHOLDER_VID = "openapi/c5114f4ec154a523dc5439396b11cf2f33d1b34d57c6ad1ea146251f91f5c1aa.mp4"
PLACEHOLDER_AUD = "openapi/1c8e34af202f94d0d741c12e4a90fe865bb4c771362102d5a730562c47655bc6.mp3"

# 每个 clip: (filename, seconds, ref_image_keys, needs_prev_tail)
# ref_image_keys: "TAIL" = 用上一个 clip 的尾帧
#                其他 = REFS 字典中的 key
CLIPS = [
    ("clip01.txt", 15, ["角色A", "场景A"], False),
    ("clip02.txt", 15, ["场景A", "角色A"], False),
    ("clip03.txt", 15, ["TAIL", "角色A"], True),
    # ... 按需添加
]


def read_prompt(filename):
    with open(os.path.join(EP_DIR, filename)) as f:
        text = f.read()
    lines = [l for l in text.split('\n') if not l.startswith('#')]
    return '\n'.join(lines).strip()


def submit_clip(prompt_text, ref_image_ids, seconds, seed):
    node_list = [{"nodeId": "84", "fieldName": "value", "fieldValue": prompt_text}]
    img_nodes = ["35", "41", "42", "43", "44", "36", "37", "38", "39"]
    for i, node_id in enumerate(img_nodes):
        val = ref_image_ids[i] if i < len(ref_image_ids) else PLACEHOLDER_IMG
        node_list.append({"nodeId": node_id, "fieldName": "image", "fieldValue": val})
    node_list.append({"nodeId": "31", "fieldName": "video", "fieldValue": PLACEHOLDER_VID})
    node_list.append({"nodeId": "28", "fieldName": "audio", "fieldValue": PLACEHOLDER_AUD})
    node_list.append({"nodeId": "29", "fieldName": "audio", "fieldValue": PLACEHOLDER_AUD})
    node_list.append({"nodeId": "30", "fieldName": "audio", "fieldValue": PLACEHOLDER_AUD})
    node_list.append({"nodeId": "74", "fieldName": "value", "fieldValue": seconds})
    node_list.append({"nodeId": "63", "fieldName": "noise_seed", "fieldValue": seed})
    payload = {"addMetadata": True, "instanceType": "plus", "nodeInfoList": node_list}
    req = urllib.request.Request(SUBMIT_URL, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    # CRITICAL: validate taskId before returning. RunningHub API can return
    # a structurally valid response with no taskId (errorCode, rate limit,
    # workflow error) — without this check the caller polls an empty taskId
    # for 1200s before timing out, wasting time and confusing diagnosis.
    task_id = data.get("taskId")
    if not task_id:
        raise RuntimeError(
            f"submit_clip: no taskId in API response: "
            f"{json.dumps(data, ensure_ascii=False)[:500]}"
        )
    return task_id


def poll_and_download(task_id, output_path, max_wait=1800):
    elapsed = 0
    while elapsed < max_wait:
        payload = json.dumps({"taskId": task_id}).encode()
        req = urllib.request.Request(QUERY_URL, data=payload,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        status = data.get("status", "UNKNOWN")
        print(f"  [{elapsed}s] {status}", flush=True)
        if status == "SUCCESS":
            for out in data.get("results", []):
                url = out.get("value", "") if isinstance(out, dict) else ""
                if url and "http" in str(url):
                    dl_req = urllib.request.Request(url)
                    with urllib.request.urlopen(dl_req, timeout=120) as dl_resp:
                        data_bytes = dl_resp.read()
                    with open(output_path, "wb") as f:
                        f.write(data_bytes)
                    print(f"  SAVED: {output_path} ({len(data_bytes)/1024/1024:.1f}MB)", flush=True)
                    return True
            return False
        elif status in ("FAILED", "ERROR"):
            failed = data.get("failedReason", {})
            print(f"  FAILED: {failed.get('exception_type','')}: {failed.get('exception_message','')[:200]}", flush=True)
            return False
        time.sleep(60)
        elapsed += 60
    return False


def extract_tail_frame(video_path, output_png):
    """提取最后一帧。必须用 subprocess 调 ffprobe/ffmpeg，不能在 execute_code 的 terminal() 里嵌套调（转义会炸）。"""
    r = subprocess.run(["ffprobe", "-v", "quiet", "-count_frames", "-select_streams", "v:0",
        "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", video_path],
        capture_output=True, text=True)
    total = int(r.stdout.strip())
    subprocess.run(["ffmpeg", "-y", "-i", video_path,
        "-vf", f"select=eq(n\\\\,{total-1})", "-vframes", "1", output_png],
        capture_output=True, text=True)
    return os.path.exists(output_png)


def upload_image(filepath):
    r = subprocess.run(["curl", "-s", "-X", "POST", UPLOAD_URL,
        "-H", f"Authorization: Bearer {API_KEY}", "-F", f"file=@{filepath}"],
        capture_output=True, text=True, timeout=60)
    return json.loads(r.stdout).get("data", {}).get("fileName", "")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    results = []
    for i, (filename, seconds, ref_keys, needs_tail) in enumerate(CLIPS):
        clip_num = i + 1
        print(f"\n{'='*60}\nCLIP {clip_num}: {filename} ({seconds}s)\n{'='*60}", flush=True)
        prompt = read_prompt(filename)
        ref_ids = []
        for key in ref_keys:
            if key == "TAIL":
                tail_png = os.path.join(OUT_DIR, f"clip{clip_num-1:02d}_tail.png")
                ref_ids.append(upload_image(tail_png) if os.path.exists(tail_png) else PLACEHOLDER_IMG)
            else:
                ref_ids.append(REFS[key])
        seed = random.randint(100000000000000, 999999999999999)
        task_id = submit_clip(prompt, ref_ids, seconds, seed)
        output_path = os.path.join(OUT_DIR, f"clip{clip_num:02d}_new_raw.mp4")
        if not poll_and_download(task_id, output_path):
            print("  Retrying in 60s...", flush=True)
            time.sleep(60)
            task_id = submit_clip(prompt, ref_ids, seconds, random.randint(100000000000000, 999999999999999))
            success = poll_and_download(task_id, output_path)
        else:
            success = True
        if success:
            extract_tail_frame(output_path, os.path.join(OUT_DIR, f"clip{clip_num:02d}_tail.png"))
            results.append((clip_num, output_path, True))
        else:
            results.append((clip_num, output_path, False))
    # 拼接
    successful = [(n, p) for n, p, ok in results if ok]
    if len(successful) == len(CLIPS):
        list_file = "/tmp/concat_all.txt"
        with open(list_file, "w") as f:
            for _, path in successful:
                f.write(f"file '{path}'\n")
        merged = os.path.join(OUT_DIR, "ep01_complete_merged.mp4")
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
            "-c:v", "libx264", "-c:a", "aac", "-b:a", "128k", merged], timeout=300)
        print(f"Merged: {merged} ({os.path.getsize(merged)/1024/1024:.1f}MB)", flush=True)
    print("DONE!", flush=True)


if __name__ == "__main__":
    main()
