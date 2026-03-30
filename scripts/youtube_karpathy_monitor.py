#!/usr/bin/env python3
"""
YouTube Channel Monitor for Andrej Karpathy
Uses jina.ai to scrape YouTube channel videos page and detect new uploads.
Sends Feishu notifications when new videos are detected.
"""

import urllib.request
import urllib.error
import json
import re
import os
import sys
import subprocess
from datetime import datetime, timezone

CHANNEL_HANDLE = "AndrejKarpathy"
CHANNEL_NAME = "Andrej Karpathy"
JINA_URL = f"https://r.jina.ai/https://www.youtube.com/@{CHANNEL_HANDLE}/videos"
STATE_FILE = "/root/.openclaw/workspace/scripts/.karpathy_last_video.json"
PYTHON_BIN = "/usr/bin/python3"

VIDEO_SUMMARIES = {
    "EWvNQjAaOHw": "2小时11分 | 实用指南：Karpathy 日常如何使用 LLM（ChatGPT、Claude等），涵盖提示工程、工作流、代码生成等实战技巧",
    "7xTGNNLPyMI": "3小时31分 | 深度解析 ChatGPT 等大语言模型原理：训练过程、RLHF、涌现能力、应用场景",
    "l8pRSuU81PU": "4小时01分 | 从零复现 GPT-2 (124M)：完整代码实现，详解 Transformer 架构与预训练流程",
    "zduSFxRajkE": "2小时13分 | 详解 GPT 分词器（Tokenizer）：BPE 算法原理、词表构建、特殊符号处理",
    "zjkBMFhNj_g": "59分 | LLM 入门导论：语言模型基础、ChatGPT 背后的技术、prompting 技巧",
    "kCc8FmEb1nY": "1小时56分 | 从零构建 GPT：手把手写代码，详解自注意力机制与生成式 AI 核心",
}

def fetch_channel_page():
    """Fetch YouTube channel videos page via jina.ai"""
    req = urllib.request.Request(
        JINA_URL,
        headers={
            "Accept": "text/plain",
            "User-Agent": "Mozilla/5.0 (compatible; OpenClaw-bot/1.0)"
        }
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")

def parse_videos(content):
    """Extract video IDs and titles from jina.ai scraped content"""
    videos = []
    seen_ids = set()
    pattern = r'watch\?v=([a-zA-Z0-9_-]+)[^"]*"([^"]+)"'
    matches = re.findall(pattern, content)
    for video_id, title in matches:
        if video_id in seen_ids:
            continue
        clean_title = title.strip()
        if not clean_title or clean_title.startswith('http') or clean_title == 'undefined':
            continue
        seen_ids.add(video_id)
        videos.append({
            "id": video_id,
            "title": clean_title
        })
    return videos

def load_state():
    """Load last checked video ID from state file"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(video_id, video_title):
    """Save latest video ID to state file"""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    state = {
        "last_video_id": video_id,
        "last_video_title": video_title,
        "last_checked": datetime.now(timezone.utc).isoformat()
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def send_feishu_message(content: str):
    """Send message via feishu_im_user_message tool"""
    try:
        from keke_openclaw_tool import feishu_im_user_message
        result = feishu_im_user_message(
            action="send",
            receive_id_type="open_id",
            receive_id="ou_63be868557327448609c28ca85abbfd7",
            msg_type="text",
            content=json.dumps({"text": content})
        )
        return result
    except Exception as e:
        print(f"  Feishu send error: {e}")
        return None

def build_new_video_message(video, include_summary=True):
    """Build message for a new video"""
    vid = video["id"]
    title = video["title"]
    
    msg = f"📺 **{CHANNEL_NAME}** — 新视频\n\n"
    msg += f"🎬 **{title}**\n"
    
    if include_summary and vid in VIDEO_SUMMARIES:
        msg += f"📝 {VIDEO_SUMMARIES[vid]}\n"
    
    msg += f"\n▶️ https://www.youtube.com/watch?v={vid}"
    
    return msg

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    
    print(f"[{datetime.now(timezone.utc).isoformat()}] Checking {CHANNEL_NAME} channel...")
    
    try:
        content = fetch_channel_page()
        videos = parse_videos(content)
        
        if not videos:
            print("  No videos found on channel page")
            return
        
        latest = videos[0]
        print(f"  Latest video: {latest['title']} ({latest['id']})")
        
        state = load_state()
        last_id = state.get("last_video_id")
        
        if last_id == latest["id"]:
            print("  No new videos — already up to date")
            if mode == "report":
                print("  Status: UP_TO_DATE")
            return
        
        # New video(s) detected
        print(f"  🆕 NEW VIDEO: {latest['title']}")
        
        if last_id:
            print(f"  Previous last: {state.get('last_video_title')} ({last_id})")
        
        # Send Feishu notification
        msg = build_new_video_message(latest)
        print(f"\n  Feishu message:\n  {msg[:100]}...")
        
        # In cron mode, use openclaw message tool
        if mode == "cron":
            try:
                result = subprocess.run(
                    ["openclaw", "message", "send",
                     "--channel", "feishu",
                     "--target", "ou_63be868557327448609c28ca85abbfd7",
                     "--message", msg],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0:
                    print("  ✅ Feishu notification sent")
                else:
                    print(f"  ⚠️ Feishu send failed: {result.stderr}")
            except Exception as e:
                print(f"  ⚠️ Could not send Feishu message: {e}")
        
        save_state(latest["id"], latest["title"])
        print(f"\n  State saved for video: {latest['id']}")
        
    except urllib.error.HTTPError as e:
        print(f"  HTTP Error: {e.code} {e.reason}")
    except Exception as e:
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
